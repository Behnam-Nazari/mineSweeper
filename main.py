import Game


#region ++++ Checking the input for the number of rows and columns of the games
while True:
    try:
        rows = int(input("choose the number of rows:"))
        if rows < 1:
            print("Please use the correct range")
            continue
    except Exception:
            print("there was an error")
            continue
    try:
        columns = int(input("choose the number of Columns:"))
        if columns < 1:
            print("Please use the correct range")
            continue
        break
    except Exception:
            print("there was an error")
            continue
#endregion 



if __name__ == "__main__":
    game = Game.Game(rows,columns)
    game.start()