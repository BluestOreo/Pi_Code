from Peripherals import Peripherals
from myServer import Server

def main():
    # Initialize peripherals and server
    peripherals = Peripherals()
    server = Server(peripherals)
    
    try:
        server.start_tcp_server()
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server.close()

if __name__ == "__main__":
    main()
