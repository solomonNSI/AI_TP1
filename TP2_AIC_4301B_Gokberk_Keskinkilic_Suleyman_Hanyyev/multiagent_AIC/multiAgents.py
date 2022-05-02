# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman_AIC.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman_AIC.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostsPos = [ghostState.getPosition() for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        """consider food and ghost locations"""

        "  Your evaluation function evaluates state-action pairs, "
        "  in later parts of the project, you will evaluate states"
        # Initialize the remaining food and ghost positions
        food = newFood.asList()
        ghostPos = successorGameState.getGhostPositions()

        # To find the min distance for the food and max dist for the ghost
        foodDistance = float("inf")
        ghostDistance = float("inf")

        for i in food:
            distance = util.manhattanDistance(newPos, i)
            if foodDistance >= distance:
                foodDistance = distance

        for i in ghostPos:
            distance = util.manhattanDistance(newPos, i)
            if distance <= 1:
                ghostDistance += 100

        if currentGameState.getPacmanPosition() == newPos:
            return (-(float("inf")))

        if foodDistance == float("inf") or ghostDistance == float("inf"):
            return foodDistance

        return successorGameState.getScore() - foodDistance - ghostDistance


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 5)
    """
   
   
    def getAction(self, gameState):
        def max_value(gameState, d):
            # computing the best direction
            # Done for readability, getting actions of the pacman and checking
            # if they are empty
            if len(gameState.getLegalActions(0)) == 0:
                return (self.evaluationFunction(gameState), None)
            
            if gameState.isWin() or gameState.isLose() or d == self.depth:
                return (self.evaluationFunction(gameState), None)
            
            actions = gameState.getLegalActions(0)
            value = -(float("inf"))
            action_final = None
            for action in actions:
                temp = MIN_VALUE(gameState.generateSuccessor(0, action), 1, d)[0]
                if ( temp > value):
                    value = temp
                    action_final = action
            return (value, action_final)
        
        def MIN_VALUE(gameState, d, indexAgent):
            # computing the worst case direction (ghost)


            # Done for readability, getting actions of the pacman and checking
            # if they are empty
            if len(gameState.getLegalActions(0)) == 0:
                return (self.evaluationFunction(gameState), None)
            
            if gameState.isWin() or gameState.isLose() or d == self.depth:
                return (self.evaluationFunction(gameState), None)
            
            actions = gameState.getLegalActions(0)
            value = -(float("inf"))
            action_final = None
            for action in actions:
                if( indexAgent == gameState.getNumAgents() -1):
                    temp = max_value(gameState.generateSuccessor(indexAgent, action), d + 1)[0]
                else:
                    temp = MIN_VALUE(gameState.generateSuccessor(indexAgent, action), d, indexAgent + 1)[0]
                if ( temp < value):
                    value = temp
                    action_final = action
            
            return ( value, action_final)
        
        return max_value(gameState, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 6)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def max_value( gameState, d, alpha, beta):
            # computing the best direction


            # Done for readability, getting actions of the pacman and checking
            # if they are empty
            if len(gameState.getLegalActions(0)) == 0:
                return (self.evaluationFunction(gameState), None)
            
            if gameState.isWin() or gameState.isLose() or d == self.depth:
                return (self.evaluationFunction(gameState), None)
            
            actions = gameState.getLegalActions(0)
            value = -(float("inf"))
            action_final = None
            for action in actions:
                temp = MIN_VALUE(gameState.generateSuccessor(0, action), 1, d)[0]
                if ( temp > value):
                    value = temp
                    action_final = action
                if ( beta < value):
                    return (value, action_final)

                alpha = max(alpha, value)
            return (value, action_final)
        
        def MIN_VALUE(gameState, d, indexAgent, alpha, beta):
            # computing the worst case direction (ghost)


            # Done for readability, getting actions of the pacman and checking
            # if they are empty
            if len(gameState.getLegalActions(0)) == 0:
                return (self.evaluationFunction(gameState), None)
            
            if gameState.isWin() or gameState.isLose() or d == self.depth:
                return (self.evaluationFunction(gameState), None)
            
            actions = gameState.getLegalActions(0)
            value = -(float("inf"))
            action_final = None

            for action in actions:
                if( indexAgent == gameState.getNumAgents() -1):
                    temp = max_value(gameState.generateSuccessor(indexAgent, action), d + 1)[0]
                else:
                    temp = MIN_VALUE(gameState.generateSuccessor(indexAgent, action), d + 1)[0]
                
                if ( temp < value):
                    value = temp
                    action_final = action
                
                if ( value < alpha):
                    return (value, action_final)

                beta = min(beta, value)

            return ( value, action_final)
        alpha = -(float("inf"))
        beta = float("inf")
        return max_value(gameState, 0, alpha, beta)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 7)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def max_value( gameState, d):
            # computing the best direction

            # Done for readability, getting actions of the pacman and checking
            # if they are empty
            if len(gameState.getLegalActions(0)) == 0:
                return (self.evaluationFunction(gameState), None)
            
            if gameState.isWin() or gameState.isLose() or d == self.depth:
                return (self.evaluationFunction(gameState), None)
            
            actions = gameState.getLegalActions(0)
            value = -(float("inf"))
            action_final = None
            for action in actions:
                temp = expected(gameState.generateSuccessor(0, action), 1, d)[0]
                if ( temp > value):
                    value = temp
                    action_final = action
            return (value, action_final)

        def expected( gameState, d, indexAgent):
            
            actions = gameState.getLegalActions(indexAgent)
            value = -(float("inf"))
            action_final = None
            if len(actions) == 0:
                return (self.evaluationFunction(gameState), None)
            
            for action in actions:
                if( indexAgent == gameState.getNumAgents() -1):
                    temp = max_value(gameState.generateSuccessor(indexAgent, action), d + 1)[0]
                else:
                    temp = expected(gameState.generateSuccessor(indexAgent, action), d, indexAgent + 1)[0]
                
                value += temp/len(actions)
                action_final = action
            return (value, action_final)
        return max_value(gameState, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 8).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

# Abbreviation
better = betterEvaluationFunction
