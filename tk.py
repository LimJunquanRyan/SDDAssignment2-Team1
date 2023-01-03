from tkinter import *
from tkinter import ttk
import random

ROWS = 20
COLS = 20

turns = 1
coins = 16
score = 0

parent = Tk()
width= parent.winfo_screenwidth()               
height= parent.winfo_screenheight()               
parent.geometry("%dx%d" % (width, height))
parent.title("Ngee Ann City")
frame = ttk.Frame(parent)
frame.grid(column=0, row=0)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
parent.columnconfigure(0, weight=1)
parent.rowconfigure(0, weight=1)
imgEmpty = PhotoImage(height=24, width=24)
imgResidential = PhotoImage(file="./assets/residential.png", height=24, width=24)
imgIndustry = PhotoImage(file="./assets/industry.png", height=24, width=24)
imgCommercial = PhotoImage(file="./assets/commercial.png", height=24, width=24)
imgPark = PhotoImage(file="./assets/park.png", height=24, width=24)
imgRoad = PhotoImage(file="./assets/road.png", height=24, width=24)

buildings = {'Residential':imgResidential, 'Industry':imgIndustry, 'Commercial':imgCommercial, 'Park':imgPark, 'Road':imgRoad}

def clearWidgets():
    for widget in frame.winfo_children():
        widget.destroy()
    
def resetVars():
    # reset variables
    global turns, coins, score
    turns = 1
    coins = 16
    score = 0

def initGrid(rows, cols):
    # initialize grid dictionary
    grid = {}

    # adds grid elements into grid dictionary with alphanumeric keys
    for i in range(rows):
        for j in range(cols):
            grid[(chr(65+j), str(i+1))] = imgEmpty
    
    return grid

def menu():
    clearWidgets()
    resetVars()
    ttk.Label(frame, text="Welcome to Ngee Ann City!", width=25).grid(column=0, row=0)
    ttk.Label(frame, text="\n").grid(column=0, row=1)
    ttk.Button(frame, command=gameturn, text="Start New Game!", width=25).grid(column=0, row=2)
    ttk.Label(frame, text="\n").grid(column=0, row=3)
    ttk.Button(frame, command="", text="Load Saved Game! (WIP)", width=25).grid(column=0, row=4)
    ttk.Label(frame, text="\n").grid(column=0, row=5)
    ttk.Button(frame, command=highscoreBoard, text="Highscore Board!", width=25).grid(column=0, row=6)

def selected(building):
    selection = f"You have selected {building}. Please enter a valid location below."
    ttk.Label(frame, text=selection, anchor="w", width=60).grid(column=COLS + 2, row=6)
    frame.grid

def getRandomBuildChoice():

    # gets random building from building dictionary
    randBuild1 = random.choice(list(buildings.items()))
    randBuild2 = random.choice(list(buildings.items()))

    # ensure each building option is different
    while randBuild2 == randBuild1:
        randBuild2 = random.choice(list(buildings.items()))

    return randBuild1, randBuild2

def gameUpdate(build, input_location, grid):
    global coins, turns, score
    # print(building)
    location = (input_location[:1].upper(), input_location[1:])

    if turns == 1:
        if location not in grid:
            ttk.Label(frame, text="Location is invalid or not on the grid.", anchor="w", width=60, foreground="red").grid(column=COLS + 2, row=9)
        else:
            # update grid
            grid[location] = buildings[build]
            ttk.Label(frame, image=buildings[build], relief="solid", background="white",).grid(column=ord(location[0])-64, row=int(location[1]))

            # generate coins
            coins = gainCoin(build, location, coins, grid)
            
            # update coins, turns and score
            coins -= 1
            turns += 1
            score = scoring(grid)
            gameTurnInfo()

            # remoive error msg if any
            ttk.Label(frame, text="", anchor="w", width=60).grid(column=COLS + 2, row=9)
            
            # randomize build choicesscore
            buildChoices(grid)
            
            # endgame
            if coins <= 0 or turns > ROWS * COLS:
                turns -= 1
                endGame(grid)
    else:
        if location not in grid:
            ttk.Label(frame, text="Location is invalid or not on the grid.", anchor="w", width=60, foreground="red").grid(column=COLS + 2, row=9)
        elif not checkAdjacency(location, grid):
            ttk.Label(frame, text="Location must be adjacent to existing buildings.", anchor="w", width=60, foreground="red").grid(column=COLS + 2, row=9)
        else:
            if grid[location] != imgEmpty:
                ttk.Label(frame, text="Location already has a building on it.", anchor="w", width=60, foreground="red").grid(column=COLS + 2, row=9)
            else:
                # update grid
                grid[location] = buildings[build]
                ttk.Label(frame, image=buildings[build], relief="solid", background="white",).grid(column=ord(location[0])-64, row=int(location[1]))

                # generate coins
                coins = gainCoin(build, location, coins, grid)
                
                # update coins, turns and score
                coins -= 1
                turns += 1
                score = scoring(grid)
                gameTurnInfo()

                # remoive error msg if any
                ttk.Label(frame, text="", anchor="w", width=60).grid(column=COLS + 2, row=9)

                # randomize build choices
                buildChoices(grid)

                # endgame
                if coins <= 0 or turns > ROWS * COLS:
                    turns -= 1
                    endGame(grid)

def checkAdjacency(location, grid): # BUG - Adjacency error, could place buildings not adjacent on outermost of grid (fixed by changing outer values slightly)
    check = ['N', 'N', 'N', 'N']
    if 1 <= int(location[1]) + 1 <= ROWS and 65 <= ord(location[0]) <= 65 + COLS - 1: # BUG - Out Of Range (fixed by changing static value to dynamic value)
        if grid[chr(ord(location[0])), str(int(location[1]) + 1)] not in buildings.values():
            check[0] = 'Y'
    else:
        check[0] = 'Y'
    if 1 <= int(location[1]) <= ROWS and 65 <= ord(location[0]) - 1 <= 65 + COLS - 1:
        if grid[chr(ord(location[0]) - 1), str(int(location[1]))] not in buildings.values():
            check[1] = 'Y'
    else:
        check[1] = 'Y'
    if 1 <= int(location[1]) - 1 <= ROWS and 65 <= ord(location[0]) <= 65 + COLS - 1:
        if grid[chr(ord(location[0])), str(int(location[1]) - 1)] not in buildings.values():
            check[2] = 'Y'
    else:
        check[2] = 'Y'
    if 1 <= int(location[1]) <= ROWS and 65 <= ord(location[0]) + 1 <= 65 + COLS - 1:
        if grid[chr(ord(location[0]) + 1), str(int(location[1]))] not in buildings.values():
            check[3] = 'Y'
    else:
        check[3] = 'Y'
    if check[0] == 'Y' and check[1] == 'Y' and check[2] == 'Y' and check[3] == 'Y':
        return False
    else:
        return True

def gainCoin(build, location, coins, grid): # BUG - Gain Infinite Coins (fixed by changing the way coins were updated)
    if build == 'Residential' or build == 'Commercial' or build == 'Industry':

        # get each adjacent location
        left = ( chr(ord(location[0])-1), str(int(location[1])) )
        right = ( chr(ord(location[0])+1), str(int(location[1])) )
        top = ( chr(ord(location[0])), str(int(location[1])-1) )
        bottom = ( chr(ord(location[0])), str(int(location[1])+1) )
        
        adjacent_sqrs = [left, right, top, bottom]

        # check adjacent location based on if building is I, R or C
        if build == 'Industry' or build == 'Commercial':
            for plot in adjacent_sqrs:
                if plot in grid.keys() and grid[plot] == imgResidential:
                    coins +=1
        else:
            for plot in adjacent_sqrs:
                if plot in grid.keys() and (grid[plot] == imgIndustry or grid[plot] == imgCommercial):
                    coins +=1

    return coins

def scoring(grid):
    # set score
    score = 0
    ind_score = 0

    for plot in grid:
        # check if plot is empty or not
        if grid[plot] == imgEmpty:
            continue
        else:
            # get each adjacent location
            left = ( chr(ord(plot[0])-1), str(int(plot[1])) )
            right = ( chr(ord(plot[0])+1), str(int(plot[1])) )
            top = ( chr(ord(plot[0])), str(int(plot[1])-1) )
            bottom = ( chr(ord(plot[0])), str(int(plot[1])+1) )

            adjacent_sqrs = [left, right, top, bottom]

            # residential
            if grid[plot] == imgResidential:
                res_score = 1

                for adj_plot in adjacent_sqrs:
                    if adj_plot not in grid.keys():
                        continue
                    elif grid[adj_plot] == imgIndustry:
                        res_score = 1
                        break
                    elif grid[adj_plot] == imgResidential or grid[adj_plot] == imgCommercial:
                        res_score += 1
                    elif grid[adj_plot] == imgPark:
                        res_score += 2
                
                # print("res: ",res_score)
                score += res_score
            # industry
            elif grid[plot] == imgIndustry:
                if ind_score == 0:
                    for ind in grid:
                        if grid[ind] == imgIndustry:
                            ind_score += 1
                    
                    # print("ind: ", ind_score*ind_score)
                    score += (ind_score * ind_score)
            # commercial & park
            elif grid[plot] == imgCommercial or grid[plot] == imgPark:
                com_park_score = 1

                for adj_plot in adjacent_sqrs:
                    if adj_plot not in grid.keys():
                        continue
                    elif grid[adj_plot] == grid[plot]:
                        com_park_score += 1
                
                # print("compark: ", com_park_score)
                score += com_park_score
            # road
            elif grid[plot] == imgRoad:
                rd_score = 1

                # checking left adjacency
                if left in grid.keys():
                    for i in range(1, ROWS):
                        left_plot = (chr(ord(plot[0])-i), plot[1])
                        if left_plot not in grid.keys() or grid[left_plot] != imgRoad:
                            break
                        else:
                            rd_score += 1
                
                # checking right adjacency
                if right in grid.keys():
                    for i in range(1, ROWS):
                        right_plot = (chr(ord(plot[0])+i), plot[1])
                        if right_plot not in grid.keys() or grid[right_plot] != imgRoad:
                            break
                        else:
                            rd_score += 1
                
                # print("rd: ", rd_score)
                score += rd_score
            
    return score

def endGame(grid):
    clearWidgets()

    # grid
    for column in range(1, COLS + 1):
        ttk.Label(frame, text=chr(64+column)).grid(column=column, row=0)
    for row in range(1, ROWS + 1):
        ttk.Label(frame, text=f"{row}  ", anchor="e", width=3).grid(column=0, row=row)
        for column in range(1, COLS + 1):   
            ttk.Label(frame, image=grid[chr(64+column),str(row)], relief="solid", background="white").grid(column=column, row=row)
    
    ttk.Label(frame, width=5).grid(column=COLS + 1, row=0)
    ttk.Label(frame, text="Ngee Ann City Builder", anchor="w", width=60).grid(column=COLS + 2, row=0)

    # game info like turns, coins and score
    gameTurnInfo()

    ttk.Label(frame, text="End of game", width=60, anchor="center").grid(column=COLS + 2, row=8)
    ttk.Label(frame, text="Thank you for playing!", width=60, anchor="center").grid(column=COLS + 2, row=9)

    #Highscore entry
    highscoreCheck()

    ttk.Button(frame, command=menu, text="Exit to Main Menu", width=60).grid(column=COLS + 2, row=20)

def gameTurnInfo():
    ttk.Label(frame, text=f"Turns: {turns}", anchor="w", width=60).grid(column=COLS + 2, row=1)
    ttk.Label(frame, text=f"Coins: {coins}", anchor="w", width=60).grid(column=COLS + 2, row=2)
    ttk.Label(frame, text=f"Score: {score}", anchor="w", width=60).grid(column=COLS + 2, row=3)

def buildChoices(grid, randBuild1=None, randBuild2=None):
    select = StringVar()

    # for saved files
    if randBuild1 is None:
        randBuild1, randBuild2 = getRandomBuildChoice()

    ttk.Radiobutton(frame, command=lambda: selected(select.get()), text=f"Build a {randBuild1[0]}", variable = select, value=randBuild1[0], width=57).grid(column=COLS + 2, row=4)
    ttk.Radiobutton(frame, command=lambda: selected(select.get()), text=f"Build a {randBuild2[0]}", variable = select, value=randBuild2[0], width=57).grid(column=COLS + 2, row=5)
    ttk.Label(frame, text="Select a building", anchor="w", width=60).grid(column=COLS + 2, row=6)

    location = StringVar()
    ttk.Entry(frame, textvariable=location, width=60).grid(column=COLS + 2, row=7)
    ttk.Button(frame, command=lambda: gameUpdate(select.get(),location.get(),grid), text="Place!", width=60).grid(column=COLS + 2, row=8)

    return select

def gameturn():
    clearWidgets()
    resetVars()
    game_grid = initGrid(ROWS, COLS)
    for column in range(1, COLS + 1):
        ttk.Label(frame, text=chr(64+column)).grid(column=column, row=0)
    for row in range(1, ROWS + 1):
        ttk.Label(frame, text=f"{row}  ", anchor="e", width=3).grid(column=0, row=row)
        for column in range(1, COLS + 1):   
            ttk.Label(frame, image=game_grid[chr(64+column),str(row)], relief="solid", background="white").grid(column=column, row=row)
    ## ttk.Label(frame, image=imgEmpty).grid(column=0, row=0)
    ttk.Label(frame, width=5).grid(column=COLS + 1, row=0)
    ttk.Label(frame, text="Ngee Ann City Builder", anchor="w", width=60).grid(column=COLS + 2, row=0)

    # game info like turns, coins and score
    gameTurnInfo()

    # building choices
    buildChoices(game_grid)
    
    ttk.Button(frame, command="", text="Save Game (WIP)", width=60).grid(column=COLS + 2, row=19)
    ttk.Button(frame, command=menu, text="Exit to Main Menu", width=60).grid(column=COLS + 2, row=20)

def highscoreCheck():
    highscoreList = []
    position = 1
    #try statement to check if there is any existing highscores for the grid size
    try:
        file = open("highscore{}x{}.txt".format(ROWS, COLS), "r")
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
    highscoreEntry(highscoreList, position)

def highscoreEntry(highscoreList, position):
    #Asking for name to be entered in high score board with input validation
    if position < 10:
        file = open("highscore{}x{}.txt".format(ROWS, COLS), "w")
        ttk.Label(frame, text=f"Congratulations! You made the high score board at position {position}!", width=60, anchor="center").grid(column=COLS + 2, row=10)
        ttk.Label(frame, text="Please enter your name: ", width=60, anchor="center").grid(column=COLS + 2, row=11)
        name = StringVar()
        ttk.Entry(frame, textvariable=name, width=60).grid(column=COLS + 2, row=12)
        ttk.Button(frame, text="Submit Name!", command=lambda: highscoreInsert(highscoreList, position, file, name.get())).grid(column=COLS + 2, row=13)
        
def highscoreInsert(highscoreList, position, file, name):
    highscoreList.insert(position - 1, [name, score])
    showHighscores(highscoreList, ROWS, COLS)
    if len(highscoreList) > 10:
        highscoreList.pop()
    for item in range(len(highscoreList)):
        file.write(highscoreList[item][0] + "," + str(highscoreList[item][1]) + "\n")
    file.close()

#function that shows highscore for each specific grid size
def showHighscores(highscoreList, row, column):
    clearWidgets()
    ttk.Label(frame, text="HIGH SCORES", width=15, anchor="center").grid(column=1, row=0)
    ttk.Label(frame, text=f"FOR GRID {row}x{column}:", width=25, anchor="center").grid(column=1, row=1)
    ttk.Label(frame, text="\n").grid(column=1, row=2)
    ttk.Label(frame, text="Position", width=15, anchor="w").grid(column=0, row=3)
    ttk.Label(frame, text="Player", width=15, anchor="center").grid(column=1, row=3)
    ttk.Label(frame, text="Score", width=15, anchor="e").grid(column=2, row=3)
    ttk.Label(frame, text="\n").grid(column=1, row=4)
    for i in range(10):
        try:
            ttk.Label(frame, text=f"{i + 1}", width=15, anchor="w").grid(column=0, row=i + 5)
            ttk.Label(frame, text=f"{highscoreList[i][0]}", width=15, anchor="center").grid(column=1, row=i + 5)
            ttk.Label(frame, text=f"{highscoreList[i][1]}", width=15, anchor="e").grid(column=2, row=i + 5)
        except:
            ttk.Label(frame, text=f"{i + 1}", width=15, anchor="w").grid(column=0, row=i + 5)
            ttk.Label(frame, text="-", width=15, anchor="center").grid(column=1, row=i + 5)
            ttk.Label(frame, text="-", width=15, anchor="e").grid(column=2, row=i + 5)
    ttk.Label(frame, text="\n").grid(column=1, row=19)
    ttk.Button(frame, text="Return to Main Menu", width=20, command=menu).grid(column=1, row=20)

def highscoreBoard():
    #try statement to check if the high score file for the specific grid size exists
    try:
        file = open("highscore{}x{}.txt".format(ROWS, COLS), "r")
        highscoreList = []
        for line in file:
            line = line.strip("\n")
            line = line.split(",")
            highscoreList.append([line[0], line[1]])
        file.close()
        showHighscores(highscoreList, ROWS, COLS)
    except:
        print("No high scores for grid size {}x{}".format(ROWS, COLS))
        print()

menu()
mainloop()
