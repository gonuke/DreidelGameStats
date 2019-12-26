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
    return summary

def record_stats(stat_table, num_players, num_coins, round_stats):
    stats = [num_players, num_coins]
    stats.extend(list(stat_summary(round_stats).values()))
    if stat_table is None:
        return stats
    else:
        return np.vstack([stat_table,stats])

num_trials = 1000

def collect_all_stats(max_players, max_coins):

    all_stats = None

    for num_players in range(2,max_players+1):
        for num_coins in range(2,max_coins+1):
            round_stats = run_trials(num_players, num_coins, num_trials)
            all_stats = record_stats(all_stats, num_players, num_coins, round_stats)

    return all_stats
        
def run_trials(num_players, num_coins, num_trials):
    for trial in tqdm(range(num_trials)):
        game = Dreidel.Dreidel(num_players, num_coins)
        game.play_game()
        if trial == 0:
            round_stats = np.array(game.exit_round)
        else:
            round_stats = np.vstack([round_stats,game.exit_round])

    return round_stats.max(axis=1)

print(report_stats(4,5,run_trials(4,5,num_trials)))

#print(collect_all_stats(5,5))




