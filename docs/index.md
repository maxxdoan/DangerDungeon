---
layout: default
title:  Home
---

Source code: https://github.com/maxxdoan/DangerDungeon
Welcome to our Danger Dungeon Project Page, this is a project for CS 175 - Project in AI (In Minecraft). 
In this project, we apply reinforment learning algorithms to teach our AI agent how to navigate through an obstacle course.

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)

![Alt Text](https://images-ext-2.discordapp.net/external/6BF6DzNVG143Fw7lkTALGRoUZasb8HKdEt1zrF1kxHo/https/cdn.mos.cms.futurecdn.net/m3WrriWje4hvzFBpALojFm-970-80.jpg.webp)


## Summary
Our project will involve training an agent to navigate a environment filled with dangerous traps and obstacles to overcome. It will be the agent's goal to navigate the environment safely which will involve jumping over the traps as necessary to escape. Using Malmo along with some Reinforcement Learning algorithms the agent will take in a state which includes the agent's current posititon in (x, y, z) format and the agent's yaw (the direction the agent is facing). The agent's reward for any one mission will be dependant on how close the agent was to the goal location by the end of mission's running time. The action space will be continuous and include the following actions: moving forward, turning, and jumping. This action pool may have more or fewer actions in the future as we learn what creative features we can implement in the agent's course.
