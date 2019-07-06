import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import math
import random
from lru import LRU
from db import Database
import os
import pickle 

CREATE_VIEW_ACTION = 1
N_JOIN_COMBINATIONS = 210

class DatabaseEnv(gym.Env):  
	metadata = {'render.modes': ['human']}   
	def __init__(self, args = {}):
		super(DatabaseEnv, self).__init__()

		# Number of actions that the database can take
		# { Create View, Do nothing }
		N_DISCRETE_ACTIONS = 2
		
		# Number of tables in the database being considered
		N_TABLES = 21
		# N_JOIN_COMBINATIONS = 
		# 		int(math.factorial(N_TABLES) / 
		# 			math.factorial(N_TABLES - N_MAX_JOINS) * math.factorial(N_MAX_JOINS))

		# Maximum number of steps in an episode
		N_MAX_STEPS = 30
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
		self.max_steps = N_MAX_STEPS
		self.history = self.reset_env_history()
		self.current_step = 0
		self.current_views = []
		self.candidate_cost = 100
		exclusion_list = ['schema.sql', 'fkindexes.sql']
		self.queries = self.get_queries_from_dataset('/home/richhiey/Desktop/workspace/dbse_project/Self-Driving-Materialized-Views/project/data/JOB', exclusion_list)
		pickle_file_path = '/home/richhiey/Desktop/workspace/dbse_project/Self-Driving-Materialized-Views/project/data/JOB/processed/job_processed.pickle'
		self.candidates = self.get_candidates_for_dataset(pickle_file_path)
		self.workload_distribution = self.get_workload_distribution(self.queries)
		self.current_candidate_queue = []
		self._obs_space = np.zeros(N_JOIN_COMBINATIONS)
		self._current_action = np.zeros(N_JOIN_COMBINATIONS)
		self.lru_cache_size = 20
		self.lru_cache = LRU(self.lru_cache_size)
		self.database = Database()

	def reset_env_history(self):
		history = {}
		for i in range(self.max_steps):
			history[i] = {'actions': [], 'query': ''}
		return history

	def get_workload_distribution(self, queries):
		# An array of the index value for weighting
		i = np.arange(len(queries))
		# Higher weights for larger index values
		w = np.exp(i/10.)
		# Weight must be normalized
		w /= w.sum()
		return w

	def get_candidates_for_query(self, query):
		return self.candidates['data/JOB/' + query]

	def get_candidates_for_dataset(self, pickle_file_path):
		with open(pickle_file_path, 'rb') as pickle_file:
			candidates = pickle.load(pickle_file)
		new_candidates = {}
		for candidate in candidates:
			for key, value in candidate.items():
				new_candidates[key] = value
		return new_candidates
		
	def get_queries_from_dataset(self, dataset_path, exclusion_list):
		queries = []
		for root, dirs, files in os.walk(dataset_path):
			for file in files:
				if file in exclusion_list:
					continue
				if '.sql' in file:
					queries.append(file)
		return queries

	def step(self, action):
		# Use the action predicted by agent to modify the
		# database environment and calculate reward of the action
		delay_modifier = (self.current_step / self.max_steps)
		# print(self._obs_space)
		print(self.current_step)

		if not current_candidate_queue:
			self.current_step = self.current_step + 1
			self.selected_query = np.random.choice(
				self.queries,
				size = 1,
				p = self.workload_distribution)[0]
			self.history[self.current_step]['query'] = selected_query 
			candidates = self.get_candidates_for_query(selected_query)
			for candidate in candidates:
				candidate = candidate.flatten()
				self.current_candidate_queue.enqueue(candidate)

		current_candidate = self.current_candidate_queue.dequeue()
		self.lru_cache[current_candidate] = self.selected_query

		# Log some info about this training step
		self.history[self.current_step]['actions'].append(
			{
				'action': action,
				'candidate': candidate,
				'obs_space': self._obs_space,
				'eviction': self.lru_cache.peek_last_item()
			}
		)

		reward, eviction = self._take_action(action, current_candidate, delay_modifier)

		done = self.current_step >= self.max_steps - 1
		
		if done and len(self.current_candidate_queue):
			reward = get_final_reward_for_episode()
			info = {}
			done = True
		else:
			done = False

		obs = self._next_observation()

		return obs, reward, done, self.history

	# Reset the state of the environment to an initial state
	def reset(self):
		self.history = self.reset_env_history()
		self.current_step = 0
		self.current_views = []
		self.candidate_cost = 100
		self._obs_space = np.zeros(N_JOIN_COMBINATIONS)
		self._current_action = np.zeros(N_JOIN_COMBINATIONS)
		self.lru_cache = LRU(self.lru_cache_size)
		return self._next_observation()

	def render(self, mode='human', close=False):
		pass

	def _next_observation(self):
		return self._obs_space

	def env_cost_of_episode(self):
		run_time = 0
		for step, step_history in history.items():
			print('------------ Step - ' + str(step) + ' -------------')
			# First run the query and check the base cost
			query = step_history['query']
			with open(os.path.join('data/JOB/', query),'r') as f:
				query_str = f.read()
				exp_analyze = self.database.explain_analyze_query(query_str)
			
			def parse_for_exec_time(exp_analyze):
				# parse the explain analuze stuff once you understand it
				return np.random.randint(100)

			def get_view_creation_query(tbl_1, tbl_2):
				view_name = str(tbl_1) + '_' + str(tbl_2)
				query_str = str(tbl_1) + ' JOIN ' + str(tbl_2) + ';'
				query_str = query_str + "CREATE VIEW IF NOT EXISTS " + view_name + " AS " + query_str
				return query_str

			execution_time = parse_for_exec_time(exp_analyze)
			run_time = run_time + execution_time
			
			# Then run through the history and get costs for the actions
			# taken by the agent
			for step in step_history['actions']:
				if step['action']:
					idx = np.where(step['candidate'] == 1)
					table_1, table_2 = table_mapping[idx]
					query_str = get_view_creation_query(table_1, table_2)
					exp_analyze = self.database.explain_analyze_query(query_str)
					execution_time = parse_for_exec_time(exp_analyze)
					run_time = run_time + execution_time

			print('---------------------------------------------------')
		return run_time

	def hawc_cost_for_episode(self):
		return np.random.randint(0,100)

	def calculate_reward_for_episode(self):
		initial_reward = 20
		env_reward = self.env_cost_of_episode()
		hawc_reward = self.hawc_cost_for_episode()
		return ((env_reward - initial_reward) / 
					(hawc_reward - initial_reward)) * 1000

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
				reward = self.calculate_reward_for_episode()
		else:
			# Add the created view to the obs space
			# Calculate reward
			if self.current_step < self.max_steps - 1:
				reward = 0
			else:
				# - Do some magic to get cost of the queries
				# to calculate a useful cost for episode
				# - Calculate reward using that
				reward = self.calculate_reward_for_episode()
		return reward

database = DatabaseEnv()
database.step(1)
database.reset()