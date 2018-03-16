# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 17:39:12 2017

@author: arago
"""

from socket import *
import base64
#메시지 입력

msg = '\r\nI love computer networks!'
endmsg = '\r\n.\r\n'

# Auth information (Encode with base64)
username = base64.b64encode("ID@seoultech.ac.kr".encode())
password = base64.b64encode("password!\r\n".encode())
#계정과 비밀번호를 base64 형식으로 변환하여 준비

      


#메일 서버 선택
mailserver = 'mail.seoultech.ac.kr'
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not recevied from server.')

#The client sends this command to the SMTP server to identify itself and initiate the SMTP conversation
#SMTP서버를 인식하고 연결을 수립하기위한 명령어 EHLO 또한 같은 목적이지만 Extended SMTP 프로토콜을 사용할 경우
#사용된다. ESMTP를 사용하지 않는다면(필요없거나 지원하지 않는 경우) 자동으로 적절한 방식으로(HELO) 연결해
heloCommand = 'HELO mail.seoultech.ac.kr\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('220 reply not received from server.')

#AUTH LOGIN 요청 - ID 포함하여 보내고 인증 시작
LoginCommand = 'AUTH LOGIN ID\r\n'
clientSocket.send(LoginCommand.encode())
clientSocket.recv(1024).decode()

#pw에 저장한 비밀번호를 보내줌
pw = 'PASSWORD\r\n'
clientSocket.send(pw.encode())
clientSocket.recv(1024).decode()


#메일 작성 시작
mailfrom = 'MAIL FROM: <aragon5198@seoultech.ac.kr>\r\n'
clientSocket.send(mailfrom.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')
#받는 사람
rcptto = 'RCPT TO:<aragon5198@seoultech.ac.kr>\r\n'
clientSocket.send(rcptto.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')
#메일 데이터 입력 - 작동 후 데이터 입력 받음
data = 'DATA\r\n'
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')
#데이터 본문 보내기

clientSocket.send('FROM:aragon5198@seoultech.ac.kr\r\n'.encode())
clientSocket.send('Subject: Greeting To you!\r\n\r\n'.encode())
clientSocket.send('test again'.encode())
clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

quitcommand = 'QUIT\r\n'
clientSocket.send(quitcommand.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '221':
    print('221 reply not received from server')
    
    
    
    
    
