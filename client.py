import socket
import threading
import sys
import select

from colorama import Fore, Style

from utils.visuals import clear_input_line

HOST = '0.0.0.0'
PORT = 9000

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def log(self, text: str, color: str = None):
        if color:
            print(color + text + Style.RESET_ALL)
        else:
            print(text)

    def recieve_messages(self):
        while self.connected:
            try:
                message = self.sock.recv(1024).decode()
                if not message:
                    self.connected = False
                    break

                if message.endswith(":"):
                    clear_input_line()
                    print(f"{message} ", end="", flush=True)
                else:
                    self.log(message)
            except:
                self.log("Disconnected from server", Fore.RED)
                self.connected = False
                break

    def send_messages(self):
        try:
            while self.connected:
                # Using select for non-blocking input
                rlist, _, _ = select.select([sys.stdin, self.sock], [], [], 0.1)

                if sys.stdin in rlist:
                    message = input()
                    clear_input_line()
                    self.sock.sendall(message.encode())

                if not self.connected:
                    break
        except KeyboardInterrupt:
            pass

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            self.connected = True
            self.log("Connected to chat server", Fore.MAGENTA)
        except Exception as e:
            self.log(f"Error connecting to the server: {str(e)}", Fore.RED)
            exit(1)

    def run(self):
        self.connect()
        threading.Thread(target=self.recieve_messages, daemon=True).start()
        self.send_messages()
        self.sock.close()

if __name__ == "__main__":
    client = ChatClient(host='0.0.0.0', port=9000)
    client.run()
