# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 21:25:36 2019

@author: laurie
"""
import numpy as np


class Dreidel:
    
    num_players = 0
    purses = []
    current_player = 0
    pot = 0
    num_spins = 0
    exit_round = []
    
    broke = 0
    out = -1
    sides = 4
    hey = 0
    gimmel = 1
    shin = 2
    nun = 3
    
    def __init__(self, number_of_players, starting_purse):
        self.num_players = number_of_players
        self.purses = np.array([starting_purse] * self.num_players)
        self.exit_round = [0] * self.num_players
        
    def ante(self):
        self.pot = sum(self.purses > self.broke)
        self.purses += (self.purses > self.out)*-1
    
    def advance_round(self):
        # everyone who is not out advances to the next round
        self.exit_round += (self.purses > self.out)

    def advance_player_round(self):
        self.current_player = self.current_player + 1
        if self.current_player == self.num_players:
            self.advance_round()
            self.current_player = 0        
        
    def advance_to_next_player(self):
        self.advance_player_round()
        while self.purses[self.current_player] == self.out:
            self.advance_player_round()
            
    def tally_spin(self,roll):
        self.num_spins += 1
        if roll == self.hey:
            prize = self.pot // 2
        elif roll == self.gimmel:
            prize = self.pot
        elif roll == self.shin:
            prize = -1
        else:
            prize = 0
        # only increase pot if player can afford it
        if prize > 0 or self.purses[self.current_player] > self.broke:
            self.pot -= prize
        self.purses[self.current_player] += prize

    def is_winner(self):
        return np.sum(self.purses > self.out) == 1
    
    def play_game(self):
        
        while not self.is_winner():
            if self.pot == 0:
                self.ante()
            roll = np.random.randint(self.sides)
            self.tally_spin(roll)
            self.advance_to_next_player()

    def __str__(self):
        response = "The current player is: {0}".format(self.current_player)
        response += "\nThe current pot is: {0}".format(self.pot)
        response += "\nThe purses are: {0}".format(self.purses)
        response += "\nThe round count is: {0}".format(self.exit_round)
        response += "\nThere have been {0} spins".format(self.num_spins)
        return response

