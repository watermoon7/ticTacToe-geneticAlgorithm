# this function looked horrible in the tic tac toe game module so I put it in its own module

def check(board):
        for i in range(3):
            if ((board[0][i] == board[1][i] == board[2][i]) and board[0][i] != 0):
                return board[0][i]
            elif ((board[i][0] == board[i][1] == board[i][2]) and board[i][0] != 0):
                return board[i][0]

        if ((board[0][0] == board[1][1] == board[2][2]) and board[1][1] != 0) or ((board[2][0] == board[1][1] == board[0][2]) and board[1][1] != 0):
            return board[1][1]
        
        if not any(any(o==0 for o in i) for i in board):
            return 3
            
        return 0
