import RPi.GPIO as GPIO # import the GPIO library	
from time import sleep # import the time for apply delay
import paho.mqtt.client as mqtt # import the mqtt.client 

import sys
GPIO.setmode(GPIO.BOARD) # set the standard mode 
GPIO.setup(40,GPIO.OUT) # set the port 40 as output to LED
GPIO.setup(36,GPIO.OUT) # RPi PIN36 is connected to IN1 of motor drive IC and set as OUTPUT
GPIO.setup(38,GPIO.OUT) # RPi PIN38 is connected to IN2 of motor drive IC and set as OUTPUT
GPIO.setup(32,GPIO.OUT) # PIN32 of RPi is connected Enable1,2 pin of the IC and set as OUTPUT
GPIO.setup(37,GPIO.OUT) # Buzzer is connected to PIN37


pi_pwm = GPIO.PWM(32,255) # Set up the PWM for PIN32 to enable PWM for Motor to reduce the speed
pi_pwm.start(50)  # Set the start frequency of the PWM as 50
GPIO.output(36,GPIO.LOW)	
GPIO.output(38,GPIO.LOW)	# set both input pins of IC as low so The motor does not move



try:
	
	def motor():	# motor starts  working
		GPIO.output(36,GPIO.HIGH)  # enable input 1 and set input 2 as low so the motor will spin anti clockwise
		GPIO.output(38,GPIO.LOW)
		sleep(0.9)
		GPIO.output(36,GPIO.LOW)		# stop the motor
		GPIO.output(38,GPIO.LOW)
	
	
	def buzzeron():	# set off buzzer
		GPIO.output(37,GPIO.HIGH)	# buzzer is set off
		
	def buzzeroff():
		GPIO.output(37,GPIO.LOW)
		
		
	
	def led():	#LED starts flashing
		GPIO.output(40,GPIO.HIGH)    # LED starts flashing
		sleep(1)
		GPIO.output(40,GPIO.LOW)
		sleep(1)
		GPIO.output(40,GPIO.HIGH)
		sleep(1)
		GPIO.output(40,GPIO.LOW)
		sleep(1)
		GPIO.output(40,GPIO.HIGH)
		sleep(1)
		GPIO.output(40,GPIO.LOW)	
		sleep(1)
		GPIO.output(40,GPIO.HIGH)
		sleep(1)
		GPIO.output(40,GPIO.LOW)
		sleep(1)
		GPIO.output(40,GPIO.HIGH)
		sleep(1)
		GPIO.output(40,GPIO.LOW)
		sleep(1)
		GPIO.output(40,GPIO.HIGH)
		sleep(1)
		GPIO.output(40,GPIO.LOW)	
		sleep(1)
	
	
		
	def on_connect(client, userdata, flags, rc):  # Check if connection is good or failed
		if rc == 0:
			print("Connected success")
		else:
			print(f"Connected fail with code {rc}")
			
		client.subscribe("Flooding")  # subscribe to Topic Flooding on connection to recieve message from Argon
		
				
				
		
		
		
	def on_message(client, userdata, msg):   # if message recieved from Argon below code is executed
		print(f"{msg.topic} {msg.payload}")  # print message on terminal
		
		pi_pwm.ChangeDutyCycle(20)  # set the PWM duty cycle low because we want to imitate a low speed motor
		
		# call each function in order
		motor()  
		buzzeron()
		led()
		buzzeroff()

		

		
		
		
		
		

	client = mqtt.Client() 	# create a mqtt client
	client.on_connect = on_connect 	# check connection
	client.on_message = on_message	# call the on_message function
	client.will_set('raspberry/status', b'{"status": "Off"}')	# Will message is sent when the RPi is disconnected to inform the owner of conenction failure 
	client.connect("broker.emqx.io", 1883, 60) # set up the connection to mqtt
	client.loop_forever()	# loop over the client to check if message recieved
	
except KeyboardInterrupt: 
	print ("Keyboard Interrupt")
	
except: 
	print ("Other error or exception occurred!")
finally: 
	GPIO.cleanup()
