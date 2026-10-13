# -*- coding: utf-8 -*-
"""
华为云 IoTDA 设备侧「属性上报 / 命令响应」JSON 构造器（纯 Python，无第三方依赖）

== 原理（面试能讲清楚）==
华为云设备接入 IoTDA 基于 MQTT，topic 与阿里云不同：
  - 设备上报属性： $oc/devices/{device_id}/sys/properties/report
  - 平台下发命令： $oc/devices/{device_id}/sys/commands/request_id={id}
  - 设备响应命令： $oc/devices/{device_id}/sys/commands/response/request_id={id}
上报 payload 结构固定为 {"services":[{"service_id":"...","properties":{...}}]}
本模块只负责把业务数据正确序列化成 IoTDA 要求的 JSON，便于在 ESP32/STM32
侧用 cJSON 做同样的事；也可在本机用 paho-mqtt 直接联调（见 device_demo.py）。
"""
import json
import re


def build_property_report(service_id, properties):
    return json.dumps({"services": [{"service_id": service_id, "properties": properties}]},
                      ensure_ascii=False)


def build_command_response(request_id, result):
    return json.dumps({"response": result, "request_id": request_id}, ensure_ascii=False)


def parse_command(topic):
    m = re.search(r"request_id=([^/]+)", topic)
    return m.group(1) if m else ""


if __name__ == "__main__":
    msg = build_property_report("sensor", {"temperature": 26.5, "humidity": 60})
    print("上报 payload:", msg)
    rid = parse_command("$oc/devices/dev001/sys/commands/request_id=123")
    print("命令 request_id:", rid)
    print("命令响应:", build_command_response(rid, {"result": "ok"}))
