import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import math
import random

CREATE_VIEW_ACTION = 1
N_JOIN_COMBINATIONS = 12

class DatabaseEnv(gym.Env):  
	metadata = {'render.modes': ['human']}   
	def __init__(self, args):
		super(DatabaseEnv, self).__init__()
                self.env=self
		# Number of actions that the database can take
		# { Create View, Do nothing }
		N_DISCRETE_ACTIONS = 2
		
		# Number of tables in the database being considered
		N_TABLES = args['n_tables']
		# N_JOIN_COMBINATIONS = 
		# 		int(math.factorial(N_TABLES) / 
		# 			math.factorial(N_TABLES - N_MAX_JOINS) * math.factorial(N_MAX_JOINS))

		# Maximum number of steps in an episode
		N_MAX_STEPS = args['max_steps']
		N_MAX_JOINS = 2

		# Define action and observation space
		# They must be gym.spaces objects
		self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
		self.observation_space = spaces.Box(
			low = 0,
			high = 1,
			shape = (
				N_JOIN_COMBINATIONS,
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

	def step(self, action, candidate):
		# Use the action predicted by agent to modify the
		# database environment and calculate reward of the action
		delay_modifier = (self.current_step / self.max_steps)
		# print(self._obs_space)
		reward = self._take_action(action, candidate, delay_modifier)
		# print(self._obs_space)
		# See the state of the new environment
		obs = self._next_observation()

		# Log some info about this training step
		info = {}
		self.current_step += 1

		# Check whether we have reached end of episode
		done = self.current_step >= self.max_steps

		return obs, reward, done, info

	# Reset the state of the environment to an initial state
	def reset(self):
		self.history = { }
		self.current_step = 0
		self.current_views = []
		self.candidate_cost = 100
		self._obs_space = np.zeros(N_JOIN_COMBINATIONS)
		self._current_action = np.zeros(N_JOIN_COMBINATIONS)

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
				reward = 0
			else:
				# - Do some magic to get cost of the queries
				# to calculate a useful cost for episode
				# - Calculate reward using that
				cost = self.get_cost_of_episode()
				reward = self.calculate_reward_for_episode(cost)
		return reward
