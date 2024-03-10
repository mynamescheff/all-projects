import gym
from gym import spaces
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class CustomGridEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    grid_size = 10
    scale = 50  # Scale the rendering up

    def __init__(self):
        super(CustomGridEnv, self).__init__()
        self.action_space = spaces.Discrete(4)  # up, down, left, right
        self.grid_size = 100  # Increase grid size for smoother movement
        self.observation_space = spaces.Box(
            low=np.array([0, 0]),
            high=np.array([self.grid_size-1, self.grid_size-1]),
            dtype=np.int32
        )
        
        self.start = (1 * self.scale, 1 * self.scale)  # Scale the start position up
        self.end = (8 * self.scale, 8 * self.scale)  # Scale the end position up
        self.obstacles = [(3 * self.scale, 4 * self.scale), 
                          (5 * self.scale, 6 * self.scale), 
                          (7 * self.scale, 3 * self.scale)]  # Scale the obstacles up

        self.agent_position = self.start

    def step(self, action):
        # Apply action
        # 0: up, 1: down, 2: left, 3: right
        if action == 0:
            self.agent_position = (self.agent_position[0], max(self.agent_position[1] - self.scale, 0))
        elif action == 1:
            self.agent_position = (self.agent_position[0], min(self.agent_position[1] + self.scale, (self.grid_size - 1) * self.scale))
        elif action == 2:
            self.agent_position = (max(self.agent_position[0] - self.scale, 0), self.agent_position[1])
        elif action == 3:
            self.agent_position = (min(self.agent_position[0] + self.scale, (self.grid_size - 1) * self.scale), self.agent_position[1])

        # Check if the agent hit an obstacle
        if any(self._is_collision(self.agent_position, obs) for obs in self.obstacles):
            reward = -1
            done = True
            self.agent_position = self.start  # Reset to start
        # Check if the agent reached the goal
        elif self._is_collision(self.agent_position, self.end):
            reward = 1
            done = True
        else:
            reward = 0
            done = False

        # Optionally we can pass additional info, not used for training
        info = {}

        return self.agent_position, reward, done, info

    def reset(self):
        self.agent_position = self.start
        return self.agent_position
    
    def _is_collision(self, pos1, pos2):
        distance = np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
        return distance < self.scale

    def render(self, mode='human'):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.grid_size * self.scale)
        ax.set_ylim(0, self.grid_size * self.scale)

        # Draw the start and end
        ax.add_patch(plt.Rectangle((0, 0), self.scale, self.scale, color='green'))
        ax.add_patch(plt.Rectangle((self.end[0], self.end[1]), self.scale, self.scale, color='green'))

        # Draw the agent
        ax.add_patch(plt.Rectangle((self.agent_position[0], self.agent_position[1]), 
                                    self.scale, self.scale, color='red'))

        # Draw the obstacles
        for obs in self.obstacles:
            ax.add_patch(plt.Circle((obs[0] + self.scale / 2, obs[1] + self.scale / 2), 
                                     self.scale / 2, color='blue'))

        plt.pause(0.01)  # Pause to update the rendering

    def close(self):
        plt.close()

# Now you can instantiate and test your custom environment
env = CustomGridEnv()
state = env.reset()
done = False
while not done:
    action = env.action_space.sample()
    next_state, reward, done, info = env.step(action)
    env.render()
env.close()
