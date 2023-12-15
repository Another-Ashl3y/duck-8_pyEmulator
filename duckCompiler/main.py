import traceback
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
    if current_pos > 61438:
        print("Max memory used")
        break
    if i:
        code_line = []
        arguments = i.split(" ")
        # print(arguments)
        
        instruction = arguments[0]
        if instruction == "mutate":
            var = arguments[1]
            value = arguments[2]
            if value[0] == ".":
                value = variables[value.replace(".","")]
            code_line += [
                "18",
                str(value),
                str(variables[var]),
                "0"
            ]
        if instruction == "var":
            code_line.append("18")
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
                if arguments[1].replace("#","") in labels:
                    line = str(labels[arguments[1].replace("#","")])
                else:
                    line = arguments[1].replace("#","")
            else:
                line = arguments[1]
            code_line.append("00021")
            code_line.append(line)
            code_line.append(str(0))
            code_line.append(str(0))
        if instruction == "goIfZ":
            line = ""
            if arguments[1][0] == "#":
                if arguments[1].replace("#","") in labels:
                    line = str(labels[arguments[1].replace("#","")])
                else:
                    line = arguments[1].replace("#","")
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
        if instruction == "copy":
            v = arguments[1]
            a = arguments[2]
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
            if v[0] == ".": # Check if location exists
                v = str(variables[v.replace(".","")])
            else: # No location to access so create one
                code_line.append("00018")
                code_line.append(str(arguments[1]).zfill(5))
                code_line.append(str(current_pos).zfill(5))
                code_line.append(str(0).zfill(5))
                v = str(current_pos)
                current_pos += 1
                offset += 1
            code_line += [
                "20",
                v,
                a,
                "0"
            ]
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("2")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("3")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("4")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
        if instruction == "div":
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("5")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
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
            if b[0] == ".":
                b = str(variables[b.replace(".","")])
            else:
                variables[b] = current_pos
                b = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("5")
            code_line.append(a)
            code_line.append(b)
            code_line.append(str(0))
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("9")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("10")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("11")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("12")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("13")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
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
            if c[0] == ".":
                c = str(variables[c.replace(".","")])
            else:
                variables[c] = current_pos
                c = str(current_pos)
                current_pos+=1
            current_pos -= offset
            code_line.append("14")
            code_line.append(a)
            code_line.append(b)
            code_line.append(c)
        if instruction == "update":
            code_line.append("24")
            code_line.append("0")
            code_line.append("0")
            code_line.append("0")
        if instruction == "for":
            start = arguments[1]
            end = arguments[2]
            name = arguments[3]
            if start[0] == ".":
                addr = variables[start.replace(".","")]
                code_line += [
                    "20",
                    addr,
                    current_pos,
                    "0"
                ]
                variables[name+":min"] = current_pos
                current_pos += 1
                code_line+=[
                    "20",
                    addr,
                    current_pos,
                    "0"
                ]
                variables[name+":index"] = current_pos
                current_pos += 1
            else:
                v = start
                code_line += [
                    "18",
                    v,
                    current_pos,
                    "0"
                ]
                variables[name+":min"] = current_pos
                current_pos += 1
                code_line+=[
                    "18",
                    v,
                    current_pos,
                    "0"
                ]
                variables[name+":index"] = current_pos
                current_pos += 1

            
            if end[0] == ".":
                addr = variables[end.replace(".","")]
                code_line += [
                    "20",
                    addr,
                    current_pos,
                    "0"
                ]
            else:
                v = end
                code_line += [
                    "18",
                    v,
                    current_pos,
                    "0"
                ]
            variables[name+":max"] = current_pos
            current_pos += 1
            labels[name] = num_of_lines(output)+(4*3)
            code_line += ["0","0","0","0"]
            # print(code_line)
        if instruction == "endfor":
            name = arguments[1]
            code_line += [
                "06", # Increment value
                variables[name+":index"],
                "00",
                "00",

                "13", # Compare index with max
                variables[name+":index"],
                variables[name+":max"],
                current_pos,
                
                "22", 
                labels[name],
                "0",
                "0"
            ]



        
        for x, j in enumerate(code_line):
            code_line[x] = str(j).zfill(5)
            # print(j)
        print(len(code_line))
        output.append(code_line)


with open("compiledCode.hdw","w") as f:
    print(variables)
    print(labels)
    q = ""
    for x, i in enumerate(output):
        for y, j in enumerate(i):
            print(j)
            try:
                q += "{0:b}".format(int(j)).zfill(16) + "\n"
            except ValueError as e:
                print(j,int(labels[j]))
                q += "{0:b}".format(int(labels[j])).zfill(16) + "\n"
    f.write(q.strip())
