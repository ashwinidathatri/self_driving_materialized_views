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
from collections import deque
import time

CREATE_VIEW_ACTION = 1

class DatabaseEnv(gym.Env):  
	metadata = {'render.modes': ['human']}   
	def __init__(self, args = {}):
		super(DatabaseEnv, self).__init__()

		# Number of actions that the database can take
		# { Create View, Do nothing }
		N_DISCRETE_ACTIONS = 2
		
		# Number of tables in the database being considered
		N_TABLES = 21
		N_JOIN_COMBINATIONS = int((N_TABLES * (N_TABLES - 1)) / 2)

		self.database = Database()
		self.table_names = self.database.get_table_names_from_hive()
		self.join_name_mappings = self.get_mapping_for_tables(self.table_names)

		# Maximum number of steps in an episode
		N_MAX_STEPS = 5
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
		self.current_candidate_queue = deque()
		self._obs_space = np.zeros(N_JOIN_COMBINATIONS)
		self._current_action = np.zeros(N_JOIN_COMBINATIONS)
		self.lru_cache_size = 20
		self.lru_cache = LRU(self.lru_cache_size)

	def get_mapping_for_tables(self, table_names):
		mapping = {}
		names = []
		for name in table_names:
			name = name[0]
			print(name)
			names.append(name)
		self.table_names = names
		num = 0
		for i in range(len(names)):
			for j in range(i + 1, len(names)):
				join_name = names[i] + '-' + names[j]
				num = num + 1
				mapping[num] = join_name
		print(mapping)
		return mapping

	def reset_env_history(self):
		history = {}
		for i in range(1, self.max_steps):
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
		if not self.current_candidate_queue:
			self.current_step = self.current_step + 1
			self.selected_query = np.random.choice(
				self.queries,
				size = 1,
				p = self.workload_distribution)[0]
			self.history[self.current_step]['query'] = self.selected_query 
			candidates = self.get_candidates_for_query(self.selected_query)
			print(self.selected_query)
			for candidate in candidates:
				candidate = candidate.flatten()
				self.current_candidate_queue.append(candidate)

		current_candidate = self.current_candidate_queue.popleft()
		print('Action - ' + str(action))
		cand_idx = np.where(current_candidate == 1)[0]
		print('Candidate - ' + self.join_name_mappings[int(cand_idx)])
		self.lru_cache[self.selected_query] = current_candidate

		# Log some info about this training step
		self.history[self.current_step]['actions'].append(
			{
				'action': action,
				'candidate': current_candidate,
				'obs_space': self._obs_space,
				'eviction': self.lru_cache.peek_last_item(),
			}
		)

		reward, eviction = self._take_action(action, current_candidate, delay_modifier)
		print('Reward - ' + str(reward))
		done = self.current_step >= self.max_steps
		
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
		for step, step_history in self.history.items():
			print('------------ Step - ' + str(step) + ' -------------')
			# First run the query and check the base cost
			query = step_history['query']
			print(query)
			with open(os.path.join('/home/richhiey/Desktop/workspace/dbse_project/Self-Driving-Materialized-Views/project/data/JOB/', query),'r') as f:
				query_str = f.read()
				start_time = time.time()
				print('Actually executing on database now ..')
				query_output = self.database.execute_query(query_str)
				total_time = time.time() - start_time
				print('Time taken - ' + str(total_time))
				run_time = run_time + total_time
				print('Execution done!')

			def get_view_creation_query(tbl_1, tbl_2):
				view_name = str(tbl_1) + '_' + str(tbl_2)
				query_str = str(tbl_1) + ' JOIN ' + str(tbl_2) + ';'
				query_str = query_str + "CREATE VIEW IF NOT EXISTS " + view_name + " AS " + query_str
				return query_str
			
			# Then run through the history and get costs for the actions
			# taken by the agent
			if len(step_history['actions']) > 0:
				for step in step_history['actions']:
					if step['action']:
						idx = np.where(step['candidate'] == 1)
						print(idx)
						temp = self.join_table_mapping[int(idx)].split('-')
						table_1 = temp[0]
						table_2 = temp[1]
						query_str = get_view_creation_query(table_1, table_2)
						start_time = time.time()
						query_output = self.database.execute_query(query_str)
						total_time = time.time() - start_time
						print('View Creation Time taken - ' + str(total_time))
						run_time = run_time + total_time
			print('Total runtime - ' + str(run_time))
			print('---------------------------------------------------')
		return run_time

	def hawc_cost_for_episode(self):
		return np.random.randint(0,100)

	def calculate_reward_for_episode(self):
		initial_reward = 20
		env_reward = self.env_cost_of_episode()
		print(env_reward)
		hawc_reward = self.hawc_cost_for_episode()
		return ((env_reward - initial_reward) / 
					(hawc_reward - initial_reward)) * 1000

	def _take_action(self, action, candidate, delay_modifier):
		if action:
			# Add the created view to the obs space
			# self._obs_space = np.add(self._obs_space, candidate)
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
		return reward, False

database = DatabaseEnv()
for i in range(50):
	database.step(np.random.randint(2))