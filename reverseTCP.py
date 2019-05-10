# coding:utf-8
import socket, sys

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))
s.listen(10)
conn, addr = s.accept()

print("[+] Connection from {}".format(str(addr[0])))

while True:
	command = raw_input("#> ")
	if command != "exit()":
		if command == "":continue
		conn.send(command)
		result = conn.recv(1024)
		if result == '':result = 16
		total_size = long(result[:16])
		result = result[16:]

		while total_size > len(result):
			data = conn.recv(1024)
			result += data

		print(result.rstrip("\n"))
	else:
		conn.send("exit()")
		print("[+] Connection Dropped!")
		break

s.close()
