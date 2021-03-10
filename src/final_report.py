# Rllib docs: https://docs.ray.io/en/latest/rllib.html
#<Reward reward="'''+str(self.last_obs[0]*50)+'''" description="found_goal"/>

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import sys
import time
import json
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint

import gym, ray
from gym.spaces import Discrete, Box
from ray.rllib.agents import ppo


class DiamondCollector(gym.Env):

    def __init__(self, env_config):  
        # Static Parameters
        self.size = 50
        self.reward_density = .1
        self.penalty_density = .02
        self.obs_size = 4 #changed from 5
        self.max_episode_steps = 100
        self.log_frequency = 10
        self.action_dict = {
            0: 'move 1',  # Move one block forward
            1: 'strafe -1',  # strafe to the left
            2: 'strafe 1',  # strafe to the right
            #3: 'turn -1',  # Turn 90 degrees to the left
        }

        # Rllib Parameters
        self.action_space = Discrete(len(self.action_dict)) #BACK TO DISCRETE FOR FINAL REPORT
        self.observation_space = Box(-1000, 1000, shape=(self.obs_size,), dtype=np.float32) # Not sure what to do here

        # Malmo Parameters
        self.agent_host = MalmoPython.AgentHost()
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

        # Agent Parameters
        self.obs = np.zeros(self.obs_size)
        self.last_obs = np.zeros(self.obs_size)
        self.zstart = 82.5
        self.zend = 96.5
        self.xstart = 655.5
        self.xend = 648.5
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []

    def reset(self):
        """
        Resets the environment for the next episode.

        Returns
            observation: <np.array> flattened initial obseravtion
        """
        # Reset Malmo
        world_state = self.init_malmo()

        # Reset Variables
        self.returns.append(self.episode_return)
        current_step = self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0

        # Log
        if len(self.returns) > self.log_frequency + 1 and \
            len(self.returns) % self.log_frequency == 0:
            self.log_returns()

        # Get Observation
        self.last_obs = self.obs
        self.obs = self.get_observation(world_state)

        return self.obs

    def step(self, action):
        """
        Take an action in the environment and return the results.

        Args
            action: <int> index of the action to take

        Returns
            observation: <np.array> flattened array of obseravtion
            reward: <int> reward from taking action
            done: <bool> indicates terminal state
            info: <dict> dictionary of extra information
        """

        #Thresholding attack value
        # Get Action
        command = self.action_dict[action]
        self.agent_host.sendCommand(command)
        time.sleep(.2)
        self.episode_step += 1

        # Get Observation
        world_state = self.agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)
        self.last_obs = self.obs
        self.obs = self.get_observation(world_state) 

        # Get Done
        done = not world_state.is_mission_running 

        # Get Reward
        reward = 0
        if command == 'move 1':
            reward += 1
        for r in world_state.rewards:
            reward += r.getValue()
        self.episode_return += reward

        return self.obs, reward, done, dict()
 
    def get_mission_xml(self):

        return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

                    <About>
                        <Summary>Final Report</Summary>
                    </About>

                    <ServerSection>
                        <ServerInitialConditions>
                            <Time>
                                <StartTime>12000</StartTime>
                                <AllowPassageOfTime>false</AllowPassageOfTime>
                            </Time>
                            <Weather>clear</Weather>
                        </ServerInitialConditions>
                        <ServerHandlers>
                            <FileWorldGenerator src="C:\\Users\\zerom\\Desktop\\Malmo\\Minecraft\\run\\saves\\New World"/>
                            <DrawingDecorator>''' + \
                                "<DrawCuboid x1='-648' x2='-648' y1='3' y2='3' z1='-89' z2='-85' type='stone'/>" + \
                                "<DrawCuboid x1='-648' x2='-648' y1='4' y2='4' z1='-89' z2='-85' type='lava'/>" + \
                                "<DrawCuboid x1='-640' x2='-640' y1='3' y2='3' z1='-89' z2='-85' type='stone'/>" + \
                                "<DrawCuboid x1='-640' x2='-640' y1='4' y2='4' z1='-89' z2='-85' type='lava'/>" + \
                                "<DrawCuboid x1='-648' x2='-648' y1='3' y2='3' z1='-95' z2='-91' type='stone'/>" + \
                                "<DrawCuboid x1='-648' x2='-648' y1='4' y2='4' z1='-95' z2='-91' type='lava'/>" + \
                                "<DrawCuboid x1='-640' x2='-640' y1='3' y2='3' z1='-95' z2='-91' type='stone'/>" + \
                                "<DrawCuboid x1='-640' x2='-640' y1='4' y2='4' z1='-95' z2='-91' type='lava'/>" + \
                                '''
                            </DrawingDecorator>
                            <ServerQuitWhenAnyAgentFinishes/>
                        </ServerHandlers>
                    </ServerSection>

                    <AgentSection mode="Survival">
                        <Name>CS175FinalReport</Name>
                        <AgentStart>
                            <Placement x="-655.5" y="5" z="-89.5" pitch="30" yaw="270"/>
                            <Inventory>
                                <InventoryItem slot="0" type="diamond_pickaxe"/>
                            </Inventory>
                        </AgentStart>
                        <AgentHandlers>
                            <DiscreteMovementCommands/>
                            <ObservationFromFullStats/>
                            <ObservationFromRay/>
                            <AgentQuitFromReachingCommandQuota description="found_goal" total="'''+str(self.max_episode_steps)+'''" />
                            <AgentQuitFromTouchingBlockType>
                                <Block type="emerald_block" />
                            </AgentQuitFromTouchingBlockType>
                        </AgentHandlers>
                    </AgentSection>
                </Mission>'''

    def init_malmo(self):
        """
        Initialize new malmo mission.
        """
        my_mission = MalmoPython.MissionSpec(self.get_mission_xml(), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(1)

        max_retries = 3
        my_clients = MalmoPython.ClientPool()
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

        for retry in range(max_retries):
            try:
                self.agent_host.startMission( my_mission, my_clients, my_mission_record, 0, 'DiamondCollector' )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)

        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print("\nError:", error.text)

        return world_state

    def get_observation(self, world_state):
        """
        Use the agent observation API to get a flattened 2 x 5 x 5 grid around the agent. 
        The agent is in the center square facing up.

        Args
            world_state: <object> current agent world state

        Returns
            observation: <np.array> the state observation
        """
        obs = np.zeros(self.obs_size)
        allow_break_action = False

        while world_state.is_mission_running:
            time.sleep(0.4)
            world_state = self.agent_host.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid.')

            if world_state.number_of_observations_since_last_state > 0:
                # First we get the json from the observation API
                msg = world_state.observations[-1].text
                observations = json.loads(msg)

                # New Observation (final report)
                obs[0] = (-observations['XPos'] - self.xstart) / (self.xend - self.xstart)
                obs[1] = 0.0 # might not need this
                obs[2] = (-observations['ZPos'] - self.zstart) / (self.zend - self.zstart)
                yaw = observations['Yaw']
                if yaw < -180:
                    yaw += 360
                if yaw > 180:
                    yaw -= 360
                yaw += 180

                obs[3] = yaw / 360

                # Rotate observation with orientation of agent
                # obs = obs.reshape((2, self.obs_size, self.obs_size))
                # yaw = observations['Yaw']
                # if yaw >= 225 and yaw < 315:
                #     obs = np.rot90(obs, k=1, axes=(1, 2))
                # elif yaw >= 315 or yaw < 45:
                #     obs = np.rot90(obs, k=2, axes=(1, 2))
                # elif yaw >= 45 and yaw < 135:
                #     obs = np.rot90(obs, k=3, axes=(1, 2))
                # obs = obs.flatten()
                
                break

        return obs

    def log_returns(self):
        """
        Log the current returns as a graph and text file

        Args:
            steps (list): list of global steps after each episode
            returns (list): list of total return of each episode
        """
        box = np.ones(self.log_frequency) / self.log_frequency
        returns_smooth = np.convolve(self.returns[1:], box, mode='same')
        plt.clf()
        plt.plot(self.steps[1:], returns_smooth)
        plt.title('Final Report')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig('returns.png')

        with open('returns.txt', 'w') as f:
            for step, value in zip(self.steps[1:], self.returns[1:]):
                f.write("{}\t{}\n".format(step, value)) 


if __name__ == '__main__':
    ray.init()
    trainer = ppo.PPOTrainer(env=DiamondCollector, config={
        'env_config': {},           # No environment parameters to configure
        'framework': 'torch',       # Use pytorch instead of tensorflow
        'num_gpus': 0,              # We aren't using GPUs
        'num_workers': 0            # We aren't using parallelism
    })

    while True:
        print(trainer.train())
