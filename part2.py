f = open('file2', 'r')
map = {'HALT': "1", 'LOAD': "2", 'STORE': "3", 'ADD': "4", 'SUB': "5", 'INC': "6", 'DEC': "7", 'XOR': "8", 'AND': "9",
       'OR': 'A', 'NOT': 'B', 'SHL': 'C', 'SHR': 'D', 'NOP': 'E', 'PUSH': 'F', 'POP': "10", 'CMP': "11", 'JMP': "12",
       'JZ': "13", 'JE': "13", 'JNZ': "14", 'JNE': "14", 'JC': "15", 'JNC': "16", 'JA': "17", 'JAE': "18", 'JB': "19",
       'JBE': '1A', 'READ': '1B', 'PRINT': '1C'}
registersaddr = {'PC': "0", 'A': "1", 'B': "2", 'C': "3", 'D': "4", 'E': "5", 'S': "6"}

def getkey(val):  #mapin tersini yazmamak için bunu yazdım valueyu yazınca keyi veriyo ama hiç gerekmeyebilir
   for key, value in map.items():
      if val == value:
         return key

register= {'0000': ' ', '0001':' ','0002':' ','0003':' ','0004':' ','0005':' ','0006':' '}
asci={'0041':45,'0042':47,'0043':49,'0044':51,'0045':53}
memory=[None]*65536

memory[45]='00'
memory[46]='41'
memory[47]='00'
memory[48]='42'
memory[49]='00'
memory[50]='43'
memory[51]='00'
memory[52]='44'
memory[53]='00'
memory[54]='45'




def getdatafrommemo(address):
    toint = int(address, 10)
    val1 = memory[toint]
    val2 = memory[toint + 1]
    data = val1 + val2
    return data

def sum(operand1, operand2):
    global CF, SF, ZF
    int1 = int(operand1, 16)
    int2 = int(operand2, 16)
    sum = int1 + int2
    print(sum)
    formed = bin(sum)[2:]
    if sum == 0 :
        ZF = True
        return format(sum, '4x')
    if len(formed) > 16:
        if formed[15] == '1':
            SF = True
        CF = True
        int_result = sum - pow(2,16)
        final = '{0:04x}'.format(int_result)
        return final
    if len(formed) == 16 and formed[15] == '1':
        SF = True
    final=format(sum, '4x')
    print(final)
    return final

def postoneg(operand):
    int1 = int(operand, 16)
    new=''
    bin_num = "{0:016b}".format(int1)
    for c in bin_num:
        if c == '0':
            new = new+'1'
        if c == '1':
            new = new+'0'
    a = int(new,2)
    a= a+1
    final = '{:x}'.format(a)
    return final

def xor(bin1,bin2):
    res=""
    for i in range(16):
        if bin1[i]==bin2[i]:
            res+="0"
        else:
            res+="1"
    return res

def anding(bin1,bin2):
    res = ""
    for i in range(16):
        if bin1[i] == "1" and bin2[i]=="1":
            res += "1"
        else:
            res += "0"
    return res

def oring(bin1,bin2):
    res = ""
    for i in range(16):
        if bin1[i] == "0" and bin2[i]=="0":
            res += "0"
        else:
            res += "1"
    return res

def noting(bin):
    res=""
    for i in range(16):
        if bin[i]=="0":
            res+="1"
        elif bin[i]=="1":
            res+="0"
    return res


SF=False
ZF=False
CF=False




for word in f:
    pos = word.find('\n') #sondaki boşlukları siliyoz
    word = word[:pos]
    firsttwo = word[:2]  # opcode için
    operand = word[-4:]
    tobinary="{0:06b}".format(int(firsttwo, 16)) #binarye cevirdim
    o = tobinary[:-2]     #bastan son iki digite kadar
    o2= int(o,2)
    o3=hex(o2)
    opcode=o3[2:]
    addr= tobinary[-2:]        #son iki digit
    #print(opcode,addr,operand)

    if(opcode=='1'):  #Halt
        print("Halts the cpu")
    elif(opcode=='2'): #Load

        if(addr=='00'):  #LOAD 'A', LOAD 0004
           # print('girdim1')
            register['0001']=operand

        if(addr=='01'):  #LOAD C
           # print('girdim2')
            val=register[operand]
            register['0001']=val

        if(addr=='10'):  #LOAD [B]
            val=register[operand]
            register['0001']=getdatafrommemo(val)

        if(addr=='11'): #LOAD [1234]
            register['0001']=getdatafrommemo(operand)

    elif(opcode=='3'):  #Store

        if(addr=='01'): #STORE C
            val=register['0001']
            register[operand]=val
        if(addr=='10'):  #STORE [C]
            val=register['0001']
            a=register[operand]
            toint=int(a,16)
            memory[toint]=val[:2]
            memory[toint+1]=val[-2:]
        if(addr=='11'):  #STORE [1234]
            val=register['0001']
            toint=int(operand,16)
            memory[toint] = val[:2]
            memory[toint + 1] = val[-2:]

        elif opcode=='4': #Add

        if addr =='00': #ADD 0D05
            val=sum(register['0001'], operand)

        if addr=='01': #ADD C
            op2 = register[operand]
            val = sum(register['0001'], op2)

        if addr=='10': #ADD [B]
            ad=register[operand]
            data = memory[ad] + memory[ad+1]
            val=sum(register['0001'],data)

        if addr=='11': #ADD [2542]
            ad = operand
            data = memory[ad] + memory[ad+1]
            val = sum(register['0001'], data)
        register['0001'] = val

    elif opcode=='5': #Sub
       
        if addr =='00': #SUB 0D05
            val=sum(register['0001'], postoneg(operand))

        if addr=='01': #SUB C
            op2 = register[operand]
            val = sum(register['0001'], postoneg(op2))

        if addr=='10': #SUB [B]
            ad=register[operand]
            data = memory[ad] + memory[ad+1]
            val=sum(register['0001'],postoneg(data))

        if addr=='11': #SUB [2542]
            ad = operand
            data = memory[ad] + memory[ad+1]
            val = sum(register['0001'], postoneg(data))
        register['0001'] = val

    elif opcode=='6' : #Inc

        if addr =='00': #INC 0D05
            val=sum(operand, '0001')

        if addr=='01': #INC C
            op2 = register[operand]
            val = sum(op2, '0001')
            register[operand] = val

        if addr=='10': #INC [B]
            ad=register[operand]
            data = memory[ad] + memory[ad+1]
            val=sum(data, '0001')
            memory[ad] = val[:2]
            memory[ad+ 1] = val[-2:]

        if addr=='11': #INC [2542]
            ad = operand
            data = memory[ad] + memory[ad+1]
            val = sum(data, '0001')
            memory[ad] = val[:2]
            memory[ad + 1] = val[-2:]

    elif opcode == '7': #Dec
       
        if addr == '00':  #DEC 0D05
            val = sum(operand, 'ffff') #'ffff' = -1 (2's complement as hex)

        if addr == '01':  #DEC C
            op2 = register[operand]
            val = sum(op2, 'ffff')
            register[operand] = val

        if addr == '10':  #DEC [B]
            ad = register[operand]
            data = memory[ad] + memory[ad + 1]
            val = sum(data, 'ffff')
            memory[ad] = val[:2]
            memory[ad + 1] = val[-2:]

        if addr == '11':  #DEC [2542]
            ad = operand
            data = memory[ad] + memory[ad + 1]
            val = sum(data, 'ffff')
            memory[ad] = val[:2]
            memory[ad + 1] = val[-2:]

    elif(opcode=='8'): #XOR
        val=register['0001']
        if(addr=='00'): #XOR 0004
            opr=operand
        elif(addr=='01'): #X0R C
            opr=register[operand]
        elif(addr=='10'): #XOR [C]
            a=register[operand]
            opr=getdatafrommemo(a)
        elif(addr=='11'):  #XOR [1234]
            opr=getdatafrommemo(operand)
        tobin="{0:06b}".format(int(val, 16)).zfill(16) #binarye çevirdim 16 digitlik
        oprtobin="{0:06b}".format(int(opr, 16)).zfill(16) #binarye çevirdim 16 digitlik
        res=xor(tobin,oprtobin)
        if(res=="0000000000000000"):
            ZF=True
        else:
            ZF=False
        if(res[0]==1):
            SF=True
        else:
            SF=False
        register["0001"]=hex(int(res,2))[2:].zfill(4)

    elif (opcode=='9'): #AND
        val = register['0001']
        if (addr == '00'):  # AND 0004
            opr = operand
        elif (addr == '01'):  # AND C
            opr = register[operand]
        elif (addr == '10'):  # AND [C]
            a = register[operand]
            opr = getdatafrommemo(a)
        elif (addr == '11'):  # AND [1234]
            opr = getdatafrommemo(operand)
        tobin = "{0:06b}".format(int(val, 16)).zfill(16)  # binarye çevirdim 16 digitlik
        oprtobin = "{0:06b}".format(int(opr, 16)).zfill(16)  # binarye çevirdim 16 digitlik
        res = anding(tobin, oprtobin)
        if (res == "0000000000000000"):
            ZF = True
        else:
            ZF = False
        if (res[0] == 1):
            SF = True
        else:
            SF = False
        register["0001"] = hex(int(res, 2))[2:].zfill(4)


    elif (opcode == 'a'):  # OR
        val = register['0001']
        if (addr == '00'):  # OR 0004
            opr = operand
        elif (addr == '01'):  # 0R C
            opr = register[operand]
        elif (addr == '10'):  # OR [C]
            a = register[operand]
            opr = getdatafrommemo(a)
        elif (addr == '11'):  # OR [1234]
            opr = getdatafrommemo(operand)
        tobin = "{0:06b}".format(int(val, 16)).zfill(16)  # binarye çevirdim 16 digitlik
        oprtobin = "{0:06b}".format(int(opr, 16)).zfill(16)  # binarye çevirdim 16 digitlik
        res = oring(tobin, oprtobin)
        if (res == "0000000000000000"):
            ZF = True
        else:
            ZF = False
        if (res[0] == 1):
            SF = True
        else:
            SF = False
        register["0001"] = hex(int(res, 2))[2:].zfill(4)

    elif (opcode == 'b'):  # NOT
        if (addr == '00'):  # NOT 0004
            opr = operand
        elif (addr == '01'):  # NOT C
            opr = register[operand]
        elif (addr == '10'):  # NOT [C]
            a = register[operand]
            opr = getdatafrommemo(a)
        elif (addr == '11'):  # NOT [1234]
            opr = getdatafrommemo(operand)
        oprtobin = "{0:06b}".format(int(opr, 16)).zfill(16)  # binarye çevirdim 16 digitlik
        res = noting(oprtobin)
        if (res == "0000000000000000"):
            ZF = True
        else:
            ZF = False
        if (res[0] == 1):
            SF = True
        else:
            SF = False
        register["0001"] = hex(int(res, 2))[2:].zfill(4)

    elif(opcode== 'c'): #SHL A
        val=register[operand]
        tobin = int(val,16) #decimala çevirdim
        shiftleft=tobin<<1
        tobin=bin(shiftleft)[2:]  #flagleri ayarlamak için bin e çevirdim
        if len(tobin)==17:
            if(tobin[0]==1):
                CF=True
            else:
                CF=False
        removefirst=tobin[1:]  #ilk digit carry flagte olduğu için artık 1. digitten başlayacak 16 digitlik olması için
        if(removefirst=="0000000000000000"):
            ZF=True
        else:
            ZF=False
        if(removefirst[0]=="1"):
            SF=True
        else:
            SF=False
        register[operand] = hex(int(removefirst, 2))[2:].zfill(4)

    elif (opcode == 'd'):  # SHR A
        val = register[operand]
        tobin = int(val, 16)  # decimala çevirdim
        shiftleft = tobin >> 1
        tobin = bin(shiftleft)[2:]  # flagleri ayarlamak için bin e çevirdim
        SF = False  #ilk basamak hep 0
        if (tobin == "0000000000000000"):
            ZF = True
        else:
            ZF = False

        register[operand] = hex(int(tobin, 2))[2:].zfill(4)

    elif(opcode=="e"): #NOP
        print("no operation")



    #print(register.items())





