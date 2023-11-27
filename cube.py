#! /usr/bin/env python3

import datetime
import random
import re

class CubeData:
    # Faces / Colors / Turns
    Faces = ['R', 'L', 'U', 'D', 'F', 'B']
    Colors = ['R', 'O', 'Y', 'W', 'B', 'G']
    Turns = ['R', 'L', 'U', 'D', 'F', 'B', 'r', 'l', 'u', 'd', 'f', 'b', 'M', 'E', 'S']
    Face_Color_Map = {
        'R': 'R',
        'L': 'O',
        'U': 'Y',
        'D': 'W',
        'F': 'B',
        'B': 'G'}
    Face_Strings = {
        'R': 'Right',
        'L': 'Left',
        'U': 'Up',
        'D': 'Down',
        'F': 'Front',
        'B': 'Back'}
    Color_Strings = {
        'R': 'Red',
        'O': 'Orange',
        'Y': 'Yellow',
        'W': 'White',
        'B': 'Blue',
        'G': 'Green'}

    # Regex Compilations
    Turn_Pattern = re.compile('^([1-3])*([RLUDFBrludfbMES]{1})(i)*$')

    # Turn Data
    Turn_Map = {
        'R': {'U': ['F', {3: 3, 6: 6, 9: 9}], 
              'D': ['B', {3: 7, 6: 4, 9: 1}],
              'F': ['D', {3: 3, 6: 6, 9: 9}], 
              'B': ['U', {1: 9, 4: 6, 7: 3}], 
              'R': ['R', {1: 7, 2: 4, 3: 1, 4: 8, 5: 5, 6: 2, 7: 9, 8: 6, 9: 3}]},
        'L': {'U': ['B', {1: 9, 4: 6, 7: 3}],
              'D': ['F', {1: 1, 4: 4, 7: 7}],
              'F': ['U', {1: 1, 4: 4, 7: 7}],
              'B': ['D', {3: 7, 6: 4, 9: 1}],
              'L': ['L', {1: 7, 2: 4, 3: 1, 4: 8, 5: 5, 6: 2, 7: 9, 8: 6, 9: 3}]},
        'U': {'R': ['B', {1: 1, 2: 2, 3: 3}],
              'L': ['F', {1: 1, 2: 2, 3: 3}],
              'F': ['R', {1: 1, 2: 2, 3: 3}],
              'B': ['L', {1: 1, 2: 2, 3: 3}],
              'U': ['U', {1: 7, 2: 4, 3: 1, 4: 8, 5: 5, 6: 2, 7: 9, 8: 6, 9: 3}]},
        'D': {'R': ['F', {7: 7, 8: 8, 9: 9}],
              'L': ['B', {7: 7, 8: 8, 9: 9}],
              'F': ['L', {7: 7, 8: 8, 9: 9}],
              'B': ['R', {7: 7, 8: 8, 9: 9}],
              'D': ['D', {1: 7, 2: 4, 3: 1, 4: 8, 5: 5, 6: 2, 7: 9, 8: 6, 9: 3}]},
        'F': {'R': ['U', {1: 7, 4: 8, 7: 9}],
              'L': ['D', {3: 1, 6: 2, 9: 3}],
              'U': ['L', {7: 3, 8: 6, 9: 9}],
              'D': ['R', {1: 7, 2: 4, 3: 1}],
              'F': ['F', {1: 7, 2: 4, 3: 1, 4: 8, 5: 5, 6: 2, 7: 9, 8: 6, 9: 3}]},
        'B': {'R': ['D', {3: 9, 6: 8, 9: 7}],
              'L': ['U', {1: 3, 4: 2, 7: 1}],
              'U': ['R', {1: 3, 2: 6, 3: 9}],
              'D': ['L', {7: 1, 8: 4, 9: 7}],
              'B': ['B', {1: 7, 2: 4, 3: 1, 4: 8, 5: 5, 6: 2, 7: 9, 8: 6, 9: 3}]},
        'M': {'U': ['B', {2: 8, 5: 5, 8: 2}],
              'D': ['F', {2: 2, 5: 5, 8: 8}],
              'F': ['U', {2: 2, 5: 5, 8: 8}],
              'B': ['D', {2: 8, 5: 5, 8: 2}]},
        'E': {'R': ['F', {4: 4, 5: 5, 6: 6}],
              'L': ['B', {4: 4, 5: 5, 6: 6}],
              'F': ['L', {4: 4, 5: 5, 6: 6}],
              'B': ['R', {4: 4, 5: 5, 6: 6}]},
        'S': {'R': ['U', {2: 4, 5: 5, 8: 6}],
              'L': ['D', {2: 4, 5: 5, 8: 6}],
              'U': ['L', {4: 8, 5: 5, 6: 2}],
              'D': ['R', {4: 8, 5: 5, 6: 2}]}}

    @staticmethod
    def rotation_keys(turn_data, face, key, rotations=1):
        if rotations == 1:
            return turn_data[face][0], turn_data[face][1][key]
        else:
            return CubeData.rotation_keys(turn_data, turn_data[face][0], turn_data[face][1][key], rotations - 1)

class Face:
    def __init__(self, face, config=None):
        color = CubeData.Face_Color_Map[face]
        self.name = face
        self.solved_config = [[color for j in range(3)] for i in range(3)]
        self.face = [[color for j in range(3)] for i in range(3)]

        if config is not None:
            self.face = config

    def __str__(self):
        out = f'{CubeData.Face_Strings[self.name]:<5} | '
        out += ' |\n      | '.join(['  '.join([f'{CubeData.Color_Strings[color]:<6}' for color in row]) for row in self.face])
        out += ' |'
        return out

    def __getitem__(self, item):
        row = (item - 1) // 3
        col = (item - 1) % 3
        return self.face[row][col]

    def __setitem__(self, item, value):
        row = (item - 1) // 3
        col = (item - 1) % 3
        self.face[row][col] = value

    def is_solved(self):
        return self.face == self.solved_config


class Cube:
    def __init__(self, configuration=None):
        self.debug = False
        self.configuration = {}
        if configuration is None:
            for face in CubeData.Faces:
                self.configuration[face] = Face(face)

    def __str__(self):
        return '\n\n'.join(str(self.configuration[face]) for face in self.configuration.keys()) + f'\n\nCube solved: {self.is_solved()}'

    def toggle_debug(self):
        self.debug = not self.debug
        if self.debug:
            print('DEBUG enabled.\n')
            self.debug_out()
        else:
            print('DEBUG disabled.\n')

    def debug_out(self):
        print(self)
        _ = input('Press enter to continue...\n')

    def is_solved(self):
        return all(self.configuration[face].is_solved() for face in self.configuration.keys())

    def rotate(self, rotation):
        # parse patern from string to determine parts of the rotation (numbers of rotation, inversions, and main rotation)
        pattern = CubeData.Turn_Pattern.match(rotation).groups()

        if pattern is not None:
            rotations = 1 if pattern[0] is None else int(pattern[0])
            direction = pattern[1]
            inverted = True if pattern[2] is not None else False
            # store 'old' configuration temporarily
            _temp = {}
            for face in self.configuration.keys():
                _temp[face] = dict([(i + 1, self.configuration[face][i + 1]) for i in range(9)])
            # turn face
            if direction in 'RrLlUuDdFfBb':
                if direction in 'Rr':
                    turn_data = CubeData.Turn_Map['R']
                elif direction in 'Ll':
                    turn_data = CubeData.Turn_Map['L']
                elif direction in 'Uu':
                    turn_data = CubeData.Turn_Map['U']
                elif direction in 'Dd':
                    turn_data = CubeData.Turn_Map['D']
                elif direction in 'Ff':
                    turn_data = CubeData.Turn_Map['F']
                elif direction in 'Bb':
                    turn_data = CubeData.Turn_Map['B']
                _rotations = 4 - rotations if inverted else rotations
                for face in turn_data.keys():
                    for key in turn_data[face][1].keys():
                        new_face, new_key = CubeData.rotation_keys(turn_data, face, key, _rotations)
                        self.configuration[face][key] = _temp[new_face][new_key]

            # turn centers
            if direction in 'MESrludfb':
                if direction in 'Mrl':
                    turn_data = CubeData.Turn_Map['M']
                    _rotations = 4 - rotations if (direction == 'r' and not inverted) or (direction != 'r' and inverted) else rotations
                elif direction in 'Eud':
                    turn_data = CubeData.Turn_Map['E']
                    _rotations = 4 - rotations if (direction =='u' and not inverted) or (direction != 'u' and inverted) else rotations
                elif direction in 'Sfb':
                    turn_data = CubeData.Turn_Map['S']
                    _rotations = 4 - rotations if (direction == 'b' and not inverted) or (direction != 'b' and inverted) else rotations
                for face in turn_data.keys():
                    for key in turn_data[face][1].keys():
                        new_face, new_key = CubeData.rotation_keys(turn_data, face, key, _rotations)
                        self.configuration[face][key] = _temp[new_face][new_key]
                    
            rotation = rotation.replace('i', '\'')
            print(f'@Rotating: {rotation}')
        else:
            print(f'Invalid Rotation: {rotation}')
        if self.debug:
            self.debug_out()


if __name__ == '__main__':
    # # test all rotations
    # cube = Cube()
    # cube.toggle_debug()
    # cube.rotate('R')
    # cube.rotate('Ri')
    # cube.rotate('L')
    # cube.rotate('Li')
    # cube.rotate('U')
    # cube.rotate('Ui')
    # cube.rotate('D')
    # cube.rotate('Di')
    # cube.rotate('F')
    # cube.rotate('Fi')
    # cube.rotate('B')
    # cube.rotate('Bi')
    # cube.rotate('M')
    # cube.rotate('Mi')
    # cube.rotate('E')
    # cube.rotate('Ei')
    # cube.rotate('S')
    # cube.rotate('Si')
    # cube.rotate('r')
    # cube.rotate('ri')
    # cube.rotate('l')
    # cube.rotate('li')
    # cube.rotate('u')
    # cube.rotate('ui')
    # cube.rotate('d')
    # cube.rotate('di')
    # cube.rotate('f')
    # cube.rotate('fi')
    # cube.rotate('b')
    # cube.rotate('bi')

    # # checker pattern
    # cube = Cube()
    # cube.rotate('2R')
    # cube.rotate('2L')
    # cube.rotate('2E')
    # cube.rotate('2f')
    # cube.rotate('2b')
    # print(cube)

    # random turns timing test
    start = datetime.datetime.now()
    cube = Cube()
    rotations = 'RLUDFBrludfbMES'
    choices = []
    for turn in rotations:
        choices.append(f'{turn}')
        choices.append(f'2{turn}')
        choices.append(f'3{turn}')
        choices.append(f'{turn}i')
        choices.append(f'2{turn}i')
        choices.append(f'3{turn}i')

    for choice in random.choices(choices, k=200):
        exec(f'cube.rotate(\'{choice}\')')
    print(cube)
    print(datetime.datetime.now() - start)
