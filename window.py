#!/usr/bin/python3
# -*-coding: utf-8 -*-
import binascii,threading,sys,ctypes,crcmod,serial,urllib.request
from shutil import copyfile
from os.path import exists
from os import mkdir, remove, system
from time import sleep
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from datetime import datetime
from math import log10
from serial.tools.list_ports import comports
from sys import getwindowsversion

f=None
serialPort = 'COM5'  # 端口
baudRate = 9600  # 波特率
data_bytes=bytearray()
port_list = list(comports())
fla=0
is_exit=False
ver='1.0.1'

#port=None
def readdata(s):
    global port,fla,entry2,entry3,entry4,entry5,entry6,baudRate,ch1,is_exit
    time=0
    while not is_exit:
        r=port.readline().decode("gbk")
        sleep(0.1)
        print("Info:read text from %s is:%s.The tested The number of times to test is %d."%(entry1.get()[0:5].replace(' ',''),r,time))
        if r.find("OK")!=-1:
            f=open('data/userinfo.txt','a')
            f.write(e3.get()+e4.get()+","+e2.get()+","+e5.get()+","+e6.get()+'\n')
            f.close
            if ch1.get()==1:
                a=int(e4.get())
                a=a+1
                l=int(log10(a))+1
                entry4.delete(0,END)
                for i in range(0,6-l):
                    entry4.insert(i,"0")
                entry4.insert(6-l,str(a))
            is_exit=True
            entry5.delete(0,END)
            entry6.delete(0,END)
            messagebox.showinfo('Info:',"测试%s已通过\n写到文件data\\userinfo.txt..."%s)
            return
        elif r.find("rror")!=-1 :
            if time>5:
                messagebox.showerror('Error:',"测试%s未通过\n,数据不保存。"%s)
                is_exit=True
            else:
                time=time+1
        elif len(r)==0:
            if time>5:
                print("Warnning:未收到数据？")
                is_exit=True
            else:
                time=time+1                
        else:time=time+1
def clenalldata():
    global entry2,entry3,entry4,entry5,entry6
    entry2.delete(0,END)
    entry3.delete(0,END)
    entry4.delete(0,END)
    entry5.delete(0,END)
    entry6.delete(0,END)
def Loadlastdata():
    global entry2,entry3,entry4,serialPort,baudRate
    entry2.delete(0,END)
    entry3.delete(0,END)
    entry4.delete(0,END)
    if exists('data/conf.dat'):
        try:
            f=open('data/conf.dat', encoding='utf-8')#,"r+"
            entry2.insert(0,f.readline())
            entry3.insert(0,f.readline())
            entry4.insert(0,f.readline())
            serialPort=f.readline()
            baudRate=int(f.readline())
        except:pass
def Loaddefaultdata():
    global entry2,entry3,entry4,serialPort,baudRate
    entry2.delete(0,END)
    entry3.delete(0,END)
    entry4.delete(0,END)
    entry2.insert(0,"100001")
    entry3.insert(0,"LY")
    entry4.insert(0,"000001")
def about():
    global ver
    messagebox.showinfo("关于","设备生成验证工具 Version:%s\n用于判断设备码及MQTT用户名密码是否正确。"%ver)
def updatecheck():
    global ver
    urllib.request.urlretrieve('http://gcore.jsdelivr.net/gh/AEnjoy/Github_figure_bed_Py@master/devicescheck.txt','che')
    f=open('che', encoding='utf-8')
    v=f.readline().replace('\n','')
    if v==ver:
        messagebox.showinfo("更新:","当前版本：%s已经是最新版本"%v)
    else:
        messagebox.showinfo("更新:","发现最新版本：%s\n当前版本为：%s\n点击OK下载更新"%(v,ver))
        url=f.readline().replace('\n','')
        if url=='null':
            messagebox.showinfo("更新：","最新版本下载连接为空")
        else:
            #webbrowser.open(url)
            urllib.request.urlretrieve(url,'设备生成验证工具v%s.exe'%v)
            system('start 设备生成验证工具v%s.exe update "%s"'%(v,sys.argv[0]) )
            f.close()
            remove('che')
            exit()
    f.close()
    remove('che')
    pass
def str_to_hexStr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')
def calc_crc(string):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    string = string.replace(" ", "")
    readcrcout = hex(crc16(binascii.unhexlify(string))).upper()
    str_list = list(readcrcout)
    if len(str_list) == 5:
        str_list.insert(2, '0') 
    crc_data = "".join(str_list)
    return (crc_data[4:]  + crc_data[2:4])
def randstr(n=8,mode=0):#n:长度 mode:0:username 1:password
    import random
    if mode==0:
        dist = '0123456789' #!@#$%^&*()-+=.' 
    elif mode==1:
        dist = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    elif mode==2: 
        dist = '0123456789abcdefghijklmnopqrstuvwxyz#!@#$%^&*()-+=.'
    t=''
    for i in range(n):
        c=random.choice(dist)
        t=t+c
    return t#.encode('utf-8')
def opencom():
    #打开串口按钮
    global port,serialPort,fla,entry1,b1
    if fla==1:
        b1=Button(myWindow, text='打开', command=opencom)
        b1.grid(column=2, padx=5, pady=5,row=0)
        port.close()
        fla=0
        messagebox.showinfo('Info:','I:端口%s关闭成功.'%entry1.get())
        return
    print("请稍后...正在连接并测试...\n该过程程序可能会出现未响应为正常现象\nTime:"+str(datetime.now()))
    serialPort=entry1.get()[0:5].replace(' ','')
    try:port = serial.Serial(serialPort, baudRate)
    except:
        print('E:端口%s打开失败,请重新选择.'%entry1.get())
        messagebox.showerror('Error:','E:端口%s打开失败,请重新选择.'%entry1.get())
        return
    if not port.isOpen():
        print('E:端口%s打开失败,请重新选择.'%entry1.get())
        messagebox.showerror('Error:','E:端口%s打开失败,请重新选择.'%entry1.get())
        return
    print("Info:%s is opened. Time is:%s"%(entry1.get(),str(datetime.now())))
    messagebox.showinfo('Info:','I:端口%s打开成功.'%entry1.get())
    b1=Button(myWindow, text='关闭', command=opencom)
    b1.grid(column=2, padx=5, pady=5,row=0)
    fla=1
    pass
def autocreat():
    #自动生成按钮
    global entry5,entry6,ch1,entry4
    entry5.delete(0,END)
    entry6.delete(0,END)
    entry5.insert(0,randstr(16,1))
    entry6.insert(0,randstr(16,1))
    s="Set:"+e3.get()+e4.get()+","+e2.get()+","+e5.get()+","+e6.get()+","
    print("Info:"+s)
    print("CRC16 decoded:"+calc_crc(str_to_hexStr(s)))#+"\nCRC16 Raw Bytes:"+str(bytes.fromhex(calc_crc(str_to_hexStr(s))))
    
    f=open('data/conf.dat',"w", encoding='utf-8')
    f.write(e2.get()+"\n"+e3.get()+"\n"+e4.get()+"\n"+entry1.get()[0:5].replace(' ','')+'\n'+str(baudRate))
    f.close()
    pass
def writetodevice():
    #写入设备按钮
    global port,fla,entry2,entry3,entry4,entry5,entry6,baudRate,ch1,is_exit
    is_exit=False

    if fla==0 or not port.isOpen():
        print("E:设备未连接.Time:%s"%str(datetime.now()))
        messagebox.showerror('Error:',"E:设备未连接,请先点击“打开”.Time:%s"%str(datetime.now()))
        return
    print("请稍后...测试...\n该过程程序可能会出现未响应为正常现象\nTime:"+str(datetime.now()))
    if (len(e2.get())+len(e3.get())+len(e4.get())+len(e5.get())+len(e6.get()))!=46:
        messagebox.showerror("Error:","参数填写不正确。\n请检查输入参数长度是否正确。\n\n输入的位数信息:\n代理商密码:%d/6\n设备Id 前缀:%d/2 编号%d/6\nMQTT 用户名:%d/16 密码:%d/16"%(len(e2.get()),len(e3.get()),len(e4.get()),len(e5.get()),len(e6.get())))    
        return
    s="Set:"+e3.get()+e4.get()+","+e2.get()+","+e5.get()+","+e6.get()+","
    x16=calc_crc(str_to_hexStr(s))
    #print("Debug data:")
    #print(str_to_hexStr(s)+x16)
    port.write(bytes.fromhex(str_to_hexStr(s)+x16))

    t1 = threading.Thread(target=readdata,args=(s,))
    t1.setDaemon(True)
    t1.start()

def callback(e):
    c=e.get()[0:6]
    e.set(c)
def callback1(e):
    c=e.get()[0:2]
    e.set(c)
def callback2(e):
    c=e.get()[0:16]
    e.set(c)    
#GUI
myWindow = Tk() 
myWindow.title('设备生成验证工具')
myWindow.resizable(width=False, height=False)
menu=Menu(myWindow)
men1 = Menu(menu,tearoff=0)
men1.add_command(label="加载上次数据",command=Loadlastdata)
men1.add_command(label="清空本次数据",command=clenalldata)
men1.add_command(label="加载默认数据",command=Loaddefaultdata)
men1.add_separator()
men1.add_command(label="退出",command=myWindow.quit)
men2= Menu(menu,tearoff=0)
men2.add_command(label="检查更新",command=updatecheck)
#men2.add_command(label="显示更新日志",command=clenalldata)
men2.add_separator()
men2.add_command(label="关于",command=about)
menu.add_cascade(label="文件",menu=men1)
menu.add_cascade(label="关于",menu=men2)

myWindow.config(menu=menu)
if getwindowsversion().build>=9600:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
    myWindow.tk.call('tk', 'scaling', ScaleFactor/75)
    menu.tk.call('tk', 'scaling', ScaleFactor/75)
    men1.tk.call('tk', 'scaling', ScaleFactor/75)
    men2.tk.call('tk', 'scaling', ScaleFactor/75)
Label(myWindow,text='串口:',justify=RIGHT).grid(row=0, column=0)
entry1=Spinbox(myWindow,exportselection=0,value=port_list)
entry1.grid(row=0, column=1)
b1=Button(myWindow, text='打开', command=opencom)
b1.grid(column=2, padx=5, pady=5,row=0)
Label(myWindow,text='代理商密码:',justify=RIGHT).grid(row=1)
e2=StringVar()
e3=StringVar()
e4=StringVar()
e5=StringVar()
e6=StringVar()
entry2=Entry(myWindow,exportselection=0,textvariable=e2)
entry2.grid(row=1, column=1)
e2.trace("w", lambda  name, index, mode, e2=e2: callback(e2))
Label(myWindow,text='[6位数字]',justify=RIGHT).grid(row=1,column=2)
Label(myWindow,text='设备ID:',justify=RIGHT).grid(row=2)
entry3=Entry(myWindow,exportselection=0,width= 4,textvariable=e3)
entry3.grid(row=2, column=1,sticky=W)
e3.trace("w", lambda  name, index, mode, e3=e3: callback1(e3))
entry4=Entry(myWindow,exportselection=0,width= 6,textvariable=e4)
entry4.grid(row=2, column=1,sticky=E)
e4.trace("w", lambda  name, index, mode, e4=e4: callback(e4))
Label(myWindow,text='[6位数字]',justify=RIGHT).grid(row=2,column=2)
Label(myWindow,text='前缀 2个字母',justify=RIGHT).grid(row=3, column=1,sticky=W)
Label(myWindow,text='编号',justify=RIGHT).grid(row=3, column=1,sticky=E)
ch1 = IntVar()
check1 = Checkbutton(myWindow, text="自动加1", variable=ch1, state='active')
check1.grid(row=3, column=2)
Label(myWindow,text='MQTT用户名:',justify=RIGHT).grid(row=4)
entry5=Entry(myWindow,exportselection=0,textvariable=e5)
entry5.grid(row=4, column=1)
Label(myWindow,text='[生成的16位用户名]',justify=RIGHT).grid(row=4,column=2)
Label(myWindow,text='MQTT密码:',justify=RIGHT).grid(row=5)
entry6=Entry(myWindow,exportselection=0,textvariable=e6)
entry6.grid(row=5, column=1)
e5.trace("w", lambda  name, index, mode, e5=e5: callback2(e5))
e6.trace("w", lambda  name, index, mode, e6=e6: callback2(e6))
Label(myWindow,text='[生成的16位密码]',justify=RIGHT).grid(row=5,column=2)
Label(myWindow,text='-----------------------').grid(row=6,column=1)
b2=Button(myWindow, text='自动生成', command=autocreat)
b2.grid(row=7,column=0)
b3=Button(myWindow, text='写入设备', command=writetodevice)
b3.grid(row=7,column=2)
Label(myWindow,text=' ',justify=RIGHT).grid(row=8,column=2)
if __name__ == '__main__':
    try:
        s1=str(sys.argv[1])
        if s1=='update':
            s2=sys.argv[2]
            sleep(1.5)
            copyfile(sys.argv[0],s2)
            system('start "%s" delete "%s"'%(s2,sys.argv[0]))
            exit(0)
        elif s1=='delete':
            s2=sys.argv[2]
            sleep(1.5)
            remove(s2)
            messagebox.showinfo("Update:","更新完成.")
    except:pass
    
    try:mkdir('data')
    except:pass
    if exists('data/conf.dat'):
        try:
            f=open('data/conf.dat', encoding='utf-8')#,"r+"
            entry2.insert(0,f.readline())
            entry3.insert(0,f.readline())
            entry4.insert(0,f.readline())
            serialPort=f.readline()
            baudRate=int(f.readline())
        except:
            f.close()
            remove('data/conf.dat')
            print("E:请重新打开软件.")
            exit(0)
    else:
        entry2.insert(0,"100001")
        entry3.insert(0,"LY")
        entry4.insert(0,"000001")
        f=open('data/conf.dat',"w", encoding='utf-8')
        d='''100001
LY
000001
COM5
9600'''
        f.write(d)
        f.close()
    #load window
    myWindow.mainloop()