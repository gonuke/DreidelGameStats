# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 08:59:56 2019

@author: laurie
"""

import numpy as np

import pytest

import Dreidel

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

def test_advance_player_round():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))
    
    game.current_player = num_players - 1
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = 0
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([1] * num_players)

    assert(np.all(obs == exp))

def test_advance_player_round_broke():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    game.purses[broke_player] = Dreidel.Dreidel.broke
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))
    
    game.current_player = broke_player - 1
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = broke_player
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)
    game.current_player = broke_player
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = broke_player + 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))

def test_advance_player_round_out():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    game.purses[out_player] = Dreidel.Dreidel.out
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))
    
    game.current_player = out_player - 1
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = out_player
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))

    game.current_player = out_player
    
    game.advance_player_round()
    
    obs = game.current_player
    exp = out_player + 1
    
    assert(obs == exp)
    
    obs = game.exit_round
    exp = np.array([0] * num_players)

    assert(np.all(obs == exp))


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


def test_advance_to_next_player_broke():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    game.purses[broke_player] = Dreidel.Dreidel.broke
    
    game.current_player = broke_player - 1

    game.advance_to_next_player()
    
    obs = game.current_player
    exp = broke_player
    
    assert(obs == exp)
    
def test_advance_to_next_player_out():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    game.purses[out_player] = Dreidel.Dreidel.out
    
    game.current_player = out_player - 1

    game.advance_to_next_player()
    
    obs = game.current_player
    exp = out_player + 1
    
    assert(obs == exp)
    
    game.current_player = num_players - 1

    game.advance_to_next_player()
    
    obs = game.current_player
    exp = 0
    
    assert(obs == exp)

    obs = game.exit_round
    exp = np.array([1] * num_players)
    exp[out_player] -= 1
    
    assert(np.all(obs == exp))
    
def test_tally_spin():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    
    game.ante()
    
    game.tally_spin(Dreidel.Dreidel.hey)
    
    obs = game.purses
    exp = np.array([6,4,4,4])
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = num_players - num_players // 2
    
    assert(obs == exp)
    
    game.tally_spin(Dreidel.Dreidel.gimmel)
    
    obs = game.purses
    exp = np.array([8,4,4,4])
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 0
    
    assert(obs == exp)

    game.tally_spin(Dreidel.Dreidel.shin)
    
    obs = game.purses
    exp = np.array([7,4,4,4])
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 1
    
    assert(obs == exp)

    game.tally_spin(Dreidel.Dreidel.nun)
    
    obs = game.purses
    exp = np.array([7,4,4,4])
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 1
    
    assert(obs == exp)

def test_tally_spin_broke():
    
    game = Dreidel.Dreidel(num_players, starting_purse)
    
    game.ante()

    game.purses[broke_player] = Dreidel.Dreidel.broke
    game.current_player = broke_player
    
    game.tally_spin(Dreidel.Dreidel.hey)
    
    obs = game.purses
    exp = np.array([4,4,4,4])
    exp[broke_player] = 2
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = num_players - num_players // 2
    
    assert(obs == exp)

    game.purses[broke_player] = Dreidel.Dreidel.broke
    
    game.tally_spin(Dreidel.Dreidel.gimmel)
    
    obs = game.purses
    exp = np.array([4,4,4,4])
    exp[broke_player] = 2
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 0
    
    assert(obs == exp)

    game.purses[broke_player] = Dreidel.Dreidel.broke
    
    game.tally_spin(Dreidel.Dreidel.shin)
    
    obs = game.purses
    exp = np.array([4,4,4,4])
    exp[broke_player] = -1
    
    assert(np.all(obs == exp))
    
    obs = game.pot
    exp = 0
    
    assert(obs == exp)
