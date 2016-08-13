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
        
        DisGhostlist=[]
        DisFood = 100000
        score = successorGameState.getScore()
        reward = score
        for s in newGhostStates:
        	if s.scaredTimer == 0:
        		DisGhostlist.append(manhattanDistance(newPos,s.getPosition()))
        if DisGhostlist:
        	DisGhost = min(DisGhostlist)
        	if DisGhost <=4:
        		reward = reward+DisGhost
        
        FoodList = newFood.asList()
        for food in FoodList:
        	dis = manhattanDistance(newPos,food)
        	if dis<DisFood:
        		DisFood = dis
        "only one food left"
        if DisFood ==0:
        	reward = reward + 10
        else:
        	reward = reward + 1.0/DisFood 
        
        return reward
        

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
        def maximizer(state,depth):
            "Pacman agent"
            
            #initial state value
            V = float('-Inf')
            #possible action of Pacman
            legalAction = state.getLegalActions(0)
            #check the search tree is at the end of the depth or not. If it is the end, return state evaluation score
            if depth == 0 or state.isLose() or state.isWin() or len(legalAction)==0:
                return self.evaluationFunction(state)
                
            #number of agents
            numAgent = state.getNumAgents()
            
            for direction in legalAction:
                successor = state.generateSuccessor(0,direction)
                V = max(V,minimizer(successor,depth,numAgent-1,1))
                
            return V
        
        
        def minimizer(state,depth,numAgent,indice):
            "Ghost agent"
            
            #initial state value
            V = float('Inf')
            #possible action of ghost
            legalAction = state.getLegalActions(indice)
            #check the search tree is at the end of the depth or not. If it is the end, return state evaluation score
            if depth == 0 or state.isLose() or state.isWin() or len(legalAction)==0:
                return self.evaluationFunction(state)
            
            #Tree search
            for direction in legalAction:
                successor = state.generateSuccessor(indice,direction)
                #if agent now is the last ghost, then next we need to consider the action of pacman (maximizer) and one depth has finished
                #if not, there are extra ghosts we need to analyses"
                if numAgent == indice:
                    V = min(V,maximizer(successor,depth-1))
                else:
                    V = min(V,minimizer(successor,depth,numAgent,indice+1))
                    
            return V
        
        
        
        #number of agents (pacman and ghosts)
        numAgent = gameState.getNumAgents()
        #possible action of pacman"
        legalAction = gameState.getLegalActions(0)
        #initial state value of pacman initial state
        V = float('-Inf')
        
        OptAction = []
        #Tree search
        for direction in legalAction:
            val = minimizer(gameState.generateSuccessor(0,direction),self.depth,numAgent-1,1)
            #find the maximum
            if val>V:
                V=val
                OptAction = direction
        return OptAction
                      

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maximizer(state,depth,alpha,beta):
            "Pacman agent"
            
            #initial state value
            V = float('-Inf')
            #possible action of Pacman
            legalAction = state.getLegalActions(0)
            #check the search tree is at the end of the depth or not. If it is the end, return state evaluation score
            if depth == 0 or state.isLose() or state.isWin() or len(legalAction)==0:
                return self.evaluationFunction(state)
                
            #number of agents
            numAgent = state.getNumAgents()
            
            for direction in legalAction:
                successor = state.generateSuccessor(0,direction)
                V = max(V,minimizer(successor,depth,numAgent-1,1,alpha,beta))
                if V > beta: #Great! we can prune this tree
                    return V
                else:#We need to continue go through the tree, meanwhile update the alpha
                    alpha = max(alpha,V)
                
            return V
        
        
        def minimizer(state,depth,numAgent,indice,alpha,beta):
            "Ghost agent"
            
            #initial state value
            V = float('Inf')
            #possible action of ghost
            legalAction = state.getLegalActions(indice)
            #check the search tree is at the end of the depth or not. If it is the end, return state evaluation score
            if depth == 0 or state.isLose() or state.isWin() or len(legalAction)==0:
                return self.evaluationFunction(state)
            
            #Tree search
            for direction in legalAction:
                successor = state.generateSuccessor(indice,direction)
                #if agent now is the last ghost, then next we need to consider the action of pacman (maximizer) and one depth has finished
                #if not, there are extra ghosts we need to analyses"
                if numAgent == indice:
                    V = min(V,maximizer(successor,depth-1,alpha,beta))
                else:
                    V = min(V,minimizer(successor,depth,numAgent,indice+1,alpha,beta))
                if V < alpha: #Great! we can prune this tree
                    return V
                else: #We need to continue go through the tree, meanwhile update the beta
                    beta = min(beta,V)
                    
            return V
        
        
        
        #number of agents (pacman and ghosts)
        numAgent = gameState.getNumAgents()
        #possible action of pacman"
        legalAction = gameState.getLegalActions(0)
        #initial state value of pacman initial state
        V = float('-Inf')
        
        OptAction = []
        #Tree search
        for direction in legalAction:
            #initialization of alpha, beta
            alpha = V
            beta = float('Inf')
            val = minimizer(gameState.generateSuccessor(0,direction),self.depth,numAgent-1,1,alpha,beta)
            #find the maximum
            if val>V:
                V=val
                OptAction = direction
        return OptAction
    

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
        def maximizer(state,depth):
            "Pacman agent"
            
            #initial state value
            V = float('-Inf')
            #possible action of Pacman
            legalAction = state.getLegalActions(0)
            #check the search tree is at the end of the depth or not. If it is the end, return state evaluation score
            if depth == 0 or state.isLose() or state.isWin() or len(legalAction)==0:
                return self.evaluationFunction(state)
                
            #number of agents
            numAgent = state.getNumAgents()
            
            for direction in legalAction:
                successor = state.generateSuccessor(0,direction)
                V = max(V,expectitor(successor,depth,numAgent-1,1))
                
            return V
            
            
        def expectitor(state,depth,numAgent,indice):
            "Expect value of ghost"
            V = []
            #possible action of ghost
            legalAction = state.getLegalActions(indice)
            #check the search tree is at the end of the depth or not. If it is the end, return state evaluation score
            if depth == 0 or state.isLose() or state.isWin() or len(legalAction)==0:
                return self.evaluationFunction(state)
                
            for direction in legalAction:
                successor = state.generateSuccessor(indice,direction)
                #if agent now is the last ghost, then next we need to consider the action of pacman (maximizer) and one depth has finished
                #if not, there are extra ghosts we need to analyses"
                if numAgent == indice:
                    V.append(maximizer(successor,depth-1))
                else:
                    V.append(expectitor(successor,depth,numAgent,indice+1))
                    
            return sum(V)/len(V)
        
        #number of agents (pacman and ghosts)
        numAgent = gameState.getNumAgents()
        #possible action of pacman"
        legalAction = gameState.getLegalActions(0)
        #initial state value of pacman initial state
        V = float('-Inf')
        
        OptAction = []
        #Tree search
        for direction in legalAction:
            val = expectitor(gameState.generateSuccessor(0,direction),self.depth,numAgent-1,1)
            #find the maximum
            if val>V:
                V=val
                OptAction = direction
        return OptAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    PacmanPos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    FoodList = Food.asList()
    GhostState = currentGameState.getGhostStates()
    
    #initialize the reward with score
    reward = currentGameState.getScore()
    #nearest ghost distance
    DisGhostlist = []
    for s in GhostState:
        if s.scaredTimer == 0:
            DisGhostlist.append(manhattanDistance(PacmanPos,s.getPosition()))
    if DisGhostlist:
        DisGhost = min(DisGhostlist)
        if DisGhost <4:
            reward = reward+DisGhost
    #nearest food distance
    DisFood = float("Inf")
    for food in FoodList:
        dis = manhattanDistance(PacmanPos,food)
        if dis<DisFood:
        		DisFood = dis
    "only one food left"
    if DisFood ==0:
        reward = reward + 20
    else:
        reward = reward + 7.0/DisFood 
    return reward
    
    

# Abbreviation
better = betterEvaluationFunction

