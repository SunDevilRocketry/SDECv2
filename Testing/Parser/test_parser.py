from Parser import Preset, PresetConfig, Bitmask, create_configs

def test_preset():
    appa_bitmask = create_configs.appa_bitmask()

    appa_preset_config = PresetConfig(
        enabled_flags=appa_bitmask,
        enabled_data=Bitmask(features=[])
    )

    appa_preset = Preset(config_settings=appa_preset_config)

    print(appa_preset)

if __name__ == "__main__":
    test_preset()