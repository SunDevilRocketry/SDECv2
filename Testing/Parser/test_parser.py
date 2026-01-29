from Parser import Parser, Preset, PresetConfig, DataBitmask, FeatureBitmask, create_configs
from SerialController import SerialObj

def test_preset():
    appa_feature_bitmask = create_configs.appa_feature_bitmask()
    appa_data_bitmask = create_configs.appa_data_bitmask()

    appa_preset_config = PresetConfig(
        enabled_features=appa_feature_bitmask,
        enabled_data=appa_data_bitmask
    )

    appa_preset = Preset(config_settings=appa_preset_config)

    print(appa_preset)

def test_flash_extract():
    serial_connection = SerialObj()
    serial_connection.init_comport("COM6", 921600, 5)
    serial_connection.open_comport()

    appa_feature_bitmask = create_configs.appa_feature_bitmask()
    appa_data_bitmask = create_configs.appa_data_bitmask()

    appa_preset_config = PresetConfig(
        enabled_features=appa_feature_bitmask,
        enabled_data=appa_data_bitmask
    )

    appa_preset = Preset(config_settings=appa_preset_config)

    appa_parser = Parser(preset=appa_preset)
    
    all_flash_data = appa_parser.flash_extract(serial_connection)

    for flash_data in all_flash_data:
        print(f"{flash_data.data_name}:")    
        for sensor, value in flash_data.values.items():
            print(f"  {sensor.short_name}: {value}")    

    serial_connection.close_comport()

if __name__ == "__main__":
    test_preset()
    test_flash_extract()