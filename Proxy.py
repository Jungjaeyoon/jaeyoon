from socket import *
import sys
#simple proxy server 

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('',8888))
tcpSerSock.listen(100)

while 1:
    print('Ready to service')
    tcpCliSock, addr = tcpSerSock.accept()
    #print('Received a connection from: ' , addr)
    message = tcpCliSock.recv(1024)
    print(message)
    filename = message.split()[1].decode().partition('/')[2]
    print(filename)
    fileExist = 'false'
    filetouse = '/' + filename
    print(filetouse)
    try:
        #proxy 서버에 저장된 파일이 있나 확인   
        f = open(filetouse[1:], 'rb')
        print('EXIST PAGE')
        outputdata = f.readlines()
        fileExist = 'true'
        tcpCliSock.send('HTTP/1.0 200 OK\r\n'.encode())
        tcpCliSock.send('Content-Type:text/html\r\n'.encode())
        for i in range(0, len(outputdata)):
              tcpCliSock.send(outputdata[i])
              print('Read from cache')
    except IOError:
        #새로 들어간 페이지일 경우 proxy 서버에 get으로 얻어온 정보를 저장 
        print('NEW PAGE')
        if fileExist == "false":
            #AF_INET - 이름 종류 / 도메인 이름 or ipv4를 적용(host, port)
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace('www.', '', 1)
            print('hostname')
            print(hostn)
            try:
                  c.connect((hostn, 80))
                  #버퍼가 0일 경우 오류가 발생
                  fileobj = c.makefile('rw', 8, encoding = 'utf-8')
                  #makefile은 소켓에 관련된 file object를 return, 
                  fileobj.write("GET "+ "https://" + filename + " HTTP/1.0\n\n")
                  buff = fileobj.readlines()
                  print(buff)
                  tmpFile = open("./" + filename, "wb")
                  for line in buff:
                        tcpCliSock.send(line.encode())
                        tmpFile.write(line.encode())  
                        print(line)
                  tmpFile.close()
                  print('save proxy')
            except Exception as e:
                  print(type(e))
                  print(e)
                  print("Illegal request")
                  
        else:
            print('errorerrorerror')
            tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n")
            tcpCliSock.send("Content-Type:text/html\r\n")
            tcpCliSock.send("\r\n")
        tcpCliSock.close()
tcpSerSock.close()
