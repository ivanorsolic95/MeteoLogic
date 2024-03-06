import urequests
import ujson as json

def sendData(payload):
    headers = {"Content-Type": "application/json"}

    if not payload:
        print("Payload is empty or None. Not sending.")
        return

    response = urequests.post(
        url="https://maker.ifttt.com/trigger/esp32_measurement/json/with/key/typeyourkey",
        data=json.dumps(payload),
        headers=headers
    )

    if response.status_code == 200:
        print("Successfully sent data to IFTTT.")
    else:
        print(f"Failed to send data to IFTTT. Status code: {response.status_code}")

    response.close()
     