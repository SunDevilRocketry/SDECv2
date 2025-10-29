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
            "\b Name: {}".format(self.name) + 
            "\b Size: {}".format(self.size) + 
            "\b Data Type: {}".format(self.data_type) +
            "\b Units: {}".format(self.units) +
            "\n}"
        )