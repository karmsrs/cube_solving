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
    Square_Pattern = re.compile('^([RLUDFBrludfb]{1})([1-9]{1})$')

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
              'U': ['L', {7: 9, 8: 6, 9: 3}],
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

    # Location / Orientation Reference
    Square_Reference = {
        'R1': ['U9', 'F3'], 'R2': 'U6', 'R3': ['U3', 'B1'], 'R4': 'F6', 'R5': None, 'R6': 'B4', 'R7': ['D3', 'F9'], 'R8': 'D6', 'R9': ['D9', 'B7'],
        'L1': ['U1', 'B3'], 'L2': 'U4', 'L3': ['U7', 'F1'], 'L4': 'B6', 'L5': None, 'L6': 'F4', 'L7': ['D7', 'B9'], 'L8': 'D4', 'L9': ['D1', 'F7'],
        'U1': ['L1', 'B3'], 'U2': 'B2', 'U3': ['R3', 'B1'], 'U4': 'L2', 'U5': None, 'U6': 'R2', 'U7': ['L3', 'F1'], 'U8': 'F2', 'U9': ['R1', 'F3'],
        'D1': ['L9', 'F7'], 'D2': 'F8', 'D3': ['R7', 'F9'], 'D4': 'L8', 'D5': None, 'D6': 'R8', 'D7': ['L7', 'B9'], 'D8': 'B8', 'D9': ['R9', 'B7'],
        'F1': ['L3', 'U7'], 'F2': 'U8', 'F3': ['R1', 'U9'], 'F4': 'L6', 'F5': None, 'F6': 'R4', 'F7': ['L9', 'D1'], 'F8': 'D2', 'F9': ['R7', 'D3'],
        'B1': ['R3', 'U3'], 'B2': 'U2', 'B3': ['L1', 'U1'], 'B4': 'R6', 'B5': None, 'B6': 'L4', 'B7': ['R9', 'D9'], 'B8': 'D8', 'B9': ['L7', 'D7']}
    Corner_Color_Map = {
        'R': {
            'Y': {'B': ['R1', 'U9', 'F3'], 'G': ['R3', 'U3', 'B1']},
            'W': {'B': ['R7', 'D3', 'F9'], 'G': ['R9', 'D9', 'B7']},
            'B': {'Y': ['R1', 'F3', 'U9'], 'W': ['R7', 'F9', 'D3']},
            'G': {'Y': ['R3', 'B1', 'U3'], 'W': ['R9', 'B7', 'D9']}},
        'O': {
            'Y': {'B': ['L3', 'U7', 'F1'], 'G': ['L1', 'U1', 'B3']},
            'W': {'B': ['L9', 'D1', 'F7'], 'G': ['L7', 'D7', 'B9']},
            'B': {'Y': ['L3', 'F1', 'U7'], 'W': ['L9', 'F7', 'D1']},
            'G': {'Y': ['L1', 'B3', 'U1'], 'W': ['L7', 'B9', 'D7']}},
        'Y': {
            'R': {'B': ['U9', 'R1', 'F3'], 'G': ['U3', 'R3', 'B1']},
            'O': {'B': ['U7', 'L3', 'F1'], 'G': ['U1', 'L1', 'B3']},
            'B': {'R': ['U9', 'F3', 'R1'], 'O': ['U7', 'F1', 'L3']},
            'G': {'R': ['U3', 'B1', 'R3'], 'O': ['U1', 'B3', 'L1']}},
        'W': {
            'R': {'B': ['D3', 'R7', 'F9'], 'G': ['D9', 'R9', 'B7']},
            'O': {'B': ['D1', 'L9', 'F7'], 'G': ['D7', 'L7', 'B9']},
            'B': {'R': ['D3', 'F9', 'R7'], 'O': ['D1', 'F7', 'L9']},
            'G': {'R': ['D9', 'B7', 'R9'], 'O': ['D7', 'B9', 'L7']}},
        'B': {
            'R': {'Y': ['F3', 'R1', 'U9'], 'W': ['F9', 'R7', 'D3']},
            'O': {'Y': ['F1', 'L3', 'U7'], 'W': ['F7', 'L9', 'D1']},
            'Y': {'R': ['F3', 'U9', 'R1'], 'O': ['F1', 'U7', 'L3']},
            'W': {'R': ['F9', 'D3', 'R7'], 'O': ['F7', 'D1', 'L9']}},
        'G': {
            'R': {'Y': ['B1', 'R3', 'U3'], 'W': ['B7', 'R9', 'D9']},
            'O': {'Y': ['B3', 'L1', 'U1'], 'W': ['B9', 'L7', 'D7']},
            'Y': {'R': ['B1', 'U3', 'R3'], 'O': ['B3', 'U1', 'L1']},
            'W': {'R': ['B7', 'D9', 'R9'], 'O': ['B9', 'D7', 'L7']}}}
    Edge_Color_Map = {
        'R': {'Y': ['R2', 'U6'], 'W': ['R8', 'D6'], 'B': ['R4', 'F6'], 'G': ['R6', 'B4']},
        'O': {'Y': ['L2', 'U4'], 'W': ['L8', 'D4'], 'B': ['L6', 'F4'], 'G': ['L4', 'B6']},
        'Y': {'R': ['U6', 'R2'], 'O': ['U4', 'L2'], 'B': ['U8', 'F2'], 'G': ['U2', 'B2']},
        'W': {'R': ['D6', 'R8'], 'O': ['D4', 'L8'], 'B': ['D2', 'F8'], 'G': ['D8', 'B8']},
        'G': {'R': ['F6', 'R4'], 'O': ['F4', 'L6'], 'Y': ['F2', 'U8'], 'W': ['F8', 'D2']},
        'B': {'R': ['B4', 'R6'], 'O': ['B6', 'L4'], 'Y': ['B2', 'U2'], 'W': ['B8', 'D8']}}
    Flat_Color_Map = {
        'R': 'R5',
        'O': 'L5',
        'Y': 'U5',
        'W': 'D5',
        'B': 'F5',
        'G': 'B5'}
    Valid_Edges = {
        'RU': ['RY', 'YR'],
        'RD': ['RW', 'WR'],
        'RF': ['RB', 'BR'],
        'RB': ['RG', 'GR'],
        'LU': ['OY', 'YO'],
        'LD': ['OW', 'WO'],
        'LF': ['OB', 'BO'],
        'LB': ['OG', 'GO'],
        'UF': ['YB', 'BY'],
        'UB': ['YG', 'GY'],
        'DF': ['WB', 'BW'],
        'DB': ['WG', 'GW']}
    Valid_Corners = {
        'RUF': ['RYB', 'RBY', 'YRB', 'YBR', 'BRY', 'BYR'],
        'RUB': ['RYG', 'RGY', 'YRG', 'YGR', 'GRY', 'GYR'],
        'RDF': ['RWB', 'RBW', 'WRB', 'WBR', 'BRW', 'BWR'],
        'RDB': ['RWG', 'RGW', 'WRG', 'WGR', 'GRW', 'GWR'],
        'LUF': ['OYB', 'OBY', 'YOB', 'YBO', 'BOY', 'BYO'],
        'LUB': ['OYG', 'OGY', 'YOG', 'YGO', 'GOY', 'GYO'],
        'LDF': ['OWB', 'OBW', 'WOB', 'WBO', 'BOW', 'BWO'],
        'LDB': ['OWG', 'OGW', 'WOG', 'WGO', 'GOW', 'GWO']}

    @staticmethod
    def rotation_keys(turn_data, face, key, rotations=1):
        if rotations == 1:
            return turn_data[face][0], turn_data[face][1][key]
        else:
            return CubeData.rotation_keys(turn_data, turn_data[face][0], turn_data[face][1][key], rotations - 1)

class Face:
    def __init__(self, face):
        self.name = face
        self.solved_config = [[f'{self.name}{j}' for j in range(i,i + 3)] for i in range(1,10,3)]
        self.face = [[f'{self.name}{j}' for j in range(i,i + 3)] for i in range(1,10,3)]

    def __str__(self):
        out = f'{CubeData.Face_Strings[self.name]:<5} | '
        out += ' |\n      | '.join(['  '.join([f'{CubeData.Color_Strings[CubeData.Face_Color_Map[square[0]]]:<6}' for square in row]) for row in self.face])
        out += ' |'
        return out

    def __repr__(self):
        out = f'{CubeData.Face_Strings[self.name]:<5} | '
        out += ' |\n      | '.join(['  '.join(row) for row in self.face])
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
        self.build_configuration(configuration)

    def __str__(self):
        return '\n\n'.join(str(self.configuration[face]) for face in self.configuration.keys()) + f'\n\nCube solved: {self.is_solved()}'

    def __repr__(self):
        return '\n\n'.join(repr(self.configuration[face]) for face in self.configuration.keys()) + f'\n\nCube solved: {self.is_solved()}'

    def __getitem__(self, item):
        try:
            match = CubeData.Square_Pattern.match(item).groups()
            face, square = match[0].upper(), int(match[1])
            return self.configuration[face][square]
        except:
            return None

    def build_configuration(self, configuration):
        self.configuration = {}
        for face in CubeData.Faces:
            self.configuration[face] = Face(face)
        if configuration is not None and self.is_valid_configuration(configuration):
            try:
                _config = {}
                for enum, face in enumerate(CubeData.Faces):
                    _config[face] = ' ' + configuration[enum]
                
                for face in 'RLUDFB':
                    for square in range(1, 10):
                        # corners
                        if face in 'RL' and square in [1, 3, 7, 9]:
                            refsquare1 = f'{face}{square}'
                            refsquare2, refsquare3 = CubeData.Square_Reference[refsquare1]
                            face2, square2 = refsquare2[0], int(refsquare2[1])
                            face3, square3 = refsquare3[0], int(refsquare3[1])
                            color_1 = _config[face][square]
                            color_2 = _config[face2][square2]
                            color_3 = _config[face3][square3]
                            face_val1, face_val2, face_val3 = CubeData.Corner_Color_Map[color_1][color_2][color_3]
                            self.configuration[face][square] = face_val1
                            self.configuration[face2][square2] = face_val2
                            self.configuration[face3][square3] = face_val3
                        # edges
                        elif face in 'RLUD' and square in [2, 4, 6, 8]:
                            if face in 'UD' and square in [4, 6]:
                                continue
                            refsquare1 = f'{face}{square}'
                            refsquare2 = CubeData.Square_Reference[refsquare1]
                            face2, square2 = refsquare2[0], int(refsquare2[1])
                            color_1 = _config[face][square]
                            color_2 = _config[face2][square2]
                            face_val1, face_val2 = CubeData.Edge_Color_Map[color_1][color_2]
                            self.configuration[face][square] = face_val1
                            self.configuration[face2][square2] = face_val2
                        # flats
                        elif square == 5:
                            color_1 = _config[face][square]
                            face_val1 = CubeData.Flat_Color_Map[color_1]
                            self.configuration[face][square] = face_val1
            except:
                self.configuration = {}
                for face in CubeData.Faces:
                    self.configuration[face] = Face(face)

    def is_valid_configuration(self, configuration):
        # ensure configuration is list or tuple
        if not (isinstance(configuration, list) or isinstance(configuration, tuple)):
            return False
        # ensure configuration has 6 faces
        if not len(configuration) == 6:
            return False
        # ensure each face has 9 squares
        if not all(len(face) == 9 for face in configuration):
            return False
        # ensure all squares are in color list
        if not all(all(square in CubeData.Colors for square in face) for face in configuration):
            return False
        # ensure all colors total 9 for entire configuration
        if not all(sum(face.count(color) for face in configuration) == 9 for color in CubeData.Colors):
            return False
        # ensure each flat has exactly 1 of each color
        if not all(''.join(face[4] for face in configuration).count(color) == 1 for color in CubeData.Colors):
            return False
        # ensure corners and edges are valid
        edge_count = dict((key, 0) for key in CubeData.Valid_Edges.keys())
        corner_count = dict((key, 0) for key in CubeData.Valid_Corners.keys())
        _config = {}
        for enum, face in enumerate(CubeData.Faces):
            _config[face] = ' ' + configuration[enum]
        for face in 'RLUD':
            for square in range(1, 10):
                if square == 5:
                    continue
                elif face in 'RL' and square in [1, 3, 7, 9]:
                    refsquare1 = f'{face}{square}'
                    refsquare2, refsquare3 = CubeData.Square_Reference[refsquare1]
                    face2, square2 = refsquare2[0], int(refsquare2[1])
                    face3, square3 = refsquare3[0], int(refsquare3[1])
                    color_1 = _config[face][square]
                    color_2 = _config[face2][square2]
                    color_3 = _config[face3][square3]
                    for key in CubeData.Valid_Corners.keys():
                        if f'{color_1}{color_2}{color_3}' in CubeData.Valid_Corners[key]:
                            corner_count[key] += 1
                elif square in [2, 4, 6, 8]:
                    if face in 'UD' and square in [4, 6]:
                        continue
                    refsquare1 = f'{face}{square}'
                    refsquare2 = CubeData.Square_Reference[refsquare1]
                    face2, square2 = refsquare2[0], int(refsquare2[1])
                    color_1 = _config[face][square]
                    color_2 = _config[face2][square2]
                    for key in CubeData.Valid_Edges.keys():
                        if f'{color_1}{color_2}' in CubeData.Valid_Edges[key]:
                            edge_count[key] += 1
        if not all(corner_count[key] == 1 for key in corner_count.keys()):
            return False
        if not all(edge_count[key] == 1 for key in edge_count.keys()):
            return False
        return True

    def toggle_debug(self):
        self.debug = not self.debug
        if self.debug:
            print('DEBUG enabled.\n')
            self.debug_out()
        else:
            print('DEBUG disabled.\n')

    def debug_out(self):
        print(self)
        print(repr(self))
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
    # print(cube['F2'])
    # print(repr(cube))

    # test pre-configured cube
    cube2 = Cube(['ORORORORO', 'ROROROROR', 'YWYWYWYWY', 'WYWYWYWYW', 'GBGBGBGBG', 'BGBGBGBGB'])
    print(cube2)
    print(repr(cube2))
    cube.rotate('2bi')
    cube.rotate('2fi')
    cube.rotate('2Ei')
    cube.rotate('2Li')
    cube.rotate('2Ri')
    print(cube)
    print(repr(cube))


    # # random turns timing test
    # start = datetime.datetime.now()
    # cube = Cube()
    # rotations = 'RLUDFBrludfbMES'
    # choices = []
    # for turn in rotations:
    #     choices.append(f'{turn}')
    #     choices.append(f'2{turn}')
    #     choices.append(f'3{turn}')
    #     choices.append(f'{turn}i')
    #     choices.append(f'2{turn}i')
    #     choices.append(f'3{turn}i')

    # for choice in random.choices(choices, k=200):
    #     exec(f'cube.rotate(\'{choice}\')')
    # print(cube)
    # print(datetime.datetime.now() - start)
