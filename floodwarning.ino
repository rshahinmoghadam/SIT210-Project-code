// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

int moisture = A1; // sensor is connected to A1
int moisture2 = A2;  // sensor2 is connected to A2

void callback(char* topic, byte* payload, unsigned int length); // Callback function when message recieved 
MQTT client("broker.emqx.io", 1883, callback); // set up a MQTT client. I have used EMQX MQTT broker for this project



void callback(char* topic, byte* payload, unsigned int length) {    //called when recieving messages from buddy depending on the topic the corresponding function is called
    
    
    if(strcmp(topic,"FloodingIncoming")==0){   //check the message incoming and execute the code
        char p[length + 1];
        memcpy(p, payload, length);
        p[length] = NULL;
        Particle.publish("Topic:FloodingIncoming",(char *)p,PRIVATE);  //publish to console 
    }
    
    if(strcmp(topic,"raspberry/status")==0){ // if this message recieved it means the RPi is disconnected
        char p[length + 1];
        memcpy(p, payload, length);
        p[length] = NULL;
        Particle.publish("Topic:raspberry/status",(char *)p,PRIVATE);   // publish on console
        Particle.publish("Moisture", "RPi is disconnected", PRIVATE);   //Also send IFTTT email to inform user
    }
    


}



void setup() {

pinMode(moisture, INPUT);   // set moisture pin as input
pinMode(moisture2, INPUT);  // set moisture2 pin as input

client.connect("sparkclient");// start the connection to broker


Particle.function("Reset", ResetArgon); // this function is used to reset the argon remotely from the particle console

if (client.isConnected()) {  //check the connection
    
    Particle.publish("Topic:Flooding","Client is connected",PRIVATE);    // publish to console
    client.subscribe("raspberry/status"); // subscribe to this topic which is published from RPi 'Will message'
    

}

}




void loop() {
    
if (client.isConnected())       
client.loop();
    
if (!client.isConnected()){  // if connection is failed inform the user
    Particle.publish("Topic:Flooding", "MQTT is not connected", PRIVATE);
}
    

    
int x = analogRead(moisture);  // Check the moisture sensor input
int y = analogRead(moisture2); // check the moisture on sensor 2

Particle.publish("Sensor1", String(x), PRIVATE); // post the moisture value of sensor 1 on console
Particle.publish("Sensor2", String(y), PRIVATE); // post the moisture value of sensor 2 on console



if(x > 700 & y > 700){  // if the value of both sensors go above 700
    
        delay(3000);    // wait 3 seconds 
        x = analogRead(moisture);  // read again to make sure there was no error
        y = analogRead(moisture2); // read sensor2 again to make sure there was no error
        if(x>700 & y>700){  // is still over 700
            Particle.publish("Moisture", "Flooding detected in the kitchen", PRIVATE);//triggers the webhook to post on IFTTT with topic moisture
            delay(400);
            client.publish("Flooding","Ramin - Flooding detected");   // publish Flooding topic to MQTT
            while(x>700 & y>700){  // we keep the execution in this loop so we wont keep recieving messages or trigger the motor 
                x = analogRead(moisture); // keep reading the values    
                y = analogRead(moisture2);
                delay(3000);
            }
        client.connect("sparkclient");
        }
        
        
        
    }
client.connect("sparkclient");
delay(3000);


}

int ResetArgon(String args){  // this function is used to reset argon remotely 
    System.reset();
    return 0;
}