import random
class Board:
    """
    The board object which is created by the Game object.

    Args:
        rows (int): number of Rows
        columbs (int): number of columns
    
    Attributes:
        rows 
        columns
        board (list[list[str]]): the actuall board which is a list of board's rows and each row list contains column number of cells
        graph (dict{(cell's col,cell's row):[list of it's neighbors]}): a dictionary which has every cell's row and column in a tuple (keys) and a list of it's neighboring cells(value).
        number_of_mines: board's number of mines, which is set by place_mines() function
    """
    def __init__(self, rows:int, columns: int):
        self.rows = rows
        self.columns = columns
        self.board , self.graph = self.create_board()

        
        
        
    def create_board(self):
        """
        Return board and graph after processing

        Returns:
            board, graph
        """
        board = [[0 for i in range(self.columns)] for i in range(self.rows)] # Creates an empty board of size row*column
        board = self.place_mines(board) # Places the mines
        graph = self.get_neighbors(board) # Generates the connections graph
        board = self.generate_numbers(board, graph) # Generates each cell's text (number) according to its neighbors
        return board , graph
    
    def get_neighbors(self, board):
        """
        Generates a crude graph of neighbor's for each cell which might include negative coordinates or coordinates that are bigger than row/columns

        Args:
            board (list[list[str]]): the board of the game

        Returns:
            ouput_dict: the graph of connections between cell's
        """
        neighbors_dict = {}
        for j, row in enumerate(board):
            for i, col in enumerate(row):
                
                neighbors_dict[(i,j)] = [(i+1, j), (i-1, j), (i, j-1), (i, j+1),
                                         (i-1, j+1), (i+1, j+1), (i-1, j-1), (i+1, j-1)] # each cell's coordinates is used as key in the following format (Column,Row)
        output_dict = self.process_neighbors(neighbors_dict) # processes each cell's neighbors to remove the invalid coordinates

        return output_dict

    def process_neighbors(self,graph:dict):
        """
        Return the graph after removing the negative coordinates or the ones that are bigger than board's row or column.

        Args:
            graph (dict): garph of the game

        Returns:
            garph (dict): the processed graph
        """
        for k, neighbors in graph.items():
            n = []
            for cell in neighbors:
                if cell[0] < self.columns and cell[0] >= 0 and cell[1] < self.rows and cell [1] >= 0:
                        n.append(cell)
            graph[k] = n
        return graph
    
    def place_mines(self, board):
        
        """
        Return the board after placing the mines. The number of mines in the board can be altered by changing the number used in the for loop

        Args:
            board (dict): the empty board
        Returns:
            baord (dict):
        """
        n = [] # the list of mines' coordinates
        for i in range(int((0.5)*(self.rows*self.columns))):
            row = random.randint(0,self.rows-1)
            col = random.randint(0,self.columns -1)
            board[row][col] = 'M'
            n.append((row,col))
        self.number_of_mines = len(set(n)) # the board's number of mines is assigned in this stage
        return board
    
    
    def generate_numbers(self,board, graph):
        """
        Generates each cell's number with the use of board's graph

        Args:
            board (list[list[str]]):
            graph (dict):

        Returns:
            board: the board after generating each cell's number of neighboring mines and converting it into a string
        """
        neighbors = graph
        for j, row in enumerate(board):
            for i, col in enumerate(row):
                cell_neighbors = neighbors[(i,j)]
                neighboring_mines = 0
                for cell in cell_neighbors:
                     if (board[cell[1]][cell[0]] == 'M'):
                        neighboring_mines +=1
                if  board[j][i] != "M":   
                    board[j][i] = str(neighboring_mines) # cells' text is a string from now on.
        return board
    

    def __str__(self) -> str:
        """
        Enables the print() funtion for the board. 

        Returns:
            string: the board's user-friendly UI format
        """
        string = ""
        for row in self.board:
            string += str(row) +"\n"
        string += f"number of mines: {self.number_of_mines}"
            
        return string  
                       
                    
if __name__ == "__main__":
    board1 = Board(3,3)
    print(board1)
    
