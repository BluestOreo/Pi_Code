import socket
from threading import Thread
from Peripherals import *

class Server:
    def __init__(self, peripherals, command_port=5000, video_port=8000):
        self.peripherals = peripherals
        self.command_port = command_port
        self.video_port = video_port
        self.command_socket = None
        self.video_socket = None

    def start_tcp_server(self):
        # Start command and video sockets
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket.bind(("", self.command_port))
        self.command_socket.listen(1)
        
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_socket.bind(("", self.video_port))
        self.video_socket.listen(1)

        print(f"TCP servers running on ports {self.command_port} and {self.video_port}")
        Thread(target=self.handle_commands).start()
        Thread(target=self.stream_video).start()

    def handle_commands(self):
        conn, addr = self.command_socket.accept()
        print(f"Command connection from {addr}")
        while True:
            data = conn.recv(1024).decode()
            if data:
                self.process_command(data)

    def stream_video(self):
        conn, addr = self.video_socket.accept()
        print(f"Video connection from {addr}")
        # Placeholder for video streaming code

   
    def process_command(self, command):
        """
        Processes incoming commands to control the wheelchair's movement.

        Commands:
        - "FORWARD": Moves the wheelchair forward.
        - "LEFT": Turns the wheelchair to the left.
        - "RIGHT": Turns the wheelchair to the right.
        - "STOP": Stops all motors.
        """
        max_speed = 50  # Set maximum speed to 50%

        if command == "FORWARD":
            # Set all motors to forward at 50% speed
            self.peripherals.set_motor_pwm("TL", max_speed, True)
            self.peripherals.set_motor_pwm("TR", max_speed, True)
            self.peripherals.set_motor_pwm("BL", max_speed, True)
            self.peripherals.set_motor_pwm("BR", max_speed, True)
            print("Moving Forward")

        elif command == "LEFT":
            # Set left motors to reverse and right motors to forward for a left turn
            self.peripherals.set_motor_pwm("TL", int(max_speed/3), False)  # Reverse top left
            self.peripherals.set_motor_pwm("BL", int(max_speed/3, False))  # Reverse bottom left
            self.peripherals.set_motor_pwm("TR", int(max_speed/3, True))   # Forward top right
            self.peripherals.set_motor_pwm("BR", int(max_speed/3, True))   # Forward bottom right
            print("Turning Left")

        elif command == "RIGHT":
            # Set right motors to reverse and left motors to forward for a right turn
            self.peripherals.set_motor_pwm("TL", int(max_speed/3, True))   # Forward top left
            self.peripherals.set_motor_pwm("BL", int(max_speed/3, True) )  # Forward bottom left
            self.peripherals.set_motor_pwm("TR", int(max_speed/3, False) ) # Reverse top right
            self.peripherals.set_motor_pwm("BR", int(max_speed/3, False) ) # Reverse bottom right
            print("Turning Right")

        elif command == "STOP":
            # Stop all motors
            self.peripherals.set_motor_pwm("TL", 0, True)  # Stop top left
            self.peripherals.set_motor_pwm("TR", 0, True)  # Stop top right
            self.peripherals.set_motor_pwm("BL", 0, True)  # Stop bottom left
            self.peripherals.set_motor_pwm("BR", 0, True)  # Stop bottom right
            print("Stopping")

        else:
            print(f"Unknown command: {command}")


    def close(self):
        self.command_socket.close()
        self.video_socket.close()
        self.peripherals.cleanup()



if __name__ == "__main__":
    pass