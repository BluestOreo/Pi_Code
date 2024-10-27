import RPi.GPIO as GPIO
from adafruit_pca9685 import PCA9685
import smbus
import time
from board import SCL, SDA
import busio

class Peripherals:
    def __init__(self):
        # Initialize GPIO and I2C devices
        GPIO.setmode(GPIO.BCM)
        self.debug_mode=False
        try:
            # MPU-6050 setup
            self.mpu_address = 0x68
            self.bus = smbus.SMBus(1)
            self.init_mpu6050()
        except:
            print("could not initialize MPU-6050. Is the board connected?")
            #self.debug_mode=True

        # Map each motor side to its corresponding channels on PCA9685
        self.motor_channels = {
            "TL": (11, 12),  # Top Left: direction on 11, duty cycle on 12
            "BL": (13, 14),  # Bottom Left: direction on 13, duty cycle on 14
            "TR": (15, 16),  # Top Right: direction on 15, duty cycle on 16
            "BR": (17, 18)   # Bottom Right: direction on 17, duty cycle on 18
        }

        try:
            # PCA9685 setup for motors
            self.i2c_bus = busio.I2C(SCL, SDA)
            self.pca = PCA9685(self.i2c_bus) #default address already set to 0x40
            self.pca.frequency = 50
        except:
              print("could not initialize PCA9685. Is the board connected?")
              self.debug_mode=True

        # Buzzer setup
        self.buzzer_pin = 17
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

    def init_mpu6050(self):
        # Initialize MPU-6050
        if not self.debug_mode:
            self.bus.write_byte_data(self.mpu_address, 0x6B, 0)

    def set_motor_pwm(self, side, duty_cycle, direction):
        """
        Sets the PWM duty cycle and direction for a specified motor side.

        """
        
        if side not in self.motor_channels and not self.debug_mode:
            print(f"Invalid motor side: {side}")
            return
        

        # Get the direction and duty cycle channels for the specified motor side
        dir_channel, pwm_channel = self.motor_channels[side]
        
        # Set the direction (0 for reverse, 1 for forward)
        self.pca.channels[dir_channel].duty_cycle = 0xFFFF if direction else 0x0000
        
        # Set the speed using duty cycle
        pulse = int(duty_cycle * 4095 / 100)  # Convert duty cycle to PCA9685 pulse width
        self.pca.channels[pwm_channel].duty_cycle = pulse

    def activate_buzzer(self, duration):
        # Activate buzzer
        GPIO.output(self.buzzer_pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.buzzer_pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
        self.pca.deinit()


if __name__ == "__main__":
    pass