import json
import os
from pycomm3 import LogixDriver

DATA_FILE = os.path.join("static", "data.json")

class PLC_IO:
    def __init__(self, ip):
        self.ip = ip
        self.plc = LogixDriver(ip)
        self.inputs = [f"Local:1:I.Data.{i}" for i in range(16)]
        self.outputs = [f"Local:1:O.Data.{i}" for i in range(16)]

    def open(self):
        self.plc.open()

    def close(self):
        self.plc.close()

    def write(self, address, value):
        print(f"Zapisujeme do PLC: {address} = {value}")
        # Zde by přišla logika s pycomm3
        # self.plc.write(address, value)

    def read(self, address):
        # Vráti hodnotu z PLC (mock):
        # return self.plc.read(address)
        pass

class PLCController:
    def __init__(self, plc_io):
        self.plc_io = plc_io

    def get_last_change(self, post_data):
        switch_id = post_data["id"]
        value = post_data["value"]
        return switch_id, value

    def get_address(self, switch_id):
        parts = switch_id.split("_")
        # Local:1:O.Data.2
        return f"Local:1:{parts[0]}.Data.{parts[1]}"

    def process_post(self, post_data):
        switch_id, value = self.get_last_change(post_data)
        address = self.get_address(switch_id)
        self.plc_io.write(address, value)
        return address, value

if __name__ == "__main__":
    ip = '192.168.1.101'
    plc_io = PLC_IO(ip)
    controller = PLCController(plc_io)

    plc_io.open()

    # Příklad POST data
    post_data = {"id": "O_2", "value": 1}
    controller.process_post(post_data)

    plc_io.close()
