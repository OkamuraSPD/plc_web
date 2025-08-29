from flask import Flask, request, jsonify, render_template
import json
import os
from plc import PLC_IO, PLCController

app = Flask(__name__)

PLC_IP = '192.168.1.10'
plc_io = PLC_IO(PLC_IP)
controller = PLCController(plc_io)

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
    switch_id = str(data.get("id"))
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

    plc_io.open()
    address, value = controller.process_post(data)
    plc_io.close()
    print(f"Zapsáno do PLC: {address} = {value}")

    return jsonify({"id": switch_id, "value": value})

if __name__ == "__main__":
    app.run(debug=True)
