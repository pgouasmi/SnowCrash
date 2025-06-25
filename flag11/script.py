#!/usr/bin/env python3
import socket

HOST = "192.168.1.183"
PORT = 5151

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

prompt = sock.recv(1024).decode()
print(f"Serveur: {prompt}", end="")

password = input()
sock.send(password.encode())

response = sock.recv(1024).decode()
print(f"Serveur: {response}")

sock.close()