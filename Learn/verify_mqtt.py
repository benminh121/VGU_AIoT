# register service
from datetime import datetime
import time
import json
import ssl
import paho.mqtt.client as paho
import requests

print("Hello MQTT")

# define callbacks
def on_message(client, userdata, message):
    print("received message =", str(message.payload.decode("utf-8")))
    responseDevice = open("response_device.txt", "w")
    responseDevice.write(str(message.payload.decode("utf-8")))
    responseDevice.close()


def on_log(client, userdata, level, buf):
    # print("log: ",buf)
    return


def on_connect(client, userdata, flags, rc):
    print("Connected to Broker!!!")
    # client.subscribe("smartspeaker_0001")
    client.subscribe("ts/event/smartspeaker_demo_0001")


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")


url = 'https://192.168.3.111:8080/register'
myobj = {
    "id": "python_smartspeaker_0001",
    "name": "python_hub",
    "software_info": {
        "version": "0.0.1",
        "commit": "0d2168e69dd18f5548d128d886ca8067aec88ab2",
        "build_date": ""
    },
    "hardware_info": {
        "protocol.zib": False,
        "protocol.zwa": False
    }
}
headers = {'Content-Type': 'application/json'}

demo_device = {
    "id": "smartspeaker_demo_0001",
    "name": "hub",
    "status": 0,
    "software_info": {
        "version": "0.0.1",
        "commit": "0d2168e69dd18f5548d128d886ca8067aec88ab2",
        "build_date": ""
    },
    "hardware_info": {
        "protocol.zib": False,
        "protocol.zwa": False
    }
}

# Login server using id and secret
url_login = "https://192.168.3.111:8080/login"
data_login = {
    "id": "smartspeaker_0001",
    "secret": "42aa73a368d0a820eeb044dcc7a55a37"
}
data_login = {
    "id": "smartspeaker_demo_0001",
    "secret": "a81aa465bf1afcde30cbc803bb7d71d0"
}

x = requests.post(url=url_login, json=data_login, verify=False)

reponse_login = x.json()
print(reponse_login["success"])
if reponse_login["success"] == True:
    print("Token: ", reponse_login["jwt_info"]["token"])
    print("Public Key: ", reponse_login["jwt_info"]["public_key"])
else:
    print("Error Login Process", reponse_login["error_info"])

# Validate the service using id and secret
url_validate = "https://192.168.3.111:8080/login"
data_validate = {
    "id": "smartspeaker_0001",
    "secret": "42aa73a368d0a820eeb044dcc7a55a37"
}
data_validate = {
    "id": "smartspeaker_demo_0001",
    "secret": "a81aa465bf1afcde30cbc803bb7d71d0"
}

x = requests.post(url=url_validate, json=data_validate, verify=False)
print(x.json())

# Get Broker Info: Certification file
request_broker_url = "https://192.168.3.111:8080/auth/broker"
params = {"AccessToken": reponse_login["jwt_info"]["token"]}
print("GET Broker Info:", params)
headers = {'AccessToken': reponse_login["jwt_info"]["token"]}
AUTH_TOKEN = reponse_login["jwt_info"]["token"]
x = requests.get(url=request_broker_url, headers=headers, verify=False)
brokerInfo = x.json()
# print("Port:", brokerInfo["broker_info"]["port"])
# print("Cafile:", brokerInfo["broker_info"]["cafile"])
# print("Address:", brokerInfo["broker_info"]["address"])

fCertificate = open("iot.crt", "w")
fCertificate.write(brokerInfo["broker_info"]["cafile"])
fCertificate.close()
# https://stackoverflow.com/questions/51942821/how-to-use-ssl-tls-in-paho-mqtt-using-python-i-got-certificate-verify-failed

client = paho.Client()
client.on_message = on_message
client.on_log = on_log
client.on_connect = on_connect
client.on_subscribe = subscribed
print("Connecting to broker")
# client.username_pw_set(username="smartspeaker_0001", password="42aa73a368d0a820eeb044dcc7a55a37")
client.username_pw_set(username="smartspeaker_demo_0001",
                       password="a81aa465bf1afcde30cbc803bb7d71d0")

client.tls_set("iot.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)
# client.tls_set(ca_certs="iot.crt", certfile=None,
#                             keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
#                             tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.connect("192.168.3.111", 8883, 60)

# start loop to process received messages
client.loop_start()
# wait to allow publish and logging and exit
time.sleep(1)
counter = 0


def publish_status():
    mydata = {
        "id": "smartspeaker_demo_0001",
        "name": "hub",
        "status": 1,
        "software_info": {
            "version": "0.0.1",
            "commit": "0d2168e69dd18f5548d128d886ca8067aec88ab2",
            "build_date": ""
        },
        "hardware_info": {
            "protocol.zib": False,
            "protocol.zwa": False
        }
    }
    client.publish("vs/status/smartspeaker_demo_0001", str(mydata))
    print("Publish device status")


def publish_device_list():
    payload = {
        "name": "vs.ts.device.list.requested",
        "scope": "device",
        "source": "vs",
        "home_id": "HOME_ID",
        "user_id": "",
        "id": "MESSAGE_ID",
        "auth_token": "AUTH_TOKEN",
        "parent_id": "",
        "client_id": "VS_ID",
        "created_time": 1584501452048,
        "data": "voice demo testing"
    }
    payload["auth_token"] = AUTH_TOKEN
    payload["client_id"] = "smartspeaker_demo_0001"
    payload["created_time"] = int(datetime.utcnow().timestamp() * 1000)
    payload["id"] = "demo_message_001"
    payload["home_id"] = "home-0c769f34-9f62-11ec-acf2-00044bebd516"
    print(payload["created_time"])
    print(payload)
    client.publish("vs/event/smartspeaker_demo_0001", str(payload))
    print("Publish get device list")
    return


def publish_control_deive():
    payload = {
        "name": "vs.ts.device.state.updated",
        "scope": "device",
        "source": "vs",
        "home_id": "HOME_ID",
        "user_id": "",
        "id": "MESSAGE_ID",
        "auth_token": "AUTH_TOKEN",
        "parent_id": "",
        "client_id": "VS_ID",
        "created_time": 1584501452048,
        "data": " "
    }
    payload["auth_token"] = AUTH_TOKEN
    payload["client_id"] = "smartspeaker_demo_0001"
    print(payload)
    return


def test_phillip_led(status):
    payload = {
        "scope": "device",
        "name": "app.ts.device.state.updated",
        "source": "app",
        "home_id": "home-0c769f34-9f62-11ec-acf2-00044bebd516",
        "user_id": "admin@home.com",
        "id": "2d4c2e61-c6cf-11ec-bf5b-17aa7d20b047",
        "auth_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTEyMjA2NjYsImlhdCI6MTY1MTEzNDI2NiwiaXNzIjoiTm92YUluVGVjaHMiLCJzZXJ2aWNlX2lkIjoiaW9zLXBob25lLTY0RTgwQUVBLTRGNTEtNDRFMy05RDIzLUZEQkQ3NDQyOEFGRCIsInVzZXJfaWQiOiJhZG1pbkBob21lLmNvbSJ9.l5e8uH-fjhdVzOryATStrg9rS8Map6KPn_JBFomTiN38xatz-yaUpQ6ImdLLCRlEZ2Z8NKWZwpcdLKQWJIpcOhDFVPNy0qujrTSqJcrAr2F5TcPUKR4Bf-YKdZou8JByTNHsb7yspX01bXBH0tNzA-_alaIlaD1sNtnGvIPNuFxXobWE3Tg5RHt232yL7VOMEzjJ0bVwA2hZaHmVy5lGcA3Sylteb0LtryWxJLYfpPN3_1TXaWGCP7glLNnMGMNXGydsPVlcf6O3-ExMZ05iulC68yzY9d467wbg25Sh7Dq_Zs4MqZXYTtrjkJTKt3-JWd2pTfRZsqGvjZ60iQjmEQ",
        "parent_id": "",
        "client_id": "ios-phone-64E80AEA-4F51-44E3-9D23-FDBD74428AFD",
        "created_time": 1651135366214,
        "data": {
            "devices": [{
                "id": "aafc7ad0-c6b2-11ec-8f35-00044bebd516",
                "name": "Phillip (new)",
                "status": 0,
                "mac": "ZIB_0017880108ACF150",
                "zone_id": "zone-0c77f51e-9f62-11ec-acf2-00044bebd516",
                "power_source": 0,
                "position": 0,
                "controller_id": "hub_ecfb1cfb-975c-4c96-83bf-2cadc5fca5b8",
                "protocol": "zib",
                "virtual_type": 0,
                "home_id": "home-0c769f34-9f62-11ec-acf2-00044bebd516",
                "hardware_type": 0,
                "profiles": {
                    "fw_version": "2",
                    "manufacturer_id": "",
                    "commit_fw_version": "",
                    "hw_version": "5",
                    "manufacturer": "Philips",
                    "joined_time": 1651123121000,
                    "product_id": "",
                    "commit_hw_version": "",
                    "nexthop_id": "id_unknown"
                },
                "end_points": [
                    {
                        "id": "11",
                        "type": 3,
                        "name": "color_switch",
                        "is_controllable": True,
                        "settings": "",
                        "user_pins": "",
                        "attributes": {
                            "on_off.value": True
                        }
                    },
                    {
                        "id": "242",
                        "type": 0,
                        "name": "name_unknown",
                        "is_controllable": True,
                        "settings": "",
                        "user_pins": "",
                        "attributes": {
                            "on_off.value": True
                        }
                    }
                ]
            }]}
    }
    payload["auth_token"] = AUTH_TOKEN
    payload["user_id"] = "smartspeaker_demo_0001"
    payload["client_id"] = "smartspeaker_demo_0001"
    payload["created_time"] = int(datetime.utcnow().timestamp() * 1000)
    payload["id"] = "demo_message_001"
    payload["home_id"] = "home-0c769f34-9f62-11ec-acf2-00044bebd516"
    payload["source"] = "vs"
    payload["name"] = "vs.ts.device.state.updated"
    jsonArray = payload["data"]["devices"][0]["end_points"]
    print(jsonArray)
    for endpoint in jsonArray:
        endpoint["attributes"]["on_off.value"] = status

    print(json.dumps(payload))
    client.publish("vs/event/smartspeaker_demo_0001", json.dumps(payload))


publish_status()
# publish_device_list()


while True:
    print("Client is running...")
    # counter = counter + 1
    # client.publish("smartspeaker_0001", "Test Smart Speaker " + str(counter))
    test_phillip_led(True)
    time.sleep(5)
    test_phillip_led(False)
    time.sleep(5)
