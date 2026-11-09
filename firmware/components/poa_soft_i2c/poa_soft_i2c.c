#include "poa_soft_i2c.h"
#include <math.h>
#include <string.h>
#include "driver/gpio.h"
#include "esp_rom_sys.h"
#include "esp_timer.h"

/* Bus targets 25 kHz (20 us half period). GPIO set/read and task pre-emption
 * can only make this slower. No push-pull high drive. */
#define POA_HALF_US 20
#define POA_STRETCH_TIMEOUT_US 2000
#define POA_ADC_TIMEOUT_US 120000
#define POA_SDA ((gpio_num_t)POA_GPIO_SDA)
#define POA_SCL ((gpio_num_t)POA_GPIO_SCL)
#define ADS_REG_CONVERSION 0x00
#define ADS_REG_CONFIG 0x01
#define ADS_OS_SINGLE (0x8000u | 0x0100u | 0x0040u | 0x0003u) /* one shot, 32 SPS, comparator disabled */
#define ADS_MUX_DIFF_01 0x0000u
#define ADS_MUX_AIN2   0x6000u
#define ADS_MUX_AIN3   0x7000u
#define ADS_PGA_0256   0x0A00u
#define ADS_PGA_4096   0x0200u

static inline void delay_half(void) { esp_rom_delay_us(POA_HALF_US); }
static inline void sda_release(void) { gpio_set_level(POA_SDA, 1); }
static inline void sda_low(void) { gpio_set_level(POA_SDA, 0); }
static inline void scl_release(void) { gpio_set_level(POA_SCL, 1); }
static inline void scl_low(void) { gpio_set_level(POA_SCL, 0); }
static inline bool sda_high(void) { return gpio_get_level(POA_SDA) != 0; }

static esp_err_t scl_high_wait(void) {
    scl_release();
    int64_t end = esp_timer_get_time() + POA_STRETCH_TIMEOUT_US;
    while (!gpio_get_level(POA_SCL)) {
        if (esp_timer_get_time() >= end) return ESP_ERR_TIMEOUT;
        esp_rom_delay_us(2);
    }
    return ESP_OK;
}
static esp_err_t start_condition(bool repeated) {
    sda_release();
    if (!repeated) {
        if (scl_high_wait() != ESP_OK) return ESP_ERR_TIMEOUT;
        if (!sda_high()) return ESP_ERR_INVALID_STATE;
    } else if (scl_high_wait() != ESP_OK) return ESP_ERR_TIMEOUT;
    delay_half();
    sda_low(); delay_half(); scl_low();
    return ESP_OK;
}
static void stop_condition(void) {
    sda_low(); delay_half();
    scl_release(); delay_half();
    sda_release(); delay_half();
}
static esp_err_t write_bit(bool bit) {
    if (bit) sda_release(); else sda_low();
    delay_half();
    esp_err_t e = scl_high_wait();
    if (e != ESP_OK) return e;
    delay_half();
    scl_low();
    return ESP_OK;
}
static esp_err_t read_bit(bool *bit) {
    sda_release(); delay_half();
    esp_err_t e = scl_high_wait();
    if (e != ESP_OK) return e;
    delay_half(); *bit = sda_high();
    scl_low();
    return ESP_OK;
}
static esp_err_t write_byte(uint8_t byte) {
    for (unsigned i=0; i<8; ++i) {
        esp_err_t e = write_bit((byte & 0x80u) != 0);
        if (e != ESP_OK) return e;
        byte <<= 1;
    }
    bool nack = true;
    esp_err_t e = read_bit(&nack);
    if (e != ESP_OK) return e;
    return nack ? ESP_ERR_NOT_FOUND : ESP_OK;
}
static esp_err_t read_byte(uint8_t *byte, bool ack) {
    uint8_t v=0;
    for (unsigned i=0; i<8; ++i) {
        bool b=false;
        esp_err_t e=read_bit(&b);
        if (e != ESP_OK) return e;
        v = (uint8_t)((v << 1) | (b ? 1u : 0u));
    }
    esp_err_t e=write_bit(!ack);
    if (e == ESP_OK) *byte=v;
    return e;
}

esp_err_t poa_i2c_recover(void) {
    sda_release(); scl_release();
    if (scl_high_wait()!=ESP_OK) return ESP_ERR_TIMEOUT;
    for (int i=0; i<9 && !sda_high(); ++i) {
        scl_low(); delay_half();
        if (scl_high_wait()!=ESP_OK) return ESP_ERR_TIMEOUT;
        delay_half();
    }
    stop_condition();
    return (sda_high() && gpio_get_level(POA_SCL)) ? ESP_OK : ESP_ERR_INVALID_STATE;
}
static esp_err_t write_reg16(uint8_t reg, uint16_t value) {
    esp_err_t e=start_condition(false);
    if (e==ESP_OK) e=write_byte((uint8_t)(POA_ADS1115_ADDR << 1));
    if (e==ESP_OK) e=write_byte(reg);
    if (e==ESP_OK) e=write_byte((uint8_t)(value >> 8));
    if (e==ESP_OK) e=write_byte((uint8_t)value);
    stop_condition();
    return e;
}
static esp_err_t read_reg16(uint8_t reg, uint16_t *out) {
    esp_err_t e=start_condition(false);
    if (e==ESP_OK) e=write_byte((uint8_t)(POA_ADS1115_ADDR << 1));
    if (e==ESP_OK) e=write_byte(reg);
    if (e==ESP_OK) e=start_condition(true);
    if (e==ESP_OK) e=write_byte((uint8_t)((POA_ADS1115_ADDR << 1) | 1));
    uint8_t hi=0,lo=0;
    if (e==ESP_OK) e=read_byte(&hi,true);
    if (e==ESP_OK) e=read_byte(&lo,false);
    stop_condition();
    if (e==ESP_OK && out) *out=((uint16_t)hi<<8)|lo;
    return e;
}
static esp_err_t read_ads_channel(uint16_t mux, uint16_t pga, int16_t *raw) {
    uint16_t cfg = (uint16_t)(ADS_OS_SINGLE | mux | pga);
    esp_err_t e=write_reg16(ADS_REG_CONFIG,cfg);
    if (e!=ESP_OK) return e;
    int64_t deadline=esp_timer_get_time()+POA_ADC_TIMEOUT_US;
    uint16_t status=0;
    do {
        esp_rom_delay_us(2000);
        e=read_reg16(ADS_REG_CONFIG,&status);
        if (e!=ESP_OK) return e;
        if (status & 0x8000u) {
            uint16_t u=0;
            e=read_reg16(ADS_REG_CONVERSION,&u);
            if (e==ESP_OK) *raw=(int16_t)u;
            return e;
        }
    } while (esp_timer_get_time()<deadline);
    return ESP_ERR_TIMEOUT;
}

esp_err_t poa_i2c_init(void) {
    const gpio_config_t cfg={
        .pin_bit_mask=(1ULL<<POA_GPIO_SDA)|(1ULL<<POA_GPIO_SCL),
        .mode=GPIO_MODE_INPUT_OUTPUT_OD,
        .pull_up_en=GPIO_PULLUP_DISABLE, .pull_down_en=GPIO_PULLDOWN_DISABLE,
        .intr_type=GPIO_INTR_DISABLE
    };
    esp_err_t e=gpio_config(&cfg);
    if (e!=ESP_OK) return e;
    e=poa_i2c_recover();
    if (e!=ESP_OK) return e;
    uint16_t status=0;
    return read_reg16(ADS_REG_CONFIG,&status);
}
poa_calibration_t poa_default_calibration(void) {
    return (poa_calibration_t){
       .shunt_ohm=1.0f, .current_zero_uv=0.0f, .isc_ref_ma_25=58.6f,
       .alpha_isc_per_k=0.0f, .ntc_beta_k=3380.0f,
       .ntc_ref_ohm=47000.0f
    };
}

esp_err_t poa_read_sample(const poa_calibration_t *cal,
                          bool reference_calibrated,
                          poa_sample_t *out) {
    if (!cal||!out||cal->shunt_ohm<=0 || cal->isc_ref_ma_25<=0 ||
        cal->ntc_beta_k<=0 || cal->ntc_ref_ohm<=0) return ESP_ERR_INVALID_ARG;
    int32_t sum=0;
    int16_t raw=0;
    for (int i=0;i<8;i++) {
        esp_err_t e=read_ads_channel(ADS_MUX_DIFF_01, ADS_PGA_0256,&raw);
        if (e!=ESP_OK) return e;
        sum += raw;
    }
    int16_t ntc_raw=0, rail_raw=0;
    esp_err_t e=read_ads_channel(ADS_MUX_AIN2, ADS_PGA_4096,&ntc_raw);
    if (e!=ESP_OK) return e;
    e=read_ads_channel(ADS_MUX_AIN3, ADS_PGA_4096,&rail_raw);
    if (e!=ESP_OK) return e;
    /* 7.8125 uV/LSB at +/-0.256 V; 0.125 mV/LSB at +/-4.096 V */
    float sense_uv=(float)sum / 8.0f * 7.8125f - cal->current_zero_uv;
    float i_ma=sense_uv / (1000.0f * cal->shunt_ohm);
    float vntc=(float)ntc_raw * 0.000125f;
    float vrail=(float)rail_raw * 0.00025f; /* AIN3 = 1:2 VDD divider */
    if (!isfinite(vntc)||!isfinite(vrail)||vrail<2.7f||vrail>3.6f||
        vntc<=0.01f||vntc>=vrail-0.01f || i_ma < -1.0f ||
        i_ma>250.0f) return ESP_ERR_INVALID_RESPONSE;
    float rntc=cal->ntc_ref_ohm*vntc/(vrail-vntc);
    if (rntc<500.0f || rntc>1000000.0f) return ESP_ERR_INVALID_RESPONSE;
    float t_c=1.0f/(1.0f/298.15f + logf(rntc/10000.0f)/cal->ntc_beta_k)-273.15f;
    float correction=1.0f+cal->alpha_isc_per_k*(t_c-25.0f);
    if (correction<0.8f||correction>1.2f || t_c < -45.0f || t_c>110.0f)
        return ESP_ERR_INVALID_RESPONSE;
    *out=(poa_sample_t){
        .current_ma=i_ma,
        .reference_cell_temp_c=t_c,
        .supply_v=vrail,
        .irradiance_w_m2=fmaxf(0.0f,i_ma)*1000.0f/cal->isc_ref_ma_25/correction,
        .calibrated=reference_calibrated,
        .timestamp_us=esp_timer_get_time(),
    };
    return ESP_OK;
}
