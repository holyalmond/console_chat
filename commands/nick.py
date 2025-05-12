from commands.base import command

import re

def validate_nickname(nickname, current_nickname, used_nicknames):
    if nickname.startswith('/'):
        return False, "Nickname cannot start with '/' as it's reserved for commands. Enter your nickname:"

    if not re.match(r'^.{3,15}$', nickname):
        return False, "Nickname must be between 3 and 15 characters. Enter your nickname:"

    if nickname in used_nicknames and nickname != current_nickname:
        return False, "Nickname is already taken. Enter your nickname:"

    return True, ""


@command(name="nick", description="Set your nickname")
def nick(server, client, *args):   
    current_nickname = client.nickname
     
    if args:
        client.nickname = args[0]
    else:
        client.conn.send("Enter your nickname:".encode())
        client.nickname = client.conn.recv(1024).decode().strip()

    while True:
        is_valid, message = validate_nickname(client.nickname, current_nickname, server.used_nicknames)
        if is_valid:
            break
        else:
            client.conn.send(message.encode())
            client.nickname = client.conn.recv(1024).decode().strip()

    server.used_nicknames.add(client.nickname)
    server.clients[client.conn] = {"nickname": client.nickname, "color": client.color}