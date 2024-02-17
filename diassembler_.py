#from app import app
from assembler import assembler
#@app.route('/diassembler')

R_type = {
    '001' : 'sll',      '011' : 'sltu',    '110':'or', 
    '010' : 'slt',      '100' : 'xor',     '111' : 'and', 
}
LOAD_type = { # opcode = 0000011
    '000' : 'lb',   '001': 'lh',  '010' : 'lw',   '011' : 'ld',
    '100' : 'lbu',  '101': 'lhu', '110': 'lwu'
}
I_type = { # opcode = 0010011
    '000' : 'addi',   '001' : 'slli',   '010' : 'slti',  '011' : 'sltiu',
    '100' : 'xori',   '110' : 'ori',    '111' : 'andi'
}
STORE_type = { # opcode = 0100011
    '000' : 'sb',   '001' : 'sh',   '010' : 'sw',   '011' : 'sd'
}
SBRANCH_type ={
    '000' : 'beq',  '001' : 'bne',  '100' : 'blt',  '101' : 'bge',
    '110' : 'bltu', '111' : 'bgeu'
}

def convert_bintodec (temp) :
    s=0
    temp= temp.rjust(32,temp[0])
    temp=temp[::-1]
    
    for i in range (0,len(temp)) :
        if temp [i] =='1':
            s+= 2**i
    if temp[len(temp)-1] == '1':
        s= s-(1<<32)  
    return str(s)

def convert_hextobin (string) :
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
    return temp 

def instructions_handler (string):
    string = string.replace(' ','')
    bcode = ''
    if string.startswith('0x') :
        bcode = convert_hextobin(string)
        bcode = bcode.rjust(32, '0')
    else :
        bcode = string.rjust(32, '0')
    return bcode[:32]

def Rtype (bcode) :
    instruction = ''
    if bcode[17:20] == '000' :
        if bcode[:7] == '0000000' :
            instruction += 'add'
        if bcode[:7] == '0100000' :
            instruction += 'sub'
    elif bcode[17:20] == '101' :
        if bcode[:7] == '0000000' :
            instruction += 'srl'
        if bcode[:7] == '0100000' :
            instruction += 'sra'
    else: 
        instruction += R_type[bcode[17:20]] 
    instruction = instruction.ljust(7, ' ')
    instruction += 'x'+convert_bintodec('0'+bcode[20:25]).ljust(3, ' ') + ', ' #rd
    instruction += 'x'+convert_bintodec('0'+bcode[12:17]).ljust(3, ' ') + ', ' #rs1
    instruction += 'x'+convert_bintodec('0'+bcode[7:12]) #rs2
    return  instruction

def Itype (bcode) :
    instruction = ''
    if bcode [25:] == '0000011' :
        instruction += LOAD_type[bcode[17:20]]
    if bcode [25:] == '0010011' :
        if bcode[17:20] == '101' and bcode[:7] == '0000000' :
            instruction += 'srli'
        elif bcode[17:20] == '101' and bcode[:7] == '0100000' :
            instruction += 'srai' 
        else :
            instruction += I_type[bcode[17:20]]
    if bcode[25:] == '1100111' : instruction += 'jalr'
    
    instruction = instruction.ljust(7, ' ')
    instruction += 'x'+convert_bintodec('0'+bcode[20:25]).ljust(3, ' ') + ', ' #rd
    if bcode [25:] == '0000011' :
        instruction += convert_bintodec(bcode[:4]+bcode[4:8]+bcode[8:12]) + '(' #immediate
        instruction += 'x'+ convert_bintodec('0'+bcode[12:17]) + ') ' #rs1
    else :
        instruction += 'x'+convert_bintodec('0'+ bcode[12:17]).ljust(3, ' ') + ', ' #rs1
        if bcode[17:20] == '101' and bcode[:7] == '0100000' : #srai has funct7
            instruction += convert_bintodec(bcode[7].rjust(4, bcode[7])+bcode[8:12])
        else:
            instruction += convert_bintodec(bcode[:4]+bcode[4:8]+bcode[8:12]) #immediate
    return instruction

def Stype (bcode) :    #sw rd, imm(rs1)
    instruction = ''
    instruction+=  STORE_type[bcode[17:20]].ljust(7, ' ')
    instruction+= 'x' +convert_bintodec('0'+bcode[7:12]).ljust(3, ' ') + ', ' #rs2
    imm = bcode[0:7]+bcode[20:25]
    instruction+= convert_bintodec ((imm[:4])+(imm[4:8])+(imm[8:12]))+'('
    instruction+= 'x' +convert_bintodec('0'+bcode[12:17]) +')' #rs1
    return instruction

def SBtype(bcode) : #beq x1, x2, imm
    instruction = ''
    instruction+= SBRANCH_type[bcode[17:20]].ljust(7, ' ')
    instruction+= 'x'+ convert_bintodec('0'+bcode[12:17]).ljust(3, ' ') + ', '#rs1
    instruction+= 'x'+ convert_bintodec('0'+bcode[7:12]).ljust(3, ' ') + ', '# rs2
    imm = bcode[0] + bcode[24] + bcode[1:7] + bcode[20:24] + '0'
    instruction+= convert_bintodec(imm[0].rjust(4, imm[0]) + (imm[1:5]) + (imm[5:9])+ (imm[9:]))
    return instruction

def Utype(bcode) : #lui x31, 4
    instruction = ''
    if bcode[25:] == '0010111' :
        instruction += 'auipc'.ljust(7, ' ')
    else:
        instruction += 'lui'.ljust(7, ' ')
    instruction += 'x' + convert_bintodec('0'+bcode[20:25]).ljust(3, ' ')  + ', '
    instruction += convert_bintodec(bcode[0:4] + (bcode[4:8]) +(bcode[8:12]) + (bcode[12:16]) +(bcode[16:20]))
    return instruction

def UJtype(bcode) :
    instuction = ''
    instuction += 'jal'.ljust(7, ' ')
    instuction += 'x' + convert_bintodec('0'+bcode[20:25]).ljust(3, ' ') + ', '
    imm = bcode[0]+bcode[12:20]+bcode[11]+bcode[1:10] + bcode[10] +'0' 
    instuction+= convert_bintodec(imm[0].rjust(4, imm[0]) + (imm[1:5]) + (imm[5:9]) + (imm[9:13]) + (imm[13:17]) + (imm[17:]))
    return instuction
    
def tmp_diassembler(instruction):
    if instruction[25:] == '0110011' : #R-TYPE
        result = Rtype(instruction)
    if instruction[25:] == '0000011' or instruction[25:]=='0010011' or instruction[25:]=='1100111': #I-TYPE
        result = Itype(instruction)
    if instruction[25:] == '0100011' : #S-TYPE
        result = Stype(instruction)
    if instruction[25:] == '1100011' : #SB-TYPE
        result = SBtype(instruction)
    if instruction[25:] == '0110111' or instruction[25:] == '0010111' : #U-TYPE
        result = Utype(instruction)
    if instruction[25:] == '1101111' :
        result = UJtype(instruction)
    return result

#print (tmp_diassembler('00000100011000000000000010010011'))
'''
fo = open('Diassembler.txt', 'w')
for i in diassembler() :
    fo.write(i+'\n')
fo.close()'''


