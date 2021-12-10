def calcGuesses(x):
    match x:
        case 1:
            return 6
        case 2:
            return x * 3
        case 3:
            return x * 3
        case 4:
            return x * 2
        case 5:
            return x * 2
        case _:
            #switch to harder list(len 7 or greater)
            return 12

while True:
    y = int(input("Number: "))
    print(calcGuesses(y))
