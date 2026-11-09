idf_component_register(
    SRCS "poa_soft_i2c.c"
    INCLUDE_DIRS "include"
    REQUIRES esp_driver_gpio esp_timer esp_rom
)
