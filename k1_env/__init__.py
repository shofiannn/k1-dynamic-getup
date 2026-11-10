from gymnasium.envs.registration import register

register(
    id="k1-standup-v0",
    entry_point="k1_env.env:K1Env",
)
