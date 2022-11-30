import random

def mainMenu():
    print("Welcome, mayor of Ngee Ann City!")
    print("----------------------------")
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Show high scores")
    print()
    print("0. Exit")
    choice = input("Your choice? ")
    print()
    return choice

def initGrid(rows, cols):
    grid = {}
    coins = 16

    for i in range(rows):
        for j in range(cols):
            grid[(chr(65+j), i+1)] = " "
    
    return grid, coins

def displayTurn(turns, rows, cols, grid):
    if turns <= rows * cols:
        print("Turn", turns)
        turns += 1
    else:
        print("Final layout of Ngee Ann City:")

    print("  ", end = "")
    for c in range(cols):
        print("{:>4}".format(chr(65+c)), end = "")   
    print()

    for row in range(rows*2+1):
        if row % 2 == 0:
            print("   ", end = "")

            for col in range(cols):
                print("+---", end = "")
            print("{:<10}".format("+"), end = "")
        else:
            if row >= 19:
                print(" {}".format(row // 2 + 1), end = "")
            else:
                print(" {} ".format(row // 2 + 1), end = "")
            for col in range(cols):
                print("| {} ".format(grid[(chr(65+col),row // 2 + 1)]), end = "")
            print("{:<10}".format("|"), end = "")
        print()

def displayGameMenu(randBuild1, randBuild2):
    
    print("1. Build a {} ({})".format(randBuild1[0], randBuild1[1]))
    print("2. Build a {} ({})".format(randBuild2[0], randBuild2[1]))
    print("3. See current score\n")
    print("4. Save game")
    print("0. Exit to main menu")
    print("Your choice? ", end = "")

def getRandomBuildChoice(buildDict):

    randBuild1 = random.choice(list(buildDict.items()))
    randBuild2 = random.choice(list(buildDict.items()))

    return randBuild1, randBuild2

ROWS = 20
COLS = 20
turns = 1

buildings = {'Residential':'R', 'Industry':'I', 'Commercial':'C', 'Park':'O', 'Road':'*'}

while True:
    choice = mainMenu()
    #Exit Game option
    if choice == "0":
        print("Game Closed.")
        break
    elif choice == "1":
        grid, coins = initGrid(ROWS, COLS)

        displayTurn(turns, ROWS, COLS, grid)

        randBuild1, randBuild2 = getRandomBuildChoice(buildings)
        displayGameMenu(randBuild1, randBuild2)
        option = input()
        if option == "0":
            break
    else:
        print("Invalid Option")
        

