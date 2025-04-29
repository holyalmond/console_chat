import socket
import threading
from datetime import datetime
import logging

from colorama import init, Fore, Style

from utils.visuals import get_color
from commands.base import get_command

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

HOST = '0.0.0.0'
PORT = 9000

init(autoreset=True)

class ChatServer:
    def __init__(self, host, port):
        self.clients = {}
        self.used_nicknames = set()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen()

    def start(self):
        logger.info("Server started")
        while True:
            try:
                conn, addr = self.sock.accept()
                logger.info(f"New connection from {addr}")
                client_handler = ClientHandler(self, conn, addr)
                threading.Thread(target=client_handler.handle_client, daemon=True).start()
            except Exception as e:
                logger.exception("Error accepting new connection")

class ClientHandler:
    def __init__(self, server, conn, addr):
        self.server = server
        self.conn = conn
        self.addr = addr
        self.username = str(addr)

    def broadcast(self, message, sender_sock=None):
        for conn in list(self.server.clients.keys()):
            if conn != sender_sock:
                try:
                    conn.sendall(message.encode())
                except Exception:
                    logger.exception("Error broadcasting message")
                    conn.close()
                    if conn in self.server.clients:
                        del self.server.clients[conn]

    def handle_command(self, message: str):
        parts = message[1:].split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        handler = get_command(cmd)
        if handler:
            try:
                handler(self.server, self, *args)
            except Exception:
                logger.exception(f"Error executing command: /{cmd}")
        else:
            self.broadcast(Fore.YELLOW + f"Unknown command: /{cmd}" + Style.RESET_ALL)

    def handle_client(self):
        try:
            self.conn.send("Enter your nickname:".encode())
            self.nickname = self.conn.recv(1024).decode().strip()

            while self.nickname in self.server.used_nicknames:
                self.conn.send("Nickname is already taken. Choose another one:".encode())
                self.nickname = self.conn.recv(1024).decode().strip()

            self.server.used_nicknames.add(self.nickname)
            self.server.clients[self.conn] = {"nickname": self.nickname, "color": "blue"}

            self.broadcast(Fore.GREEN + f"{self.nickname} joined" + Style.RESET_ALL, self.conn)
            self.conn.send((Fore.LIGHTGREEN_EX + "Welcome! Type /help to see available commands" + Style.RESET_ALL).encode())

            while True:
                try:
                    message = self.conn.recv(1024).decode()
                    if not message:
                        break
                    if message.startswith("/"):
                        self.handle_command(message)
                    else:
                        timestamp = datetime.now().strftime("%H:%M")
                        nickname_color = get_color(self.server.clients[self.conn]["color"])
                        self.broadcast(
                            f"{Fore.LIGHTBLACK_EX}[{timestamp}]{Style.RESET_ALL} "
                            f"{nickname_color}{self.nickname}{Style.RESET_ALL}: {message}"
                        )
                except Exception:
                    logger.exception("Error receiving or handling client message")
                    break

        except Exception:
            logger.exception("Error during client setup or main loop")

        finally:
            try:
                if self.conn in self.server.clients:
                    nickname = self.server.clients[self.conn].get("nickname")
                    if nickname:
                        self.server.used_nicknames.discard(nickname)
                    del self.server.clients[self.conn]
                    self.broadcast(Fore.GREEN + f"{nickname} left the chat" + Style.RESET_ALL, self.conn)
            except Exception:
                logger.exception("Error cleaning up client on disconnect")

            try:
                self.conn.close()
            except Exception:
                logger.exception("Error closing connection")

if __name__ == "__main__":
    try:
        server = ChatServer(host=HOST, port=PORT)
        server.start()
    except KeyboardInterrupt:
        logger.info("Server stopped manually (KeyboardInterrupt)")
    except Exception:
        logger.exception("Unhandled exception in server")
