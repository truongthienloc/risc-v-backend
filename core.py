from app import app, request, json
from assembler import assembler

#INSTRUCTION MEMORY
instruction_memory={}

#REGISTER 
register={
'00000': '00000000000000000000000000000000',
'00001': '00000000000000000000000000000000',
'00010': '00000000000000000000000000000000',
'00011': '00000000000000000000000000000000',
'00100': '00000000000000000000000000000000',
'00101': '00000000000000000000000000000000',
'00110': '00000000000000000000000000000000',
'00111': '00000000000000000000000000000000',
'01000': '00000000000000000000000000000000',
'01001': '00000000000000000000000000000000',
'01010': '00000000000000000000000000000000',
'01011': '00000000000000000000000000000000',
'01100': '00000000000000000000000000000000',
'01101': '00000000000000000000000000000000',
'01110': '00000000000000000000000000000000',
'01111': '00000000000000000000000000000000',
'10000': '00000000000000000000000000000000',
'10001': '00000000000000000000000000000000',
'10010': '00000000000000000000000000000000',
'10011': '00000000000000000000000000000000',
'10100': '00000000000000000000000000000000',
'10101': '00000000000000000000000000000000',
'10110': '00000000000000000000000000000000',
'10111': '00000000000000000000000000000000',
'11000': '00000000000000000000000000000000',
'11001': '00000000000000000000000000000000',
'11010': '00000000000000000000000000000000',
'11011': '00000000000000000000000000000000',
'11100': '00000000000000000000000000000000',
'11101': '00000000000000000000000000000000',
'11110': '00000000000000000000000000000000',
'11111': '00000000000000000000000000000000',
'pc'   : '00000000000000000000000000000000'
}
read_register_1=''
read_register_2=''
write_register=''
write_data_r=0
read_data_1=0
read_data_2=0

#DATA_MEMORY
Data_memory ={}
write_data_d=''
read_data=''

#CONTROL
jalr = 0
branch ='000'
jal = 0
slt = 0 
mem_read = '000' 
mem_to_reg = 0
ALU_op = '00'
mem_write = '000'
ALU_src = 0
reg_write = 0
aui_or_lui = 0
unsigned = 0
wb = 0

#ALU
operation=''
zero=0
sign_bit=0
ALU_result=0

#BRANCH
pc_src_1=0
pc_src_2=0
jump=0

#GRARPHIC
color_dir = {
    '0': 'FF8000', '1' : 'FF0000', '2' : 'FFFF00', '3' : '', '4' : '00CC00', '5' : 'FF66FF', '6' : '', '7' : '00CC00', '8' : '',
    '9' : '', '10' : '', '11' : '', '12' : '', '13' : 'B85C00', '14' : '7F00FF', '15': '', '16' : '', '17' :'',
    'jal':'', 'jalr':'', 'branch': '', 'AuiOrLui': '', 'wb':'', 'slt':'', 'MemtoRegister':'', 'jump':'',
    'ALUOp': '', 'Unsigned':'', 'MemRead':'', 'MemWrite':'', 'ALUSrc':'', 'RegWrite': '', 'zero' :'', 'sign-bit':''
}
#ALL TIME DATA
all_time_register = []
all_time_data_memory = []
all_time_grapic = []
# s = '.text\n\n\n\n\n\n\n\n\nMain:\n\n\t\tauipc    x8 , 6\n\n\t\tauipc    x18 , 1\n\n\t\tauipc    x25 , 8\n\n\t\tauipc    x13 , 1\n\n\t\tlui      x9 , 9\n\n\t\tlui      x1 , 2\n\n\t\tlui      x2 , 9\n\n\t\tlui      x31 , 4\n\n\t\tsw       x14 , 24 (x8) \n\n\t\tsw       x29 , 28 (x18) \n\n\t\tsw       x20 , 32 (x25) \n\n\t\tsw       x30 , 36 (x13) \n\n\t\tsw       x10 , 40 (x9) \n\n\t\tsw       x27 , 44 (x1) \n\n\t\tsw       x23 , 48 (x2) \n\n\t\tsw       x15 , 52 (x31) \n\n\t\tlw       x19 , 52 (x31) \n\n\t\tlw       x24 , 48 (x2) \n\n\t\tlw       x7 , 44 (x1) \n\n\t\tlw       x6 , 40 (x9) \n\n\t\tlw       x4 , 36 (x13) \n\n\t\tlw       x12 , 32 (x25) \n\n\t\tlw       x21 , 28 (x18) \n\n\t\tlw       x16 , 24 (x8) \n\n\t\tbne      x16 , x14 , Fail\n\n\t\tbne      x21 , x29 , Fail\n\n\t\tbne      x12 , x20 , Fail\n\n\t\tbne      x4 , x30 , Fail\n\n\t\tbne      x6 , x10 , Fail\n\n\t\tbne      x7 , x27 , Fail\n\n\t\tbne      x24 , x23 , Fail\n\n\t\tbne      x19 , x15 , Fail\n\nPass: \n\n\t\taddi    x1 , x0 , 084 \n\n\t\tjal     x0 , End \n\nFail: \n\n\t\taddi    x1 , x0 , 070 \n\nEnd: \n\n'

@app.route('/core', methods=['POST'])
def core ():
    s = json.loads(request.data)['code']
    #print(s)
    global instruction_memory, register, Data_memory, read_data, all_time_register, all_time_data_memory
    pc=0
    binary_code = []
    binary_code= assembler(s)
    instruction_memory = {}
    for i in binary_code :
        instruction_memory[bin(pc)[2:]] = i
        pc+=4
    pc=0
    #ALL TIME DATA
    all_time_register = []
    all_time_data_memory = []
    all_time_grapic = []
    register={
    '00000': '00000000000000000000000000000000',
    '00001': '00000000000000000000000000000000',
    '00010': '00000000000000000000000000000000',
    '00011': '00000000000000000000000000000000',
    '00100': '00000000000000000000000000000000',
    '00101': '00000000000000000000000000000000',
    '00110': '00000000000000000000000000000000',
    '00111': '00000000000000000000000000000000',
    '01000': '00000000000000000000000000000000',
    '01001': '00000000000000000000000000000000',
    '01010': '00000000000000000000000000000000',
    '01011': '00000000000000000000000000000000',
    '01100': '00000000000000000000000000000000',
    '01101': '00000000000000000000000000000000',
    '01110': '00000000000000000000000000000000',
    '01111': '00000000000000000000000000000000',
    '10000': '00000000000000000000000000000000',
    '10001': '00000000000000000000000000000000',
    '10010': '00000000000000000000000000000000',
    '10011': '00000000000000000000000000000000',
    '10100': '00000000000000000000000000000000',
    '10101': '00000000000000000000000000000000',
    '10110': '00000000000000000000000000000000',
    '10111': '00000000000000000000000000000000',
    '11000': '00000000000000000000000000000000',
    '11001': '00000000000000000000000000000000',
    '11010': '00000000000000000000000000000000',
    '11011': '00000000000000000000000000000000',
    '11100': '00000000000000000000000000000000',
    '11101': '00000000000000000000000000000000',
    '11110': '00000000000000000000000000000000',
    '11111': '00000000000000000000000000000000'
    }

    Data_memory ={}

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
    
    def data_memory (address, mem_read, mem_write, write_data) :
        global read_data, Data_memory
        if mem_read[0] == '1' :
            if address not in Data_memory :
                Data_memory[address] = '00000000000000000000000000000000'
            if mem_read == '100' :
                read_data = Data_memory[address][-8:]
            if mem_read == '101' :
                read_data = Data_memory[address][-16:]
            if mem_read == '110' :
                read_data = Data_memory[address]
        if mem_write[0] == '1':
            if address not in Data_memory :
                Data_memory[address] = '00000000000000000000000000000000'
            if mem_write == '100' :
                string = Data_memory[address][8:] + write_data [-8:]
                Data_memory[address] = string
            if mem_write == '101' :
                string = Data_memory[address][16:] +  write_data [-16:] 
                Data_memory[address] = string
            if mem_write == '110' :
                Data_memory[address] = write_data
        
    def ALU (operand_1 ,operand_2 ,operation) :
        global zero, sign_bit, ALU_result
        if operation == 'z' : 
            ALU_result = '0'
            return
       
        if operation[0] == '1' : #unsigned 
            operand_1 =dec ('0'+operand_1)
            operand_2 =dec ('0'+operand_2)
        else : #signed
            operand_1 =dec (operand_1)
            operand_2 =dec (operand_2)
        #print (operand_1, operand_2)

        if operand_1 <0 : sign_operand_1 =1
        else: sign_operand_1 =0

        if operation[1:] == '000': #and
            ALU_result = operand_1 & operand_2
        if operation[1:] == '001': #or
            ALU_result = operand_1 | operand_2
        if operation[1:] == '010':  #Xor
            ALU_result = operand_1 ^ operand_2
        if operation[1:] == '011': #add
            ALU_result = operand_1 + operand_2
        if operation[1:] == '100':  #sub
            ALU_result = operand_1 - operand_2
        
        operand_2 = operand_2 & 31
        if operation[1:] == '101': #Sll
            ALU_result = operand_1 << operand_2
        if operation[1:] == '110' :  #Slr
            ALU_result = operand_1 >> operand_2
        if operation[1:] == '111': #Sra
            if sign_operand_1 :
                ALU_result = dec (bin(operand_1 >> operand_2)[2:].rjust(32,'1'))
            else:
                ALU_result = dec (bin(operand_1 >> operand_2)[2:].rjust(32,'0'))
        if ALU_result == 0 : zero = 1
        if ALU_result < 0  :
            sign_bit=1
            ALU_result = (1<<32) + ALU_result
        ALU_result = bin (ALU_result)

        if ALU_result[0] == '-' : ALU_result= ALU_result[3:].rjust(32,'1')
        if ALU_result[0] == '0' : ALU_result= ALU_result[2:].rjust(32,'0')

    def mux (input1, input2, sel) :
        if sel ==0 :
            return input1
        if sel ==1 :
            return input2

    def data_gen (read_data, unsigned) :
        if unsigned == 0 and read_data != '' :
            read_data = read_data.rjust(32, read_data[0])
        if unsigned == 1 and read_data != '' :
            read_data = read_data.rjust(32, '0')
        return read_data
    
    def imm_gen (instruction) :
        imm=''
        if instruction [-7:] == '0110011' : #R-type
            return '0'
        if instruction [-7:] == '0010011' or instruction [-7:] == '0000011' or instruction[-7:] == '1100111' :  #I-TYPE
            imm= instruction[0:12]
            #if instruction[-15:-12] == '011' : return imm.rjust(32, '0')
        
        if instruction[-7:] =='0100011' :#S-TYPE
            imm= instruction[0:7]+instruction[20:25] 
    
        if instruction[-7:] =='1100011' : #B-TYPE
            imm= instruction[0]+instruction[24]+instruction[1:7]+ instruction[20:24]
    
        if instruction[-7:] =='1101111' :#J-TYPE
            imm= instruction[0] + instruction[12:20] +instruction[11] + instruction[1:11]
        
        if instruction[-7:] == '0110111' or instruction[-7:] == '0010111': #U-TYPE
            imm= instruction[:20]
        
        if instruction[-7:] == '0110111' or instruction[:7] == '0010111': #LUI AUIPC
            return imm.rjust(32, '0')
        else:
            return imm.rjust(32, imm[0])

    def control (opcode, funct3) :
        global jalr, branch, jal, slt, mem_read, mem_to_reg, ALU_op, mem_write, ALU_src, reg_write, aui_or_lui, unsigned, wb
        
        if opcode == '0110011'  : #R-type
            jal =0; jalr = 0;   branch = '000';     aui_or_lui = 0;     wb = 0
            mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
            ALU_src = 0;        reg_write = 1;      ALU_op = '10' 
            if funct3 == '010' or funct3 =='011': slt = 1  
            else: slt =0
        
        if opcode == '1100011'  : #BEQ
            jal =0;         jalr = 0;       aui_or_lui = 0;     wb = 0      
            mem_to_reg =0;  unsigned = 0;   mem_read = '000';   mem_write = '000'
            ALU_src = 0;        reg_write = 0;      ALU_op = '01' 
            slt = 0

            if funct3== '000' :
                branch= '100' #BEQ
            if funct3== '001' :
                branch= '101'  #BNE
            if funct3== '100' :
                branch= '110' #BLT
            if funct3== '101' :
                branch= '111' #BGE
            if funct3== '110' :
                branch= '110' #BLTU
            if funct3== '111' : 
                branch= '111' #BGEU
        
        if opcode == '0000011' : #LOAD
            jal =0;     jalr = 0;               branch = '000';         aui_or_lui = 0
            wb = 0;     mem_to_reg =1;          unsigned = funct3[0];   mem_read ='1'+ funct3[1:]
            mem_write = '000';   ALU_src = 1;   reg_write = 1;          ALU_op = '00' ; slt =0
        
        if  opcode == '0100011': #STORE
            jal =0;     jalr = 0;        branch = '000';         aui_or_lui = 0
            wb = 0;     mem_to_reg =0;   unsigned = funct3[0];   mem_read = '000'
            mem_write = '1'+ funct3[1:];      ALU_src = 1;   reg_write = 0;       ALU_op = '00' ; slt=0
        
        if opcode == '0010011' : #I-FORMAT
            jal =0;             jalr = 0;   branch = '000';     aui_or_lui = 0;     wb = 0
            mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
            ALU_src = 1;        reg_write = 1;      ALU_op = '11' 
            if funct3 == '010' or funct3 =='011': slt = 1
            else: slt =0

        if opcode == '1100111' :   #JALR
            jal =0;             jalr = 1;           branch = '000';     aui_or_lui = 0;     wb = 0
            mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
            ALU_src = 1;        reg_write = 1;      ALU_op = '00' ; slt =0
        
        if opcode == '1101111' :   #JAL
            jal =1;             jalr = 0;           branch = '000';     aui_or_lui = 0;     wb = 0
            mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
            ALU_src = 0;        reg_write = 1;      ALU_op = 'z' ;      slt= 0
        
        if opcode == '0110111' : #LUI   
            jal = 0;             jalr = 0;           branch = '000';     aui_or_lui = 1;     wb = 1
            mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
            ALU_src = 0;        reg_write = 1;      ALU_op = 'z' ;      slt= 0
            
        if opcode == '0010111' : #AUIPC
            jal = 0;             jalr = 0;           branch = '000';     aui_or_lui = 0;     wb = 1
            mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
            ALU_src = 0;        reg_write = 1;      ALU_op = 'z' ; slt=0

    def alu_control (alu_op, funct3, funct7):
        global operation
        if alu_op == '00' : #   LOAD and STORE and JALR
            operation = '0011'
        if alu_op == '01' : #BRANCH
            if funct3 == '000' or funct3 == '001' or funct3 == '100' or funct3 == '101' :
                operation = '0100'
            if funct3 == '110' or funct3 == '111' :
                operation = '1100'
        
        if alu_op == '10' : #R-TYPE 
            if funct3 == '000' :
                if funct7 =='0' :
                    operation = '0011'
                if funct7 == '1':
                    operation = '0100'

            if funct3 == '001' : operation= '0101'
            if funct3 == '010' : operation= '0100'
            if funct3 == '011' : operation= '1100'
            if funct3 == '100' : operation= '0010'
            if funct3 == '101' :
                if funct7 == '0' :
                    operation = '0110'
                if funct7 == '1' :
                    operation = '0111'
            if funct3 == '110' : operation= '0001'
            if funct3 == '111' : operation= '0000'
        
        if alu_op == '11' : #I-TYPE
            if funct3 == '000' : operation= '0011'  #ADDI
            if funct3 == '001' : operation= '0101'  #SLLI
            if funct3 == '010' : operation= '0100'  #SLTI
            if funct3 == '011' : operation= '1100'  #SLTIU
            if funct3 == '100' : operation= '0010'  #XORI
            if funct3 == '101' : #SRLI OR SRAI
                if funct7 == '0' :
                    operation= '0110'
                if funct7 == '1' :
                    operation= '0111'
            if funct3 == '110' : operation= '0001'  #ORI
            if funct3 == '111' : operation= '0000'  #ANDI
        if alu_op == 'z': operation = 'z'
        
    def branch_control (jal, jalr, Branch) :
        global pc_src_1, pc_src_2, jump
        if jal == 1: 
            jump = 1
            pc_src_1 = 1
            pc_src_2 = 0
            return
        if jalr == 1 :
            jump = 1
            pc_src_1 = 0
            pc_src_2 = 1
            return
        if Branch == '000' :
            pc_src_1= 0
            pc_src_2= 0
            jump= 0
            return
        
        if Branch[0] == '1' :
            if Branch == '100' : #beq
                
                if zero == 1 :
                    pc_src_1 = 1
                    pc_src_2 = 0
                    jump = 0
                else :
                    pc_src_1 = 0
                    pc_src_2 = 0
                    jump = 0
            if Branch == '101' : #bne
                if zero == 0 :
                    pc_src_1 = 1
                    pc_src_2 = 0
                    jump = 0
                if zero == 1 :
                    pc_src_1 = 0
                    pc_src_2 = 0
                    jump = 0
            if Branch == '110' : #blt
                if sign_bit == 1 :
                    pc_src_1 = 1
                    pc_src_2 = 0
                    jump = 0
                else :
                    pc_src_1 = 0
                    pc_src_2 = 0
                    jump = 0  
            if Branch == '111' : #bge
                if sign_bit == 0 :
                    pc_src_1 = 1
                    pc_src_2 = 0
                    jump = 0
                else :
                    pc_src_1 = 0
                    pc_src_2 = 0
                    jump = 0        

    def graphic () :
            global color_dir
            color_dir = {
                '0': 'FF8000', '1' : 'FF0000', '2' : 'FFFF00', '3' : '', '4' : '00CC00', '5' : 'FF66FF', '6' : '', '7' : '00CC00', '8' : '',
                '9' : '', '10' : '', '11' : '', '12' : '', '13' : 'B85C00', '14' : '7F00FF', '15': '', '16' : '', '17' :'',
                'jal':'', 'jalr':'', 'branch': '', 'AuiOrLui': '', 'wb':'', 'slt':'', 'MemtoRegister':'',
                'ALUOp': '', 'Unsigned':'', 'MemRead':'', 'MemWrite':'', 'ALUSrc':'', 'RegWrite': '', 'zero' :'', 'sign-bit':'',
                'pcsrc1':'', 'pcsrc2': ''
            }
            
            color_dir['3']              = mux(color_dir['2'], color_dir['1'], ALU_src)
            color_dir['6']              = mux(color_dir['0'],color_dir['4'], pc_src_1)
            color_dir['9']              = mux(color_dir['6'], color_dir['5'], pc_src_2)
            color_dir['10']             = mux(color_dir['5'], color_dir['8'], mem_to_reg)
            color_dir['11']             = mux(color_dir['10'], color_dir['0'], jump)
            color_dir['12']             = mux(color_dir['14'], color_dir['13'], sign_bit)
            color_dir['15']             = mux(color_dir['11'], color_dir['12'], slt)
            color_dir['16']             = mux(color_dir['7'], color_dir['1'], aui_or_lui)
            color_dir['17']             = mux(color_dir['15'], color_dir['16'], wb)
            color_dir['8']              = mux('', '00FFFF', int (mem_read[0]))
            color_dir['jal']            = jal
            color_dir['jalr']           = jalr
            color_dir['branch']         = branch
            color_dir['AuiOrLui']       = aui_or_lui
            color_dir['wb']             = wb
            color_dir['slt']            = slt
            color_dir['MemtoRegister']  = mem_to_reg
            if ALU_op == 'z':
                color_dir['ALUOp']          = '0'
            else:
                color_dir['ALUOp']          = '1'
            color_dir['Unsigned']       = unsigned
            color_dir['MemRead']        = mem_read
            color_dir['MemWrite']       = mem_write
            color_dir['ALUSrc']         = ALU_src
            color_dir['RegWrite']       = reg_write 
            color_dir['sign-bit']       = sign_bit
            color_dir['zero']           = zero
            color_dir['pcsrc1']         =pc_src_1
            color_dir['pcsrc2']         =pc_src_2
            color_dir['jump']           =jump

    while pc < 4*len(instruction_memory) :
        global zero, sign_bit
        zero =0
        sign_bit =0
        instruction = instruction_memory [bin(pc)[2:]][:32]
        control(instruction[25:32], instruction[17:20])
        
        read_register_1 = instruction [12:17]
        read_register_2 = instruction [7:12]
        write_register  = instruction [20:25]
        read_data_1     = register[read_register_1]
        read_data_2     = register[read_register_2]
        
        imm= imm_gen(instruction)
        alu_control(ALU_op, instruction[17:20], instruction[1])
        ALU(read_data_1, mux(read_data_2,imm, ALU_src), operation)  
        branch_control(jal, jalr, branch)

        data_memory(ALU_result, mem_read, mem_write, read_data_2)
        read_data = data_gen(read_data, unsigned)
    
        write_data_r = mux(mux(mux(mux(ALU_result, read_data, mem_to_reg ), bin(pc+4)[2:] ,jump), mux ('00000000000000000000000000000000','00000000000000000000000000000001', sign_bit), slt), mux (bin((dec(imm)<<12)+pc)[2:].rjust(32, '0') ,bin(dec(imm)<<12)[2:].rjust(32, '0'), aui_or_lui), wb )
        if jump == 1:
            write_data_r = write_data_r.rjust(32,'0')
        write_data_r = write_data_r.rjust(32,write_data_r[0])
        if reg_write == 1 :
            register[write_register] = write_data_r
    
        register['00000'] = '00000000000000000000000000000000'
        register['pc']    = pc
        #print (register)
        graphic ()
        
        coppy_register = register.copy()
        coppy_data_memory = Data_memory.copy()
        copp_graphic = color_dir.copy()
        all_time_register.append(coppy_register)
        all_time_data_memory.append(coppy_data_memory)
        all_time_grapic.append(copp_graphic)

        # if pc == 4 :
        #     break
        pc = mux(mux(pc+4,(dec(imm)<<1)+pc, pc_src_1), ALU_result, pc_src_2)

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

    instruction_memory = instruction_arr
    # for i in instruction_arr :
    #     instruction_memory.append(str(i)+':\t'+ instruction_arr[i])

    def adjust_all_time_register (j):
        register = all_time_register[j]
        count = 0
        re = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1', 't2', 's0/fp', 's1', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 't3', 't4', 't5', 't6']
        mdic = {}
        for i in register :
            if i == 'pc' :
                mdic['pc'.ljust(12, ' ')] = '0x'+hex(register[i])[2:].rjust(8,'0')
                print(mdic['pc'.ljust(12, ' ')])
            else:
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
            
            
    temp_all_time_register = []
    for i in range (len (all_time_register)) :
        temp_all_time_register.append(adjust_all_time_register(i))
    all_time_register= temp_all_time_register

####------------------------------------------------------------  
    # last_reg = list((all_time_register.keys()))[-1]
    # reg = all_time_register[last_reg]
    #print (reg)
    #fo_1= open(s[:-2]+'_register'+'.txt', 'w')
    #fo_1.write('Register Expected Results\n')
    # count=0
    # for i in reg :
    #     fo_1.write('## expect['+str(count)+'] = '+reg[i]+'\n')
    #     count+=1
    # fo_1.close()
####------------------------------------------------------------  
    # registers=[]
    # for i in register :
    # registers.append(i +'\t'+ register[i])

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

    return {'Registers': all_time_register,'len_register': len(all_time_register), 'Data_memory': all_time_data_memory, 'Instruction_memory': instruction_memory, 'Graphic': all_time_grapic}
'''
fo= open('Data_Segment.txt','w')
data_segment = core('Code_editor.txt')
for j in data_segment['Registers'][(len(data_segment['Registers'])-1)*4]:
    fo.write(str(j)+'\t'+str(data_segment['Registers'][(len(data_segment['Registers'])-1)*4][j])+ '\n')
fo.close()'''
'''core('Code_editor.txt')
import sys
import glob
obj_list = []
mlist=[]
mlist = sys.argv


for i in range (len(mlist)) :
    if mlist[i]=='-o':
        obj_list= glob.glob(mlist[i+1]+"/**",recursive=True)
    if mlist[i].endswith('.s'):
        core(mlist[i])
for i in range (len(obj_list)) :
    if obj_list [i].endswith ('.s') or obj_list[i].endswith('.S'):
        core(obj_list[i])
'''