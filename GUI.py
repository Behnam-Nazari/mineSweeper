import tkinter as tk
import tkinter.messagebox as MS
import Game

    

class App():
    """
    The App object which instantiates a game object and and creates a GUI based on that
    
    Attribues:
        game (list[list[str]]): the game object on which the GUI is based on.
        buttons (list[list[tkinter.Button]]): list of the the buttons that are used in the game 
        
    """
    def __init__(self,parent,rows,cols) -> None:
        self.root = parent
        self.rows = rows
        self.columns = cols
        self.game = Game.Game(rows,cols)
        print(self.game.board)
        self.buttons = []
        self.create_gui_board()

        
    def create_gui_board(self):
        """
        Create the gui of the game by creating buttons
        """
        for i, rows in enumerate(self.game.player_view):
            row = []
            for j, cell in enumerate(rows):
                button = tk.Button(self.root,text=cell,command=lambda row = i, col =j : self.click(row,col),
                                   height=2, width=3)
                button.grid(row=i,column=j)
                row.append(button)
            self.buttons.append(row)
    
    def update_board(self,result):
        """
        Updates the board after selecting a cell

        Args:
            result (list[list[str]]): the new state of the game's player_view
        """
        for i, row in enumerate(result):
            for j, cell in enumerate(row):
                if cell == "0":
                    # the buttons representing blank cells are updtaded and disabled
                    self.buttons[i][j].config(text= "0", bg= "gray",state= "disabled",disabledforeground="black")
                    
                elif cell =="M":
                    # if a mine was selected, the button will turn red
                    self.buttons[i][j].config(text= "M", bg= "red")
                elif cell != "H":
                    # the buttons representing numbered cells are updtaded and disabled
                    self.buttons[i][j].config(text= cell, bg= "green",state="disabled",disabledforeground="black")
                
    def click(self,row:int,column:int):
        """
        The click function that is used for buttons' command attribute

        Args:
            row (int): button's row
            column (int): button's column
        """
        result = self.game.ripple(row,column)
        self.update_board(result)
        
        if self.game.has_lost(row,column):
            # If the game is lost, a message show up asking to restrt or quit
            response = MS.askyesno("You lost!", "Do You Want to play again?")
            if response:
                self.restart_game()
            else:
                self.root.quit()
        
        if self.game.has_won():
            # If the game is won, a message show up asking to restrt or quit
            response = MS.askyesno("You Won!", "Do You Want to play again?")
            if response:
                self.restart_game()
            else:
                self.root.quit()
        
            
    def restart_game(self):
        """
        Restart the game if the player chooses to.
        """
        self.game = Game.Game(self.rows,self.columns)
        for b_row in self.buttons:
            for button in b_row:
                button.config(text="H",bg="SystemButtonFace",state="normal")
        print(self.game.board)
        


    
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root,3,8)
    # root.after(100,App.update)
    root.mainloop()