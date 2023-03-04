import random
availableIPs = [str(i) for i in range(17, 255)]

print(len(availableIPs))

print(availableIPs)

ranIP = random.choice(availableIPs)
print(ranIP)
print(availableIPs)


