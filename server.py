import socket
import os
from _thread import *

ThreadCount = 0

def threaded_client(connection):
    #connection.send(str.encode('Welcome to the Servern'))
    req = sc.recv(50).decode('utf-8')
    if req == "GET":
        questions = os.listdir("./questions")
        response = ",".join(questions)
        print(response)
        sc.send(response.encode('utf-8'))
        sc.shutdown(socket.SHUT_WR)
    elif req.startswith("VIEW"):
        print(req)
        req = req.replace("VIEW","")
        print(req)
        que_text = open(f"./questions/{req}/{req}.txt","r").read()
        print(que_text)
        sc.send(que_text.encode('utf-8'))
        sc.shutdown(socket.SHUT_WR)
    else:
        id =req  
        print("ID = ",id)
        if not os.path.isdir(id):
            os.system(f"mkdir {id}")
        sc.send('id_received'.encode('utf-8'))
        #sc.shutdown(socket.SHUT_WR)
        Q_NO = sc.recv(50).decode('utf-8')
        print("QNO = ",Q_NO)
        sc.send('qno_received'.encode('utf-8'))
        lang = sc.recv(7).decode('utf-8')
        print("lang = ",lang)
        sc.send('lang_received'.encode('utf-8'))
        if lang=="Python3":
            k = f"{id}/"+Q_NO+".py"
        else:
            k = f"{id}/"+Q_NO+".cpp"
        print(k)
        f = open(str(k),'wb')
        l = sc.recv(1024)
        
        while l:
            f.write(l)
            l = sc.recv(10)

        f.close()
        sc.send('received'.encode('utf-8'))
        if lang=="Python3":
            os.system("python3 "+k+f"< questions/{Q_NO}/input.txt > "+k+".txt")
        else:
            os.system("g++ -o "+k+".obj "+k)
            os.system("./"+k+f".obj < questions/{Q_NO}/input.txt > "+k+".txt")
        x = open(k+".txt","r")
        p = x.read()
        y = open(f"questions/{Q_NO}/output.txt","r")
        q = y.read()
        p = p.replace(" ","")
        p = p.replace("\n","")
        q = q.replace(" ","")
        q = q.replace("\n","")
        print(p)
        print(q)
        if p=='':
            print("Error")
            sc.send("error_pls_re_write".encode('utf-8'))
        elif p==q:
            print("accepted")
            sc.send("accepted".encode('utf-8'))
        else:
            print("Wrong Ans")
            sc.send("wrong_ans".encode('utf-8'))
        sc.close()
    connection.close()
    

s = socket.socket()
s.bind(("localhost",9999))
s.listen(10) 

while True:
    sc, address = s.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (sc, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    
s.close()