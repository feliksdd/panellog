#pragma once
#include <stdbool.h>
#include <stdint.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Dedicated software I2C: ESP32-C6-MINI-1 pad 27 / GPIO21 = SDA;
 * pad 28 / GPIO22 = SCL. Not shared with INA237 GPIO6/7.
 * External pull-ups REQUIRED. */
#define POA_GPIO_SDA 21
#define POA_GPIO_SCL 22
#define POA_ADS1115_ADDR 0x48

typedef struct {
    float shunt_ohm;         /* calibrated, default 1.0 */
    float current_zero_uv;   /* measured ADC shunt zero at dark */
    float isc_ref_ma_25;     /* individual cell calibration; nominal 58.6 */
    float alpha_isc_per_k;   /* measured Isc temperature coefficient; 0 if unknown */
    float ntc_beta_k;       /* prototype approximation, use R/T table for release */
    float ntc_ref_ohm;      /* divider top resistor, default 47000 */
} poa_calibration_t;

typedef struct {
    float irradiance_w_m2;  /* nominal/uncompensated until reference calibration */
    float reference_cell_temp_c;
    float current_ma;
    float supply_v;
    bool calibrated;
    int64_t timestamp_us;
} poa_sample_t;

/* Initialize independent 25 kHz, open-drain software I2C; idle-high sanity test.
 * On absent/unpowered POA, returns ESP_ERR_NOT_FOUND, never zero irradiance. */
esp_err_t poa_i2c_init(void);
esp_err_t poa_i2c_recover(void);
esp_err_t poa_read_sample(const poa_calibration_t *cal,
                          bool reference_calibrated,
                          poa_sample_t *out);
poa_calibration_t poa_default_calibration(void);

#ifdef __cplusplus
}
#endif
