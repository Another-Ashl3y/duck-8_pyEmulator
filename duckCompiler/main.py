file = input("File to compile -> ")
with open(file,"r") as f:
    data = f.read().strip().splitlines()
# 0 -> 1023 ROM
# 1024 -> 61438 FREE
# 61439 -> 65535 MONITOR
output = []
variables = {}
labels = {}
start_pos = 1024
current_pos = start_pos

# @ value at this address
# . to access a variable
# # to access a label

def num_of_lines(x):
    q = 0
    for i in x:
        for j in i:
            q += 1
    return q

for i in data:
    if i:
        code_line = []
        arguments = i.split(" ")
        print(arguments)
        
        instruction = arguments[0]
        if instruction == "var":
            code_line.append("00018")
            code_line.append(str(arguments[2]).zfill(5))
            code_line.append(str(current_pos).zfill(5))
            code_line.append(str(0).zfill(5))
            variables[arguments[1]] = current_pos
            current_pos += 1

        if instruction == "label":
            labels[arguments[1]] = num_of_lines(output)
            code_line.append(str(0).zfill(5))
            code_line.append(str(0).zfill(5))
            code_line.append(str(0).zfill(5))
            code_line.append(str(0).zfill(5))
        
        if instruction == "goto":
            line = ""
            if arguments[1][0] == "#":
                line = str(labels[arguments[1].replace("#","")])
            else:
                line = arguments[1]
            code_line.append("00021")
            code_line.append(line)
            code_line.append(str(0))
            code_line.append(str(0))
        if instruction == "goIfZ":
            line = ""
            if arguments[1][0] == "#":
                line = str(labels[arguments[1].replace("#","")])
            else:
                line = arguments[1]
            code_line.append("22")
            code_line.append(line)
            code_line.append(str(0))
            code_line.append(str(0))

        if instruction == "save":
            a = arguments[1]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1
            
            code_line.append("00016")
            code_line.append(str(a).zfill(5))
            code_line.append(str(arguments[2]).zfill(5))
            code_line.append(str(0).zfill(5))
        if instruction == "load":
            code_line.append("00015")
            code_line.append(str(arguments[1]).zfill(5))
            code_line.append(str(current_pos).zfill(5))
            code_line.append(str(0).zfill(5))
            variables[arguments[2]] = current_pos
            current_pos += 1
        if instruction == "raw":
            v = arguments[1]
            a = arguments[2]
            print(a)
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
                print(a)
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1
            code_line.append("19")
            code_line.append(str(v).zfill(5))
            code_line.append(str(a).zfill(5))
            code_line.append(str(0).zfill(5))

        if instruction == "add":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("2")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1
        if instruction == "sub":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("3")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1
        if instruction == "mul":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("4")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1
        if instruction == "add":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("5")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1
        if instruction == "inc":
            offset = 0
            a = arguments[1]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            current_pos -= offset
            code_line.append("6")
            code_line.append(a)
            code_line.append(str(0))
            code_line.append(str(0))
        if instruction == "dec":
            offset = 0
            a = arguments[1]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            current_pos -= offset
            code_line.append("7")
            code_line.append(a)
            code_line.append(str(0))
            code_line.append(str(0))
        if instruction == "not":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("5")
            code_line.append(a)
            code_line.append(str(current_pos))
            code_line.append(str(0))
            variables[b] = current_pos
            current_pos += 1
        if instruction == "orr":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("9")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1
        if instruction == "and":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("10")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1
        if instruction == "xor":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("11")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1
        if instruction == "equ":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("12")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1
        if instruction == "grt":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("13")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1
        if instruction == "les":
            offset = 0
            a = arguments[1]
            b = arguments[2]
            c = arguments[3]
            if a[0] == ".": # Check if location exists
                a = str(variables[a.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                a = str(current_pos)
                current_pos += 1
                offset += 1

            if b[0] == ".": # Check if location exists
                b = variables[b.replace(".","")]
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[2]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                b = str(current_pos)
                current_pos += 1
                offset += 1
            current_pos -= offset
            code_line.append("14")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(current_pos))
            variables[c] = current_pos
            current_pos += 1


        for x, j in enumerate(code_line):
            code_line[x] = str(j).zfill(5)
        print(len(code_line))
        output.append(code_line)

with open("compiledCode.hdw","w") as f:
    print(variables)
    print(labels)
    q = ""
    for x in output:
        print(x)
        for y in x:
            q += "{0:b}".format(int(y)).zfill(16) + "\n"
    f.write(q.strip())
