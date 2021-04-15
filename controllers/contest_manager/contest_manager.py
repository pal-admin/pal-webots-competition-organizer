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


referee = Supervisor()
timestep = int(referee.getBasicTimeStep())

robot_node = referee.getFromDef('PARTICIPANT_ROBOT')
emitter = referee.getDevice('emitter')

points = None

while referee.step(timestep) != -1:
    points = robot_node.getPosition()[1]
    break

# Store the results
with open('/tmp/results.txt', 'w') as f:
    f.write(f'points: {points}\n')

# We want to see the fall :)
referee.step(20 * timestep)

# Notify the end of the game
emitter.send('done'.encode('utf-8'))
referee.step(timestep)
