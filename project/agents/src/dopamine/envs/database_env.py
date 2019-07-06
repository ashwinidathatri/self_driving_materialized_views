import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import math
import random
import itertools
import re
import pylru
from os import listdir
from os.path import isfile, join
import Queue

class DatabaseEnv(gym.Env):  
	metadata = {'render.modes': ['human']}
	
  
	def __init__(self):
		self.table_array=["aka_name","aka_title","cast_info","char_name","comp_cast_type","company_name","company_type","complete_cast","employee","info_type","keyword","kind_type",
		"link_type","movie_companies","movie_info","movie_info_idx","movie_keyword","movie_link","name","person_info","role_type","title"]
		self.query_array= [f for f in listdir("src/dopamine/envs/env/job") if ((isfile(join("src/dopamine/envs/env/job", f))) and re.match("^[0-9]+.*sql$",f))]
		self.action_to_table=dict()
		self.CREATE_VIEW_ACTION = 1
		print(self.query_array)
		super(DatabaseEnv, self).__init__()
		self.env= self
		# Number of actions that the database can take
		# { Create View, Do nothing }
		self.N_DISCRETE_ACTIONS = 2
		
		#Form a dictionary that gives a number (between 0 and 210) to each pair of tables.
		temp = [list(x) for x in itertools.combinations(self.table_array, 2)]
		for i in range(0,len(temp)):
			self.action_to_table[i]=temp[i] 			

		# Number of tables in the database being considered
		self.N_TABLES = 21#args['n_tables']
		self.N_JOIN_COMBINATIONS =int(math.factorial(self.N_TABLES) / (math.factorial(self.N_TABLES - 2) * math.factorial(2)))

		# Maximum number of steps in an episode
		self.N_MAX_STEPS = 100#args['max_steps']
		self.N_MAX_VIEWS = 15
		#N_MAX_JOINS = 10 #Max mat. views
		self.current_candidate=0
		# Define action and observation space
		# They must be gym.spaces objects
		self.action_space = spaces.Discrete(self.N_DISCRETE_ACTIONS)
		self.observation_space = spaces.Box(
			low = 0,
			high = 1,
			shape = (
				2, self.N_JOIN_COMBINATIONS,
			),
			dtype = np.uint8
		)

		# Capture information about episode to replay the same
		# on the real database
		self.history = { }
		self.current_step = 0
		self.max_steps = self.N_MAX_STEPS
		self.current_views = []
		self.candidate_cost = 100
		self.obs_space = np.zeros(2,self.N_JOIN_COMBINATIONS)
		self.cache=pylru.lrucache(size)
		self.candidate_pool = Queue.Queue()
		self._candidate_picker()

	def _pick_query(self):
		return np.random.choice(self.query_array, size=1)#Here we can pass the probability distribution

	def _candidate_picker(self):
		if self.candidate_pool.empty():
			q=self._pick_query()
			#Task 6 Given query get candidates...
			#Here we enqueue the candidates
			#Add q to history
		cand = np.zeros(1,self.N_JOIN_COMBINATIONS)
		self.current_candidate=self.candidate_pool.pop()
		cand[0][self.current_candidate]=1
		self._obs_space[1]=cand	
				
	def step(self, action):
		if self.current_candidate in self.cache:
			value = self.cache[self.current_candidate]#Here we mark the current candidate as used...
		# Use the action predicted by agent to modify the
		# database environment and calculate reward of the action
		delay_modifier = (self.current_step / self.max_steps)
		# print(self._obs_space)
		reward = self._take_action(action, self.current_candidate, delay_modifier)
		# print(self._obs_space)
		# See the state of the new environment
		obs = self._next_observation()
		# Log some info about this training step
		info = {}
		self.current_step += 1
		# Check whether we have reached end of episode
		done = self.current_step >= self.max_steps
		if not done:
			self._candidate_picker()
		return obs, reward, done, info

	# Reset the state of the environment to an initial state
	def reset(self):
		self.history = { }#TASK 11- Double check that you delete your history, that the init and reset work fine.
		self.current_step = 0
		self.current_views = []
		self.candidate_cost = 100
		self._obs_space = np.zeros(self.N_JOIN_COMBINATIONS)
		self._current_action = np.zeros(self.N_JOIN_COMBINATIONS)
		self.candidate_picker()
		return self._next_observation()
	def render(self, mode='human', close=False):
		pass

	def _next_observation(self):
		return self._obs_space

	def get_cost_of_episode(self):
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
