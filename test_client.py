# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 17:44:54 2025

@author: aruni1
"""

import requests

BASE_ITEM = "http://127.0.0.1:8001"
BASE_LOG = "http://127.0.0.1:8002"

def checkout_item(person, item_id):
    r = requests.post(f"{BASE_ITEM}/items/{item_id}/checkout")
    if r.ok:
        item_name = r.json()['item']
        requests.post(f"{BASE_LOG}/logs", json={"person": person, "item": item_name, "action": "checkout"})
        print(f"{person} checked out {item_name}")
    else:
        print(r.json()['detail'])

def checkin_item(person, item_id):
    r = requests.post(f"{BASE_ITEM}/items/{item_id}/checkin")
    if r.ok:
        item_name = r.json()['item']
        requests.post(f"{BASE_LOG}/logs", json={"person": person, "item": item_name, "action": "checkin"})
        print(f"{person} checked in {item_name}")
    else:
        print(r.json()['detail'])

def show_logs(person):
    r = requests.get(f"{BASE_LOG}/logs/{person}")
    for log in r.json():
        print(log)

# Example Usage
checkout_item("Arun", 1)
checkin_item("Arun", 1)
show_logs("Arun")