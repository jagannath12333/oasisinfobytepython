import socket
import threading
import tkinter as tk

# Client configuration
HOST = '127.0.0.1'
PORT = 5555

# Create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Function to send message
def send_message(event=None):
    message = message_entry.get()
    if message:
        client.send(message.encode())
        message_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Chat Application")

message_listbox = tk.Listbox(root, width=50, height=20)
message_listbox.pack()

message_entry = tk.Entry(root, width=50)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

message_entry.bind("<Return>", send_message)

# Function to receive message
def receive_message():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                message_listbox.insert(tk.END, message)
                message_listbox.yview(tk.END)
        except:
            break

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

root.mainloop()
