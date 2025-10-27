import copy

from .comport import Comport, Status
from .serial_controller import SerialObj
from dataclasses import dataclass
from time import sleep
from threading import Thread
from typing import List, Dict

@dataclass
class SnapshotSerialObj:
    comport_status: Status
    name: str

@dataclass
class ChangedSerialObj:
    time_changed: int
    initial_snapshot: SnapshotSerialObj
    new_snapshot: SnapshotSerialObj

class SerialSentry:
    def __init__(self):
        self.serial_objs: List[SerialObj] = []

        self.changed_serial_objs: List[ChangedSerialObj] = []

    def open_serial(self, name: str, baudrate: int, timeout: int) -> SerialObj:
        new_serial_connection = SerialObj()

        new_serial_connection.init_comport(name, baudrate, timeout)

        new_serial_connection.open_comport()

        self.serial_objs.append(new_serial_connection)

        return new_serial_connection
    
    def close_serial(self, serial_controller: SerialObj) -> bool:
        if serial_controller.close_comport():
            self.serial_objs.remove(serial_controller)
            
            return True
        else:
            return False
        
    def snapshot_serial_objs(self) -> List[SnapshotSerialObj]:
        snapshots = []
        for serial_obj in self.serial_objs:
            snapshots.append(SnapshotSerialObj(
                comport_status=serial_obj.comport.status,
                name=serial_obj.comport.name
            ))
        return snapshots
        
    def monitor_serial_objs_thread(self, time: int) -> None:
        curr_time = 0
        initial_serial_objs = self.snapshot_serial_objs()
        changed_serial_objs = []

        while curr_time < time:
            curr_serial_objs = self.snapshot_serial_objs()

            for initial_serial_obj, curr_serial_obj in zip(initial_serial_objs, curr_serial_objs):
                print("Initial Comport: {}".format(initial_serial_obj))
                print("Current Comport: {}".format(curr_serial_obj))
                if initial_serial_obj != curr_serial_obj:
                    print("Found difference")
                    serial_obj_report = ChangedSerialObj(
                        time_changed=curr_time,
                        initial_snapshot=initial_serial_obj,
                        new_snapshot=curr_serial_obj
                    )
                    changed_serial_objs.append(serial_obj_report)
                    initial_serial_objs = self.snapshot_serial_objs()

            print("Current changed_serial_objs:")
            print(changed_serial_objs)

            sleep(1)
            curr_time += 1

        self.changed_serial_objs = changed_serial_objs
    
    def monitor_serial_objs(self, time: int) -> None:
        monitor = Thread(target=self.monitor_serial_objs_thread, args=[time], daemon=True)
        monitor.start()

    def get_changed_serial_objs(self) -> List[ChangedSerialObj]:
        return self.changed_serial_objs
        
    def __str__(self):
        return (
            "Serial Sentry: " +
            "Serial Controllers: {}".format(self.serial_objs)
        )
    
    def __repr__(self):
        return self.__str__()
