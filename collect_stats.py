# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 08:49:28 2019

@author: laurie
"""
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

import Dreidel

def stat_summary(round_stats):

    stats = {'mean' : np.mean(round_stats),
             'min' : np.min(round_stats),
             'p10' : int(np.percentile(round_stats,10)),
             'p25' : int(np.percentile(round_stats,25)),
             'p50' : int(np.percentile(round_stats,50)),
             'p75' : int(np.percentile(round_stats,75)),
             'p90' : int(np.percentile(round_stats,90)),
             'max' : np.max(round_stats)}

    return stats

def report_stats(num_players, num_coins, round_stats):
    stats = stat_summary(round_stats)
    plt.hist(round_stats)
    summary  = "When playing with {0} players that each start with {1} coins,\n".format(num_players, num_coins)
    summary += "the average number of rounds is {0}, \n".format(stats['mean'])
    percentile = 10
    summary += "the shortest game took {0} rounds\n".format(stats['min'])
    summary += "{0}% of all games will take fewer than {1} or more than {2} rounds,\n".format(percentile, stats['p10'], stats['p90'])
    percentile = 25
    summary += "{0}% of all games will take fewer than {1} or more than {2} rounds,\n".format(percentile, stats['p25'], stats['p75'])
    summary += "the median number of rounds is {0}, \n".format(stats['p50'])
    summary += "the longest game took {0} rounds, and\n".format(stats['max'])
    print(summary)

def record_stats(stat_table, num_players, num_coins, round_stats):
    stats = [num_players, num_coins]
    stats.extend(list(stat_summary(round_stats).values()))
    if stat_table is None:
        return stats
    else:
        return np.vstack([stat_table,stats])

num_trials = 1000

all_stats = None

for num_players in tqdm([2,3,4,5]):
    for num_coins in [3,4,5]:
        for trial in range(num_trials):
            game = Dreidel.Dreidel(num_players, num_coins)
            game.play_game()
            if trial == 0:
                round_stats = np.array(game.exit_round)
            else:
                round_stats = np.vstack([round_stats,game.exit_round])

        round_stats = round_stats.max(axis=1)
        all_stats = record_stats(all_stats, num_players, num_coins, round_stats)

