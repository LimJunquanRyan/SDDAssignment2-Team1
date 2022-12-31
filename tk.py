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

def reset():
    for widget in frame.winfo_children():
        widget.destroy()
    
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
    reset()
    ttk.Label(frame, text="Welcome to Ngee Ann City!", width=25).grid(column=0, row=0)
    ttk.Label(frame, text="\n").grid(column=0, row=1)
    ttk.Button(frame, command=gameturn, text="Start New Game!", width=25).grid(column=0, row=2)
    ttk.Label(frame, text="\n").grid(column=0, row=3)
    ttk.Button(frame, command="", text="Load Saved Game! (WIP)", width=25).grid(column=0, row=4)
    ttk.Label(frame, text="\n").grid(column=0, row=5)
    ttk.Button(frame, command="", text="Highscore Board! (WIP)", width=25).grid(column=0, row=6)

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

def addBuilding(build, input_location, grid):
    global coins, turns
    # print(building)
    location = (input_location[:1].upper(), input_location[1:])

    if turns == 1:
        if location not in grid:
            ttk.Label(frame, text="Location is invalid or not on the grid.", anchor="w", width=60, foreground="red").grid(column=COLS + 2, row=9)
        else:
            # update coins, turns and score
            coins -= 1
            turns += 1
            gameTurnInfo()

            # update grid
            grid[location] = buildings[build]
            ttk.Label(frame, image=buildings[build], relief="solid", background="white",).grid(column=ord(location[0])-64, row=int(location[1]))

            # remoive error msg if any
            ttk.Label(frame, text="", anchor="w", width=60).grid(column=COLS + 2, row=9)
            
            # randomize build choices
            buildChoices(grid)
    else:
        if location not in grid:
            ttk.Label(frame, text="Location is invalid or not on the grid.", anchor="w", width=60, foreground="red").grid(column=COLS + 2, row=9)
        elif not checkAdjacency(location, grid):
            ttk.Label(frame, text="Location must be adjacent to existing buildings.", anchor="w", width=60, foreground="red").grid(column=COLS + 2, row=9)
        else:
            if grid[location] != imgEmpty:
                ttk.Label(frame, text="Location already has a building on it.", anchor="w", width=60, foreground="red").grid(column=COLS + 2, row=9)
            else:
                # update coins, turns and score
                coins -= 1
                turns += 1
                gameTurnInfo()

                # update grid
                grid[location] = buildings[build]
                ttk.Label(frame, image=buildings[build], relief="solid", background="white",).grid(column=ord(location[0])-64, row=int(location[1]))

                # remoive error msg if any
                ttk.Label(frame, text="", anchor="w", width=60).grid(column=COLS + 2, row=9)

                # randomize build choices
                buildChoices(grid)

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
    ttk.Button(frame, command=lambda: addBuilding(select.get(),location.get(),grid), text="Place!", width=60).grid(column=COLS + 2, row=8)

    return select

def gameturn():
    reset()
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

menu()
mainloop()
