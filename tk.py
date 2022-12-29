from tkinter import *
from tkinter import ttk

ROWS = 20
COLS = 20

turns = 1
coins = 16
score = 10

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

def clear():
    for widget in frame.winfo_children():
        widget.destroy()

def menu():
    clear()
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

#need to be integrated
def checkAdj(building, location):
    print(building)
    if False:
        
        ttk.Label(frame, text="Invalid Location", anchor="w", width=60).grid(column=COLS + 2, row=9)
    else:
        if building == "Residential":
            ttk.Label(frame, image=imgResidential, relief="solid", background="white",).grid(column=ord(location[0])-64, row=int(location[1:]))
        elif building == "Industry":
            ttk.Label(frame, image=imgIndustry, relief="solid", background="white",).grid(column=ord(location[0])-64, row=int(location[1:]))
        elif building == "Commercial":
            ttk.Label(frame, image=imgCommercial, relief="solid", background="white",).grid(column=ord(location[0])-64, row=int(location[1:]))
        elif building == "Park":
            ttk.Label(frame, image=imgPark, relief="solid", background="white",).grid(column=ord(location[0])-64, row=int(location[1:]))
        elif building == "Road":
            ttk.Label(frame, image=imgRoad, relief="solid", background="white",).grid(column=ord(location[0])-64, row=int(location[1:]))

def gameturn():
    clear()
    for column in range(1, COLS + 1):
        ttk.Label(frame, text=chr(64+column)).grid(column=column, row=0)
    for row in range(1, ROWS + 1):
        ttk.Label(frame, text=f"{row}  ", anchor="e", width=3).grid(column=0, row=row)
        for column in range(1, COLS + 1):   
            ttk.Label(frame, image=imgEmpty, relief="solid", background="white").grid(column=column, row=row)
    ttk.Label(frame, image=imgEmpty).grid(column=0, row=0)
    ttk.Label(frame, width=5).grid(column=COLS + 1, row=0)
    ttk.Label(frame, text="Ngee Ann City Builder", anchor="w", width=60).grid(column=COLS + 2, row=0)
    ttk.Label(frame, text=f"Turns: {turns}", anchor="w", width=60).grid(column=COLS + 2, row=1)
    ttk.Label(frame, text=f"Coins: {coins}", anchor="w", width=60).grid(column=COLS + 2, row=2)
    ttk.Label(frame, text=f"Score: {score}", anchor="w", width=60).grid(column=COLS + 2, row=3)
    select = StringVar()
    ttk.Radiobutton(frame, command=lambda: selected(select.get()), text="Building 1", variable = select, value="Commercial", width=57).grid(column=COLS + 2, row=4)
    ttk.Radiobutton(frame, command=lambda: selected(select.get()), text="Building 2", variable = select, value="Industry", width=57).grid(column=COLS + 2, row=5)
    instruction = ttk.Label(frame, text="Select a building", anchor="w", width=60).grid(column=COLS + 2, row=6)
    location = StringVar()
    ttk.Entry(frame, textvariable=location, width=60).grid(column=COLS + 2, row=7)
    ttk.Button(frame, command=lambda: checkAdj(select.get(),location.get()), text="Place! (does not check for adjacency yet)", width=60).grid(column=COLS + 2, row=8)
    ttk.Button(frame, command="", text="Save Game (WIP)", width=60).grid(column=COLS + 2, row=19)
    ttk.Button(frame, command=menu, text="Exit to Main Menu", width=60).grid(column=COLS + 2, row=20)

menu()
mainloop()
