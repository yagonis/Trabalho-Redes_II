import socket

#Socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#server address
server_address = ('127.0.0.1', 8080)

#sent message to server
message = "Hello, UDP Server!"
client_socket.sendto(message.encode('utf-8'), server_address)

#receive response from server
data, server = client_socket.recvfrom(1024)
print(f"Response from server: {data.decode('utf-8')}")

client_socket.close()