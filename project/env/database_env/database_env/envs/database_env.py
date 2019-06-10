import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import math

class DatabaseEnv(gym.Env):  
	metadata = {'render.modes': ['human']}   
	def __init__(self, args):
		super(DatabaseEnv, self).__init__()

		# Number of actions that the database can take
		# { Create View, Do nothing }
		N_DISCRETE_ACTIONS = 2
		
		# Number of tables in the database being considered
		N_TABLES = args['n_tables']

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
				1,
				int(math.factorial(N_TABLES) / math.factorial(N_TABLES - N_MAX_JOINS) * math.factorial(N_MAX_JOINS))
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


	def step(self, action):
		# Use the action predicted by agent to modify the
		# database environment and calculate reward of the action
		delay_modifier = (self.current_step / self.max_steps)
		reward = self._take_action(action, delay_modifier)

		# See the state of the new environment
		obs = self._next_observation(action)

		# Log some info about this training step
		info = {}
		self.current_step += 1

		# Check whether we have reached end of episode
		done = self.current_step < self.max_steps

		return obs, reward, done, info

	# Reset the state of the environment to an initial state
	def reset(self):
		return self._next_observation()

	def render(self, mode='human', close=False):
		pass

	def _next_observation(self, params):
		pass

	def _take_action(self, action):
		print('Taking action in environment')
		
		if self.current_step < self.max_steps:
			reward = 1
		else:
			# - Do some magic to get cost of the queries
			# to calculate a useful cost for episode
			# - Calculate reward using that
			cost = self.get_cost_of_episode()
			reward = self.calculate_reward_for_episode()
		print('Step in environment has completed!')
		return reward

# Random testing stuff
d = DatabaseEnv({'max_steps': 100, 'n_tables': 20})
print(d)
print("Action Space -")
print(d.action_space)
print("Observation Space -")
print("Max values for observation space -")
print(d.observation_space.high)
print("Min values for observation space -")
print(d.observation_space.low)