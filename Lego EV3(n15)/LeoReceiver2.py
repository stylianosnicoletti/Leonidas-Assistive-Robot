#!/usr/bin/env python3
# file: rfcomm-client.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $

from bluetooth import *
from time import *
import sys

fsock = open('out.txt', 'w')
sys.stdout = sys.stderr = fsock
print("standard output")

# search for the SampleServer service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = "F0:43:47:51:71:B1" )

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.listen(1)
sock.connect((host, port))
#print("connected.  type stuff")
#sock.send(bytes('Hello Andorid', 'UTF-8'))
sleep(100)
try:
    print("receiving")
    while True:
        data = sock.recv(3)
        print("received [%s]" % data.decode('utf-8'))
        if len(data) != 0:
            print("received [%s]" % data.decode('utf-8'))
            sock.close()
            exit()

except IOError:
    pass

sock.close()




# from bluetooth import *
# import os
#
# hostMACAddress = 'A0:E6:F8:DB:8C:21' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
# #port = 3
# backlog = 1
# size = 1024
# s = BluetoothSocket(RFCOMM)
# s.bind(("", PORT_ANY))
# s.listen(backlog)
# print("Listening")
#
# port = s.getsockname()[1]
#
# uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
#
# """
# advertise_service( s, "SampleServer",
#                    service_id = uuid,
#                    service_classes = [ uuid, SERIAL_PORT_CLASS ],
#                    profiles = [ SERIAL_PORT_PROFILE ]
#                 )
#                 """
#
# try:
#     client, clientInfo = s.accept()
#     while 1:
#         data = client.recv(size)
#         if data:
#             print(data)
#             os.system(str(data))
#             client.send(data) # Echo back to client
# except:
#     print("Closing socket")
#     client.close()
#     s.close()
#
# '''
# def clientthread(conn):
# #    conn.send("welcome connect to server.Type something and hit enter!\n")
#
#     while True:
#         data = conn.recv(4096)
#         #客户端传过来的数据为空
#         if not data:
#             conn.sendall("command is empty,do nothing!")
#             continue
#         #防止端口被利用来进行破坏活动
#         patt = r'\b%s\b'% str(data).strip()
#         match_result = re.findall(patt,white_list)
# #        if str(data).strip() in "pwd*ls -l*cd /home/xiaoyong/p2p/*sh deploy.sh*sh restart_p2p_service.sh":
#         if match_result:
#             #conn.sendall(replay)
#             print (conn.getpeername()[0] + " : " + str(data))
#             #用subprocess.Popen()方法另起子线程执行shell程序,并将标准输出保存到stdout,标准错误输出到stderr
#             handler = subprocess.Popen([str(data).strip()], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
#
#             output = handler.stdout.readlines()
#             errinfo = handler.stderr.readlines()
#
#             if output is None:
#                 conn.sendall("command execute successfully and has no result return.")
#             else:
#                 for one_line in output:
#                     print (one_line)
#                     conn.sendall(one_line)
#             if errinfo is None:
#                 conn.sendall("command execute successfully and no error occurred.")
#             else:
#                 for one_line in errinfo:
#                     print (one_line)
#                     conn.sendall(one_line)
#
#             print ("command " + data + " is completed.")
#
#         else:
#             conn.sendall("command is not allowed to execute!")
#             uselessWord = " " * (4096 - 5)
#             conn.send(uselessWord + "Done")
#             continue
#
#         time.sleep(2)
#         uselessWord = " "*(4096-5)
#         conn.send(uselessWord+"Done")
#
#     conn.close()
#
#
# #wait to accept a connection
# while 1:
#     try:
#         conn, addr = s.accept()
#         conn.sendall("***************Support command are:***********\n* 1.ls -l;ll                                 *\n* 2.pwd;ps aux|grep kw-live                  *\n* 3.cd ~/p2p/;cd /home/xiaoyong/p2p/         *\n* 4.sh deploy.sh;sh restart_p2p_service.sh   *\n* 5.cat deploy.sh;cat restart_p2p_service.sh *\n**********************************************\n")
#     except Exception,e:
#         traceback.print_exc()
#         continue
#     print ('Connected with ' + addr[0] + ':' + str(addr[1]))
#
#     #receive data from client and replay to client
#
#     try:
#         start_new_thread(clientthread,(conn,))
#     except Exception,e:
#         traceback.print_exc()
#         continue
#
# s.close()
# '''
