from Parser import Parser, Preset, PresetConfig, Bitmask, create_configs
from SerialController import SerialObj

def test_preset():
    appa_bitmask = create_configs.appa_bitmask()

    appa_preset_config = PresetConfig(
        enabled_flags=appa_bitmask,
        enabled_data=Bitmask(features=[])
    )

    appa_preset = Preset(config_settings=appa_preset_config)

    print(appa_preset)

def test_flash_extract():
    serial_connection = SerialObj()
    serial_connection.init_comport("COM3", 921600, 5)
    serial_connection.open_comport()

    appa_bitmask = create_configs.appa_bitmask()

    appa_preset_config = PresetConfig(
        enabled_flags=appa_bitmask,
        enabled_data=Bitmask(features=[])
    )

    appa_preset = Preset(config_settings=appa_preset_config)

    # TODO move this to a create function since frame size is a hard value
    appa_parser = Parser(preset=appa_preset,
                         data_bitmask=appa_bitmask,
                         features=appa_bitmask.features,
                         sensor_frame_size=126,
                         num_frames=524288 // 126)
    
    appa_parser.flash_extract(serial_connection)

if __name__ == "__main__":
    test_preset()