X = 7
Y = 14

def coordinatesToLedAddress(x,y):
    x += 1
    y += 1
    address = X * y
    if (y%2) == 0:address -= x
    else:address -= X - x + 1
    return address


while True:
    print(coordinatesToLedAddress(int(input("x:")),int(input("y:"))))