#!/usr/bin/python3
import sys
import re
lines=[]
cp=0
loopstack=[]

def out_header():
    print("#include <stdio.h>")
    print("#include <stdlib.h>")
    print("#include <string.h>")
    print("static short A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z;")
    print("static unsigned char memory[65536]={0};")
    print("static int tmp,reminder;")
    print("static char buff[100]={0};")
    print("int ia(char *s,int v) {if (v){int i=0,r=v;while(r/=10)i++;ia(s,v/10);s[i++]=v%10+48;s[i]=0;}}");
    print("void pretprt(short c,short v) {")
    print("ia(buff,v); ")
    print("for(short j=0;j<c-strlen(buff);j++) printf(\" \"); ")
    print("printf(buff); ")
    print("}")
    print("void main() {")
    return

def out_tailer():
    print("}")
    return


def gethexstr(s,idx):
    d="0x"
    while idx<len(s) and s[idx] in '0123456789ABCDEF':
        d=d+s[idx]
        idx+=1
    return (d,idx)

def getdcmstr(s,idx):
    d=""
    while idx<len(s) and s[idx] in "0123456789":
        d=d+s[idx]
        idx+=1
    return (d,idx)

def term(s,idx):
    u=''
    if idx>=len(s):
        return s,-1

    if s[idx]=='(':
        (o,idx)=expression(s,idx+1)

        if s[idx]==')':
            idx+=1
        return ("("+o+")",idx) # normal end.

    elif s[idx]=='$' and idx+1<len(s) and s[idx+1].upper() in "0123456789ABCDEF":
        (o,idx)=gethexstr(s,idx+1)
        return (o,idx)

    elif s[idx] in "0123456789":
        (o,idx)=getdcmstr(s,idx)
        return (o,idx)

    elif s[idx]=='-':
        (o,idx)=term(s,idx+1)
        return "-"+o,idx

    elif s[idx]=='+':
        (o,idx)=term(s,idx+1)
        return "abs("+o+")",idx

    elif s[idx]=='#':
        (o,idx)=term(s,idx+1)
        return "!("+o+")",idx

    elif s[idx]=='\'':
        (o,idx)=term(s,idx+1)
        u="(rand()%("+o+"))"
        return u,idx

    elif s[idx]=='%':
        (o,idx)=term(s,idx+1)
        u="(reminder)"
        return u,idx+1

    elif s[idx]=='$' and not xdigit(s[idx+1]):
        return "getchar()",idx+1

    elif s[idx]=='"':   # 文字定数
        return "'"+s[idx+1]+"'",idx+2

    elif s[idx]=='?':
        u="(scanf(\"%d\",&tmp),(short)tmp)"
        return u,idx+1

    elif s[idx].upper()>='A' and s[idx].upper()<='Z':
        if (idx+1)<len(s) and s[idx+1]==':': # 8 bit array
            l=s[idx].upper()
            p,idx=expression(s,idx+2)
            o="memory["+l+"+"+p+"]"
            return o,idx

        elif (idx+1)<len(s) and s[idx+1]=='(': # 16 bit array
            l=s[idx].upper()
            p,idx=expression(s,idx+1)
            o="*((short *)(&memory["+l+"+("+p+"*2)]))"
            return o,idx

        else: # variable
            idx+=1
            return (s[idx-1].upper()),idx
    return s,idx+1

def expression(s,idx):
    (o,idx)=term(s,idx)
    w=o
    while True:
        if idx>=len(s):
            break
        if s[idx]=='+':
            op='+'
            idx+=1
        elif s[idx]=='-':
            op='-'
            idx+=1
        elif s[idx]=='/':
            op='/'
            idx+=1
        elif s[idx]=='*':
            op='*'
            idx+=1
        elif s[idx]=='=':
            op='=='
            idx+=1
        elif s[idx:idx+2]=='<>':
            op='<>'
            idx+=2
        elif s[idx:idx+2]=='<=':
            op='<='
            idx+=2
        elif s[idx:idx+2]=='>=':
            op='>='
            idx+=2
        elif s[idx]=='<':
            op='<'
            idx+=1
        elif s[idx]=='>':
            op='>'
            idx+=1
        else:
            break
        (v,idx)=term(s,idx)
        if op=='/':
            return ("((reminder="+w+"%"+v+"),("+w+"/"+v+"))",idx)
        w="("+w+op+v+")"
    return w,idx

def value(s,idx):
    return(int(s[idx:]))

def parse(l):
    global loopstack
    index=0
    while index<len(l):
        s=l[index]
        index+=1

        # Statements

        if s[0:2]=='#=':
            goto(value(s,2))

        elif s[0:2]=='!=':
            gosub(value(s,2))

        elif s[0:2]==';=':
            (o,idx)=expression(s,2)
            if__(o)

        elif s[0:3]=='??=':
            (o,idx)=expression(s,3)
            print(f"printf(\"%04x\",{o}); ",end='')

        elif s[0:3]=='?$=':
            (o,idx)=expression(s,3)
            print(f"printf(\"%02x\",{o}); ",end='')

        elif s[0:2]=='$=':
            (o,idx)=expression(s,2)
            print(f"printf(\"%c\",{o}); ",end='')

        elif s[0:2]=='.=':
            (o,idx)=expression(s,2)
            print(f"for(int i=0;i<{o};i++) printf(\" \"); ",end='')

        elif s[0:2]=='\'=':
            (o,idx)=expression(s,2)
            print(f"srand({o}); ",end='')

        elif s[0:2]=='?(':
            o,idx=getdcmstr(s,2)
            o=int(o)
            if s[idx:idx+2]==')=':
                idx+=2
                p,idx=expression(s,idx)
                print(f"pretprt((short){o},(short){p}); ")
            else:
                pass
            pass

        elif s[0]==']':
            ret()

        elif s[0]=='"':
            print(f"printf({s}); ",end='')

        elif s[0]=='/':
            idx=0
            while idx<len(s) and s[idx]=='/':
                print("printf(\"\\n\"); ",end='')
                idx+=1

        elif s[0].upper()>='A' and s[0].upper()<='Z':
            if s[1]==':': # 8bit array
                ch=s[0].upper()
                v,idx=expression(s,2)
                if s[idx:idx+2]==')=':
                    idx+=2
                    w,idx=expression(s,idx)
                    print("memory["+ch+"+"+v+"]=",end='')
                    print(f"{w}; ",end='')

            elif s[1]=='(': # 16 bit array
                ch=s[0].upper()
                v,idx=expression(s,2)
                if s[idx:idx+2]==')=':
                    idx+=2
                    w,idx=expression(s,idx)
                    print("*((short *)(&memory["+ch+"+"+v+"*2]))=",end='')
                    print(f"{w}; ",end='')

            elif s[1]=='=': # assignment
                ch=s[0].upper()
                (o,idx)=expression(s,2)
                print(f"{ch}={o};",end='')
                if idx<len(s) and s[idx]==',': # for
                    (p,idx)=expression(s,idx+1)
                    print("while(1) { if (!(",end='')
                    ies='<' if eval(o)<eval(p) else '>'
                    print(f"{ch}{ies}={p})) break; ",end='')
                    loopstack+=["for"]
            else:
                pass

        elif s[0:3]=='@=(':

            l=loopstack[0:len(loopstack)-1]
            if len(loopstack):
                i=loopstack[len(loopstack)-1:len(loopstack)]

            if i==["do"]: # until
                loopstack=l
                v,idx=expression(s,2)
                print("} ",end='')
                print(f"while(!{v}); ",end='')

            elif i==["for"]: # next
                ch=s[3].upper()
                loopstack=l
                v,idx=expression(s,2)
                print(f"{ch}={v};",end='')
                print(" }",end='')

        elif s[0:2]=='@=': # next
            ch=s[2].upper()
            l=loopstack[0:len(loopstack)-1]
            if len(loopstack):
                i=loopstack[len(loopstack)-1:len(loopstack)]
            if i==["for"]:
                loopstack=l
                v,idx=expression(s,2)
                print(f"{ch}={v};",end='')
                print(" }",end='')

        elif s[0]=='@': # do
            print("do { ",end='')
            loopstack+=["do"]

        elif s[0:2]=='?=':
            v,idx=expression(s,2)
            print(f"printf(\"%d\",{v}); ",end='')

        else:
            pass
    return

def adjust_go(n):
    for i in lines:
        if i>=n:
            return i
    return -1

def ret():
    print("__asm__ (\"ret\" : : :); ",end='')

def if__(o):
    print(f"if (!({o})) ",end='')
    goto(cp+1);
    return

def gosub(n):
    print(f"__asm__ goto(\"call %l[l{adjust_go(n)}]\" : : : :l{adjust_go(n)}); ",end='')
    return

def goto(n):
    if n==-1:
        print("return; ",end='')
        return
    print(f"goto l{adjust_go(n)}; ",end='')
    return

def getl(line):
    ln=line.replace('\n','')
    split_s=re.split(r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)',ln)
    s=[i for i in split_s if i]
    try:
        n=int(s[0])
    except:
        return (-1,[""])
    else:
        return (n,s[1:])

def pass1(file):
    global lines
    f=open(file,"rt")
    while True:
        l=f.readline()
        if not l:
            break
        (n,s)=getl(l)
        if n==-1:
            pass
        else:
            lines+=[n]
    f.close()
    return

def pass2(file):
    global lines,cp
    f=open(file,"rt")
    while True:
        l=f.readline()
        if not l:
            break
        (n,s)=getl(l)
        if n==-1:
            pass
        else:
            print(f"l{n}: ",end='')
            cp=n
            if s:
                parse(s)
        print("")
    f.close()
    return

def compile(file):
    pass1(file)
    pass2(file)

def main():
    out_header()
    compile(sys.argv[1])
    out_tailer()
    return

if __name__=='__main__':
    if len(sys.argv)!=2:
        print("Usage: game2c.py file.gm >c.out")
        exit(1)
    main()
    exit(0)
