import numpy as np
import os
import pickle

class EnvRunner():
	################## Constructor #####################
	#
	# 1. max_steps -> Number of steps for an episode 
	# - (select max_step number of queries per episode)
	#
	####################################################
	def __init__(self, run_config):
		self.max_steps = run_config['max_steps']

	########## Method to run the agent in an environment ##########
	#
	# 1. Select a query according to the defined workload distribution
	# 2. Get all candidates for the query and enqueue them
	# 3. Send all these candidates to the agent and take step in env
	# 4. Do max_step number of times
	# 5. Once i == max_step (Episode end) - Replay history of env for episode
	#
	###############################################################
	def run(self, env):
		step = 0

		queries = []
		exclusion_list = ['schema.sql', 'fkindexes.sql']
		for root, dirs, files in os.walk('../data/JOB/'):
			for file in files:
				if file in exclusion_list:
					continue
				if '.sql' in file:
					queries.append(file)

		print(queries)
		pickle_file_path = '../data/JOB/processed/job_processed.pickle'
		with open(pickle_file_path, 'rb') as pickle_file:
			candidates = pickle.load(pickle_file)

		while(step < self.max_steps):
			step = step + 1			
			############## Step 1 - Define distribution and pick query ############
			# TODO - replace with actual database workload distribution
			
			# An array of the index value for weighting
			i = np.arange(len(queries))
			# Higher weights for larger index values
			w = np.exp(i/10.)
			# Weight must be normalized
			w /= w.sum()

			# Now, select query according to above distribution
			selected_query = np.random.choice(queries, size = 1, p = w)[0]
			print('Current Query - ' + selected_query + ' ...')

			# Hack for parsing processed candidates.
			# TODO - Fix preprocessing for candidates to return a dictionary
			# with keys as query names, and list of candidates as values 
			new_candidates = {}
			for candidate in candidates:
				for key, value in candidate.items():
					new_candidates[key] = value

			print('Current candidate ...')
			curr_candidates = new_candidates['data/JOB/' + selected_query]
			print(curr_candidates)
			###########################################################################

			############## Step 2 - Get all candidates and enqueue ####################
			for candidate in curr_candidates:
				candidate = candidate.flatten()
				# Send to agent and get back action
				# Currently hacked. Replace with real agent later
				action = env.action_space.sample()
				obs, reward, done, info = env.step(action, candidate)
			###########################################################################

		env.replay_history_on_db()
		env.reset()


params = {
	'max_steps': 40
}
runner = EnvRunner(params)
runner.run()