from bot_class import happyBot, randomBot
from check import check
import numpy, random, time


def game(player1, player2):
  
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    dictionary = {0:'-',1:'X',2:'O',3:'Draw'}

    order = [player1, player2]
    random.shuffle(order)
    
    player = 1
    while True:
        # make a move and edit the board
        # each element in the list order is on object each with the method 'play' which returns where on the board to play
        board[order[player-1].play(board, player)] = player

        player = 1 if player == 2 else 2
        #print('\n'.join([str(board[i*3:(i+1)*3]) for i in range(3)]))

        temp = check(numpy.array(board).reshape((3,3)))
        if temp != 0:
            #print(dictionary[temp] + (" won!" if temp != 3 else '.'))
            
            return (board, (order.index(player1)+1, temp))


