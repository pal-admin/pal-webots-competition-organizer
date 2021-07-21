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

MAXIMUM_TIME = 3*60*1000
SPENT_TIME = 0
EPS = 0.2

def getPoints(dist):
    poi_points = 0
    for j in range(10):
        if dist < EPS*(j+1):
            poi_points += 1
    return poi_points

referee = Supervisor()
timestep = int(referee.getBasicTimeStep())

robot_node = referee.getFromDef('PARTICIPANT_ROBOT')
emitter = referee.getDevice('emitter')
touch_sensor = referee.getDevice('touch sensor')

poi_list = []
poi_string_list = robot_node.getField('customData').getSFString().split()

for i in range(10):
    poi_element = [float(poi_string_list[2*i]), float(poi_string_list[2*i+1])]
    poi_list.append(poi_element)
            
min_dist = [20]*10
points = 0

touch_sensor.enable(timestep)

while referee.step(timestep) != -1 and SPENT_TIME < MAXIMUM_TIME:
    final_points = 0
    for i in range(10):
        dist = abs(poi_list[i][0] - robot_node.getPosition()[0]) + abs(poi_list[i][1] - robot_node.getPosition()[1])
        if i == 9:
            final_points = 2*getPoints(dist)
        min_dist[i] = min(min_dist[i], dist)
    SPENT_TIME += timestep
    label = ''
    point_value = 0
    for i in range(10):
        poi_ind = str(i+1)
        if i == 9:
            poi_ind = 'F'
        poi_points = getPoints(min_dist[i])
        point_value += poi_points
        poi_label = 'POI_' + poi_ind + ': ' + str(poi_points) + '\n'
        label += poi_label
    point_value += final_points
    label += 'Final position: ' + str(final_points) + '\n'
    label += 'Total points: ' + str(point_value) + '\n'
    label += 'Time spent: ' + str(SPENT_TIME) + '\n'
    points = point_value
    referee.setLabel(1, label, 0.15, 0.55, 0.05, 16777215, 0)

    if points == 120:
        points += max(0, MAXIMUM_TIME - SPENT_TIME)/100
        break

# Store the results
with open('/tmp/results.txt', 'w') as f:
    f.write(f'points: {points}\n')

# We want to see the fall :)
referee.step(20 * timestep)

# Notify the end of the game
emitter.send('done'.encode('utf-8'))
referee.step(timestep)
