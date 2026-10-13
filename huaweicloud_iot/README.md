# 华为云 IoT 接入 · 原理与本地联调指南

## 一、端—云—端链路（面试讲法）
1. 终端（STM32）：采集数据 → UART 用 AT 指令驱动 ESP8266 联网
2. 网络（ESP8266）：作为 WiFi 透传模组，把 STM32 串口数据发到华为云 MQTT
3. 云平台（IoTDA）：设备接入服务，管理设备、转发属性、下发命令
4. 应用（微信小程序）：订阅设备 Topic 实时展示，并下发控制指令

## 二、MQTT Topic 约定（华为云 IoTDA）
- 属性上报：`$oc/devices/{device_id}/sys/properties/report`
- 命令下发：`$oc/devices/{device_id}/sys/commands/request_id={id}`
- 命令响应：`$oc/devices/{device_id}/sys/commands/response/request_id={id}`

## 三、本仓库新增的可运行代码
- `payload_builder.py`：纯 Python、零依赖，构造/解析 IoTDA 的 JSON 报文，可直接运行验证格式。
- `device_demo.py`：用 paho-mqtt 在 PC 上完整演示「连接→上报→收命令→回包」握手，无需硬件。

> 真实性说明：STM32/ESP8266 固件为课程实验的真实实现思路；本目录 Python 代码用于
> 在 PC 端复现并讲解 MQTT 接入原理，便于面试演示与联调测试。
