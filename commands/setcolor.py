from commands.base import command
from utils.visuals import color_map

@command(name="setcolor", description="Set nickname color")
def set_color(server, client, *args):
    client.conn.send(f"Choose your color ({', '.join(color_map)}):".encode())
    color = client.conn.recv(1024).decode().strip().lower()
    while color not in color_map:
        client.conn.send(f"Invalid or taken color. Choose from: {', '.join(color_map)}:".encode())
        color = client.conn.recv(1024).decode().strip().lower()
    client.color = color
    server.clients[client.conn]["color"] = client.color
    return
