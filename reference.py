# Lim Junquan Ryan (S10192609) - IT02

import random

allBuildings = ("BCH", "FAC", "HSE", "SHP", "HWY", "MON")
buildings = []
turns = 1
placed = []
gridRow = 0
gridColumn = 0

#Function to access main menu of the game
def mainMenu():
    print("Welcome, mayor of Simp City!")
    print("----------------------------")
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Show high scores")
    print()
    print("0. Exit")
    choice = input("Your choice? ")
    print()
    return choice

#Initialises board which I named "placed"
def gridInit():
    #Creates Rows
    for i in range(gridRow + 2):
        placed.append([])
    #Finalises Grid
    for row in range(gridRow + 2):
        for column in range(gridColumn + 2):
            placed[row].append("   ")
    #Places row numbers into the Grid
    for rows in range(1, gridRow + 1):
        placed[rows][0] = str(rows)
    #Places column letters into the Grid
    for columns in range(1, gridColumn + 1):
        placed[0][columns] = " " + chr(64 + columns) + " "

#Function that prints out game grid and options every turn
def gameTurn(turns):
    remainderList = seeRemain()
    #if statement checks if game is over
    if turns <= gridRow * gridColumn:
        print("Turn", turns)
        turns += 1
    else:
        print("Final layout of Simp City:")
    #Prints game grid
    print(" ", end = "")
    for column in range(1, gridColumn + 1):
        print("{:>6}".format(placed[0][column]), end = "")   
    print()
    for row in range(gridRow * 2 + 1):
        #When row is odd, prints grid elements, when even, prints grid lines
        if row % 2 == 0:
            print("  ", end = "")
            for columns in range(gridColumn):
                print("+-----", end = "")
            print("{:<10}".format("+"), end = "")
        else:
            print(" {}".format(placed[row // 2 + 1][0]), end = "")
            for column in range(gridColumn):
                print("| {} ".format(placed[row // 2 + 1][column + 1]), end = "")
            print("{:<10}".format("|"), end = "")
        #prints remaining buildings next to Grid
        try:
            print("{:<10}{}".format(remainderList[row * 2], remainderList[row * 2 + 1]))
        except:
            print()

#Function that prints out game menu and requests input
def gameMenu(randBuilding):
    #checks if there is stored value in randomBuiliding1/2 as that is my checker
    #as to whether user entered option 1 or 2 or others
    if not randBuilding:
        for i in range(2):
            randBuilding.append(buildings[random.randint(0, len(buildings) - 1)])
        #Next 2 while loops checks if there are builidngs are still in building pool
        for i in range(2):
            while remainingBuildings.get(randBuilding[i]) == 0:
                randBuilding[i] = buildings[random.randint(0, len(buildings) - 1)]

    print("1. Build a", randBuilding[0])
    print("2. Build a", randBuilding[1])
    print("3. See current score")
    print()
    print("4. Save game")
    print("0. Exit to main menu")
    choice = input("Your choice? ")
    while choice not in ["0", "1", "2", "3", "4"]:
        print("Invalid choice")
        print()
        choice = input("Your choice? ")
    #option 3 for scoring
    if choice == "3":
        print()
        scoring()
    #option 4 for save game
    elif choice == "4":
        print()
        saveGame(randBuilding)     
    elif choice in ["1", "2"]:
        location = input("Build where? ").upper()
        #input validation checker for location
        if turns == 1: 
            if len(location) != 2 or (ord(location[1]) - 48) not in range(1, gridRow + 1) or (ord(location[0]) - 64) not in range(1, gridColumn + 1):
                if len(location) != 2:
                    print("Location entered is invalid")
                else:
                    print("Location entered is out of range")
                print()
                gameTurn(turns)
                return gameMenu(randBuilding)
        else:
            if len(location) != 2 or placed[int(location[1])][ord(location[0]) - 64] != "   " or (ord(location[1]) - 48) not in range(1, gridRow + 1) or \
                  (ord(location[0]) - 64) not in range(1, gridColumn + 1) or not checkAdjacency(location):
                if len(location) != 2:
                    print("Location entered is invalid")
                elif (ord(location[1]) - 48) not in range(1, gridRow + 1) or (ord(location[0]) - 64) not in range(1, gridColumn + 1):
                    print("Location entered is out of range")
                elif placed[int(location[1])][ord(location[0]) - 64] != "   ":
                    print("Building already present. Please choose another location.")
                else:
                    print("You must build next to an existing building.")
                print()
                gameTurn(turns)
                return gameMenu(randBuilding)
        #removes 1 copy of the building built from remaining buildings
        placed[int(location[1])][ord(location[0]) - 64] = randBuilding[int(choice) - 1]
        remainingBuildings[randBuilding[int(choice) - 1]] = remainingBuildings.get(randBuilding[int(choice) - 1], 8) - 1
        randBuilding.clear()
    print()
    return choice, randBuilding

#function to check for adjacency when placing buildings
def checkAdjacency(location):
    if placed[int(location[1]) + 1][ord(location[0]) - 64] not in buildings and placed[int(location[1]) - 1][ord(location[0]) - 64] not in buildings and \
       placed[int(location[1])][ord(location[0]) - 63] not in buildings and placed[int(location[1])][ord(location[0]) - 65] not in buildings:
        return False
    else:
        return True

#function to check whether buildings entered are valid buildings
def whetherBuilding(buildings):
    for building in buildings:
        if building in allBuildings:
            continue
        else:
            return True
        return False

#function to check whether there are building duplicates
def buildingDupes(buildings):
    for building in buildings:
        if buildings.count(building) > 1:
            return True
        return False

#function that prepares a remaing buildings list from the dictionary to be printed out on the right of the grid
def seeRemain():
    remainderList = ["Building", "Remaining", "-" * 8, "-" * 9]
    for building in buildings:
        remainderList.append(building)
        remainderList.append(remainingBuildings.get(building))
    return remainderList

#function that does scoring for each builiding
def scoring():
    scoreDict = {}
    facCount = 0
    cornerCount = 0
    monCount = 0
    #Fills scoreDict with lists that can be appended with scoring of each individual building
    for building in buildings:
        scoreDict[building] = []
    #Nested for loop that scores all the buildings in the grid
    for rows in range(1, gridRow + 1):
        for columns in range(1, gridColumn + 1):
            #HSE Scoring
            if placed[rows][columns] == "HSE":
                if placed[rows][columns - 1] == "FAC" or placed[rows][columns + 1] == "FAC" or placed[rows - 1][columns] == "FAC" or placed[rows + 1][columns] == "FAC":
                    scoreDict["HSE"].append("1")
                else:
                    score = 0
                    if placed[rows][columns - 1] in ["HSE", "SHP"]:
                        score += 1
                    elif placed[rows][columns - 1] in ["BCH", "MON"]:
                        score += 2
                    if placed[rows][columns + 1] in ["HSE", "SHP"]:
                        score += 1
                    elif placed[rows][columns + 1] in ["BCH", "MON"]:
                        score += 2
                    if placed[rows - 1][columns] in ["HSE", "SHP"]:
                        score += 1
                    elif placed[rows - 1][columns] in ["BCH", "MON"]:
                        score += 2
                    if placed[rows + 1][columns] in ["HSE", "SHP"]:
                        score += 1
                    elif placed[rows + 1][columns] in ["BCH", "MON"]:
                        score += 2
                    scoreDict["HSE"].append(str(score))
            #FAC Counting
            elif placed[rows][columns] == "FAC":
                facCount += 1
            #BCH Scoring
            elif placed[rows][columns] == "BCH":
                if columns == 1 or columns == gridColumn:
                    scoreDict["BCH"].append("3")
                else:
                    scoreDict["BCH"].append("1")
            #SHP Scoring
            elif placed[rows][columns] == "SHP":
                score = 0
                scored = []
                if placed[rows - 1][columns] in buildings:
                    scored.append(placed[rows][columns + 1])
                    score += 1
                if placed[rows + 1][columns] in buildings and placed[rows + 1][columns] not in scored:
                    scored.append(placed[rows + 2][columns + 1])
                    score += 1
                if placed[rows][columns + 1] in buildings and placed[rows][columns + 1] not in scored:
                    scored.append(placed[rows + 1][columns])
                    score += 1
                if placed[rows][columns - 1] in buildings and placed[rows][columns - 1] not in scored:
                    score += 1
                scoreDict["SHP"].append(str(score))
            #HWY Scoring
            elif placed[rows][columns] == "HWY":
                columnCount = 1
                score = 1
                for i in range(2):
                    while True:
                        if i == 0:
                            if placed[rows][columns + columnCount] == "HWY":
                                score += 1
                                columnCount += 1
                            else:
                                break
                        elif i == 1:
                            if placed[rows][columns + columnCount] == "HWY":
                                score += 1
                                columnCount -= 1
                            else:
                                break
                    columnCount = -1
                scoreDict["HWY"].append(str(score))
            #MON Counting
            elif placed[rows][columns] == "MON":
                if rows == 1:
                    if columns == 1:
                        cornerCount += 1
                        scoreDict["MON"].append("2")
                    elif columns == gridColumn:
                        cornerCount += 1
                        scoreDict["MON"].append("2")
                    monCount += 1
                elif rows == gridRow:
                    if columns == 1:
                        cornerCount += 1
                        scoreDict["MON"].append("2")
                    elif columns == gridColumn:
                        cornerCount += 1
                        scoreDict["MON"].append("2")
                    monCount += 1
                else:
                    monCount += 1
                    scoreDict["MON"].append("1")
                    
    #FAC Scoring but placed after to ensure all FAC are accounted for before scoring
    if facCount >= 5:
        for i in range(4):
            scoreDict["FAC"].append("4")
        for i in range(facCount - 4):
            scoreDict["FAC"].append("1")
    elif facCount >= 1:
        for i in range(facCount):
            scoreDict["FAC"].append(str(facCount))
    #MON Scoring override
    if cornerCount >= 3:
        scoreDict["MON"].clear()
        for count in range(monCount):
            scoreDict["MON"].append("4")

    #Displays scoring
    finalTotal = 0
    for building in buildings:
        total = 0
        print("{}: ".format(building), end = "")
        for scores in scoreDict[building]:
            total += int(scores)
        if len(scoreDict[building]) > 0:
            print(" + ".join(scoreDict[building]), end = "")
            print(" =", total)
            finalTotal += total
        else:
            print("0")
    print("Total Score:", finalTotal)
    return finalTotal

#function which saves the game into a text file
def saveGame(randBuilding):
    file = open("saveFile.txt", "w")

    file.write(str(turns) + "\n")
    file.write(randBuilding[0] + "," + randBuilding[1] + "\n")
    file.write(str(gridRow) + "," + str(gridColumn) + "\n")
    for building in buildings:
        file.write(building + "," + str(remainingBuildings[building]) + ",")
    file.write("\n")
    for rows in range(gridRow + 2):
        rowSave = ""
        for columns in range(gridColumn + 2):
            rowSave = rowSave + placed[rows][columns] + ","
        file.write(rowSave + "\n")

    file.close()
    print("Game saved!")

#function which loads game from a text file saved by the above function
def loadGame():
    global turns
    file = open("saveFile.txt", "r")
    turns = int(file.readline())
    randBuilding = file.readline()
    randBuilding = randBuilding.strip("\n")
    randBuilding = randBuilding.split(",")
    gridSize = file.readline()
    gridSize = gridSize.strip("\n")
    gridSize = gridSize.split(",")
    global gridRow
    global gridColumn
    gridRow, gridColumn = int(gridSize[0]), int(gridSize[1])
    remainingBuildings = {}
    remain = file.readline()
    remain = remain.strip("\n")
    remain = remain.split(",")
    remain.pop()
    for i in range(5):
        remainingBuildings[remain[i * 2]] = int(remain[i * 2 + 1])
        buildings.append(remain[i * 2])
    gridInit()
    rows = 0
    for line in file:
        line = line.strip("\n")
        buildingRow = line.split(",")
        for columns in range(gridRow + 2):
            placed[rows][columns] = buildingRow[columns]
        rows += 1
    file.close()
    return randBuilding, remainingBuildings

#function that shows highscore for each specific grid size
def showHighscores(highscoreList, row, column):
    print("-" * 9, "HIGH SCORES", "-" * 9)
    print("-" * 8, "FOR GRID {}X{}:".format(row, column), "-" * 8)
    print("{:<4}{:<22}{}".format("Pos", "Player", "Score"))
    print("{:<4}{:<22}{}".format("-" * 3, "-" * 6, "-" * 5))
    for i in range(10):
        try:
            print("{:>2}. {:<25}{}".format(i + 1, highscoreList[i][0], highscoreList[i][1]))
        except:
            print("{:>2}. {:<25}{}".format(i + 1, "-", "--"))
    print("-" * 31)
    print()

#While Loop that runs the whole game
while True:
    choice = mainMenu()
    #Exit Game option
    if choice == "0":
        print("Game Closed.")
        break
    #New Game option
    elif choice in ["1", "2"]:
        remainingBuildings = {}
        if choice == "1":
            randBuilding = []
            #Asks for grid size to be generated
            gridSize = input("Please enter the grid size you would like (separated by 'x' & within 3x3 to 9x9): ").upper()
            while len(gridSize) != 3 or "X" not in gridSize or int(gridSize[0]) not in range(3,10) and int(gridSize[2]) not in range(3,10):
                gridSize = input("Please enter the grid size you would like (separated by 'x' & within 3x3 to 9x9): ")
            gridSize = gridSize.split("X")
            gridRow = int(gridSize[0])
            gridColumn = int(gridSize[1])
            gridInit()
            #Allow user to choose buildings to be in game
            buildings = input("Please Enter 5 buildings out of BCH, FAC, HSE, SHP, HWY, MON (seperated by ','): ").upper()
            buildings = buildings.split(",")
            while len(buildings) != 5 or whetherBuilding(buildings) or buildingDupes(buildings):
                if len(buildings) != 5:
                    print("Buildings entered are more or less than 5")
                elif whetherBuilding(buildings):
                    print("Building entered are not valid buildings")
                else:
                    print("Building entered have duplicates")
                buildings = input("Please Enter 5 buildings out of BCH, FAC, HSE, SHP, HWY, MON (seperated by ','): ").upper()
                buildings = buildings.split(",")
            #Initialise building pool
            for building in buildings:
                remainingBuildings[building] = gridRow * gridColumn // 2
        elif choice == "2":
            #try statement to search for save file to be loaded
            try:
                randBuilding, remainingBuildings = loadGame()
            except:
                print("No file found")
                print()
                continue
        #Main gameplay loop
        for n in range(gridRow * gridColumn):
            gameTurn(turns)
            choice, randBuilding = gameMenu(randBuilding)
            if choice in ["0", "4"]:
                turns = 1
                placed.clear()
                break
            while choice not in ["1", "2"]:
                gameTurn(turns)
                choice, randBuilding = gameMenu(randBuilding)
            turns += 1
        #End of the game
        if turns > (gridRow * gridColumn):
            gameTurn(turns)
            score = scoring()
            highscoreList = []
            position = 1
            #try statement to check if there is any existing highscores for the grid size
            try:
                file = open("highscore{}x{}.txt".format(gridRow, gridColumn), "r")
                for line in file:
                    line = line.strip("\n")
                    line = line.split(",")
                    highscoreList.append([line[0], line[1]])
                for item in range(len(highscoreList)):
                    if score <= int(highscoreList[item][1]):
                        position += 1
                file.close()
            except:
                pass
            #Asking for name to be entered in high score board with input validation
            if position < 10:
                file = open("highscore{}x{}.txt".format(gridRow, gridColumn), "w")
                print("Congratulations! You made the high score board at position {}!".format(str(position)))
                name = input("Please enter your name (max 20 chars): ")
                while len(name) > 20:
                    name = input("Please enter your name (max 20 chars): ")
                highscoreList.insert(position - 1, [name, score])
                print()
                showHighscores(highscoreList, gridRow, gridColumn)
                if len(highscoreList) > 10:
                    highscoreList.pop()
                for item in range(len(highscoreList)):
                    file.write(highscoreList[item][0] + "," + str(highscoreList[item][1]) + "\n")
                file.close()
        break
    #check high scores for all grid sizes
    elif choice == "3":
        for r in range(3,10):
            for c in range(3,10):
                #try statement to check if the high score file for the specific grid size exists
                try:
                    file = open("highscore{}x{}.txt".format(r, c), "r")
                    highscoreList = []
                    for line in file:
                        line = line.strip("\n")
                        line = line.split(",")
                        highscoreList.append([line[0], line[1]])
                    showHighscores(highscoreList, r, c)
                    file.close()
                except:
                    print("No high scores for grid size {}x{}".format(r, c))
                    print()
    #if choices other than 1, 2 or 0 are entered        
    else:
        print("Invalid Selection. Please Try Again.\n")
