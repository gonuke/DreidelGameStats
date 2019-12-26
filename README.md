Dreidel Game with Statistics
------------------------------

This project began in 2019 when a Dreidel game seemed to be taking a long
time.  It got me wondering what the distribution of game times would be.  I
wrote this python code to simulate a single game, and then simulated multiple
games to collect the PDF of game times.

Dreidel Game Rules
==================

This particular dreidel game has the following rules:

* all players start with the same number of coins/tokens/gelt/etc

* any time that the pot is empty, all players ante up a single coin

* players take turns spinning the dreidel with the following outcomes:

   * Gimmel - collect the entire pot
   * Hey - collect half the pot, rounding down for odd numbers
   * Shin - put one coin in the pot
   * Nun - do nothing

* any time that a player must put in a coin (ante or shin) and has no coins,
  they are out of the game

* the game ends when only one player remains


