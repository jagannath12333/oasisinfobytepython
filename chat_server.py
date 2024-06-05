import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind the socket to the address and port
    server.bind((HOST, PORT))
    print(f"Server running on {HOST}:{PORT}")

    # Listen for incoming connections
    server.listen()

    # Function to handle client connections
    def handle_client(client_socket, addr):
        print(f"Accepted connection from {addr}")

        while True:
            try:
                # Receive message from client
                message = client_socket.recv(1024).decode()

                if not message:
                    break

                print(f"Received message: {message}")

                # Broadcast message to all clients
                for client in clients:
                    if client != client_socket:
                        client.send(message.encode())
            except Exception as e:
                print(f"Error handling client: {e}")
                break

        print(f"Connection from {addr} closed")
        clients.remove(client_socket)
        client_socket.close()

    # List to store connected clients
    clients = []

    # Accept incoming connections
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

except Exception as e:
    print(f"Error starting server: {e}")
finally:
    server.close()
