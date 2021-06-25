# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from game import Actions
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    #variables
    from util import Stack
    fringe = Stack() #stack of tuples containing: state, directions from start to state
    closed = [] #closed states
    fringe.push((problem.getStartState(), []))

    #loop
    while not fringe.isEmpty():
        state, directions = fringe.pop()    #pop top off fringe
        if state not in closed:             #if state not visited
            if problem.isGoalState(state):  #if state is goal
                return directions           #return directions to goal /if
            closed.append(state)            #add state to closed states
            for succ in problem.getSuccessors(state):            #for every successor to current state
                fringe.push((succ[0], directions + [succ[1]]))   #add succesors to fringe /if

    #end, should never be reached
    return 

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #pretty much the same as DFS except a priority queue is used so that the lowest distance is picked

    #variables
    from util import PriorityQueue
    fringe = PriorityQueue() #Queue of tuples containing: state, directions from start to state
    closed = [] #closed states
    fringe.push((problem.getStartState(), [], 0), 0)

    #loop
    while not fringe.isEmpty():
        state, directions, distance = fringe.pop()      #pop top off fringe
        if state not in closed:                         #if state not visited
            if problem.isGoalState(state):              #if state is goal
                return directions                       #return directions to goal /if
            closed.append(state)                        #add state to closed states
            for succ in problem.getSuccessors(state):   #for every successor to current state
                newDistance = distance + succ[2]           
                fringe.push((succ[0], directions + [succ[1]], newDistance), newDistance)   #add succesors to fringe /if

    #end, should never be reached
    return 

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #similar to DFS except states can be re-visited if a path with a better score has been found
    #distance was re-named to score, using golf rules ofcourse

    #variables
    from util import PriorityQueue
    fringe = PriorityQueue() #Queue of tuples containing: state, directions from start to state
    closed = {} #closed states, now a dictionary so that states can have best scores associated with them
    fringe.push((problem.getStartState(), [], 0), 0)

    #loop
    while not fringe.isEmpty():
        state, directions, score = fringe.pop()                 #pop top off fringe
        if (state not in closed) or (score < closed[state]):    #if state not visited or re-visting state grants a better score
            closed[state] = score                               #add state to closed states, include score. Update if already in
            if problem.isGoalState(state):                      #if state is goal
                return directions                               #return directions to goal /if
            for succ in problem.getSuccessors(state):           #for every successor to current state
                newScore = score + succ[2]           
                fringe.update((succ[0], directions + [succ[1]], newScore), newScore)   #add succesors to fringe, or update if already in /if

    #end, should never be reached
    return

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #variables
    from util import PriorityQueue
    fringe = PriorityQueue() #Queue of tuples containing: state, directions from start to state
    closed = [] #closed states, back to a list because otherwise test case graph_manypaths does not pass, not 100% sure why
    fringe.push((problem.getStartState(), [], 0), 0)

    #loop
    while not fringe.isEmpty():
        state, directions, score = fringe.pop()             #pop top off fringe
        closed.append((state,score))                        #add to closed
        if problem.isGoalState(state):                      #if state is goal
            return directions                               #return directions to goal /if
        for succ in problem.getSuccessors(state):           #for every successor to current state
            newDirections = directions + [succ[1]]
            newScore = problem.getCostOfActions(newDirections)
            visit = True
            for visited in closed:
                if (succ[0] == visited[0]) and (newScore >= visited[1]): #check if need to visit
                    visit = False
            if visit: 
                fringe.update((succ[0], newDirections, newScore), newScore + heuristic(succ[0], problem)) #add succesors to fringe, or update if already in /if
                closed.append((succ[0], newScore)) #add to closed

    #end, should never be reached
    return 


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
