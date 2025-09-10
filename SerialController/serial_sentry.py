import copy

from .comport import Comport
from .serial_controller import SerialObj
from dataclasses import dataclass
from time import sleep
from threading import Thread
from typing import List

@dataclass
class ChangedComport:
    time_changed: int
    initial_comport: Comport
    new_comport: Comport

class SerialSentry:
    def __init__(self):
        self.comports: List[Comport] = []
        self.serial_controllers: List[SerialObj] = []

        self.changed_comports: List[ChangedComport] = []

    def open_comport(self) -> SerialObj:
        new_serial_controller = SerialObj()

        new_comport = new_serial_controller.init_comport()
        self.comports.append(new_comport)

        new_serial_controller.open_comport()
        self.serial_controllers.append(new_serial_controller)

        return new_serial_controller
    
    def close_comport(self, serial_controller: SerialObj) -> bool:
        if serial_controller.close_comport():
            self.comports.remove(serial_controller.comport)
            self.serial_controllers.remove(serial_controller)
            
            return True
        else:
            return False
        
    def monitor_comports_thread(self, time) -> None:
        curr_time = 0
        #initial_comports = list(self.comports) # Take a snapshot of initial comports
        initial_comports = copy.deepcopy(self.comports)
        changed_comports = []

        while curr_time < time:
            #curr_comports = list(self.comports) # Take a snapshot of current comports
            curr_comports = copy.deepcopy(self.comports)

            for initial_comport, curr_comport in zip(initial_comports, curr_comports):
                print("Initial Comport: {}".format(initial_comport))
                print("Current Comport: {}".format(curr_comport))
                if initial_comport != curr_comport:
                    print("Found difference")
                    comport_report = ChangedComport(
                        time_changed=curr_time,
                        initial_comport=initial_comport,
                        new_comport=curr_comport
                    )
                    changed_comports.append(comport_report)
                    #initial_comports = list(self.comports) # Take a snapshot of new initial comports
                    initial_comports = copy.deepcopy(self.comports)

            print("Current changed_comports:")
            print(changed_comports)

            sleep(1)
            curr_time += 1

        self.changed_comports = changed_comports
    
    def monitor_comports(self, time: int) -> None:
        monitor = Thread(target=self.monitor_comports_thread, args=[time], daemon=True)
        monitor.start()

    def get_changed_comports(self) -> List[ChangedComport]:
        return self.changed_comports

    def monitor_serial_controllers(self) -> List[SerialObj]:
        return []
        
    def __str__(self):
        return (
            "Serial Sentry: " + " "
            "Comports: {}".format(self.comports) + " "
            "Serial Controllers: {}".format(self.serial_controllers)
        )
    
    def __repr__(self):
        return self.__str__()
