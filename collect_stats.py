import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

import Dreidel

def stat_summary(round_stats):

    stats = {'mean' : np.mean(round_stats),
             'min' : np.min(round_stats),
             'max' : np.max(round_stats)}
    for percentile in (10,25,50,75,90):
        stats[percentile] = int(np.percentile(round_stats,percentile))

    return stats

def report_stats(num_players, num_coins, round_stats):
    stats = stat_summary(round_stats)

    percentile_range = "{0}% of all games will between {1} and {2} rounds\n"
    summary  = "When playing with {0} players that each start with {1} coins,\n".format(num_players, num_coins)
    summary += " * the average number of rounds is {0}, \n".format(stats['mean'])
    summary += " * the median number of rounds is {0}, \n".format(stats[50])
    summary += " * the shortest game took {0} rounds\n".format(stats['min'])
    summary += " * the longest game took {0} rounds\n".format(stats['max'])
    for percentile in (10,25):
        summary += percentile_range.format(100-2*percentile, stats[percentile], stats[100 - percentile])
    return summary

def record_stats(stat_table, num_players, num_coins, round_stats):
    stats = [num_players, num_coins]
    stats.extend(list(stat_summary(round_stats).values()))
    if stat_table is None:
        return stats
    else:
        return np.vstack([stat_table,stats])

num_trials = 10000

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

num_players = 4
num_coins = 3
one_case_results = run_trials(num_players,num_coins,num_trials)
print(report_stats(num_players,num_coins,one_case_results))
plt.clf()
plt.hist(one_case_results,bins=30)
plt.show()

#print(collect_all_stats(5,5))




