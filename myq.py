import requests
import os
import json
import time

class MyQ:

    APP_ID = "Vj8pQggXLhLy0WHahglCD4N1nAkkXQtGYpq2HrHD7H1nvmbT55KqtN6RSF4ILB/i"
    LOCALE = "en"
    HOST_URI = "myqexternal.myqdevice.com"
    LOGIN_ENDPOINT = "api/v4/User/Validate"
    DEVICE_LIST_ENDPOINT = "api/v4/UserDeviceDetails/Get"
    DEVICE_SET_ENDPOINT = "api/v4/DeviceAttribute/PutDeviceAttribute"

    username = "<MYQ_LOGIN_USERNAME>"
    password = "<MYQ_LOGIN_PASSWORD>"

    myq_userid                  = ""
    myq_security_token          = ""
    myq_cached_login_response   = ""
    myq_device_id               = False
    myq_lamp_device_id          = False

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def open(self):
        self.change_door_state("open")
    
    def close(self):
        self.change_door_state("close")
        
    def lamp_on(self):
        self.change_lamp_state("on")
    
    def lamp_off(self):
        self.change_lamp_state("off")
    
    def status(self):
        state = self.check_door_state()
    
        if state == "1":
            return "open"
        elif state == "2":
            return "closed"
        elif state == "3":
            return "stopped"
        elif state == "4":
            return "opening"
        elif state == "5":
            return "closing"
        elif state == "8":
            return "moving"
        elif state == "9":
            return "open"
        else:
            return str(state) + ", an unknown state for the door."
    
    def lamp_status(self):
        state = self.check_lamp_state()
        if state == "0":
            return "off"
        elif state == "1":
            return "on"
        else:
            return "unknown"
    
    
    def login(self):
        params = {
            'username': self.username,
            'password': self.password
        }
        login = requests.post(
                'https://{host_uri}/{login_endpoint}'.format(
                    host_uri=self.HOST_URI,
                    login_endpoint=self.LOGIN_ENDPOINT),
                    json=params,
                    headers={
                        'MyQApplicationId': self.APP_ID
                    }
            )
    
        auth = login.json()
        self.myq_security_token = auth['SecurityToken']
        return True
    
    def change_device_state(self, payload):
        device_action = requests.put(
            'https://{host_uri}/{device_set_endpoint}'.format(
                host_uri=self.HOST_URI,
                device_set_endpoint=self.DEVICE_SET_ENDPOINT),
                data=payload,
                headers={
                    'MyQApplicationId': self.APP_ID,
                    'SecurityToken': self.myq_security_token
                }
        )
        return device_action.status_code == 200
    
    def change_lamp_state(self, command):
        newstate = 1 if command.lower() == "on" else 0
        payload = {
            "attributeName": "desiredlightstate",
            "myQDeviceId": self.myq_lamp_device_id,
            "AttributeValue": newstate
        }
        return self.change_device_state(payload)
    
    def change_door_state(self, command):
        open_close_state = 1 if command.lower() == "open" else 0
    
        payload = {
            'attributeName': 'desireddoorstate',
            'myQDeviceId': self.myq_device_id,
            'AttributeValue': open_close_state,
        }
        return self.change_device_state(payload)
    
    def get_devices(self):
        devices = requests.get(
            'https://{host_uri}/{device_list_endpoint}'.format(
                host_uri=self.HOST_URI,
                device_list_endpoint=self.DEVICE_LIST_ENDPOINT),
                headers={
                    'MyQApplicationId': self.APP_ID,
                    'SecurityToken': self.myq_security_token
                }
        )
        return devices.json()['Devices']
    
    def get_device_id(self):
        devices = self.get_devices()
        for dev in devices:
            print("Device => " + dev["MyQDeviceTypeName"])
            if (not self.myq_device_id) and dev["MyQDeviceTypeName"] in ["VGDO", "GarageDoorOpener", "Garage Door Opener WGDO"]:
                self.myq_device_id = str(dev["MyQDeviceId"])
            elif (not self.myq_lamp_device_id) and dev["MyQDeviceTypeName"] == "LampModule":
                self.myq_lamp_device_id = str(dev["MyQDeviceId"])
                
    def check_door_state(self):
        return self.check_device_state(self.myq_device_id, "doorstate")
    
    def check_lamp_state(self):
        return self.check_device_state(self.myq_lamp_device_id, "lightstate")
        
    def check_device_state(self, device_id, state_name):
        devices = self.get_devices()
        for dev in devices:
            if str(dev["MyQDeviceId"]) == str(device_id):
                for attribute in dev["Attributes"]:
                    if attribute["AttributeDisplayName"] == state_name:
                        door_state = attribute['Value']
        
        return door_state
