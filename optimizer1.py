def unbrac(s):
    #print(s, "sss")
    if s[0]=="(" and s[-1]==")":
        c=0
        i=1
        while c>=0:
            if s[i]=="(":
                c+=1
            elif s[i]==")":
                c-=1 
            i+=1
        if i==len(s):
            #print(s[1:-1], "qwqwq")
            return unbrac(s[1:-1])
        else:
            return s
    else:
        return s
def ssnf(s):
    s=unbrac(s)
    if s.find("*")==-1:
        return s 
    elif s.find("|")==-1:
        if s[0]=="(" and s[-2]==")" and s[-1]=="*":
            if s[:-1]!=unbrac(s[:-1]):
                return ssnf(s[:-1])
            else:
                return ssnf(optimise(s))
        else:
            l=len(s)
            c=""
            f=0
            for i in range (l):
                if s[i]=="*":
                    if c!="" and s[i-1]!=c[0]:
                        f=1 
                        break
                    c=s[i-1]
            if f==0 and s.count("*")>=(l//2):
                return c
            else:
                return s
    else:
        n=s.count("|")+1
        l=len(s)
        s2=""
        s1=""
        for i in range (l):
            if s[i]=="|":
                s2=s2+ssnf(s1)+"|"
                s1=""
            else:
                s1=s1+s[i]
        s2=s2+ssnf(s1)
        return s2
def dstr(string):
    if string.find("|")==-1:
        return string
    else:
        strings=[]
        s1=""
        i=0
        while i<len(string):
            if string[i]=="|":
                strings.append(s1)
                s1=""
                i+=1
            elif string[i]=="(":
                s2=""
                c=1
                i+=1
                while c!=0:
                    if string[i]==")":
                        c-=1 
                    elif string[i]=="(":
                        c+=1 
                    s2=s2+string[i]
                    i+=1
                #print(s2, "s2222")
                s3=dstr(s2[:-1])
                #print(s3, "s333")
                if i<=len(s1) and s1[i]=="*":
                    if s3[0]=="(" and s3[-1]==")":
                        s1=s1+s3+"*"
                    else:
                        s1=s1+"("+s3+")*"
                    i+=1
                else:
                    s1=s1+s3
            else:
                s1=s1+string[i]
                i+=1
        strings.append(s1)
        l=len(strings)
        if l==1:
            strings[0]="("+strings[0]+")"
            return (strings[0])
        for i in range(0,l-1):
            for j in range(i+1,l):
                if strings[i]==strings[j]:
                    strings.pop(j)
        f=0
        left=""
        while f==0:
            s1=strings[0][0]
            for s in strings:
                if s[0]!=s1:
                    f=1 
            if f==0:
                left=left+s1
                f1=0
                for s in range(len(strings)):
                    if len(strings[s])>1 and strings[s][1]=="*" and f1==0:
                        f1=1
                    elif len(strings[s])==1 or (len(strings[s])>1 and strings[s][1]!="*" and f1==0):
                        f1=2 
                    else:
                        f1=3
                if f1!=3:
                    for s in range(len(strings)):
                        strings[s]=strings[s][1:]
                        if len(strings[s])==0:
                            f=2
                else:
                    for s in range(len(strings)):
                        if len(strings[s])==1 or (len(strings[s])>1 and strings[s][1]!="*"):
                            strings[s]=strings[s][1:]
                            if len(strings[s])==0:
                                f=2
        if f!=2:
            f=0
        right=""
        while f==0:
            s1=strings[0][-1]
            for s in strings:
                if s[-1]!=s1:
                    f=1 
            if f==0:
                right=s1+right
                for s in range(len(strings)):
                    strings[s]=strings[s][:-1]
                    if len(strings[s])==0:
                        f=2
        new=left+"("
        for s in strings:
            if s=="":
                s="e"
            new=new+s+"|"
        new=new[:-1]+")"+right
        #print(strings)
        #print("new", new)
        return new
def optimise(string):
    alf=""
    s=""
    while string.find("**")!=-1:
        string=string.replace("**","*")
    i=len(string)-1
    while i>=0:
        if string[i]=='*' and string[i-1]==')':
            i-=1
            s1=""
            c=1
            while c!=0:
                s1=string[i]+s1
                i-=1
                if string[i]==")":
                    c+=1 
                elif string[i]=="(":
                    c-=1 
            i-=1
            d=len(s1)
            s2=ssnf(s1[:-1])
            d1=len(s2)
            d2=2
            if d1==1:
                s=s2+"*"+s
                d2=1
            else:
                s="("+s2+")*"+s
            f=0
            while string[i]=="*" and f==0:
                if string[:i].rfind(s1)==i-d:
                    i=i-d-2
                    if i<0:
                        break
                elif string[:i].rfind(s2)==i-d1:
                    print(string[:i])
                    i=i-d1-d2
                    if i<0:
                        break
                else:
                    f=1
        elif string[i]=='*':
            s=string[i-1:i+1]+s
            i-=2
            while i>=1 and string[i]=="*" and string[i-1]==s[0]:
                i-=2 
        elif string[i]==')':
            s1=""
            c=1
            while c>0:
                s1=string[i]+s1
                i-=1
                if string[i]==")":
                    c+=1 
                elif string[i]=="(":
                    c-=1 
                #print(c,string[i], "ccc")
            s1=string[i]+s1
            #print(unbrac(s1), "s11")
            i-=1
            s="("+unbrac(s1)+")"+s
        else:
            s=string[i]+s 
            i-=1
    i=0
    new=""
    while i<len(s):
        i1=i
        i+=s[i:].find("(")+1 
        if i1==i:
            return(new+s[i:])
        new=new+s[i1:i-1]
        c=1 
        s1=""
        while c!=0:
            if s[i]==")":
                c-=1 
            elif s[i]=="(":
                c+=1 
            s1=s1+s[i]
            i+=1
        s2=dstr(s1[:-1])
        if i<len(s) and s[i]=="*":
            if s2[0]=="(" and s2[-1]==")":
                new=new+s2+"*"
            else:
                new=new+"("+s2+")*"
            i+=1
        else:
            new=new+s2
    return(new)
    
#aa*(c|aa)  ((((a|b)ab)*a)*|ba|c)
#(a*|b*|c*)*dada*a*a*((bb))a(c**)**(a|ca)*a((ba)*(ba)*)*
s=str(input())

#print(optimise(s))