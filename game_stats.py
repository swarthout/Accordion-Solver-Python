#This is where we can add a bunch of different functions for testing the game and obtaining data and drawing conclusions. 
from accordion import game_loop
import random
import time
import numpy as np
import matplotlib.pyplot as plt

riffles = []
stacks = []
games = []
for i in range(6):
    stack_filename = f"stack_distribution_{i+1}_riffle.npy"
    games_filename = f"gamesplayed_{i+1}_riffle.npy"
    
    riffles.append(i+1)
    stacks.append(np.load(stack_filename))
    games.append(np.load(games_filename))

riffles = np.array(riffles)
avg_games = [np.average(games[i]) for i in range(len(games))]
std_games = [np.stddev(games[i]) for i in range(len(games))]

plt.errorbar(riffles, avg_games, yerr=std_games, uplims=True, lolims=True)
plt.show()
