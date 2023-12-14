file = "code.duck"

with open(file, "r") as f:
    data = f.read()
    data = data.split("\n")
    for x,y in enumerate(data):
        q = ""
        n = y.split(" ")
        for i in n:
            q+="{0:b}".format(int(i,16)).zfill(16)
            q += " "
        data[x] = q

with open("compiled.hdw","w") as f:
    f.writelines(data)