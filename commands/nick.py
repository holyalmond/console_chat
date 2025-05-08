from commands.base import command

@command(name="nick", description="Set your nickname")
def nick(server, client, *args):    
    if args:
        client.nickname = args[0]
    else:
        client.conn.send("Enter your nickname:".encode())
        client.nickname = client.conn.recv(1024).decode().strip()

        while client.nickname in server.used_nicknames:
            client.conn.send("Nickname is already taken. Choose another one:".encode())
            client.nickname = client.conn.recv(1024).decode().strip()

    server.used_nicknames.add(client.nickname)
    server.clients[client.conn] = {"nickname": client.nickname, "color": client.color}
