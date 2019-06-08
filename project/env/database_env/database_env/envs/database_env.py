import gym
from gym import error, spaces, utils
from gym.utils import seeding
 
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

        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.observation_space = spaces.Box(
            low = 0,
            high = 1,
            shape = (
                N_TABLES
            ),
            dtype = np.uint8
        )

        # Capture information about episode to replay the same
        # on the real database
        self.history = { }
        self.current_step = 0
        self.max_steps = N_MAX_STEPS
        self.current_views = []


    def step(self, action):
        # Use the action predicted by agent to modify the
        # database environment
        self._take_action(action)

        # See the state of the new environment
        obs = self._next_observation(action)

        # Calculate reward of the action
        delay_modifier = (self.current_step / MAX_STEPS)
        reward = self.candidate_cost * delay_modifier

        # Log some info about this training step
        info = {}
        self.current_step += 1
        # Check whether we have reached end of episode
        done = self.current_step < self.max_steps

        return obs, reward, done, info

    # Reset the state of the environment to an initial state
    def reset(self):
        self.candidate_cost = INITIAL_ACCOUNT_BALANCE
        return self._next_observation()

    def render(self, mode='human', close=False):
        pass

    def _next_observation(self, params):
        pass

    def _take_action(self, action):
        pass
        