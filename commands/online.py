from commands.base import command

@command(name="online", description="Show online users")
def online(server, client, *args):
    users = [user["nickname"] for user in server.clients.values()]
    full_message = "\n".join(users)    
    client.conn.send(full_message.encode())