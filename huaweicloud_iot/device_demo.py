# -*- coding: utf-8 -*-
"""
华为云 IoTDA 设备侧 MQTT 联调示例（参考实现，需 paho-mqtt）

运行： pip install paho-mqtt
      python device_demo.py
说明：演示设备如何连上华为云并上报/接收命令的完整握手，
      用于在没有硬件时也能在 PC 上把协议跑通、讲清原理。
      真实 STM32/ESP8266 侧是把下面逻辑用 C + AT 指令 + cJSON 实现。
"""
import json
import time
from paho.mqtt import client as mqtt

SERVER = "iot-mqtts.cn-north-4.myhuaweicloud.com"
PORT = 8883
DEVICE_ID = "dev001"
SECRET = "your_device_secret"
USERNAME = f"{DEVICE_ID}_0_0_20250101"


def on_connect(c, u, f, rc):
    print("connected rc=", rc)
    c.subscribe(f"$oc/devices/{DEVICE_ID}/sys/commands/#")


def on_message(c, u, msg):
    print("命令到达 topic:", msg.topic, "payload:", msg.payload.decode())
    rid = msg.topic.split("request_id=")[-1]
    c.publish(f"$oc/devices/{DEVICE_ID}/sys/commands/response/request_id={rid}",
              json.dumps({"response": {"result": "ok"}}))


def main():
    c = mqtt.Client(client_id=DEVICE_ID)
    c.username_pw_set(USERNAME, SECRET)
    c.tls_set()
    c.on_connect = on_connect
    c.on_message = on_message
    c.connect(SERVER, PORT, 60)
    c.loop_start()
    for i in range(5):
        payload = json.dumps({"services": [{"service_id": "sensor",
                                            "properties": {"temperature": 25 + i}}]})
        c.publish(f"$oc/devices/{DEVICE_ID}/sys/properties/report", payload)
        print("已上报:", payload)
        time.sleep(2)
    c.loop_stop()


if __name__ == "__main__":
    main()
