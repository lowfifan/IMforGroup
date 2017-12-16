import socket
import threading
import time
import os
from tkinter import*
from tkinter.filedialog import *
import datetime
class server:
    def accept(self,c,addr,num):
        while True:
            msg=[]
            str1=c.recv(1024).decode('utf-8')
            msgnum=str1.split()[0]

            if msgnum=='连接成功！':
                self.text.insert(END,'客户端'+str(self.numtotal)+' ('+str1.split()[1]+') 连接成功'+'\n')
                self.name.append(str1.split()[1])

                self.sendnoself(self.numtotal,('0客户端'+str(self.numtotal)+' ('+str1.split()[1]+') 已上线'))
                continue
                
            for i in range(1,len(str1.split())):
                msg.append(str1.split()[i])
            msgsend=' '.join(msg)
            thisname=self.name[int(msgnum)-1]
            self.text.insert(END,'客户端'+msgnum+' ('+thisname+')'+' '+datetime.datetime.now().strftime('%Y-%m-%d %T')+'\n  '+msgsend+'\n')
#talk
            self.sendnoself(msgnum,(thisname+' '+msgsend))

    def sendnoself(self,nonum,msg):
        for i in range(1,self.numtotal+1):
            if str(i)!=str(nonum):
                try:
                    self.add[i-1].send(msg.encode('utf-8'))
                except:
                    continue


    def send(self):
        while True:
            if self.isbutton != 1:
                continue
            time.sleep(0.1)
            str1=self.sendmsg.get()
            #            str1=input('\nServer: ')
            self.text.insert(END,'系统消息(ME) '+datetime.datetime.now().strftime('%Y-%m-%d %T')+'\n  '+str1+'\n')
            for i in self.add:
                try:
                    i.send(('0'+str1).encode('utf-8'))
                except:
                    continue
            self.isbutton=0

    def isButton(self):
        self.isbutton=1




    def saveAs(self):
        fileName=asksaveasfilename()
        file=open(fileName,'w')
        file.write(self.text.get(1.0,END))
        file.close()
    #读取记录函数
    def read(self):
        fileName=askopenfilename()
        infilr=open(fileName,'r')
        self.text.delete(1.0,END)
        self.text.insert(END,infilr.read())
        infilr.close()
    def cleanout(self):
        num=self.sendmsg.get()
        try:
            num=int(num)
        except:
            self.text.insert(END,'系统消息(ME) '+datetime.datetime.now().strftime('%Y-%m-%d %T')+'\n  '+str(num)+'不是有效数字\n')
            return 0
        if num<1 or num>self.numtotal:
            self.text.insert(END,'系统消息(ME) '+datetime.datetime.now().strftime('%Y-%m-%d %T')+'\n  '+str(num)+'不是有效数字\n')
            return 0
        self.add[num-1].send(('0你已被系统踢出').encode('utf-8'))
        self.sendnoself(num,'0客户端'+str(num)+'('+self.name[num-1]+') 被系统踢出')
        self.add[num-1].close()
        self.text.insert(END,'系统消息(ME) '+datetime.datetime.now().strftime('%Y-%m-%d %T')+'\n  '+'客户端'+str(num)+' 已断开\n')








    def mainloop1(self):
        window=Tk()
        window.title('程迅PP--关注沟通，更关心你')
        frame1=Frame(window)
        frame1.pack()
        label=Label(frame1, text='服务器')
        self.text=Text(frame1)
        self.text.grid(row=2,column=1)
        label.grid(row=1,column=1)
        frame2=Frame(window)
        frame2.pack()
        self.sendmsg=StringVar()
        entry=Entry(frame2,textvariable=self.sendmsg)
        button=Button(frame2,text='发送',command=self.isButton)
        buttonclean=Button(frame2,text='踢人',command=self.cleanout)
        entry.grid(row=1,column=1)
        button.grid(row=1,column=2)
        buttonclean.grid(row=1,column=3)
        buttonsave=Button(frame2,text='保存聊天记录',command=self.saveAs)
        buttonread=Button(frame2,text='读取',command=self.read)
        buttonsave.grid(row=1,column=4)
        buttonread.grid(row=1,column=5)

        window.mainloop()




    def __init__(self):
        s=socket.socket()
        host='localhost'
        port=12345
        print (host)
        s.bind((host,port))
        s.listen(5)
        
        self.name=[]
        self.numtotal=0
        self.add=[]
        self.isbutton=0

        while True:
            c,addr=s.accept()
            self.add.append(c)
            self.numtotal+=1
            #    threading.Thread(target=server,args=(c,addr,num)).start()
            c.send(('连接成功！你是第 '+str(self.numtotal)+' 号\n  注：对话框没有自动滚动功能，要用鼠标滚动；').encode('utf-8'))
            threading.Thread(target=self.accept,args=(self.add[self.numtotal-1],addr,self.numtotal)).start()

            if self.numtotal==1:
                threading.Thread(target=self.send).start()
                threading.Thread(target=self.mainloop1).start()








class client:      
    def accept(self,s):
            while True:
                testmsg=[]
                showmsg=[]
                msg=s.recv(1024).decode('utf-8')
                num=msg[0]

                if num==str(0) or msg[0]=='连':
                    for i in range(1,len(msg)):
                        testmsg.append(msg[i])
                    ultmsg=''.join(testmsg)
                    if msg[0]=='连':
                        self.num=msg.split()[1]
                        ultmsg='连'+ultmsg

                else:
                    showname=msg.split()[0]
                    for i in range(1,len(msg.split())):
                        showmsg.append(msg.split()[i])
                    ultmsg=' '.join(showmsg)

                time.sleep(1.5)
                if num==str(0) or num=='连':
                    self.text.insert(END,'系统消息 '+datetime.datetime.now().strftime('%Y-%m-%d %T')+'\n  '+ultmsg+'\n')
                    num=str(1)
                else:
                    self.text.insert(END,showname+' '+datetime.datetime.now().strftime('%Y-%m-%d %T')+'\n  '+ultmsg+'\n')



    def send(self,s):
            time.sleep(0.5)
            while True:
                if self.isbutton!=1:
                    continue
                #            msg=input('\nClient '+str(self.num)+': ')
                msg=self.sendmsg.get()
                sendmsg=str(self.num)+' '+msg
                self.text.insert(END,self.conname+'(ME) '+datetime.datetime.now().strftime('%Y-%m-%d %T')+'\n  '+msg+'\n')
                s.send(sendmsg.encode('utf-8'))
                self.isbutton=0

                #客户端界面绘制
    def mainloop1(self):
            window=Tk()
            window.title('程迅PP--关注沟通，更关心你')
            frame1=Frame(window)
            frame1.pack()
            label=Label(frame1, text='实名客户端 the num.'+self.num)
            self.text=Text(frame1)
            self.text.grid(row=2,column=1)
            label.grid(row=1,column=1)
            frame2=Frame(window)
            frame2.pack()
            self.sendmsg=StringVar()
            entry=Entry(frame2,textvariable=self.sendmsg)
            button=Button(frame2,text='发送',command=self.buttonaa )
            buttonsave=Button(frame2,text='保存记录',command=self.saveAs)
            buttonread=Button(frame2,text='读取记录',command=self.read)
            buttonsave.grid(row=1,column=3)
            buttonread.grid(row=1,column=4)
            entry.grid(row=1,column=1)
            button.grid(row=1,column=2)
            window.mainloop()


    def saveAs(self):
#            fileName=asksaveasfilename()
            fileName='record.chengxun'
            file=open(fileName,'w')
            file.write(self.text.get(1.0,END))
            file.close()

    def read(self):
#            fileName=askopenfilename()
            fileName='record.chengxun'
            infilr=open(fileName,'r')
            self.text.delete(1.0,END)
            self.text.insert(END,infilr.read())
            infilr.close()

    def buttonaa(self):
            self.isbutton=1

    def __init__(self):
            s=socket.socket()
            self.conname=socket.gethostname()
            host='localhost'
            port=12345
            s.connect((host,port))
            self.isbutton=0
            threading.Thread(target=self.accept,args=(s,)).start()
            threading.Thread(target=self.send,args=(s,)).start()
            time.sleep(0.5)
            threading.Thread(target=self.mainloop1).start()
            s.send(('连接成功！ '+self.conname).encode('utf-8'))












