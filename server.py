from socket import *
import time
import random
import os
import binascii
import sys

host=''
port=8080

ADDR=(host,port)

s=socket(AF_INET, SOCK_STREAM)
s.bind(ADDR)
s.listen(3)
try:
	while 1:
		print 'Waiting for connection...'
		c,addr=s.accept()
		print 'Connected',addr
		smsg = c.recv(1024)
		if (smsg.find('oscp')!=-1):
			continue
		
		web = smsg[smsg.find('Host: ')+6:smsg.find('\r\nUser')]
		print web
		if (web.find('dummy')!=-1):
			continue
	
		newmsg = 'GET / HTTP/1.1\r\nHost: \r\n\r\n'+smsg.replace('Host: '+web,'Host: dummy.com')
		
		#print newmsg
		w = socket(AF_INET, SOCK_STREAM)
		w.connect((web,80))
		w.send(newmsg)
	
		while 1:
			rmsg = w.recv(8192)
			print rmsg
			if(rmsg.rfind('200 OK\r\n')!=-1):
				if(rmsg.count('HTTP/1.1')>1):
					rmsg = rmsg[rmsg.rfind('HTTP/1.1'):]
					c.send(rmsg)
					if(len(rmsg)<8192):
						print 'less...'
						break
					else:
						continue
				else:
					c.send(rmsg)
					if(len(rmsg)<8192):
	       	       	                        print 'less...'
       		       	                        break
					else:
						continue
		else:
			continue
finally:
   try:
       sys.stdout.flush()
   finally:
       try:
           sys.stdout.close()
       finally:  
           try:
               sys.stderr.flush()
           finally:
               sys.stderr.close()
