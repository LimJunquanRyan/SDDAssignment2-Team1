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
    if turns > rows * cols or coins == 0:
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

def displayGameMenu(turns, coins, randBuild1, randBuild2):
    print("\nTurn", turns)
    print("Coins", coins)
    print()
    
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
    # print(location)
    if turns == 1:
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
                return build, location, coins
    else:
        if location not in grid:
            print("Location is invalid or not on the grid.")
            return addBuildingToGrid(build, grid, coins)
        elif not checkAdjacency(location):
            print("Location must be adjacent to existing buildings.")
            return addBuildingToGrid(build, grid, coins)
        else:
            if grid[location] != " ":
                print("Location already has a building on it.")
                return addBuildingToGrid(build, grid, coins)
            else:
                grid[location] = build[1]
                coins -= 1
                return build, location, coins
    
def checkAdjacency(location):
    build = ['R', 'I', 'C', 'O', '*']
    check = ['N', 'N', 'N', 'N']
    # print(location[1])
    # print(ord(location[0]))
    if 1 <= int(location[1]) + 1 <= ROWS and 65 <= ord(location[0]) <= 65 + COLS - 1:
        if grid[chr(ord(location[0])), str(int(location[1]) + 1)] not in build:
            check[0] = 'Y'
    if 1 <= int(location[1]) <= ROWS and 65 <= ord(location[0]) - 1 <= 65 + COLS - 1:
        if grid[chr(ord(location[0]) - 1), str(int(location[1]))] not in build:
            check[1] = 'Y'
    if 1 <= int(location[1]) - 1 <= ROWS and 65 <= ord(location[0]) <= 65 + COLS - 1:
        if grid[chr(ord(location[0])), str(int(location[1]) - 1)] not in build:
            check[2] = 'Y'
    if 1 <= int(location[1]) <= ROWS and 65 <= ord(location[0]) + 1 <= 65 + COLS - 1:
        if grid[chr(ord(location[0]) + 1), str(int(location[1]))] not in build:
            check[3] = 'Y'
    if check[0] == 'Y' and check[1] == 'Y' and check[2] == 'Y' and check[3] == 'Y':
        return False
    else:
        return True

# def gainCoin(coins):
#     build = ['I', 'C']
#     build2 = ['R']
#     for rows in range(1, ROWS):
#         for columns in range(1, COLS):
#             if grid[chr(65+rows), str(columns+1)] in build:
#                 if 1 <= columns+1 + 1 <= COLS and 65 <= 64+rows <= 65 + ROWS - 1:
#                     print(columns,rows)
#                     if grid[chr(65+rows), str(columns)] in build2:
#                         coins += 1
#                 if 1 <= columns+1 + 1 <= COLS and 65 <= 66+rows <= 65 + ROWS - 1:
#                     if grid[chr(65+rows), str(columns+2)] in build2:
#                         coins += 1
#                 if 1 <= columns+1 + 2 <= COLS and 65 <= 64+rows <= 65 + ROWS - 1:
#                     if grid[chr(64+rows), str(columns+1)] in build2:
#                         coins += 1
#                 if 1 <= columns+1 <= COLS and 65 <= 64+rows <= 65 + ROWS - 1:
#                     if grid[chr(66+rows), str(columns+1)] in build2:
#                         coins += 1
#     return coins

def gainCoin(build, location, coins, grid):
    if build[1] == 'R' or build[1] == 'C' or build[1] == 'I':

        # get each adjacent location
        left = ( chr(ord(location[0])-1), str(int(location[1])) )
        right = ( chr(ord(location[0])+1), str(int(location[1])) )
        top = ( chr(ord(location[0])), str(int(location[1])-1) )
        bottom =( chr(ord(location[0])), str(int(location[1])+1) )

        # check adjacent location based on if building is I, R or C
        if build[1] == 'I' or build[1] == 'C':
            if left in grid.keys() and grid[left] == 'R':
                coins +=1
            if right in grid.keys() and grid[right] == 'R':
                coins +=1
            if top in grid.keys() and grid[top] == 'R':
                coins +=1
            if bottom in grid.keys() and grid[bottom] == 'R':
                coins +=1
        else:
            if left in grid.keys() and (grid[left] == 'I' or grid[left] == 'C'):
                coins +=1
            if right in grid.keys() and (grid[right] == 'I' or grid[right] == 'C'):
                coins +=1
            if top in grid.keys() and (grid[top] == 'I' or grid[top] == 'C'):
                coins +=1
            if bottom in grid.keys() and (grid[bottom] == 'I' or grid[bottom] == 'C'):
                coins +=1

    return coins
                
def saveGame():
    file = open("saveFile.txt", "w")
    file.write(str(turns) + "\n")
    file.write(str(coins) + "\n")
    file.write(str(randBuild1) + "\n")
    file.write(str(randBuild2) + "\n")

    for rows in range(ROWS):
        rowSave = ""
        for columns in range(COLS):
            rowSave = rowSave + grid[chr(65+rows), str(columns+1)] + ","
        file.write(rowSave + "\n")

    file.close()
    print("Game saved!")

def loadGame():
    global turns, coins, randBuild1, randBuild2
    file = open("saveFile.txt", "r")
    turns = int(file.readline())
    coins = int(file.readline())
    randBuild1 = file.readline()
    randBuild2 = file.readline()
    rows = 0
    grid = {}
    for line in file:
        line = line.strip("\n")
        buildingRow = line.split(",")
        for columns in range(20):
            grid[chr(65+rows), str(columns+1)] = buildingRow[columns]
        rows += 1
    file.close()
    return grid

ROWS = 20
COLS = 20
turns = 1

buildings = {'Residential':'R', 'Industry':'I', 'Commercial':'C', 'Park':'O', 'Road':'*'}

isInvalid = False

while True:
    choice = mainMenu()
    #Exit Game option
    if choice == "0":
        print("Game Closed.")
        break
    # start new game
    elif choice in ["1", "2"]:
        if choice == "1":
            grid, coins = initGrid(ROWS, COLS)
        else:
            grid = loadGame()
        while True:
            displayTurn(turns, coins, ROWS, COLS, grid)

            if turns <= ROWS * COLS and coins > 0:

                # prevent random building from being randomized if first option is wrong
                if isInvalid == False:
                    randBuild1, randBuild2 = getRandomBuildChoice(buildings)
                else:
                    isInvalid == False

                displayGameMenu(turns, coins, randBuild1, randBuild2)
                option = input()
                # return to main menu
                if option == "0":
                    break
                elif option == "1":
                    selectedBuilding, location, coins = addBuildingToGrid(randBuild1, grid, coins)
                    coins = gainCoin(selectedBuilding, location, coins, grid)
                elif option == "2":
                    selectedBuilding, location, coins = addBuildingToGrid(randBuild2, grid, coins)
                    coins = gainCoin(selectedBuilding, location, coins, grid)

                elif option == "4":
                    saveGame()
                else:
                    print("Invalid option. Please try again.")
                    isInvalid = True
                    continue
            else:
                print()
                print("Thank you for playing!")
                print()
                break
            
            turns += 1
    else:
        print("Invalid Option")
        

