from Parser import Parser, PresetConfig, DataBitmask, FeatureBitmask, create_configs
from SerialController import SerialObj

def test_preset():
    appa_feature_bitmask = create_configs.appa_feature_bitmask()
    appa_data_bitmask = create_configs.appa_data_bitmask()
    appa_preset_config = create_configs.appa_preset_config()

    print(appa_preset_config.pretty_print())

def test_flash_extract():
    serial_connection = SerialObj()
    serial_connection.init_comport("COM6", 921600, 1)
    serial_connection.open_comport()

    appa_preset_config = create_configs.appa_preset_config()
    appa_parser = Parser(
        preset_config=appa_preset_config,
        preset_data=None
    )
    
    all_flash_data = appa_parser.flash_extract(serial_connection, store_preset=True, store_data=True)

    serial_connection.close_comport()

def test_upload_preset():
    serial_connection = SerialObj()
    serial_connection.init_comport("COM5", 921600, 1)
    serial_connection.open_comport()

    parser = Parser.upload_preset(serial_connection, path="a_input/to_upload_preset.json")

    serial_connection.close_comport()

def test_download_preset():
    serial_connection = SerialObj()
    serial_connection.init_comport("COM5", 921600, 1)
    serial_connection.open_comport()

    appa_preset_config = create_configs.appa_preset_config()
    appa_parser = Parser(
        preset_config=appa_preset_config,
        preset_data=None
    )

    appa_parser.download_preset(serial_connection)

    serial_connection.close_comport()

def test_verify_preset():
    serial_connection = SerialObj()
    serial_connection.init_comport("COM5", 921600, 1)
    serial_connection.open_comport()

    downoaded_parser = Parser.from_file(path="a_output/downloaded_preset.json")
    verify_result = downoaded_parser.verify_preset(serial_connection)

    # print(f"{"Valid Preset" if verify_result else "Invalid Preset"}")

def test_from_file_flash_extract():
    serial_connection = SerialObj()
    serial_connection.init_comport("COM5", 921600, 1)
    serial_connection.open_comport()

    downloaded_parser = Parser.from_file(path="a_input/to_upload_preset.json")
    
    all_flash_data = downloaded_parser.flash_extract(serial_connection, store_preset=True, store_data=True)

    serial_connection.close_comport()

if __name__ == "__main__":
    test_flash_extract()