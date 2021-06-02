
import sys
f = open(sys.argv[1], 'r')
outputf=sys.argv[1][:-3]+"txt"
output1=open(outputf,'w')

register = {'0000': ' ', '0001': ' ', '0002': ' ', '0003': ' ', '0004': ' ', '0005': ' ', '0006': 65534}
asci = {'0041': 45, '0042': 47, '0043': 49, '0044': 51, '0045': 53}
memory = ["0"] * 65536


i=0
lenofinst=0
for instr in f: #48006c
    memory[i]=instr[:2]
    memory[i+1]=instr[2:4]
    memory[i+2]=instr[4:6]
    lenofinst=lenofinst+3
    i=i+3

f.close()

SF = False
ZF = False
CF = False

def getdatafrommemo(address):  #Finds the data in the given address
    toint = int(address, 16)   #To do this converts the hex address to integer and finds data in the corresponding index of memory
    val1 = memory[toint]
    val2 = memory[toint + 1]   #Since datas are 16 bit they occupy 2 byte in memory the one in address and the one next to it.
    data = val1 + val2         #We concatanete them and return data
    return data


def putdatatomemo(address, data):   #Puts data to given address

    global error                    #In the case one tries to put data to an invalid address
    toint = int(address, 16)
    if toint+1 > 65535:
        print("INVALID MEMORY ADDRESS")
        error=True
        return
    memory[toint] = data[:2]        #Here it puts data to corresponding index and to the next.
    memory[toint + 1] = data[-2:]


def sum(operand1, operand2, operand3): #Performs addition and subtraction operations
    global CF, SF, ZF
    SF = False
    sum=0                              #This will be determined later in function
    formed=""
    if(operand3 == ""):                #This means the operation is addition
        int1 = int(operand1, 16)
        int2 = int(operand2, 16)
        sum = int1 + int2
        formed = bin(sum)[2:]

    else:                              #This means we are performing subtraction and we have three operand A + 1 + not(B)
        oprtobin = "{0:06b}".format(int(operand3, 16)).zfill(16)
        notted = noting(oprtobin)
        int3 = int(notted, 2)           #This is the subtrahend
        int1 = int(operand1, 16)        #This is the minuend
        int2 = int(operand2, 16)        #This is just 1
        sum = int1 + int2 + int3
        formed = bin(sum)[2:]           #This is the binary form of the result

    if sum == 65536 or sum == 0:        #If sum is 0
        ZF = True
        if len(formed) > 16:            #It checks if it is 10000000000000000 or not
            SF = False
            CF = True
            int_result = sum - pow(2, 16)     #This is 0
            final = '{0:04x}'.format(int_result)
            return final
        return format(sum, '04x')

    if len(formed) > 16:                #If not 0 and there is an overflow
        if formed[1] == '1':            #Checks sign flag
            SF = True
        CF = True                       #Carry will be true since overflow is happening
        int_result = sum - pow(2, 16)   #Goes back to 16 bits
        final = '{0:04x}'.format(int_result)
        return final

    if len(formed) == 16 and formed[0] == '1':  #Checks sign flag
        SF = True

    CF = False                          #If not true makes flags false
    ZF = False
    final = format(sum, '04x')
    return final


def xor(bin1, bin2):
    res = ""
    for i in range(16):
        if bin1[i] == bin2[i]:
            res += "0"
        else:
            res += "1"
    return res


def anding(bin1, bin2):
    res = ""
    for i in range(16):
        if bin1[i] == "1" and bin2[i] == "1":
            res += "1"
        else:
            res += "0"
    return res


def oring(bin1, bin2):
    res = ""
    for i in range(16):
        if bin1[i] == "0" and bin2[i] == "0":
            res += "0"
        else:
            res += "1"
    return res


def noting(bin):
    res = ""
    for i in range(16):
        if bin[i] == "0":
            res += "1"
        elif bin[i] == "1":
            res += "0"
    return res


i=0

error= False


while(i < lenofinst and error is False):  #48006c

    register["0000"] = i
    word1=memory[i]
    word2=memory[i+1]
    word3=memory[i+2]
    operand=word2+word3
    tobinary = "{0:06b}".format(int(word1, 16))  # binarye cevirdim
    o = tobinary[:-2]  # bastan son iki digite kadar
    o2 = int(o, 2)
    o3 = hex(o2)
    opcode = o3[2:]
    addr = tobinary[-2:]  # son iki digit

    if (opcode == '1'):  # Halts the cpu
        break
        
    elif (opcode == '2'):  # Loads data to register A

        if (addr == '00'):  # LOAD 'A', LOAD 0004  
            register['0001'] = operand      #puts directly since it is an immediate data

        if (addr == '01'):  # LOAD C
            val = register[operand]         #puts the data in given register
            register['0001'] = val

        if (addr == '10'):  # LOAD [B]
            val = register[operand]                    #gets the address in given register
            register['0001'] = getdatafrommemo(val)    #then puts data in the memory address to register A

        if (addr == '11'):  # LOAD [1234]
            register['0001'] = getdatafrommemo(operand)     #puts data in the given memory address to register A

    elif (opcode == '3'):  # Stores the content of register A 

        if (addr == '01'):  # STORE C       
            val = register['0001']                  
            register[operand] = val
            
        if (addr == '10'):  # STORE [C]
            val = register['0001']
            a = register[operand]
            putdatatomemo(a,val)
            
        if (addr == '11'):  # STORE [1234]
            val = register['0001']
            putdatatomemo(operand, val)

    elif opcode == '4':  # Add

        if addr == '00':  # ADD 0D05
            val = sum(register['0001'], operand, "")

        if addr == '01':  # ADD C
            op2 = register[operand]
            val = sum(register['0001'], op2, "")

        if addr == '10':  # ADD [B]
            ad = register[operand]
            data = getdatafrommemo(ad)
            val = sum(register['0001'], data, "")

        if addr == '11':  # ADD [2542]
            ad = operand
            data = getdatafrommemo(ad)
            val = sum(register['0001'], data, "")
        register['0001'] = val

    elif opcode == '5':  # Sub

        if addr == '00':  # SUB 0D05
            val = sum(register['0001'], "0001" , operand)

        if addr == '01':  # SUB C
            op2 = register[operand]
            val = sum(register['0001'], "0001" , op2)

        if addr == '10':  # SUB [B]
            ad = register[operand]
            data = getdatafrommemo(ad)
            val = sum(register['0001'], "0001", data)

        if addr == '11':  # SUB [2542]
            ad = operand
            data = getdatafrommemo(ad)
            val = sum(register['0001'], "0001", data)

        register['0001'] = val

    elif opcode == '6':  # Inc

        if addr == '00':  # INC 0D05
            val = sum(operand, '0001', "")

        if addr == '01':  # INC C
            op2 = register[operand]
            val = sum(op2, '0001', "")
            register[operand] = val

        if addr == '10':  # INC [B]
            ad = register[operand]
            data = getdatafrommemo(ad)
            val = sum(data, '0001', "")
            putdatatomemo(ad, val)

        if addr == '11':  # INC [2542]
            ad = operand
            data = getdatafrommemo(ad)
            val = sum(data, '0001', "")
            putdatatomemo(ad, val)

    elif opcode == '7':  # Dec

        if addr == '00':  # DEC 0D05
            val = sum(operand, '0001', '0001')

        if addr == '01':  # DEC C
            op2 = register[operand]
            val = sum(op2, '0001', '0001')
            register[operand] = val

        if addr == '10':  # DEC [B]
            ad = register[operand]
            data = memory[ad] + memory[ad + 1]
            val = sum(data, '0001', '0001')
            putdatatomemo(ad, val)

        if addr == '11':  # DEC [2542]
            ad = operand
            data = memory[ad] + memory[ad + 1]
            val = sum(data, '0001', '0001')
            putdatatomemo(ad, val)

    elif (opcode == '8'):  # XOR
        val = register['0001']
        if (addr == '00'):  # XOR 0004
            opr = operand
        elif (addr == '01'):  # X0R C
            opr = register[operand]
        elif (addr == '10'):  # XOR [C]
            a = register[operand]
            opr = getdatafrommemo(a)
        elif (addr == '11'):  # XOR [1234]
            opr = getdatafrommemo(operand)
        tobin = "{0:06b}".format(int(val, 16)).zfill(16)  # binarye çevirdim 16 digitlik
        oprtobin = "{0:06b}".format(int(opr, 16)).zfill(16)  # binarye çevirdim 16 digitlik
        res = xor(tobin, oprtobin)
        if (res == "0000000000000000"):
            ZF = True
        else:
            ZF = False
        if (res[0] == 1):
            SF = True
        else:
            SF = False
        register["0001"] = hex(int(res, 2))[2:].zfill(4)

    elif (opcode == '9'):  # AND
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

    elif (opcode == 'c'):  # SHL A
        val = register[operand]
        tobin = int(val, 16)  # decimala çevirdim
        shiftleft = tobin << 1
        tobin = bin(shiftleft)[2:]  # flagleri ayarlamak için bin e çevirdim
        if len(tobin) == 17:
            if (tobin[0] == 1):
                CF = True
            else:
                CF = False
            tobin = tobin[1:]  # ilk digit carry flagte olduğu için artık 1. digitten başlayacak 16 digitlik olması için
            if (tobin == "0000000000000000"):
                ZF = True
            else:
                ZF = False
        if (tobin[0] == "1"):
            SF = True
        else:
            SF = False
        register[operand] = hex(int(tobin, 2))[2:].zfill(4)

    elif (opcode == 'd'):  # SHR A
        val = register[operand]
        tobin = int(val, 16)  # decimala çevirdim
        shiftleft = tobin >> 1
        tobin = bin(shiftleft)[2:]  # flagleri ayarlamak için bin e çevirdim
        SF = False  # ilk basamak hep 0
        if (tobin == "0000000000000000"):
            ZF = True
        else:
            ZF = False

        register[operand] = hex(int(tobin, 2))[2:].zfill(4)

    elif (opcode == "e"):  # NOP
        i=i+3
        continue

    elif(opcode=="f"):  #push
        val=register[operand]
        #print(val)
        a=hex(register['0006'])[2:]
        putdatatomemo(a,val)
        register['0006']=register['0006']-2


    elif(opcode=="10"):  #pop
        if register['0006'] ==65534:
            print("STACK IS EMPTY")
            error=True
            break
        register['0006'] = register['0006'] + 2
        val=getdatafrommemo(hex(register['0006']))
        register[operand]=val



    elif(opcode=="11"): #CMP A-opr
        if (addr == '00'):  # NOT 0004
            opr = operand
        elif (addr == '01'):  # NOT C
            opr = register[operand]
        elif (addr == '10'):  # NOT [C]
            a = register[operand]
            opr = getdatafrommemo(a)
        elif (addr == '11'):  # NOT [1234]
            opr = getdatafrommemo(operand)

        sum(register["0001"], "0001", opr)



    elif(opcode =="12"): #JMP unconditional jump
        jumpto=int(operand,16)
        i=jumpto
        register["0000"]=int(operand, 16)
        continue

    elif(opcode=="13"): #JZ JE
        if ZF is True:
            jumpto=int(operand,16)
            i=jumpto
            register["0000"] = int(operand, 16)
            continue

    elif(opcode=="14"):  #JNZ JNE -> jump the address if ZF is false
        #print(ZF)
        if ZF is False:
            jumpto=int(operand,16)
            i=jumpto
            register["0000"] = int(operand, 16)
            continue
            #print(i)
    elif(opcode=="15"): #JC
        if CF is True:
            jumpto = int(operand, 16) 
            i = jumpto
            register["0000"] = int(operand, 16)
            continue
    elif(opcode=="16"): #JNC
        if CF is False:
            jumpto = int(operand, 16) 
            i = jumpto
            register["0000"] = int(operand, 16)
            continue
    elif(opcode=="17"): #JA jump if above
        if SF is False:
            jumpto = int(operand, 16) 
            i = jumpto
            register["0000"] = int(operand, 16)
            continue
    elif(opcode=="18"): #JAE jump if above or equal
        if SF is False or ZF is True:
            jumpto = int(operand, 16) 
            i = jumpto
            register["0000"] = int(operand, 16)
            continue
    elif (opcode == "19"):  # JB if below
        if SF is True:
            jumpto = int(operand, 16) 
            i = jumpto
            register["0000"] = int(operand, 16)
            continue
    elif (opcode == "1a"):  # JBE if below or equal
        if SF is True or ZF is True:
            jumpto = int(operand, 16) 
            i = jumpto
            register["0000"] = int(operand, 16)
            continue

    elif(opcode=="1b"): #READ
        user = input()
        toasc = ord(user)
        tohex = hex(toasc)[2:].zfill(4)
        if(addr=='01'):
            register[operand]=tohex
        elif(addr=='10'):
            ad = register[operand]
            putdatatomemo(ad,tohex)
        elif(addr=='11'):
            putdatatomemo(operand,tohex)

    elif(opcode=="1c"): #Print
        if (addr == '00'):  # Print 0004
            opr = operand
        elif (addr == '01'):  # Print C
            opr = register[operand]
        elif (addr == '10'):  # Print [C]
            a = register[operand]
            opr = getdatafrommemo(a)
        elif (addr == '11'):  # Print [1234]
            opr = getdatafrommemo(operand)
        todec=int(opr,16)
        print(chr(todec))
        output1.write(chr(todec)+"\n")

    i=i+3
    #print(ZF,"B:",register['0002'],"A:",register['0001'])
    #print(register.items())
    #print(memory[int("0104",16) + 1])
    #for l in range(1,10):
     #   print(memory[-l])
    #print(postoneg("0003"))


