import numpy as np

class Dreidel:
    """A class the represents the rules of a dreidel game.  

    A game is initializes with a number of players and the size
    of the starting purse for each player.

    The game is then played (play_game()) until there is a winner.

    The outcome is recorded in a list of when each player is eliminated from
    the game.
    """

    # member variables initialized to default values
    num_players = 0
    purses = []
    current_player = 0
    pot = 0
    num_spins = 0
    exit_round = []
    
    # constants for convenience and readability
    broke = 0
    out = -1
    sides = 4
    hey = 0
    gimmel = 1
    shin = 2
    nun = 3
    
    def __init__(self, number_of_players, starting_purse):
        """Initialize the game with the number of players and starting purse.

        Inputs
        ------
        number_of_players : integer representing how many 
                            players in the game
        starting_purse : integer representing how many coins 
                         each player begins the game with
        """

        self.num_players = number_of_players
        self.purses = np.array([starting_purse] * self.num_players)
        self.exit_round = [0] * self.num_players
        
    def ante(self):
        """All players who are not broke add one to the pot.
        All players who are not out remove one from their purse.
        This may result in a player going from broke to out.
        """

        self.pot = sum(self.purses > self.broke)
        self.purses += (self.purses > self.out)*-1
    
    def advance_round(self):
        """Everyone who is not out advances to the next round."""

        # this syntax adds 1 to each element of exit_round for which
        # purses is > out.  Note that broke players may still move on
        # to the next round.
        self.exit_round += (self.purses > self.out)

    def advance_player_round(self):
        """Advance the current player by one and advance the round when the next
        player is the first player.  This method may land on a player that is
        out, and dealing with that is not in the scope of this method.
        """
        
        self.current_player = self.current_player + 1
        if self.current_player == self.num_players:
            self.advance_round()
            self.current_player = 0        
        
    def advance_to_next_player(self):
        """Advance to the next player that is not out.  This largely relies on a
        different method that advances through all players and this one simply
        skips players who are out.
        """

        self.advance_player_round()
        while self.purses[self.current_player] == self.out:
            self.advance_player_round()
            
    def tally_spin(self,roll):
        """Process the results of a spin of the dreidel.

        Inputs
        ------
        roll : integer between [0,3] indicating which face of 
               the dreidel was rolled
        """
        
        self.num_spins += 1
        if roll == self.hey:
            prize = self.pot // 2
        elif roll == self.gimmel:
            prize = self.pot
        elif roll == self.shin:
            prize = -1
        else:
            prize = 0
        # only change the pot if the prize is positive or
        # the player can afford the negative prize
        if prize > 0 or self.purses[self.current_player] > self.broke:
            self.pot -= prize
        self.purses[self.current_player] += prize

    def is_winner(self):
        """Check for a winner by counting how many are not out."""
        return np.sum(self.purses > self.out) == 1
    
    def play_game(self):
        """Play a full game by looping over each turn 
           until there is a winner:
           * ante into the put
           * spin the dreidel
           * process the spin
           * advance to the next player
        """
        while not self.is_winner():
            if self.pot == 0:
                self.ante()
            roll = np.random.randint(self.sides)
            self.tally_spin(roll)
            self.advance_to_next_player()

    def __str__(self):
        """Produce a summary of the current state of the game a string."""
        response = "The current player is: {0}".format(self.current_player)
        response += "\nThe current pot is: {0}".format(self.pot)
        response += "\nThe purses are: {0}".format(self.purses)
        response += "\nThe round count is: {0}".format(self.exit_round)
        response += "\nThere have been {0} spins".format(self.num_spins)
        return response

