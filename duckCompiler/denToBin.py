file = "duckCompiler/code.duck"

with open(file, "r") as f:
    data = f.read()
    data = data.split("\n")
    hex_data = []
    instructions = 0
    for x,y in enumerate(data):
        q = ""
        n = y.split(" ")
        for i in n:
            if i:
                hex_data.append(hex(int(i)).replace("0x","").zfill(4)+"\n")
                instructions += 1
                q+="{0:b}".format(int(i)).zfill(16)
                q += "\n"
        data[x] = q

with open("compiled.hdw","w") as f:
    q = ""
    for i in data:
        q += i
    fill = 1024-len(data)
    print(f"Number of instructions: {instructions}")
    print(f"Fill lines: {fill}")
    f.write(q.strip())
with open("hex_data.txt","w") as f:
    q = ""
    for i in hex_data:
        q += i
    f.write(q)