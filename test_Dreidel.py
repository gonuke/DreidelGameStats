# tests for Dreidel class
import numpy as np
import pytest

import Dreidel

# standard values for setting up tests
num_players = 4
starting_purse = 5
broke_player = 1
out_player = 2

def test_init():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    
    obs = game.num_players
    exp = num_players
    
    assert(obs == exp)

    obs = game.purses
    exp = np.array([starting_purse] * num_players)
    
    assert(np.all(obs == exp))
    
    obs = game.current_player
    exp = 0
    
    assert(obs == exp)
    
    obs = game.pot
    exp = 0
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = [0] * num_players
    
    assert(obs == exp)
    
# normal circumstance - all players have gelt
def test_ante_std():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    
    game.ante()
    
    obs = game.purses
    exp = np.array([starting_purse - 1] * num_players)
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = num_players
    
    assert(obs == exp)

    game.ante()
    
    obs = game.purses
    exp = np.array([starting_purse - 2] * num_players)
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = num_players
    
    assert(obs == exp)
    
# at least one player has no gelt but is not yet out
def test_ante_some_broke():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    
    game.purses[broke_player] = Dreidel.Dreidel.broke
    
    # first ante
    game.ante()
    
    obs = game.purses
    exp = np.array([starting_purse - 1] * num_players)
    exp[broke_player] = Dreidel.Dreidel.out
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = num_players - 1
    
    assert(obs == exp)


# at least one player is already out    
def test_ante_some_out():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    
    game.purses[out_player] = Dreidel.Dreidel.out
    
    game.ante()
    
    obs = game.purses
    exp = np.array([starting_purse - 1] * num_players)
    exp[out_player] = Dreidel.Dreidel.out
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = num_players - 1
    
    assert(obs == exp)
    
# one player is already out and one player is broke
def test_ante_some_broke_and_out():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    
    game.purses[broke_player] = Dreidel.Dreidel.broke
    game.purses[out_player] = Dreidel.Dreidel.out
    
    game.ante()
    
    obs = game.purses
    exp = np.array([starting_purse - 1] * num_players)
    exp[broke_player] = Dreidel.Dreidel.out
    exp[out_player] = Dreidel.Dreidel.out
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = num_players - 2
    
    assert(obs == exp)

# standard case when all players are still playing
def test_advance_round_std():

    game = Dreidel.Dreidel(num_players, starting_purse)

    game.advance_round()
    
    obs = game.exit_round
    exp = np.array([1] * num_players)
    
    assert(np.all(obs == exp))
    
    game.advance_round()
    
    obs = game.exit_round
    exp = exp + exp
    
    assert(np.all(obs == exp))

# one player is broke - should behave the same as the std case
def test_advance_round_broke():

    game = Dreidel.Dreidel(num_players, starting_purse)

    game.advance_round()
    
    obs = game.exit_round
    exp = np.array([1] * num_players)
    
    assert(np.all(obs == exp))
    
    game.purses[broke_player] = Dreidel.Dreidel.broke

    game.advance_round()
    
    obs = game.exit_round
    exp = exp + exp
    
    assert(np.all(obs == exp))

# one player is out - their round counter should not advance
def test_advance_round_out():
  
    game = Dreidel.Dreidel(num_players, starting_purse)

    game.advance_round()
    
    obs = game.exit_round
    exp = np.array([1] * num_players)
    
    assert(np.all(obs == exp))
    
    game.purses[out_player] = Dreidel.Dreidel.out
    
    game.advance_round()
    
    obs = game.exit_round
    exp = exp + exp
    exp[out_player] -= 1
    
    assert(np.all(obs == exp))

# one player is broke and another is out
# - the broke player's round counter should advance
# - the out player's round counter should not advance
def test_advance_round_broke_and_out():

    game = Dreidel.Dreidel(num_players, starting_purse)

    game.advance_round()
    
    obs = game.exit_round
    exp = np.array([1] * num_players)
    
    assert(np.all(obs == exp))

    game.purses[broke_player] = Dreidel.Dreidel.broke
    game.purses[out_player] = Dreidel.Dreidel.out

    
    game.advance_round()
    
    obs = game.exit_round
    exp = exp + exp
    exp[out_player] -= 1
    
    assert(np.all(obs == exp))

# advance to the next player, possibly incrementing the round
# all players still available to play
def test_advance_player_round():
    
    game = Dreidel.Dreidel(num_players, starting_purse)

    # first test should not advance the round, but only the player
    game.advance_player_round()
    
    obs = game.current_player
    exp = 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))
    
    # set current player to last player
    # this test should advance the round and the player
    game.current_player = num_players - 1
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = 0
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([1] * num_players)

    assert(np.all(obs == exp))

# advance to the next player, possibly incrementing the round
# one broke player - should advance to broke player and 
def test_advance_player_round_broke():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    game.purses[broke_player] = Dreidel.Dreidel.broke

    # test 1 - advance to next player without changing round
    game.advance_player_round()
    
    obs = game.current_player
    exp = 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))
    
    # test 2 - advance to next player, even if they are the broke player,
    #          without changing round
    game.current_player = broke_player - 1
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = broke_player
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)
    game.current_player = broke_player
    
    # test 3 - advance to next player, after the broke player,
    #          without changing round
    game.advance_player_round()
    
    obs = game.current_player
    exp = broke_player + 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))

# advance to the next player, possibly incrementing the round
# one out player - should advance to out player in this method
def test_advance_player_round_out():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    game.purses[out_player] = Dreidel.Dreidel.out
    
    # test 1 - advance to next player without changing round
    game.advance_player_round()
    
    obs = game.current_player
    exp = 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))
    
    # test 2 - advance to next player, even if they are the out player,
    #          without changing round
    game.current_player = out_player - 1
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = out_player
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))

    # test 3 - advance to next player, after the out player,
    #          without changing round
    game.current_player = out_player
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = out_player + 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))

# advance to the next VALID player, possibly incrementing the round
# all players still available to play
def test_advance_to_next_player_std():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    
    game.advance_to_next_player()
    
    obs = game.current_player
    exp = 1
    
    assert(obs == exp)
    
    game.advance_to_next_player()
    
    obs = game.current_player
    exp = 2
    
    assert(obs == exp)

    game.current_player = num_players - 1
    
    game.advance_to_next_player()
    
    obs = game.current_player
    exp = 0
    
    assert(obs == exp)

    obs = game.exit_round
    exp = np.array([1] * num_players)

    assert(np.all(obs == exp))

# advance to the next VALID player, possibly incrementing the round
# one broke player - all players still available to play
# only need to test behavior when advancing to the broke player
def test_advance_to_next_player_broke():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    game.purses[broke_player] = Dreidel.Dreidel.broke
    
    game.current_player = broke_player - 1

    game.advance_to_next_player()
    
    obs = game.current_player
    exp = broke_player
    
    assert(obs == exp)
    
# advance to the next VALID player, possibly incrementing the round
# one out player - that player should be skipped
# only need to test behavior when advancing past the out player
def test_advance_to_next_player_out():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    game.purses[out_player] = Dreidel.Dreidel.out
    
    game.current_player = out_player - 1

    game.advance_to_next_player()
    
    obs = game.current_player
    exp = out_player + 1
    
    assert(obs == exp)
    
# test that all spins are handled correctly
# all players are available to play in all ways
def test_tally_spin():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    # game state: pot = 0, purses = 5 each

    game.ante()
    # game state: pot = 4, purses = 4 each

    game.tally_spin(Dreidel.Dreidel.hey)
    # game state: pot = 2, first player purse = 6, other player purses = 4

    obs = game.purses
    exp = np.array([6,4,4,4])
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = num_players - num_players // 2
    
    assert(obs == exp)
    
    game.tally_spin(Dreidel.Dreidel.gimmel)
    # game state: pot = 0, first player purse = 8, other player purses = 4
    # Note: Did not advance player
    
    obs = game.purses
    exp = np.array([8,4,4,4])
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 0
    
    assert(obs == exp)

    game.tally_spin(Dreidel.Dreidel.shin)
    # game state: pot = 1, first player purse = 7, other player purses = 4
    # Note: Did not advance player
    
    obs = game.purses
    exp = np.array([7,4,4,4])
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 1
    
    assert(obs == exp)

    game.tally_spin(Dreidel.Dreidel.nun)
    # game state: pot = 1, first player purse = 7, other player purses = 4
    
    obs = game.purses
    exp = np.array([7,4,4,4])
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 1
    
    assert(obs == exp)

# test play for a broke player
def test_tally_spin_broke():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    # game state: pot = 0, purses = 5 each
    
    game.ante()
    # game state: pot = 4, purses = 4 each
 
    game.purses[broke_player] = Dreidel.Dreidel.broke
    # game state: pot = 4, purses = 4 each except broke player = 0

    game.current_player = broke_player
    
    game.tally_spin(Dreidel.Dreidel.hey)
    # game state: pot = 2, purses = 4 each except broke player = 2
    
    obs = game.purses
    exp = np.array([4,4,4,4])
    exp[broke_player] = 2
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = num_players - num_players // 2
    
    assert(obs == exp)

    game.purses[broke_player] = Dreidel.Dreidel.broke
    # game state: pot = 2, purses = 4 each except broke player = 0
    
    game.tally_spin(Dreidel.Dreidel.gimmel)
    # game state: pot = 0, purses = 4 each except broke player = 2
    
    obs = game.purses
    exp = np.array([4,4,4,4])
    exp[broke_player] = 2
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 0
    
    assert(obs == exp)

    game.purses[broke_player] = Dreidel.Dreidel.broke
    # game state: pot = 0, purses = 4 each except broke player = 0
    
    game.tally_spin(Dreidel.Dreidel.shin)
    # game state: pot = 0, purses = 4 each except broke player = -1
    # Note: broke player had no coins to put in so pot stays the same
    #       and broke player goes out.
    
    obs = game.purses
    exp = np.array([4,4,4,4])
    exp[broke_player] = Dreidel.Dreidel.out
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 0
    
    assert(obs == exp)
