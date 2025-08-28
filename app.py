from flask import Flask, request, jsonify, render_template
import json
import os
from plc import write_to_plc
from plc import PLC_IO
from pycomm3 import LogixDriver

app = Flask(__name__)

PLC_IP = '192.168.1.10'
plc = LogixDriver(PLC_IP)

DATA_FILE = os.path.join("static", "data.json")

# inicializace JSONu pokud neexistuje
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/toggle", methods=["POST"])
def toggle():
    data = request.get_json()
    switch_id = str(data.get("id"))  # klíč bude string
    value = data.get("value")

    # načti aktuální JSON
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            current = json.load(f)
    else:
        current = {}

    # aktualizuj příslušný přepínač
    current[switch_id] = value

    # ulož zpět
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f)

    plc.open()
    plc.write(write_to_plc(data) )
    plc.close()
    print(write_to_plc(data) )
    
    
    return jsonify({"id": switch_id, "value": value})
    


if __name__ == "__main__":
    app.run(debug=True)
