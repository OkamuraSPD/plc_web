import json
import os
from pycomm3 import LogixDriver

DATA_FILE = os.path.join("static", "data.json")

# Funkce pro získání poslední změny
def get_last_change(post_data):
    # post_data = {"id": "2", "value": 1}
    switch_id = post_data["id"]
    value = post_data["value"]
    return switch_id, value

# Funkce pro zápis do PLC
def write_to_plc(post_data):
    switch_id, value = get_last_change(post_data)
    print(f"Zapisujeme do PLC: switch {switch_id} = {value}")
    return "Local:1:"+switch_id.split("_")[0]+".Data."+switch_id.split("_")[1], value
    # Zde by přišla logika s pycomm3
    # with LogixDriver('192.168.1.10/1') as plc:
    #     plc.write(f"Switch_{switch_id}", value)





class PLC_IO:
    def __init__(self, ip):
        self.plc = LogixDriver(ip)
        # seznam 16 vstupů a 16 výstupů ve správném formátu
        self.inputs = [f"Local:1:I.Data.{i}" for i in range(16)]
        self.outputs = [f"Local:1:O.Data.{i}" for i in range(16)]

    def open(self):
        
        self.plc.open()

    def close(self):
        
        self.plc.close()

    



if __name__ == "__main__":
    ip = '192.168.1.101'

    
    plc = PLC_IO(ip)
    plc.open()
    

    plc.close()


