from dataclasses import dataclass

@dataclass
class Sensor:
    short_name: str
    name: str
    size: int
    data_type: type
    units: str

    def __str__(self):
        return (
            "Sensor:{" +
            "\n Short Name: {}".format(self.short_name) +
            "\n Name: {}".format(self.name) + 
            "\n Size: {}".format(self.size) + 
            "\n Data Type: {}".format(self.data_type) +
            "\n Units: {}".format(self.units) +
            "\n}"
        )