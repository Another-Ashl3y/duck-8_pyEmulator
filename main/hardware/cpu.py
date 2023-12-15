import traceback, pygame
class cpu:
    def __init__(self):
        f = [
            PAS,
            HLT,
            ADD,SUB,MUL,DIV,INC,DEC,
            NOT,ORR,AND,XOR,
            EQU,GRT,LES,
            STO,STI,STQ,STR,STT,MOV,
            JMP,JMZ,JMC,
            UPD
        ]
        self.functions = {}
        docs = []
        for x, i in enumerate(f):
            self.functions[format_binary(x,16)] = i
            print(f"{format_binary(x,16)} | {x} : {i.__name__}")
            docs.append(f"{i.__name__} {format_binary(x,16)} |  | {str(x).zfill(5)} |")
        with open("docs.duck","w") as f:
            q = ""
            for i in docs:
                q += i + "\n"
            f.write(q)
        # 0 -> 1024 ROM
        # 61439 -> 65535 MONITOR
        self.MEMORY = ["0000000000000000" for _ in range(65536)]
        self.alive = True
        self.program_counter = "0000000000000000"
        self.carry = "0"
        self.alu = "0000000000000000"
        print("--------------------------------------------")

    def tick(self):

        pygame.display.update()
        
        print(int(self.MEMORY[1025],2))
        instruction = self.MEMORY[int(self.program_counter,2)+0]
        arg0 = self.MEMORY[int(self.program_counter,2)+1]
        arg1 = self.MEMORY[int(self.program_counter,2)+2]
        arg3 = self.MEMORY[int(self.program_counter,2)+3]
        # print(instruction)
        try:
            q = self.functions[instruction](self, arg0, arg1, arg3)
            if not(q):
                next_instruction(self)


        except KeyError as e:
            print("-- Function not found --")
            print(f"Error at point {int(self.program_counter,2)}")
            traceback.print_exception(e)
            self.alive = False


def format_binary(x, bits):
    return "{0:b}".format(x).zfill(bits)

def ADD(this:cpu,a,b,c):
    this.MEMORY[int(c,2)] = format_binary(int(this.MEMORY[int(a,2)],2) + int(this.MEMORY[int(b,2)],2),16)
    this.alu = format_binary(int(this.MEMORY[int(a,2)],2) + 1,16)
def SUB(this:cpu,a,b,c):
    this.MEMORY[int(c,2)] = format_binary(int(this.MEMORY[int(a,2)],2) - int(this.MEMORY[int(b,2)],2),16)
    this.alu = format_binary(int(this.MEMORY[int(a,2)],2) - 1,16)
def MUL(this:cpu,a,b,c):
    this.MEMORY[int(c,2)] = format_binary(int(this.MEMORY[int(a,2)],2) * int(this.MEMORY[int(b,2)],2),16)
    this.alu = format_binary(int(this.MEMORY[int(a,2)],2) * 1,16)
def DIV(this:cpu,a,b,c):
    this.MEMORY[int(c,2)] = format_binary(int(this.MEMORY[int(a,2)],2) // int(this.MEMORY[int(b,2)],2),16)
    this.alu = format_binary(int(this.MEMORY[int(a,2)],2) // 1,16)
def INC(this:cpu,a,c,_):
    this.MEMORY[int(a,2)] = format_binary(int(this.MEMORY[int(a,2)],2) + 1,16)
    this.alu = format_binary(int(this.MEMORY[int(a,2)],2) + 1,16)
def DEC(this:cpu,a,c,_):
    this.MEMORY[int(a,2)] = format_binary(int(this.MEMORY[int(a,2)],2) - 1,16)
    this.alu = format_binary(int(this.MEMORY[int(a,2)],2) - 1,16)
def NOT(this:cpu,a,c,_):
    q = 0
    if int(this.MEMORY[int(a,2)],2) > 0:
        q = 1
    this.MEMORY[int(c,2)] = format_binary(q,16)
    this.alu = format_binary(q,16)
def ORR(this:cpu,a,b,c):
    q = 0
    if int(this.MEMORY[int(a,2)],2) > 0 or int(this.MEMORY[int(b,2)],2) > 0:
        q = 1
    this.MEMORY[int(c,2)] = format_binary(q,16)
    this.alu = format_binary(q,16)
def AND(this:cpu,a,b,c):
    q = 0
    if int(this.MEMORY[int(a,2)],2) > 0 and int(this.MEMORY[int(b,2)],2) > 0:
        q = 1
    this.MEMORY[int(c,2)] = format_binary(q,16)
    this.alu = format_binary(q,16)
def XOR(this:cpu,a,b,c):
    q = 0
    if (
        int(this.MEMORY[int(a,2)],2) > 0 and not(int(this.MEMORY[int(b,2)],2) > 0)
        ) or int(this.MEMORY[int(b,2)],2) > 0 and not(int(this.MEMORY[int(a,2)],2) > 0):
        q = 1
    this.MEMORY[int(c,2)] = format_binary(q,16)
    this.alu = format_binary(1,16)
def EQU(this:cpu,a,b,c):
    q = 0
    if int(this.MEMORY[int(a,2)],2) > 0 == int(this.MEMORY[int(b,2)],2) > 0:
        q = 1
    this.MEMORY[int(c,2)] = format_binary(q,16)
    this.alu = format_binary(1,16)
def GRT(this:cpu,a,b,c):
    q = 0
    if int(this.MEMORY[int(a,2)],2) > int(this.MEMORY[int(b,2)],2):
        q = 1
    this.MEMORY[int(c,2)] = format_binary(q,16)
    this.alu = format_binary(q,16)
def LES(this:cpu,a,b,c):
    q = 0
    if int(this.MEMORY[int(a,2)],2) < int(this.MEMORY[int(b,2)],2):
        q = 1
    this.MEMORY[int(c,2)] = format_binary(q,16)
    this.alu = format_binary(1,16)
def STO(this:cpu,a,b,_):
    with open("hardware/harddrive.hdw","r") as f:
        data = f.read().split("\n")
        this.MEMORY[int(b,2)] = data[int(a,2)] 
def STI(this:cpu,a,b,_):
    with open("hardware/harddrive.hdw","r") as f:
        data = f.read().split("\n")
        data[int(b,2)] = this.MEMORY[int(a,2)]
    with open("hardware/harddrive.hdw","w") as f:
        q = ""
        for i in data:
            q += i+"\n"
        f.write(q.strip())
def STQ(this:cpu,a,_0,_1):
    this.MEMORY[int(a,2)] = this.alu
def HLT(this:cpu,_0,_1,_2):
    this.alive = False
def JMP(this:cpu,a,_0,_1):
    this.program_counter = format_binary(int(a,2),16)
    return 1
def JMZ(this:cpu,a,_0,_1):
    if int(this.alu,2) == 0:
        this.program_counter = format_binary(int(a,2),16)
    return 1
def JMC(this:cpu,a,_0,_1):
    if int(this.alu,2) == 0:
        this.program_counter = format_binary(int(a,2),16)
    return 1
def STR(this:cpu,a,b,_):
    this.MEMORY[int(b,2)] = a
def STT(this:cpu,a,b,_):
    this.MEMORY[int(this.MEMORY[int(b,2)],2)] = a
def MOV(this:cpu,a,b,_):
    this.MEMORY[int(b,2)] = this.MEMORY[int(a,2)]
def PAS(this:cpu,a,b,c):
    pass
def next_instruction(this:cpu):
    this.program_counter = format_binary(int(this.program_counter,2)+4, 16)
def UPD(this:cpu,_a,_b,_c):
    pygame.display.update()
