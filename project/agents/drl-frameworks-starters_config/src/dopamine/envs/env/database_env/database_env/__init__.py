from gym.envs.registration import register
 
register(id='DatabaseEnv-V0', 
    entry_point='database_env.envs:DatabaseEnv', 
)