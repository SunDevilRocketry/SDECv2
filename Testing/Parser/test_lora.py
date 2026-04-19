from time import sleep

from Parser import Parser, PresetConfig, DataBitmask, FeatureBitmask, create_configs
from SerialController import SerialObj

def test_upload_download():
    serial_connection = SerialObj()
    serial_connection.init_comport("COM4", 921600, 1)
    serial_connection.open_comport()

    appa_preset_config = create_configs.appa_preset_config()
    parser = Parser(
        preset_config=appa_preset_config,
        preset_data=None
    )

    parser.upload_lora_preset(serial_connection, path="a_input/lora_preset.json")
    print("uploaded lora_preset.json")
    sleep(1)
    parser.download_lora_preset(serial_connection, path="a_output/downloaded_lora_preset.json")
    print("downloaded downloaded_lora_preset.json")
    sleep(1)
    # parser.flash_extract(serial_connection)
    # print("extracted flash")

    serial_connection.close_comport()

if __name__ == "__main__":
    test_upload_download()