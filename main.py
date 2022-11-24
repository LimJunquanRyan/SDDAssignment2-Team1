def mainmenu():
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

while True:
    choice = mainmenu()
    #Exit Game option
    if choice == "0":
        print("Game Closed.")
        break