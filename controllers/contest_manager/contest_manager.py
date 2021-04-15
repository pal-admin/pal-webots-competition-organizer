#!/usr/bin/env python3
#
# Copyright 1996-2021 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from controller import Supervisor

MAXIMUM_TIME = 60
SPENT_TIME = 0
MAXIMUM_POINTS = 9+9
NEGATIVE_POINTS = MAXIMUM_POINTS
GOAL_X = 4.5
GOAL_Z = 4.5
EPS = 0.2

referee = Supervisor()
timestep = int(referee.getBasicTimeStep())

robot_node = referee.getFromDef('PARTICIPANT_ROBOT')
emitter = referee.getDevice('emitter')

while referee.step(timestep) != -1 and SPENT_TIME < MAXIMUM_TIME:
    manh_dist = GOAL_X - robot_node.getPosition()[0] + GOAL_Z - robot_node.getPosition()[2] 
    if manh_dist < EPS:
        NEGATIVE_POINTS = 0
        break
    NEGATIVE_POINTS = min(NEGATIVE_POINTS, manh_dist)
    SPENT_TIME += timestep

points = (MAXIMUM_POINTS - NEGATIVE_POINTS)*(70/MAXIMUM_POINTS) + (MAXIMUM_TIME - SPENT_TIME)*(30/MAXIMUM_TIME)

# Store the results
with open('/tmp/results.txt', 'w') as f:
    f.write(f'points: {points}\n')

# We want to see the fall :)
referee.step(20 * timestep)

# Notify the end of the game
emitter.send('done'.encode('utf-8'))
referee.step(timestep)
