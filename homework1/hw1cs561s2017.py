#------ CSCI 561 Homework #1 - Ahmad Fallahpour
import copy as mycopy

def change_player(A):
    if A == 'X':
        return 'O'
    else:
        return 'X'

def grid_number_to_name(Number):
    GridName = [['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'], ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
                ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'], ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
                ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'], ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
                ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'], ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']]
    return GridName[Number[0]][Number[1]]

def valid_move_finder(Board, Player):
    Possible_Moves = []
    for i in range(0,8):
        for j in range(0,8):
            if Board[i][j] == change_player(Player):
                if Board[i-1][j-1]=='*' and Board[i+1][j+1]==Player:
                    Possible_Moves.append([i-1,j-1])
                if Board[i][j-1]=='*' and Board[i][j+1]==Player:
                    Possible_Moves.append([i,j - 1])
                if Board[i+1][j-1]=='*' and Board[i-1][j+1]==Player:
                    Possible_Moves.append([i + 1,j - 1])
                if Board[i-1][j]=='*' and Board[i+1][j]==Player:
                    Possible_Moves.append([i - 1,j])
                if Board[i+1][j]=='*' and Board[i-1][j]==Player:
                    Possible_Moves.append([i+1,j])
                if Board[i-1][j+1]=='*' and Board[i+1][j-1]==Player:
                    Possible_Moves.append([i-1,j + 1])
                if Board[i][j+1]=='*' and Board[i][j-1]==Player:
                    Possible_Moves.append([i,j + 1])
                if Board[i+1][j+1]=='*' and Board[i-1][j-1]==Player:
                    Possible_Moves.append([i + 1,j+1])
    Possible_Moves.sort()
    return Possible_Moves

def result(state,a):
    next2 = mycopy.deepcopy(state)
    next2[2][2] = "A"
    return next2

def update_board(Board, Player, Move):
    Updated_Board = mycopy.deepcopy(Board)
    Updated_Board[Move[0]][Move[1]]=Player
    if Board[Move[0]-1][Move[1]-1] == change_player(Player) and Board[Move[0]-2][Move[1]-2]==Player:
        Updated_Board[Move[0]-1][Move[1]-1]=Player
    if Board[Move[0]][Move[1]-1] == change_player(Player) and Board[Move[0]][Move[1]-2]==Player:
        Updated_Board[Move[0]][Move[1] - 1] = Player
    if Board[Move[0]+1][Move[1]-1] == change_player(Player) and Board[Move[0]+2][Move[1]-2]==Player:
        Updated_Board[Move[0]+1][Move[1]-1]=Player
    if Board[Move[0]-1][Move[1]] == change_player(Player) and Board[Move[0]-2][Move[1]]==Player:
        Updated_Board[Move[0]-1][Move[1]] = Player
    if Board[Move[0]+1][Move[1]] == change_player(Player) and Board[Move[0]+2][Move[1]]==Player:
        Updated_Board[Move[0]+1][Move[1]]=Player
    if Board[Move[0]-1][Move[1]+1] == change_player(Player) and Board[Move[0]-2][Move[1]+2]==Player:
        Updated_Board[Move[0]-1][Move[1] + 1] = Player
    if Board[Move[0]][Move[1]+1] == change_player(Player) and Board[Move[0]][Move[1]+2]==Player:
        Updated_Board[Move[0]][Move[1]+1]=Player
    if Board[Move[0]+1][Move[1]+1] == change_player(Player) and Board[Move[0]+2][Move[1]+2]==Player:
        Updated_Board[Move[0]+1][Move[1] + 1] = Player
    return Updated_Board

def terminal_test(Depth, Cut_off_depth):
    if Depth < Cut_off_depth:
        return 0
    else:
        return 1

def utility(state, Player):
    GridValue = [[99, -8, 8, 6, 6, 8, -8, 99], [-8, -24, -4, -3, -3, -4, -24, -8],
                [8, -4, 7, 4, 4, 7, -4, 8], [6, -3, 4, 0, 0, 4, -3, 6],
                [6, -3, 4, 0, 0, 4, -3, 6], [8, -4, 7, 4, 4, 7, -4, 8],
                [-8, -24, -4, -3, -3, -4, -24, -8], [99, -8, 8, 6, 6, 8, -8, 99]]
    Utility = 0
    for i in range(0,8):
        for j in range(0,8):
            if state[i][j] == Player:
                Utility = Utility + GridValue[i][j]
            elif state[i][j] == change_player(Player):
                Utility = Utility - GridValue[i][j]
    return  Utility

def max_value(state, alpha, beta, Player, Depth, Cut_off_depth):
    if terminal_test(Depth, Cut_off_depth):
        return utility(state, Player)
    else:
        Depth += 1
        v = float("-inf")
        Possible_Moves = valid_move_finder(state, Player)
        if len(Possible_Moves)==0:
            Player = change_player(Player)

        else:
            for i in range(0, len(Possible_Moves)):
                Updated_Board = update_board(state, Player, Possible_Moves[i])
                v = max(v, min_value(Updated_Board, alpha, beta, change_player(Player), Depth, Cut_off_depth))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            Depth -= 1
            return v

def min_value(state, alpha, beta, Player, Depth, Cut_off_depth):
    if terminal_test(Depth, Cut_off_depth)==1:
        return utility(state, Player)
    else:
        Depth += 1
        v = float("inf")
        Possible_Moves = valid_move_finder(state, Player)
        if len(Possible_Moves) == 0:
            Player = change_player(Player)
            Depth += 1
        else:
            for i in range(0, len(Possible_Moves)):
                Updated_Board = update_board(state, Player, Possible_Moves[i])
                v = min(v, max_value(Updated_Board, alpha, beta, change_player(Player), Depth, Cut_off_depth))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            Depth -= 1
            return v


#------ Open the file and read the content
f = open('./Sample Test Cases/Test Case 1/input.txt','r')
Content = f.read().splitlines()
Player = Content[0]
if Player == 'X':
    Opponent = 'O'
else:
    Opponent = 'X'
Cut_off_depth = int(Content[1])
Board = Content[2:]
for i in range(0,8):
    Board[i]= list(Board[i])

#------ Main Function
Depth = 0
alpha = float("-inf")
beta = float("inf")
state = mycopy.deepcopy(Board)

v = max_value(state, alpha, beta, Player, Depth, Cut_off_depth)
