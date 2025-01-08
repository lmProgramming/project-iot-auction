import paho.mqtt.client as mqtt

BROKER = "localhost"  # Use your PC's IP (e.g., 192.168.x.x) on Raspberry Pi
PORT = 1883
TOPIC_SUBSCRIBE = "auction/#"
TOPIC_PUBLISH = "auction/1"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_SUBSCRIBE)
    else:
        print(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    print(f"Received message: Topic: {
          msg.topic}, Payload: {msg.payload.decode()}")


def on_publish(client, userdata, mid):
    print(f"Message published: {mid}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

try:
    client.connect(BROKER, PORT, 60)
    print("Connecting to broker...")
    client.loop_start()

    client.publish(TOPIC_PUBLISH, "Test bid from connector")

    input("Press Enter to disconnect...\n")
    client.loop_stop()
    client.disconnect()
    print("Disconnected from broker.")
except Exception as e:
    print(f"Error: {e}")
