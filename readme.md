# IoT MQTT Network Simulation

| **Category** | **Type**    | **JSON-Schema**                                                       | **Trigger**               |
|--------------|-------------|-----------------------------------------------------------------------|---------------------------|
| Sensor       | Temperature | _{ "temperature": 0, "humidity": 0, "battery": 0, "linkquality": 0 }_ |           _n.a._          |
| Sensor       | Motion      |    _{ "on": true, "alert": true, "battery": 0, "linkquality": 0 }_    |           _n.a._          |
| Sensor       | Window      |           _{ "open": true, "battery": 0, "linkquality": 0 }_          |           _n.a._          |
| Sensor       | Door        |           _{ "open": true, "battery": 0, "linkquality": 0 }_          |           _n.a._          |
| Sensor       | Smoke       |    _{ "on": true, "alert": true, "battery": 0, "linkquality": 0 }_    |           _n.a._          |
| Actuator     | LED bulb    |            _{ "on": true, "battery": 0, "linkquality": 0 }_           |   _{"on": true\|false}_   |
| Actuator     | Fire alarm  |          _{ "alert": true, "battery": 0, "linkquality": 0 }_          |  _{"alert": true\|false}_ |
| Actuator     | Shutter     | _{ "active": true, "percentage": 0, "battery": 0, "linkquality": 0 }_ | _{"active": true\|false}_ |
| Actuator     | Door opener |           _{ "open": true, "battery": 0, "linkquality": 0 }_          |  _{"open": true\|false}_  |
| Actuator     | Thermostat  |    _{ "active": true, "state": 0, "battery": 0, "linkquality": 0 }_   | _{"active": true\|false, "state": 0-100}_ |

## Run

```python
py run.py 
```