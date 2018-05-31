import SimpleHTTPServer
import SocketServer
import json
import RPi.GPIO as GPIO
from random import randint
from time import sleep


PORT = 8001

class SAMHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", 'application/json')
        self.end_headers()

        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        data = json.loads(self.data_string)
        if data["type"] == "light":
            self.toggle_light(data["light"], data["status"])
        elif data["type"] == "servo":
            self.feedMe()

    def toggle_light(self, light_type, light_status):
        print(("Turning {}  {} light".format(light_status, light_type)))
        if light_type == "day":
            if light_status == "on":
                self.toggleOn(31)
            elif light_status == "off":
                self.toggleOff(31)
        elif light_type == "night":
            if light_status == "on":
                self.toggleOn(29)
            elif light_status == "off":
                self.toggleOff(29)
 
    def toggleOn(self, gpio_pin_number):
        GPIO.setup(gpio_pin_number, GPIO.OUT)

        print ("Turn Relay ON")
        GPIO.output(gpio_pin_number, GPIO.LOW)

    def toggleOff(self, gpio_pin_number):
        GPIO.setup(gpio_pin_number, GPIO.OUT)

        print ("Turn Relay OFF")
        GPIO.output(gpio_pin_number, GPIO.HIGH)
    
    def feedMe(self):
        self.servo(0, 3)
        self.servo(0, 11)
        self.servo(0, 13)
        self.servo(0, 15)
        self.servo(180, 3)
        self.servo(180, 11)
        self.servo(180, 13)
        self.servo(180, 15)

    def servo(self, angle, number):
        pause = 1
        GPIO.setup(number, GPIO.OUT)
        pwm=GPIO.PWM(number, 50)
        pwm.start(0)
        duty = angle / 18 + 2
        GPIO.output(number, True)
        pwm.ChangeDutyCycle(duty)
        sleep(0.5)
        GPIO.output(number, False)
        pwm.ChangeDutyCycle(0)
    

# Run this all everytime.
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT)
pwm=GPIO.PWM(03, 50)
pwm.start(0)

Handler = SAMHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print("serving at port {}".format(PORT))
httpd.serve_forever()

GPIO.cleanup()
