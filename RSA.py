import random
from tkinter import *
from tkinter.messagebox import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

def gcd(a,b):           #欧几里得算法
    if b==0:
        return a
    return gcd(b,a%b)


def exgcd(a, b):                            #扩展的欧几里得算法
    if b == 0:
        return 1, 0, a
    else:
        x, y, q = exgcd(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, q
def invert(a,b):        #a为求逆的数，b为模数。求逆元
    if gcd(a,b)!=1:
        return "无逆元！"
    return exgcd(b, a)[1] % b

def getint(n):                                  #获取二进制n位大小的整数
    rand = random.randint(2**(n-1),2**n)
    return rand

#通过Miller—Rabin算法判断是不是素数
def isPrime(testNum):
    smallPrime=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,233,239,
                241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,
                421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,
                607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,
                809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
    if(testNum<2):
        return False
    if testNum in smallPrime:
        return True
    for prime in smallPrime:
        if(testNum%prime==0):
            return False
    return(Miller_Rabin(testNum))
def Miller_Rabin(testNum):
    safeTime=20#素性检测次数
    eulerN=testNum-1
    oddQ=0
    testNum2=0
    #计算n-1=2^s*t
    while(eulerN%2==0):
        testNum2=testNum2+1
        eulerN=eulerN//2
    #计算n-1=2^s*t
    oddQ=eulerN#得到t
    for trials in range(safeTime):
        random_a=random.randrange(2,testNum-1)
        firstTest=pow(random_a,oddQ,testNum)
        if(firstTest==1 or firstTest==testNum-1):
            continue
        else:
            nextTest=firstTest
            for i in range(1,testNum2):
                nextTest=(nextTest**2)%testNum
                if(nextTest==testNum-1):
                    break
            return False
    return True
def getprime(bit):                  #获取大素数
    i=1
    while(True):
        num=getint(bit)
        if(isPrime(num)):
            return num
        else:
            i+=1
def fastexpmod(b, e, m):                #快速幂模
    result = 1
    while e != 0:
        if e%2 == 1:

            result = (result * b) % m
        e = e//2
        b = (b*b) % m
    return result

def RSA():          #获取rsa p,q,e,d,n
    q = getprime(1024)
    while 1:
        p = getprime(1024)
        if q == p:
            p = getprime(1024)
        else:
            break
    e = 65537
    d = invert(e, (q - 1) * (p - 1))
    n = q * p
    return p,q,e,d,n

def encrypt(m,e,n):
    c = fastexpmod(m,e,n)
    return c

def decrypt(c,d,n):
    m = fastexpmod(c,d,n)
    return m
#4个按钮点击事件
def bu_0():
    en1.delete("1.0", "end")
    en2.delete("1.0", "end")
    en3.delete("1.0", "end")
    en4.delete("1.0", "end")
    en5.delete("1.0", "end")
    en6.delete("1.0", "end")
    en7.delete("1.0", "end")

def bu_1():
    if en1.get('0.0','end') =="\n":
        showinfo("提示","请在m处输入数据!")
    else:
        mm = en1.get('0.0','end').strip()
        mm = (mm).encode('utf-8')

        inp = bytes_to_long(mm)
        global  c
        c = encrypt(inp, e, n)
        en7.insert("end", c)
        en2.insert("end", e)
        en5.insert("end", n)

def bu_2():
    r = askquestion("提示","是否解密上次加密内容！")
    if r==YES:
        mm = decrypt(c, d, n)
        mm = long_to_bytes(mm).decode('utf-8')
        en1.insert("end",mm)
    else:
        pass

def bu_3():
    p, q, e, d, n = RSA()
    en3.insert("end", q)
    en4.insert("end", p)
    en6.insert("end", d)
    
if __name__ == '__main__':

    global p, q, e, d, n,c,mm
    p, q, e, d, n = RSA()
    root = Tk()
    root.geometry("540x300")
    root.title("Te的RSA加密")
    lab0 = Label(root,text="欢迎使用RSA加密！",fg="red",
                 font=("华文行楷",20,)
                 )
    lab0.grid(column=0,row=0,columnspan=4)
    lab1 = Label(root,text="m：",relief=FLAT)
    lab1.grid(column=0,row=1)
    en1 = Text(root,width=50,height=2)
    en1.grid(column=1,row=1,columnspan=2)

    lab2 = Label(root, text="e：",relief=FLAT)
    lab2.grid(column=0, row=2)
    en2 = Text(root, width=50,height=2)
    en2.grid(column=1,row=2,columnspan=2)

    lab3 = Label(root, text="q：", relief=FLAT)
    lab3.grid(column=0, row=3)
    en3 = Text(root, width=50,height=2)
    en3.grid(column=1, row=3, columnspan=2)

    lab4 = Label(root, text="p：", relief=FLAT)
    lab4.grid(column=0, row=4)
    en4 = Text(root, width=50, height=2)
    en4.grid(column=1, row=4, columnspan=2)

    lab5 = Label(root, text="n：", relief=FLAT)
    lab5.grid(column=0, row=5)
    en5 = Text(root, width=50, height=2)
    en5.grid(column=1, row=5, columnspan=2)

    lab6 = Label(root, text="d：", relief=FLAT)
    lab6.grid(column=0, row=6)
    en6 = Text(root, width=50, height=2)
    en6.grid(column=1, row=6, columnspan=2)

    lab7 = Label(root, text="c：", relief=FLAT)
    lab7.grid(column=0, row=7)
    en7 = Text(root, width=50, height=2)
    en7.grid(column=1, row=7, columnspan=2)

    bu0 = Button(root, text="清空所有", bg="grey", width=20, height=1, command=bu_0)
    bu0.grid(column=3, row=1)
    bu1 = Button(root,text="加密",bg="grey",width=20, height=1,command=bu_1)
    bu1.grid(column=1,row=8)
    bu2 = Button(root,text="解密",bg="grey",width=20, height=1,command=bu_2)
    bu2.grid(column=2,row=8)
    bu3 = Button(root, text="获取加密过程的q和p",bg="grey", width=20, height=1, command=bu_3)
    bu3.grid(column=3, row=8)

    lab8 = Label(root,text="another：te_mgl",fg="blue",
                 font=("",8),
                 anchor="center")
    lab8.grid(column=3, row=9)
    mes = Label(root,text="RSA算法过程简介：\n\nn = p*q\ne*d = k*(p-1)*(q-1)-1\nc = (m^e)%n\nm = (c^d)%n")
    mes.grid(column=3,row=3,rowspan=4)
    root.mainloop()








