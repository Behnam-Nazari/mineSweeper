import Board
class Game():
    """
    The Game class which includes a board object
    Attributes:
        board : the main and the underlying Board object which will be used to create a player_view 
        graph : the Board object's graph
        player_view : the board that the player sees    
    """
    def __init__(self, rows:int, columns:int) -> None:
        self.board = Board.Board(rows, columns)
        self.graph = self.board.graph
        self.player_view = self.create_player_view()
    
    def select(self,row:int,column:int):
        """
        Checks if the user has lost, and if not, calls the ripple function. 

        Args:
            row (int): cell's row
            column (int): cell's column

        Returns:
            player_view : returns the updated player view
        """
        if self.has_lost(row,column):
            return True
        else:
            self.ripple(row,column)
            
            return self.player_view
        
    def has_lost(self,row:int,column:int):
        """
        Checks if the player has lost by selecting a mine.

        Args:
            row (int): cell's row
            column (int): cell's column

        Returns:
            bool: True if player has lost
        """
        if self.board.board[row][column] == "M":
            return True
        return False
    
    def has_won(self):
        """checks if the remaining hidden cells are all mines

        Returns:
            bool: True if the all the remaining cells are mines
        """
        hidden_cells = 0
        for i, row in enumerate(self.player_view): #goes through all the cell's in the board and counts them if they are hidden.
            for j, cell in enumerate(row):
                if self.player_view[i][j] == "H":
                    hidden_cells +=1
        if hidden_cells == self.board.number_of_mines: # if number of hidden cells is equal to board's number of mines, the player wins.
            return True
        return False
            
        

                  
    def ripple(self,row:int,column:int):
        """
        Carries out the ripple effect after selecting a cell.
        

        Args:
            row (int): cell's row
            column (int): cell's column

        Returns:
            list[list[str]]: the updated player_view
        """
        cleared_cells = self.bfs(row, column) # gets the list of cleared cells from the breadth first search function

        for cell in cleared_cells:
            self.player_view[cell[1]][cell[0]] = self.board.board[cell[1]][cell[0]] 
            #sets the text of player_view to be equal to the underlying board's
        return self.player_view
        
        
        
    def bfs(self, row:int,column:int):
        """
        Bredth first search is used to find the neighboring cells of a selected cell. if the neighboring cells meet certain criteria, they are added to the cleared list, wich is returned.
        The criteria are:
        1. if the source cell(m) is not zero and the neighbor is not zero, then only the source is appended.
        2. if the source is not zero but its neighbor is, the neighbor is appended.
        3. if the soruce is zero, all of its neighbors are added to cleared list

        Args:
            row (int): cell's  row
            column (_type_): cell's column

        Returns:
            list[(column,row)]: the list of all the cells that should be revealled to the user 
        """
        graph = self.graph
        visited = [(column,row)]
        queue = [(column,row)]
        cleared = [(column,row)]
        while queue:
            m = queue.pop(0)
            if m in graph:
                for neighbor in graph[m]:
                    if neighbor not in visited:
                        visited.append(neighbor)     
                        if self.board.board[neighbor[1]][neighbor[0]] == "0":    
                            queue.append(neighbor)
                        if self.board.board[m[1]][m[0]] != "0" and self.board.board[neighbor[1]][neighbor[0]] != "0": # Criteria 1
                            cleared.append(m)
                        if self.board.board[m[1]][m[0]] != "0" and self.board.board[neighbor[1]][neighbor[0]] == "0": # Criteria 2
                            cleared.append(neighbor)
                        if self.board.board[m[1]][m[0]] == "0": # Criteria 3
                            cleared.extend(graph[m])
                        
                            
                        
                          
                            

        cleared = set(cleared) #remove the duplicate coordinates
        return cleared
        
    def create_player_view(self):
        """
        Creates the player view by replacing all the cells with "H"

        Returns:
            list[list[str]]: the board that the player sees at the beggining of the game.
        """
        player_board = [["H" for i in range((self.board.columns))] for i in range((self.board.rows))]
        return player_board
    
    def __str__(self):
        """
        Enables the print function for the class to print the player_view
        """
        string = "\n"
        for row in self.player_view:
            string += str(row) +"\n" 
        return(string)
     
    def start(self):
        """
        The start Function for the game to be used for the command line
        """
        print(self.board)
        print(self)
        while True:
            
            #region ++++ Checking the input ++++
            try:
                row = int(input("select a row:")) - 1
                if row > self.board.rows - 1 or row < 0:
                    print("Please use the correct range")
                    continue
            except Exception:
                print("there was an error")
                continue
                
            try:
                col = int(input("select a column:")) - 1
                if col > self.board.columns - 1 or col < 0:
                    print("Please use the correct range")
                    continue
            except Exception:
                print("there was an error")
                continue
            
            if self.player_view[row][col] != "H":
                print("This cell is already discovered! Choose another one.")
                continue
            #endregion
            
            self.select(row,col)
            
            if self.has_lost(row,col):
                print("\n\t"+"*"*8)
                print("\t"+"You Lost!")
                print("\t"+"*"*8)
                break
            print(self)
            if self.has_won():
                print("\n\t"+"*"*8)
                print("\t"+"You Won!")
                print("\t"+"*"*8)
                break
            
    