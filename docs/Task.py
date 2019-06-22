import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import math
import random
import itertools

CREATE_VIEW_ACTION = 1
#N_JOIN_COMBINATIONS = 12

class DatabaseEnv(gym.Env):  
metadata = {'render.modes': ['human']}
table_array=["movie","cast"]#Task 1 Fill this
query_array=[] #Task 2 Fill this
        action_to_table=dict()
        
  
def __init__(self):
super(DatabaseEnv, self).__init__()
self.env= self
# Number of actions that the database can take
# { Create View, Do nothing }
N_DISCRETE_ACTIONS = 2

                #Form a dictionary that gives a number (between 0 and 210) to each pair of tables.
                temp = list(x) for x in itertools.combinations(table_array, 2)
                for i in range(0,len(temp)):
action_to_table[i]=temp[i] 

# Number of tables in the database being considered
N_TABLES = 21#args['n_tables']
N_JOIN_COMBINATIONS = 
int(math.factorial(N_TABLES) / 
math.factorial(N_TABLES - 2) * math.factorial(2))

# Maximum number of steps in an episode
N_MAX_STEPS = 100#args['max_steps']

#N_MAX_JOINS = 10 #Max mat. views

# Define action and observation space
# They must be gym.spaces objects
self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
self.observation_space = spaces.Box(
low = 0,
high = 1,
shape = (
2, N_JOIN_COMBINATIONS,
),
dtype = np.uint8
)

# Capture information about episode to replay the same
# on the real database
self.history = { }
self.current_step = 0
self.max_steps = N_MAX_STEPS
self.current_views = []
self.candidate_cost = 100
self._obs_space = np.zeros(N_JOIN_COMBINATIONS)
self._current_action = np.zeros(N_JOIN_COMBINATIONS)
self._lru_info = np.zeros(N_JOIN_COMBINATIONS)

#TASK #4 decide on the lru data structure

#TASK #5 initialize a queue of candidates
                
#TASK 6- Replace the following 3 lines with a function CANDIDATE_PICKER that (you also need to sync this with self._next_observation()): 
                #if the queue is empty, picks a query (first randomly), enqueues the candidates from the query.. it also adds this query to the HISTORY
                #(not if and else, but if and then if) next, if your queue is not empty: picks a candidte from the queue and adds this to your observation space (the second row).
        sampled_action = self.action_space.sample()
temp = np.eye(N_JOIN_COMBINATIONS)
self.candidate=dummy_candidate = temp[np.random.choice(temp.shape[0], size=1)].squeeze()
             
        
def step(self, action):
                #TASK 7 Look at your candidate, in the observation space, and mark it as "used in the lru"

# Use the action predicted by agent to modify the
# database environment and calculate reward of the action
delay_modifier = (self.current_step / self.max_steps)
# print(self._obs_space)
reward = self._take_action(action, self.candidate, delay_modifier)
# print(self._obs_space)
# See the state of the new environment
obs = self._next_observation()

# Log some info about this training step
info = {}
self.current_step += 1

# Check whether we have reached end of episode
done = self.current_step >= self.max_steps
if not done:
              #TASK 6- Replace the following 3 lines with a function CANDIDATE_PICKER (you also need to sync this with self._next_observation())
sampled_action = self.action_space.sample()
temp = np.eye(N_JOIN_COMBINATIONS)
self.candidate=dummy_candidate = temp[np.random.choice(temp.shape[0], size=1)].squeeze()

return obs, reward, done, info

# Reset the state of the environment to an initial state
def reset(self):
self.history = { }#TASK 11- Double check that you delete your history, that the init and reset work fine.
self.current_step = 0
self.current_views = []
self.candidate_cost = 100
self._obs_space = np.zeros(N_JOIN_COMBINATIONS)
self._current_action = np.zeros(N_JOIN_COMBINATIONS)
                #TASK 6- Replace the following 3 lines with a function CANDIDATE_PICKER (you also need to sync this with self._next_observation())
sampled_action = self.action_space.sample()
temp = np.eye(N_JOIN_COMBINATIONS)
self.candidate = temp[np.random.choice(temp.shape[0], size=1)].squeeze()
return self._next_observation()

def render(self, mode='human', close=False):
pass

def _next_observation(self):
return self._obs_space

def get_cost_of_episode(self):
        """Task 10- Time to let go of the random rewards... We're starting with some real ones.
Intialize a totalRuntimeCounter=0
Initialize an array to keep track of the views that you will create.
          Go through your history: 
               every time you see a query: run it, get the time and add it to totalRuntimeCounter.
     every time you see the request to create a MV, create it: get the time and add it to totalRuntimeCounter.
     every time you see the request to delete a MV, delete it (dont get the time, for this, as it can be done asynchronously)
                      every time you see a view that is just seen (nothing is created), do nothing
       By the end, you should have a totalTime. Return 1000 over that as your reward for the episode. (this we will change, so I mark it with an asterisk (*)).
Here remember to drop all the views that you created (by using the tracking array). Also delete the tracking array.
Task 12: Fix the tabs vs. spaces thingy and get it to run with the agents.
Task 13: Hawc: 

                We need a dictionary data structure to track credit that has for each candidate a nested dictionary, that in turn goes from query to credit. 
                We need to again track with an array the views that you to are creating.
                Initialize your window to -10
                We need a dictionary called baseline, which goes from query (identified by the position) to runtime previous to view creation.                              to 
  NOTE: In many cases queries will be need to be tracked by their position.
            
Go through your history:
                      if window is >0:
                        look at what is in history position window
                        if it is a query, then delete it from the baseline, and from the credit tracking.
                        if it is a candidate, do nothing.

               every time you see a query: run it, get the time and add it to totalRuntimeCounter. put this to the baseline.
                      every time you see you see a MV that was either seen or created:

     we will create it (if it does not exist), so:
add to totalRuntimeCounter, the time of creating it.
once we create it we need to give it credit, so, go through each item in baseline, and run the query now that the view was created. The division of the this new runtime, by what was in baseline for that query will go into the credit tracker as the entry for that candidate query pair.
                        put now into the baseline for that query the time that was your numerator in the previous line.
                        if the number of views in the credit tracker is greater than the limit, then we need to delete one: for this we go through the credit tracker and sum the credits for all views; we  delete the one  with the smallest credit. we also delete the view from the actual database.

       if the view exists in the credit tracker, then you need to update its credit with all queries that it has no credit for within the window.
    every time you see the request to delete a MV: do nothing

                      increase your window counter by 1
                     

                      every time you see a view that is just seen (nothing is created), do nothing

(After going through the history) Delete the views that you created, according to the tracking array.
                Finally, use 1000/the time that you got for Hawc for calculating the real reward= ((Us/Hawc) *100)
Task 14: Go to the picking of the queries and make the logic to pick them not uniformly at random, but based on probabilities given in an array. Then, fihsgure out how to create a zipfian/biased distribution in this array. 
Task 15: Meet with Gabriel, design tests, run them...he 
"""
return random.randint(1, 100)

def calculate_reward_for_episode(self, cost):
return cost

def _take_action(self, action, candidate, delay_modifier):
if action:
                        #TASK 8 Check if eviction is needed, and evict, based on the LRU.
                        #TASK 9 Mark MV as deleted in history, and also mark the new MV created. If no action is done, still mark the view as something seen.

# Add the created view to the obs space
self._obs_space = np.add(self._obs_space, candidate)
# Calculate reward
if self.current_step < self.max_steps - 1:
reward = 1
else:
# - Do some magic to get cost of the queries
# to calculate a useful cost for episode
# - Calculate reward using that
cost = self.get_cost_of_episode()
reward = self.calculate_reward_for_episode(cost)
else:
# Add the created view to the obs space
# Calculate reward
if self.current_step < self.max_steps - 1:
reward = 1
else:
# - Do some magic to get cost of the queries
# to calculate a useful cost for episode
# - Calculate reward using that
cost = self.get_cost_of_episode()
reward = self.calculate_reward_for_episode(cost)
return reward