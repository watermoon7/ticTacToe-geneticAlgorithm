import numpy
import random
from copy import deepcopy

class happyBot():

    def __init__(self, gen='', bot=''):
        self.layer1 = numpy.array([numpy.random.randn(90)]).reshape((9,10))
        self.layer2 = numpy.array([numpy.random.randn(100)]).reshape((10,10))
        self.layer3 = numpy.array([numpy.random.randn(90)]).reshape((10,9))
        self.layers = [self.layer1, self.layer2, self.layer3]

        self.ID = f'G_{gen} B_{bot}'

    def ReLU(self, n):
        return numpy.array([max(0, i) for i in n])
        
    def sigmoid(self, n):
        return numpy.array([1/(1+numpy.exp(-x)) for x in n])
        #return 1/(1+numpy.exp(-n))

    def change_ID(self, gen, bot):
        self.ID = f'G_{gen} B_{bot}'

    def change_genetic_code(self, layer1, layer2, layer3):
        self.layer1 = layer1
        self.layer2 = layer2
        self.layer3 = layer3
        self.layers = [self.layer1, self.layer2, self.layer3]

    def evolve(self):
        for layer in self.layers:
            x, y = layer.shape
            num_changes = random.randint(5, 10)
            for _ in range(num_changes):
                layer[random.randint(0, x-1)][random.randint(0, y-1)] += random.randint(-50, 50)/random.randint(40, 100)
            layer = self.sigmoid(layer)

    def play(self, inputs, player):
        temp = inputs

        for layer in self.layers:
            temp = numpy.dot(temp, layer)

        # a sorted list of tuples
        # each tuple contains the original input and its correspondant weight
        zipped_list = sorted(zip(inputs, temp), key = lambda x: x[1], reverse = True)
        
        for element in zipped_list:
            if element[0] == 0:
                return list(temp).index(element[1])

        raise Exception(f"No possible move with inputted board \n{inputs}")

class randomBot():

    # (random bot got an upgrade)
    def play(self, inputs, player):
        
        # Order of operations:
        #   - search for a winning move
        #   - search to block the opponent from winning
        #   - depending on probabilities, the bot either:
        #      - tries to play in the center
        #      - tries to play in a corner
        #      - tries to play in the middle of the edges

        board = [inputs[:3],inputs[3:6],inputs[6:]]
        #print('\n'.join(str(i) for i in board))

        opponent = 1 if player == 2 else 2
        
        lines = (
            ((0, 0), (0, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2)),
            ((2, 0), (2, 1), (2, 2)),
            ((0, 0), (1, 0), (2, 0)),
            ((0, 1), (1, 1), (2, 1)),
            ((0, 2), (1, 2), (2, 2)),
            ((0, 0), (1, 1), (2, 2)),
            ((0, 2), (1, 1), (2, 0)),
        )

        combinations = ((0, 1),(1, 2),(0, 2))

        def other(comb):
            return 0 if 0 not in comb else 1 if 1 not in comb else 2
      
        # searching for a winning move
        for i in lines:
            l = [board[i[o][0]][i[o][1]] for o in range(3)]
            if l.count(player) == 2:
                for comb in combinations:
                    if board[i[comb[0]][0]][i[comb[0]][1]] == board[i[comb[1]][0]][i[comb[1]][1]] == player and board[i[other(comb)][0]][i[other(comb)][1]] == 0:
                        multiplier = other(comb)
                        return i[multiplier][0]*3+i[multiplier][1]
                      
        # searching to block the opponend from winning
        for i in lines:
            l = [board[i[o][0]][i[o][1]] for o in range(3)]
            if l.count(opponent) == 2:
                for comb in combinations:
                    if board[i[comb[0]][0]][i[comb[0]][1]] == board[i[comb[1]][0]][i[comb[1]][1]] == opponent and board[i[other(comb)][0]][i[other(comb)][1]] == 0:
                        multiplier = other(comb)
                        return i[multiplier][0]*3+i[multiplier][1]
        
        # plays the center
        def one():
            if inputs[4] == 0:
                return 4
        
        # plays a corner
        def two():
            if any(inputs[i] == 0 for i in [0, 2, 6, 8]):
                return random.choice([[0, 2, 6, 8][i] for i in range(4) if inputs[[0, 2, 6, 8][i]] == 0])
        
        # plays the middle of an edge
        def three():
            return random.choice([i for i in range(len(inputs)) if inputs[i] == 0])
        
        # mixes the functions in order of operation based on percentage probabilities
        funcs = (one, two, three)
        # function one has a 55% chance of being first, function two has a 35% chance etc.
        order = (55, 35, 10)

        choice = random.randint(1, 100)
        if 1 <= choice < order[0]:
            pass
        elif order[0] <= choice < order[1]:
            if random.randint(1, 5) == 1:
                funcs = (funcs[1], funcs[0], funcs[2])
            else:
                funcs = (funcs[1], funcs[2], funcs[0])
        else:
            if random.randint(1, 3) == 1:
                funcs = (funcs[2], funcs[0], funcs[1])
            else:
                funcs = (funcs[1], funcs[1], funcs[0])
                
             
        # calls the functions based on the order chosen
        for f in funcs:
            t = f()
            if t != None:
                return t
            else:
                return random.choice([i for i in range(len(inputs)) if inputs[i] == 0])

       
