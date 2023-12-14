import pygame
from hardware.cpu import cpu
pygame.init()

SCALE = 5
ROM = "hardware/ROM.hdw"

# 0 -> 1024 ROM
# 1024 -> 
# 61439 -> 65535 MONITOR
CPU = cpu()
MONITOR = pygame.display.set_mode((64*SCALE,64*SCALE))
pygame.display.set_caption("DUCK-8 EMULATOR")

def main() -> str:
    # Read ROM
    try:
        with open(ROM, "r") as f:
            data = f.read()
        data = data.split("\n")
        print("-- ROM --")
        for i in range(1024):
            if not(i>len(data)-1):
                if i % 4 == 0:
                    try:
                        instruct = CPU.functions[data[i]]
                        print(f"| {instruct.__name__} |")
                    except KeyError:
                        return "faulty instruction at line: " + str(i)
                print(f"{str(i).format().zfill(5)} | {data[i]} |")
                CPU.MEMORY[i] = data[i]
                
            else:
                CPU.MEMORY[i] = "0000000000000000"
        print("ROM read successfully")
    except:
        return "Failed to load ROM"
    # Load ROM
    for x, i in enumerate(data):
        CPU.MEMORY[x] = i.strip()

    while CPU.alive:
        MONITOR.fill((0,0,0))
        # Draw from memory 
        for i in range(61440, 65536, 1):
            x = (i-61440) % 64
            y = ((i-61440) // 64)
            c = int(CPU.MEMORY[i],2)
            pygame.draw.rect(
                MONITOR,
                (
                    c,
                    c,
                    c
                ),
                (x*SCALE, y*SCALE, 1*SCALE, 1*SCALE)
            )


        CPU.tick()


        # Check for emulator close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "-- Emulator closed by user --"


    return "-- Emulator closed --"


err = main()
print(err)
