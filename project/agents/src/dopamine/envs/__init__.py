from gym.envs.registration import register

register(
    id='selma-v0',
    entry_point='envs.database_env:DatabaseEnv',
    max_episode_steps=100,
)
