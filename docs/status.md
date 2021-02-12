---
layout: default
title: Status Report
---

## 1. Summary of the Project
<br>
Our project will involve training an agent to navigate a environment filled with dangerous traps and obstacles to overcome. It will be the agent's goal to navigate the environment safely which will involve jumping over the traps as necessary to escape. Using Malmo along with some Reinforcement Learning algorithms the agent will take in a state which includes the agent's current posititon in (x, y, z) format and the agent's yaw (the direction the agent is facing). The agent's reward for any one mission will be dependant on how close the agent was to the goal location by the end of mission's running time. The action space will be continuous and include the following actions: moving forward, turning, and jumping. This action pool may have more or fewer actions in the future as we learn what creative features we can implement in the agent's course.

[Project Video](https://www.youtube.com/watch?v=NuP8E1t58Sgk "Danger Dungeon")

## 2. Approach
<br>
We have the agent traverses an obstacle course. The goal is for the agent to safely cross the lave river and reach the emerald on the other side of the course.
<br>
We design 2 separate experiment:
<br>
In the first experiment, the agent would be place in a big environment and could perform 3 actions: moving, jumping and turning. 
<br>
In the second experiment, the agent would be place in a smaller environment and could only perform 2 actions: moving and jumping.

![Alt Text](https://github.com/maxxdoan/DangerDungeon/blob/main/DangerDungeon.jpg)


## 3. Evaluation
The agent will received a reward on the scale of 0 to 50, which is based on its end location when th timer runs out.
<br>
First Experiment - Bigger Room with Turning:
<br>
The agent had the ability to turn and was placed in a broad environment. The agent managed to travel around 100,000 steps but could only receive half of the reward and never managed to get over the lava line. We believe this is because the environment was too big and that lead to too many options.
<br>
Second Experiment - Bigger Room with Turning:
<br>
We took away the turning ability and placed the agent in a smaller environment. The agent managed to get more reward this time.
<br>

![Alt Text](https://github.com/maxxdoan/DangerDungeon/blob/main/RewardGraph.jpg) 


## 4. Remaining Goals and Challenges

## 5. Resources Used
1. We used Homework 2 Template as a skeleton for our reinforcement learning algorithm
