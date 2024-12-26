from config import *
import RPi.GPIO as GPIO
from time import sleep

'''Wykorzystując treść opisaną w lab09.pdf proszę o wykonanie zadania:

Napisz program, który pozwala regulować przy pomocy enkodera jasność świecenia diody LED 1/2/3/4
w module niebieskich diod świecących. Do obsługi enkodera wykorzystaj zdarzenia (events). W
danym czasie świeci się tylko jedna dioda LED. Wybór diody z modułu odbywa się poprzez przyciski.
Enkoder zmienia jedynie intensywność świecenia. Proszę na konsoli wyświetlać aktualną wartość intensywności.
'''

intensity: int = 50
leds: list = [led1, led2, led3, led4]
diodes: list[GPIO.PWM] = []
encoder_change: int = 5
current_led: int = 0

encoder_left_prev = GPIO.input(encoderLeft)
encoder_right_prev = GPIO.input(encoderRight)

def encoder_callback(channel) -> None:
    global intensity
    global encoder_left_prev
    global encoder_right_prev

    encoder_left_cur = GPIO.input(encoderLeft)
    encoder_right_cur = GPIO.input(encoderRight)

    if (encoder_left_prev == 1 and encoder_left_cur == 0):
        intensity = max(0, min(100, intensity + encoder_change))
    if (encoder_right_prev == 1 and encoder_right_cur == 0):
        intensity = max(0, min(100, intensity - encoder_change))

    diodes[current_led].ChangeDutyCycle(intensity)
    print(f"Current intensity: {intensity}")

    encoder_left_prev = encoder_left_cur
    encoder_right_prev = encoder_right_cur


def change_led(channel, change: int) -> None:
    global current_led

    diodes[current_led].stop()

    print(f"Changed from led {current_led}")
    current_led = (current_led + change) % 4

    diodes[current_led].start(intensity)
    
    print(f"Changed to led {current_led}")


def setup() -> None:
    for led in leds:
        print(f"setting led {led}")
        diode = GPIO.PWM(led, 50)
        diode.start(0)
        diodes.append(diode)
        diode.ChangeDutyCycle(0)

    GPIO.add_event_detect(encoderLeft, GPIO.FALLING,
                          callback=encoder_callback, bouncetime=55)
    GPIO.add_event_detect(encoderRight, GPIO.FALLING,
                          callback=encoder_callback, bouncetime=55)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING,
                          callback=lambda channel: change_led(channel, 1), bouncetime=200)
    GPIO.add_event_detect(buttonRed, GPIO.FALLING,
                          callback=lambda channel: change_led(channel, -1), bouncetime=200)
    
    diodes[0].ChangeDutyCycle(intensity)

    print(f"Current intensity: {intensity}")


def loop() -> None:
    sleep(0.5)


def main() -> None:
    setup()

    try:
        while True:
            loop()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
