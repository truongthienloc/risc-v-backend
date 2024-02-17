def dec (temp) :
    s=0
    temp= temp.rjust(32,temp[0])
    temp=temp[::-1]
    
    for i in range (0,len(temp)) :
        if temp [i] =='1':
            s+= 2**i
    if temp[len(temp)-1] == '1':
        s= s-(1<<32)  
    return s

def convert_hextodec (string) :
        string =string[2:]
        string= string.upper()
        temp =""
        for i in range (len(string)) :
            if string[i] == '0' :
                temp+='0000'
            if string[i] == '1' :
                temp+='0001'
            if string[i] == '2' :
                temp+='0010'
            if string[i] == '3' :
                temp+='0011'
            if string[i] == '4' :
                temp+='0100'
            if string[i] == '5' :
                temp+='0101'
            if string[i] == '6' :
                temp+='0110'
            if string[i] == '7' :
                temp+='0111'
            if string[i] == '8' :
                temp+='1000'
            if string[i] == '9' :
                temp+='1001'
            if string[i] == 'A' :
                temp+='1010'
            if string[i] == 'B' :
                temp+='1011'
            if string[i] == 'C' :
                temp+='1100'
            if string[i] == 'D' :
                temp+='1101'
            if string[i] == 'E' :
                temp+='1110'
            if string[i] == 'F' :
                temp+='1111'
        s=0
        temp = temp [::-1]
        for i in range (len(temp)) :
            if temp [i] =='1':
                s+= 2**i
        return s

def convert_bin_to_hex (binary_code) :
        hexan=''
        if binary_code == '0000' :
            hexan = '0'
        if binary_code == '0001' :
            hexan = '1'
        if binary_code == '0010' :
            hexan = '2'
        if binary_code == '0011' :
            hexan = '3'
        if binary_code == '0100' :
            hexan = '4'
        if binary_code == '0101' :
            hexan = '5'
        if binary_code == '0110' :
            hexan = '6'
        if binary_code == '0111' :
            hexan = '7'
        if binary_code == '1000' :
            hexan = '8'
        if binary_code == '1001' :
            hexan = '9'
        if binary_code == '1010' :
            hexan = 'a'
        if binary_code == '1011' :
            hexan = 'b'
        if binary_code == '1100' :
            hexan = 'c'
        if binary_code == '1101' :
            hexan = 'd'
        if binary_code == '1110' :
            hexan = 'e'
        if binary_code == '1111' :
            hexan = 'f'
        return hexan

def handle_intruction_memory (instruction_memory):
    instruction_arr = {}
    for i in instruction_memory :
        instructions = ''
        instructions += convert_bin_to_hex(instruction_memory[i][0:4]) 
        instructions += convert_bin_to_hex(instruction_memory[i][4:8]) 
        instructions += convert_bin_to_hex(instruction_memory[i][8:12]) 
        instructions += convert_bin_to_hex(instruction_memory[i][12:16]) 
        instructions += convert_bin_to_hex(instruction_memory[i][16:20])
        instructions += convert_bin_to_hex(instruction_memory[i][20:24])
        instructions += convert_bin_to_hex(instruction_memory[i][24:28])
        instructions += convert_bin_to_hex(instruction_memory[i][28:32])
        instruction_arr ['0x'+(hex (dec('0'+i))[2:]).rjust(8,'0')] = '0x' + instructions 

    return instruction_arr
def handle_register (register):
    count = 0
    re = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1', 't2', 's0/fp', 's1', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 't3', 't4', 't5', 't6','0' ]
    mdic = {}
    for i in register :
        if count <10 :
            if dec(str(register[i])) <0 :
                mdic['x'+ str(count) + (' ('+re[count]+')').ljust(10, ' ')] = '0x'+hex ((1<<32) +dec(str(register[i])))[2:].rjust(8, '0')
            else :
                mdic['x'+ str(count) + (' ('+re[count]+')').ljust(10, ' ')] = '0x'+hex(dec(str(register[i])))[2:].rjust(8, '0')
            #mdic['x'+ str(count) + (' ('+re[count]+')').ljust(10, ' ')+ ':'] += '  '
            #mdic['x'+ str(count) + (' ('+re[count]+')').ljust(10, ' ')+ ':'] += str (dec(str(register[i])))
        else : 
            if dec(str(register[i])) <0 :
                mdic['x'+ str(count) + (' ('+re[count]+')').ljust(9, ' ')] = '0x'+hex ((1<<32) +dec(str(register[i])))[2:].rjust(8, '0')
            else :
                mdic['x'+ str(count) + (' ('+re[count]+')').ljust(9, ' ')] = '0x'+hex(dec(str(register[i])))[2:].rjust(8, '0')
            #mdic['x'+ str(count) + (' ('+re[count]+')').ljust(9, ' ')+ ':'] += '  '
            #mdic['x'+ str(count) + (' ('+re[count]+')').ljust(9, ' ')+ ':'] += str (dec(str(register[i])))
        count+=1
    return mdic
def handle_data_memory (Data_memory):

    DATA_list = {}
    for i in Data_memory :
        DATA_list[convert_hextodec('0x'+ hex(dec('0'+i))[2:])] = i
    DATA_list = sorted(DATA_list.keys())

    memdic = {}
    for i in range (len(DATA_list)) :
    
        DATA_list[i] = bin(DATA_list[i])[2:].rjust(32, '0')
        if dec(Data_memory[DATA_list[i]]) < 0 :
            memdic ['0x'+ hex(dec('0'+ DATA_list[i]))[2:].rjust(8, '0')+':'] = ('0x'+ hex ((1<<32) + dec(Data_memory[DATA_list[i]]))[2:].rjust(8, '0')) + ' ' + str(dec(Data_memory[DATA_list[i]]))
        else :
            memdic ['0x'+ hex(dec('0'+ DATA_list[i]))[2:].rjust(8, '0')+':'] = ('0x'+ hex (dec(Data_memory[DATA_list[i]]))[2:].rjust(8, '0')) + ' ' + str(dec(Data_memory[DATA_list[i]]))
    Data_memory = []
    for i in memdic :
        Data_memory.append(i+'\t'+memdic[i]) 
    return Data_memory

def Rd (intruction):
    opcode = intruction[25:]
    if opcode  == '0110011' or opcode  == '0010011' or opcode  == '0000011' or opcode  == '0110111' or opcode  == '0010111' or opcode  == '1101111' or opcode  == '1100111':
        rd = intruction[20:25] 
    else: rd= '-1'
    return rd

def Rs1 (intruction):
    opcode = intruction[25:]
    if opcode  == '0110011' or opcode  == '0010011' or opcode  == '0000011' or opcode  == '1100111' or opcode == '0100011' or opcode == '1100011':
        rs1 = intruction[12:17] 
    else: rs1= '-2'
    return rs1

def Rs2 (intruction):
    opcode = intruction[25:]
    if opcode  == '0110011' or opcode == '0100011' or opcode == '1100011':
        rs2 = intruction[7:12] 
    else: rs2= '-3'
    return rs2