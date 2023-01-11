from bot_class import happyBot, randomBot
from tic_tac_toe_gameFunction import game
from copy import deepcopy


def save_data(bots):
    global count
    with open (f"/workspaces/69s-maker/bot_data/data_{count}.txt", 'a') as f:
        for bot in bots:
            lines = [str(list(bot[0].layer1)), str(list(bot[0].layer2)), str(list(bot[0].layer3))]
            f.write(bot[0].ID)
            f.writelines(lines)
            f.write('buffer\n')

    
count = int(open("count.txt").read()) + 1
with open (f"count.txt", 'w') as f: f.write(str(count))


bots = []
for num in range(100):
    bots.append(happyBot('000', f'{num:02d}'))

training_bot = randomBot()

generations = 1000

for gen in range(generations):
    win_percentages = []
    for bot in bots:
        wins = losses = 0
        for _ in range(100):
            result = game(bot, training_bot)[1]
            if result[0] == result[1]:
                wins += 5
            elif result[1] != 3:
                losses += 1
            else:
                wins += 1
        win_percentages.append((bot, wins/(wins+losses)))
    

    top_10 = sorted(win_percentages, key = lambda x: x[1])[-10:]
    save_data(top_10)
    new_bots = []
    for i, b in enumerate(top_10):
        for o in range(10):
            temp = deepcopy(b[0])
            temp.evolve()
            temp.change_ID(gen+1, i*10+o)
            new_bots.append(temp)
    
    bots = deepcopy(new_bots)

