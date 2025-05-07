from commands.base import command

@command(name="msg", description="Send private message with: /msg nickname message")
def online(server, client, *args):
    if args:
        parts = args[0].split(" ", 1)
        nickname, message = parts
    for user_sock, user_info in server.clients.items():
        if user_info.get("nickname") == nickname:
            receiver_sock = user_sock
    client.broadcast(message, client.conn, receiver_sock)