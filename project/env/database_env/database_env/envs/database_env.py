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

        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.observation_space = spaces.Box(
            low = 0,
            high = 1,
            shape = (
                N_TABLES,
                N_TABLES
            ),
            dtype = np.uint8
        )

    def step(self, action):
        pass
 
    def reset(self):
        pass
 
    def render(self, mode='human', close=False):
        pass