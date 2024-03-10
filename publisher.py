# Import package
import paho.mqtt.client as mqtt
import subprocess
from ultralytics import YOLO
import numpy as np
import cv2
import torch
import threading

def publish(): 

	# Define Variables
	MQTT_HOST = "test.mosquitto.org"
	MQTT_PORT = 1883
	MQTT_TOPIC = "east/west"
	MQTT_KEEPALIVE_INTERVAL = 5


	def process_frame():
		
		class_id = []
		names_arr = []
		count = 0
		
		model = YOLO('yolov8n.pt')
		
		cap = cv2.VideoCapture(0)

		success, frame = cap.read()
			
		if success:
			
			results = model(frame)
			
			classes = results[0].boxes.cls.tolist()
			
			for i in classes:
				class_id.append(int(i))
				
				if i == 63:
					count += 1
				
			return count	
			
			cap.release()
			cv2.destroyAllWindows()
			

	# Define on_connect event Handler
	def on_connect(mosq, obj, rc):
		print ("Connected to MQTT Broker")

	# Define on_publish event Handler
	def on_publish(client, userdata, mid):
		print ("Message Published...")
		
	def execute_script():
		result = subprocess.run(["python", "helloworld.py"], capture_output=True, text=True)
		return result.stdout

	# Initiate MQTT Client
	mqttc = mqtt.Client()

	# Register Event Handlers
	mqttc.on_publish = on_publish
	mqttc.on_connect = on_connect

	# Connect with MQTT Broker
	mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL) 

	# Publish message to MQTT Topic 
	results = process_frame()
	mqttc.publish(MQTT_TOPIC,results)

	# Disconnect from MQTT_Broker
	mqttc.disconnect()
	
	threading.Timer(10, publish).start()

publish()
