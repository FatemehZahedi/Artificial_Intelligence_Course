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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
      
        Foodlist = newFood.asList()
        score = successorGameState.getScore()
        ghostpositions = successorGameState.getGhostPositions()

        distance = []
        for food in Foodlist:
          distance.append(manhattanDistance(food, newPos))
        if distance:
          score += 1/float(min(distance))
        distance = []

        for ghost in ghostpositions:
          newdist = manhattanDistance(ghost, newPos)
          if newdist < 2: #it means ghost is in neighbor
            score -= 20  # choose it big enough to avoid ghosts that are very close 
          distance.append(newdist)
        if distance:
          if sum(distance):
            score -= 1/float(sum(distance))
        distance = []

        return score

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
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def minimax_decision(state, depth, agent):
          if agent == 0: 
              return maxvalue(state, depth, agent)
          else:  
              return minvalue(state, depth, agent)

        def maxvalue(state, depth, agent):
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          v = []
          for action in state.getLegalActions(agent):
            v.append((minimax_decision(state.generateSuccessor(agent, action), depth, 1),action))
          return max(v)

        def minvalue(state, depth, agent):
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          v = []
          nextagent = agent + 1 
          if state.getNumAgents() == nextagent:
              nextagent = 0
              depth += 1
          for action in state.getLegalActions(agent):
            v.append((minimax_decision(state.generateSuccessor(agent, action), depth, nextagent),action))
          return min(v)

        (score, action) = minimax_decision(gameState, 0, 0)    
        
        return action
            
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alpha_beta_search(state, depth, agent, alpha, beta):
          if agent == 0: 
              return maxvalue(state, depth, agent, alpha, beta)
          else:  
              return minvalue(state, depth, agent, alpha, beta)

        def maxvalue(state, depth, agent, alpha, beta):
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          v = [float("-inf"),]
          for action in state.getLegalActions(agent):
            v1 = []
            if type(alpha_beta_search(state.generateSuccessor(agent, action), depth, 1, alpha, beta)) is not float:
              v1 = [alpha_beta_search(state.generateSuccessor(agent, action), depth, 1, alpha, beta)[0],action]
            else:
              v1 = [alpha_beta_search(state.generateSuccessor(agent, action), depth, 1, alpha, beta),action]
            v = max(v, v1)
            if v1[0] > beta:
              return v1
            alpha = max(alpha, v1[0])
          return v

        def minvalue(state, depth, agent, alpha, beta):
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          v = [float("inf"),]
          nextagent = agent + 1 
          if state.getNumAgents() == nextagent:
              nextagent = 0
              depth += 1
          for action in state.getLegalActions(agent):
            v1 = []
            if type(alpha_beta_search(state.generateSuccessor(agent, action), depth, nextagent, alpha, beta)) is not float:
              v1 = [alpha_beta_search(state.generateSuccessor(agent, action), depth, nextagent, alpha, beta)[0],action]
            else:
              v1 = [alpha_beta_search(state.generateSuccessor(agent, action), depth, nextagent, alpha, beta),action]
            v = min(v, v1)
            if v1[0] < alpha:
              return v1
            beta = min(beta, v1[0])
          return v

        [score, action] = alpha_beta_search(gameState, 0, 0, float("-inf"), float("inf"))    
        
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(state, depth, agent):
          if agent == 0: 
              return maxvalue(state, depth, agent)
          else:  
              return expvalue(state, depth, agent)

        def maxvalue(state, depth, agent):
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          v = []
          for action in state.getLegalActions(agent):
            if type(expectimax(state.generateSuccessor(agent, action), depth, 1)) is not float:
              v.append((expectimax(state.generateSuccessor(agent, action), depth, 1)[0],action))
            else:
              v.append((expectimax(state.generateSuccessor(agent, action), depth, 1),action))
          return max(v)

        def expvalue(state, depth, agent):
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          v = []
          nextagent = agent + 1 
          if state.getNumAgents() == nextagent:
              nextagent = 0
              depth += 1
          prob = 1.0/float(len(state.getLegalActions(agent)))
          for action in state.getLegalActions(agent):
            if type(expectimax(state.generateSuccessor(agent, action), depth, nextagent)) is not float:
              v.append(expectimax(state.generateSuccessor(agent, action), depth, nextagent)[0]*prob)
            else:
              v.append(expectimax(state.generateSuccessor(agent, action), depth, nextagent)*prob)
          return (sum(v),action)

        (score, action) = expectimax(gameState, 0, 0)    
        
        return action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()

  
    Foodlist = newFood.asList()
    score = currentGameState.getScore() - len(currentGameState.getCapsules())
    ghostpositions = currentGameState.getGhostPositions()


    distance = []
    for food in Foodlist:
      distance.append(manhattanDistance(food, newPos))
    if distance:
      score += 1/float(min(distance))
    distance = []

    for ghost in ghostpositions:
      newdist = manhattanDistance(ghost, newPos)
      if newdist < 2: #it means ghost is in neighbor
        score -= 20  # choose it big enough to avoid ghosts that are very close 
      distance.append(newdist)
    if distance:
      if sum(distance):
        score -= 1/float(sum(distance))
    distance = []

    return score

# Abbreviation
better = betterEvaluationFunction

