# SDECv2 Coding Standards

SDECv2 aims to upgrade SDEC by incorporating Object Oriented Programming to encourage Modularity, Scalability, and Maintainability. As well as coding standards and consistent styles to promote ease of use and understanding.  

---

## 1. License Header

Every source file must begin with the BSD-3-Clause SPDX header:

```python
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry
```

This applies to all `.py` files, including `__init__.py`.

---

## 2. Project Structure

The project is organized into top-level **module packages**, each with its own `__init__.py`. New functionality belongs in the appropriate existing module, or in a new top-level package following the same pattern.

```
SDECv2/
├── a_input/          # Input files (e.g., presets to upload)
├── a_output/         # Output files (e.g., downloaded presets, CSVs)
├── BaseController/   # Hardware abstraction (Controller, Firmware, BaseSensor)
├── Parser/           # Preset config parsing and flash extraction
├── Sensor/           # Sensor definitions, polling, and sentry logic
├── SerialController/ # Serial port management and sentry
└── Testing/          # Test scripts, mirroring the module structure above
    ├── BaseController/
    ├── Parser/
    ├── Sensor/
    └── SerialController/      
```

Test files are named `test_<subject>.py` and placed under `Testing/<module>/`.

---

## 3. Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Classes | `PascalCase` | `BaseController`, `SerialObj` |
| Functions / Methods | `snake_case` | `open_comport`, `flash_extract` |
| Variables | `snake_case` | `preset_data`, `sensor_frame_names` |
| Constants | `UPPER_SNAKE_CASE` | `FLASH_SIZE` |
| Private methods | Leading underscore | `_parse_preset`, `_compute_frames` |
| Module-level files | `snake_case` | `serial_controller.py`, `create_configs.py` |
| Factory files | `create_<subject>.py` | `create_controllers.py`, `create_configs.py` |

| Abbreviation | Full Name | Description |
|---|---|---|
| SDEC | Sun Devil Embedded Control | Refers to the original program to control the Flight Computer |
| SDECv2 | Sun Devil Embedded Control Version 2 | Refers to this project, the upgrade to SDEC |
| APPA | All Purpose Primary Avionics | Refers to v2.5.0 of the Flight Computer Firmware |

---

## 4. Imports

Imports follow this order, separated by a blank line between each group:

1. Standard library (`builtins`, `json`, `os`, `struct`, `time`)
2. Third-party packages (`serial`, `pandas`)
3. Internal relative imports (`.module`)
4. Cross-package absolute imports (`SDECv2.BaseController`, `SDECv2.SerialController`)
5. `typing` imports (`List`, `Callable`, `Generator`)

```python
import json
import os
import struct

import pandas as pd
import serial

from .preset_config import PresetConfig, ConfigEntry
from .preset_data import PresetData

from SDECv2.SerialController import SerialObj

from typing import List
```

Wildcard imports (`from module import *`) are not used. These can cause the python interpreter in VSCode to incorrectly show import errors.

---

## 5. Type Annotations

All function signatures include type annotations for parameters and return values. Use `|` union syntax (Python 3.10+) for optional or multi-type parameters.

```python
def poll(
    self,
    serial_connection: SerialObj,
    timeout: int | None = None,
    count: int | None = None
) -> Generator[float | int, None, None]:
```

Use `typing.List`, `typing.Callable`, and `typing.Generator` for complex generic types. For forward references to the enclosing class, use a string literal:

```python
@classmethod
def from_file(cls, path: str) -> "Parser":
```

---

## 6. Docstrings

Every class and public method has a docstring. Use the following format:

```python
def method(self, arg: Type) -> ReturnType:
    """
    One-sentence summary of what this method does.

    Args:
        arg (Type): Description of the argument.

    Returns:
        ReturnType: Description of the return value.

    Raises:
        ExceptionType: When and why this is raised.
    """
```

- The `Raises` section is included only when the method explicitly raises exceptions.
- Private methods (prefixed with `_`) follow the same docstring format.
- Inline comments are used for non-obvious protocol details, especially serial byte sequences.

---

## 7. Classes

Classes use `PascalCase` and include a two-line class-level docstring: one sentence describing the class purpose, and one sentence describing what it provides.

```python
class Parser:
    """
    Parses and manages preset configurations and data for the Flight Computer.
    Provides methods to load, verify, upload, and manipulate presets.
    """
```

`__str__` and `__repr__` are implemented for all major model classes. `__str__` uses a consistent `"ClassName:{\n...\n}"` format:

```python
def __str__(self):
    return (
        "Base Controller:{" + 
        "\n{}".format(self.firmware) +
        "\n{}".format(self.controller) +
        "\n}"
    )
```

`__eq__` and `__hash__` are implemented together whenever objects are compared or used in sets/dicts.

---

## 8. Error Handling

- Raise `ValueError` with a descriptive `"Error: ..."` message for invalid inputs or state.
- Use `print(f"Error: {e}")` inside `try/except` blocks for serial communication failures — do not let serial exceptions propagate silently.
    - This will eventually be required to raise a custom Exception instead. As the CLI and API projects will want to catch any error states SDEC enters.
- Use `print(f"Warning: ...")` for non-fatal anomalies (e.g., checksum mismatches).
    - This will eventually be required to raise a custom Exception instead. Projects, such as CLI or API, that use SDEC should determine if an error is fatal or non-fatal.
- Guard against missing files with an existence check and a descriptive print before raising:

```python
if not os.path.exists(path):
    print(f"File {path} does not exist")
```

---

## 9. Serial Protocol Conventions

Serial opcodes and subcommand codes are written as byte literals inline, always accompanied by a comment:

```python
serial_connection.send(b"\x24")  # preset opcode
serial_connection.send(b"\x01")  # upload subcommand code
```

- Opcodes are in [mod/commands/commands.h](https://github.com/SunDevilRocketry/mod/blob/4b30d34fa129b3bf7de8c2788d69bee6090bcc5d/commands/commands.h)
- Subcommand codes are in the command's implementation in `mod/<command>.h`
    - For example, Sensor subcommand codes would be in `mod/sensor.h`
    - Preset subcommand codes exist in [app/flight/appa/rev2/prelaunch.c](https://github.com/SunDevilRocketry/Flight-Computer-Firmware/blob/17f114ad792112b6ff1f475bb20944a4bf81f99c/app/flight/appa/rev2/prelaunch.c#L362)

---

## 10. Factory Functions

Reusable object construction is handled by dedicated `create_<subject>.py` files (e.g., `create_controllers.py`, `create_configs.py`). These expose named factory functions rather than requiring callers to construct objects manually. When adding a new hardware configuration or preset type, add a factory function to the appropriate `create_` file rather than inlining construction in calling code.

---

## 11. Testing

- Test files are standalone scripts with a `if __name__ == "__main__":` guard.
- Each test file contains one or more `test_<scenario>()` functions.

---

*Last updated: 3/24/2026*
