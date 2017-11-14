from socket import *
import time
import random
import os
import binascii

host=''
port=8080

ADDR=(host,port)

s=socket(AF_INET, SOCK_STREAM)
s.bind(ADDR)
s.listen(3)

while 1:
	print 'Waiting for connection...'
	c,addr=s.accept()
	print 'Connected',addr
	smsg = c.recv(1024)
	
	web = smsg[smsg.find('Host: ')+6:smsg.find('\r\nUser')]
	print web
	
	w = socket(AF_INET, SOCK_STREAM)
	w.connect((web,80))
	newmsg = 'GET / HTTP/1.1\r\nHost: \r\n\r\n'+smsg.replace('Host: '+web,'Host: dummy.com')
	#print newmsg
	w.send(newmsg)
	
	rmsg = w.recv(1024)
	print rmsg
	if(rmsg.rfind('HTTP/1.1 200 OK\r\n')!=-1):
		if(rmsg.count('HTTP')>1):
			rmsg = rmsg[rmsg.rfind('HTTP/1.1'):]
			leng = rmsg[rmsg.find('Content-Length: ')+16:]
			leng = leng[:leng.find('\r\n')]
			print leng
			c.send(rmsg)
			if(int(leng)>1024):
				for i in range(int(leng)/1024):
					rmsg = w.recv(1024)
					c.send(rmsg)
