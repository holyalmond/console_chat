import socket
import threading
import sys

HOST = 'localhost'
PORT = 57890

def clear_input_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    sys.stdout.flush()

def recieve_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(f"{message}")
        except:
            print("Disconnected from server.")
            break

def send_messages(sock):
    while True:
        try:
            message = input()

            if message.strip().lower() == "/quit":
                print("Disconnecting from server...")
                sock.close()
                break

            clear_input_line()
            sock.sendall(message.encode())
            
        except:
            break

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print("Connected to chat server. Type /quit to exit")
    thread = threading.Thread(target=recieve_messages, args=(sock, ), daemon=True)
    thread.start()

    send_messages(sock)

if __name__ == "__main__":
    start_client()
            