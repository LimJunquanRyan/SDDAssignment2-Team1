import random

def mainMenu():
    # prints main menu and gets user's input
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
    # initialize grid dictionary and coins
    grid = {}
    coins = 16

    # adds grid elements into grid dictionary with alphanumeric keys
    for i in range(rows):
        for j in range(cols):
            grid[(chr(65+j), str(i+1))] = " "
    
    return grid, coins

def displayTurn(turns, coins, rows, cols, grid):
    print()
    # checks if game is over
    if turns <= rows * cols and coins > 0:
        print("Turn", turns)
        print("Coins", coins)
    else:
        print("Final layout of Ngee Ann City:")

    print()
    # print game grid
    print("  ", end = "")
    for c in range(cols):
        print("{:>4}".format(chr(65+c)), end = "")   
    print()

    #print all rows including grid lines
    for row in range(rows*2+1):
        # if even, print grid lines
        if row % 2 == 0:
            print("   ", end = "")

            for col in range(cols):
                print("+---", end = "")
            print("{:<10}".format("+"), end = "")
        else: # if odd, print grid elements
            if row >= 19:
                print(" {}".format(row // 2 + 1), end = "")
            else:
                print(" {} ".format(row // 2 + 1), end = "")
            for col in range(cols):
                print("| {} ".format(grid[(chr(65+col),str(row // 2 + 1))]), end = "")
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

    # gets random building from building dictionary
    randBuild1 = random.choice(list(buildDict.items()))
    randBuild2 = random.choice(list(buildDict.items()))

    # ensure each building option is different
    while randBuild2 == randBuild1:
        randBuild2 = random.choice(list(buildDict.items()))

    return randBuild1, randBuild2

def addBuildingToGrid(build, grid, coins):

    buildOption = input("Build where? ").upper()
    location = (buildOption[:1], buildOption[1:])
    print(location)

    if location not in grid:
        print("Location is invalid or not on the grid.")
        return addBuildingToGrid(build, grid, coins)
    else:
        if grid[location] != " ":
            print("Location already has a building on it.")
            return addBuildingToGrid(build, grid, coins)
        else:
            grid[location] = build[1]
            coins -= 1
            return coins


def saveGame():
    file = open("saveFile.txt", "w")
    file.write(str(turns) + "\n")
    file.write(str(coins) + "\n")
    file.write(randBuild1 + "," + randBuild2 + "\n")

    for rows in range(ROWS + 2):
        rowSave = ""
        for column in range(COLS  + 2):
            rowSave = rowSave #not done yet due to building not implemented yet
        file.write(rowSave + "\n")

    file.close()
    print("Game saved!")

def loadGame():
    global turns, coins, randBuild1, randBuild2
    file = open("saveFile.txt", "r")
    turns = int(file.readline())
    coins = int(file.readline())
    randBuild = file.readline()
    randBuild = randBuild.strip("\n")
    randBuild = randBuild.split(",")
    randBuild1 = randBuild[0]
    randBuild2 = randBuild[1]
    # the rest implementing when building feature is completed

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
    # start new game
    elif choice == "1":
        grid, coins = initGrid(ROWS, COLS)

        while True:
            displayTurn(turns, coins, ROWS, COLS, grid)

            if turns <= ROWS * COLS and coins > 0:
                randBuild1, randBuild2 = getRandomBuildChoice(buildings)
                displayGameMenu(randBuild1, randBuild2)
                option = input()
                # return to main menu
                if option == "0":
                    break
                elif option == "1":
                    coins = addBuildingToGrid(randBuild1, grid, coins)
                elif option == "2":
                    coins = addBuildingToGrid(randBuild2, grid, coins)
                elif option == "4":
                    saveGame()
                else:
                    continue
            else:
                print()
                print("Thank you for playing!")
                print()
                break
            
            turns += 1
    else:
        print("Invalid Option")
        

