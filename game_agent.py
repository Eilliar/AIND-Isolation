"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random, itertools


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def percent_occupation(game):
    """
    Checks percentage of occupied space in the board.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    Returns
    -------
    int
        The percentage of occupied space in the board
    """
    blank_spaces = game.get_blank_spaces()
    return (len(blank_spaces)/float((game.width * game.height)))

def distance_to_opponent(game, player):
    """
    Checks player distance to opponent using the Taxicab Distance.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    
    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    -------
    int
        The player distance to opponent
    """
    # Get Player's position
    (x0, x1) = game.get_player_location(player)
    # Get Opponent's position
    (y0, y1) = game.get_player_location(game.get_opponent(player))
    
    # Taxicab Distance
    return abs(x0 - y0) + abs(x1 - y1)

def third_heuristic(game, player):
    """

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    weight_opp : int
        penalization weight on number of opponent moves

    Returns
    ----------
    float
        The heuristic value of the current game state
    """

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # Taxicab Distance between the two players
    distance = distance_to_opponent(game, player)
    # Board percentual occupation
    occupation = percent_occupation(game)

    return float(own_moves + distance - occupation - opp_moves)

def second_heuristic(game, player):
    """
    
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    weight_opp : int
        penalization weight on number of opponent moves

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    
    # Available moves
    own_moves = len(game.get_legal_moves(player))
    # Board percentual occupation
    occupation = percent_occupation(game)

    return float(own_moves/occupation)

def aggressive_chaser(game, player, weight_opp = 2):
    """Score function for an aggressive chaser. Something like the 
    chaser that we saw on lecture videos, but can make it more aggressive 
    pennalizing heavily number of opponent moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    weight_opp : int
        penalization weight on number of opponent moves

    Returns
    ----------
    float
        The heuristic value of the current game state
    """

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - weight_opp*opp_moves)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # First heuristic: Aggressive Chaser
    # return aggressive_chaser(game, player)
    # Second heuristic:
    #return second_heuristic(game, player)
    # Third heuristic:
    return third_heuristic(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if not legal_moves:
            return (-1, -1)
        
        # Check wheter is minimax or alphabeta search
        search = None
        if self.method == 'minimax':
            search = self.minimax
        elif self.method == 'alphabeta':
            search = self.alphabeta

        v, move = None, None
        # Do I need to check if it's first move?
        if (len(game.get_legal_moves()) == (game.width * game.height) ):
            # If available moves are all the board squares get the center position
            return (int(game.width/2), int(game.height/2))

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            #v , move = self.minimax(game, self.search_depth)
            # Perform Iterative Deepening Search
            if self.iterative:
                for i in itertools.count():
                    v, move = search(game, i+1, True)
            else:
                # Perform Non-Iterative Deepening Search
                v, move = search(game, self.search_depth, True)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return move

        # Return the best move from the last completed search iteration
        return move
    
    def dls(self, game, depth, maximizing_player):
        """Depth Limited Search for MinimMax."""
        no_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        
        if (depth == 0):
            # Get the Score
            return self.score(game, self), no_move

        # Maximizing Player
        if maximizing_player:
            # Defaults
            bestValue = float("-inf")
            bestMove = no_move
            # Loop over all possible children nodes
            for child in legal_moves:
                # Recursive minimax, decrease depth and flip player
                v, move = self.dls(game.forecast_move(child), depth -1, not(maximizing_player))
                # Update bestValue and bestMove
                if v > bestValue:
                    bestValue = v
                    bestMove = child

            return bestValue, bestMove
        # Minimizing Player
        else:
            # Defaults
            bestValue = float("inf")
            bestMove = no_move
            # Loop over all possible children nodes
            for child in legal_moves:
                # Recursive minimax, decrease depth and flip player
                v, move = self.dls(game.forecast_move(child), depth -1, not(maximizing_player))
                if v < bestValue:
                    bestValue = v
                    bestMove = child

            return bestValue, bestMove
            

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        return self.dls(game, depth, maximizing_player)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        # Define default move and get all available legal moves
        no_move = (-1, -1)
        legal_moves = game.get_legal_moves()

        if (depth == 0) or (len(legal_moves) == 0):
            return self.score(game, self), no_move

        # Maximizing Player
        if maximizing_player:
            # Defaults
            bestValue = float("-inf")
            bestMove = no_move
            # Loop over all possible children nodes
            for child in legal_moves:
                v, move = self.alphabeta(game.forecast_move(child), depth -1, alpha, beta, not(maximizing_player))
                # max(bestValue, v)
                if (v > bestValue):
                    bestValue = v
                    bestMove = child
                # Update Alpha
                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break
            return bestValue, bestMove
        
        # Minimizing Player
        else:
            # Defaults
            bestValue = float("inf")
            bestMove = no_move
            # Loop over all possible children nodes
            for child in legal_moves:
                v, move = self.alphabeta(game.forecast_move(child), depth -1, alpha, beta, not(maximizing_player))
                # min(bestValue, v)
                if (v < bestValue):
                    bestValue = v
                    bestMove = move
                # Update Beta
                beta = min(beta, bestValue)
                if beta <= alpha:
                    break
            return bestValue, bestMove