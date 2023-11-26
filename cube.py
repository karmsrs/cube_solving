#! /usr/bin/env python3

import json
import re
from traceback import print_exc

##### ROTATIONS
#
# Rotations are always "clockwise" from the perspective of the face indicated
# Anti-clockwise rotations are indicated using an i for "inverted"
# in cube notation, inversions are noted by an apostrophe after the rotation
#
### Face rotations
# R = Right
# L = Left
# U = Up (top)
# D = Down (bottom)
# F = Front
# B = Back
#
### Middle layer rotations
# M = Middle (between R and L), and it turns the same as L
# E = Equator (between U and D), and it turns the same as D
# S = Standing (between F and B), and it turns the same as F
#
### Major rotations (turning two layers at a time)
# r = R & M (turn as R)
# l = L & M (turn as L)
# u = U & E (turn as U)
# d = D & E (turn as D)
# f = F & S (turn as F)
# b = B & S (turn as B)
#
### Cube orientation
# X  = rotate entire cube on R
# Xi = rotate entire cube on L
# Y  = rotate entire cube on U
# Yi = rotate entire cube on D
# Z  = rotate entire cube on F
# Zi = rotate entire cube on B
#
#
### Examples of "cube notation"
# 2R = 2x clockwise rotations of the right face
# L' (or Li) = 1x anti-clockwise rotation of the left face


##### ORIENTATION
#
### It's necessary to establish a viewpoint looking directly onward at a face "F" or "Front"
### In order to standardize the numbering, numbering will be indicated by the color of the face after a specified rotation
# R will be considered "F" after  Y rotation
# L will be considered "F" after Yi rotation
# U will be considered "F" after Xi rotation
# D will be considered "F" after  X rotation
# F will be considered "F" after no rotation
# B will be considered "F" after 2Y rotation
#
### Numbering
# Each space will be numbered as follows based upon the face pointing directly at the viewport (forward):
#     0 1 2
#    ------
#   0|1 2 3
#   1|4 5 6
#   2|7 8 9
#
### Colors in orientation
# We will also establish "solved" colors as:
# Right = Red
# Left  = Orange
# Up    = Yellow
# Down  = White
# Front = Blue
# Back  = Green

class Face:
  FACES = ['R', 'L', 'U', 'D', 'F', 'B']
  COLORS = ['R', 'O', 'Y', 'W', 'B', 'G']
  FACE_COLOR_MAP = {
    'R': 'R',
    'L': 'O',
    'U': 'Y',
    'D': 'W',
    'F': 'B',
    'B': 'G'}
  FACE_STRINGS = {
    'R': 'Right',
    'L': 'Left',
    'U': 'Up',
    'D': 'Down',
    'F': 'Front',
    'B': 'Back'}
  COLOR_STRINGS = {
    'R': 'Red',
    'O': 'Orange',
    'Y': 'Yellow',
    'W': 'White',
    'B': 'Blue',
    'G': 'Green'}

  def __init__(self, face, config=None):
    color = Face.FACE_COLOR_MAP[face]

    self.face = face
    self.solved_config = [[color for j in range(3)] for i in range(3)]
    self.squares = [[color for j in range(3)] for i in range(3)]

    if config is not None:
      self.squares = config

  def __str__(self):
    out = f'{Face.FACE_STRINGS[self.face]:<5} | '
    out += ' |\n      | '.join(['  '.join([f'{Face.COLOR_STRINGS[color]:<6}' for color in row]) for row in self.squares])
    out += ' |'
    return out

  def __getitem__(self, item):
    row = (item - 1) // 3
    col = (item - 1) % 3
    return self.squares[row][col]

  def __setitem__(self, item, value):
    row = (item - 1) // 3
    col = (item - 1) % 3
    self.squares[row][col] = value

  def is_solved(self):
    return self.squares == self.solved_config


class Cube:
  TURN_PATTERN = re.compile('([1-3])*([RLUDFBrludfbMES]{1})(i)*')

  def __init__(self, configuration=None):
    self.debug = False
    self.configuration = None
    if configuration is None:
      for face in Face.FACES:
        setattr(self, face, Face(face))

  def toggle_debug(self):
    self.debug = not self.debug
    if self.debug:
      print('DEBUG enabled.\n')
      print(self)
    else:
      print('DEBUG disabled.\n')

  def __str__(self):
    return '\n\n'.join(str(face) for face in self.get_faces()) + f'\n\nCube solved: {self.is_solved()}'

  def get_faces(self):
    return [getattr(self, face) for face in Face.FACES]

  def is_solved(self):
    return all(face.is_solved() for face in self.get_faces())

  def rotate(self, rotation=None):
    if rotation is None:
      print('ROTATION WAS NONE')
    else:
      try:
        # parse patern from string to determine parts of the rotation (numbers of rotation, inversions, and main rotation)
        pattern = Cube.TURN_PATTERN.match(rotation).groups()
        rotations = 1 if pattern[0] is None else int(pattern[0])
        rotation = pattern[1]
        inverted = True if pattern[2] is not None else False

        if inverted:
          print(f'Rotating: {rotations} * inverted {rotation}')
        else:
          print(f'Rotating: {rotations} * {rotation}')

        for _ in range(rotations):
          # temporarily store colors so they can be moved all at once
          _R = dict([(i + 1, self.R[i + 1]) for i in range(9)])
          _L = dict([(i + 1, self.L[i + 1]) for i in range(9)])
          _U = dict([(i + 1, self.U[i + 1]) for i in range(9)])
          _D = dict([(i + 1, self.D[i + 1]) for i in range(9)])
          _F = dict([(i + 1, self.F[i + 1]) for i in range(9)])
          _B = dict([(i + 1, self.B[i + 1]) for i in range(9)])
          if rotation in ['R', 'r']:
            if not inverted:
              self.U[3], self.U[6], self.U[9] = _F[3], _F[6], _F[9]
              self.D[3], self.D[6], self.D[9] = _B[7], _B[4], _B[1]
              self.F[3], self.F[6], self.F[9] = _D[3], _D[6], _D[9]
              self.B[1], self.B[4], self.B[7] = _U[9], _U[6], _U[3]
            else:
              self.U[3], self.U[6], self.U[9] = _B[7], _B[4], _B[1]
              self.D[3], self.D[6], self.D[9] = _F[3], _F[6], _F[9]
              self.F[3], self.F[6], self.F[9] = _U[3], _U[6], _U[9]
              self.B[1], self.B[4], self.B[7] = _D[9], _D[6], _D[3]
          if rotation in ['L', 'l']:
            if not inverted:
              self.U[1], self.U[4], self.U[7] = _B[9], _B[6], _B[3]
              self.D[1], self.D[4], self.D[7] = _F[1], _F[4], _F[7]
              self.F[1], self.F[4], self.F[7] = _U[1], _U[4], _U[7]
              self.B[3], self.B[6], self.B[9] = _D[7], _D[4], _D[1]
            else:
              self.U[1], self.U[4], self.U[7] = _F[1], _F[4], _F[7]
              self.D[1], self.D[4], self.D[7] = _B[9], _B[6], _B[3]
              self.F[1], self.F[4], self.F[7] = _D[1], _D[4], _D[7]
              self.B[3], self.B[6], self.B[9] = _U[7], _U[4], _U[1]
          if rotation in ['U', 'u']:
            if not inverted:
              self.R[1], self.R[2], self.R[3] = _B[1], _B[2], _B[3]
              self.L[1], self.L[2], self.L[3] = _F[1], _F[2], _F[3]
              self.F[1], self.F[2], self.F[3] = _R[1], _R[2], _R[3]
              self.B[1], self.B[2], self.B[3] = _L[1], _L[2], _L[3]
            else:
              self.R[1], self.R[2], self.R[3] = _F[1], _F[2], _F[3]
              self.L[1], self.L[2], self.L[3] = _B[1], _B[2], _B[3]
              self.F[1], self.F[2], self.F[3] = _L[1], _L[2], _L[3]
              self.B[1], self.B[2], self.B[3] = _R[1], _R[2], _R[3]
          if rotation in ['D', 'd']:
            if not inverted:
              self.R[7], self.R[8], self.R[9] = _F[7], _F[8], _F[9]
              self.L[7], self.L[8], self.L[9] = _B[7], _B[8], _B[9]
              self.F[7], self.F[8], self.F[9] = _L[7], _L[8], _L[9]
              self.B[7], self.B[8], self.B[9] = _R[7], _R[8], _R[9]
            else:
              self.R[7], self.R[8], self.R[9] = _B[7], _B[8], _B[9]
              self.L[7], self.L[8], self.L[9] = _F[7], _F[8], _F[9]
              self.F[7], self.F[8], self.F[9] = _R[7], _R[8], _R[9]
              self.B[7], self.B[8], self.B[9] = _L[7], _L[8], _L[9]
          if rotation in ['F', 'f']:
            if not inverted:
              self.R[1], self.R[4], self.R[7] = _U[7], _U[8], _U[9]
              self.L[3], self.L[6], self.L[9] = _D[1], _D[2], _D[3]
              self.U[7], self.U[8], self.U[9] = _L[3], _L[6], _L[9]
              self.D[1], self.D[2], self.D[3] = _R[7], _R[4], _R[1]
            else:
              self.R[1], self.R[4], self.R[7] = _D[3], _D[2], _D[1]
              self.L[3], self.L[6], self.L[9] = _U[9], _U[8], _U[7]
              self.U[7], self.U[8], self.U[9] = _R[1], _R[4], _R[7]
              self.D[1], self.D[2], self.D[3] = _L[3], _L[6], _L[9]
          if rotation in ['B', 'b']:
            if not inverted:
              self.R[3], self.R[6], self.R[9] = _D[9], _D[8], _D[7]
              self.L[1], self.L[4], self.L[7] = _U[3], _U[2], _U[1]
              self.U[1], self.U[2], self.U[3] = _R[3], _R[6], _R[9]
              self.D[7], self.D[8], self.D[9] = _L[1], _L[4], _L[7]
            else:
              self.R[3], self.R[6], self.R[9] = _U[1], _U[2], _U[3]
              self.L[1], self.L[4], self.L[7] = _D[7], _D[8], _D[9]
              self.U[1], self.U[2], self.U[3] = _L[7], _L[4], _L[1]
              self.D[7], self.D[8], self.D[9] = _R[9], _R[6], _R[3]
          if rotation in ['M', 'r', 'l']:
            if (rotation == 'r' and inverted) or (rotation != 'r' and not inverted):
              # rotate like L
              self.U[2], self.U[5], self.U[8] = _B[8], _B[5], _B[2]
              self.D[2], self.D[5], self.D[8] = _F[2], _F[5], _F[8]
              self.F[2], self.F[5], self.F[8] = _U[2], _U[5], _U[8]
              self.B[2], self.B[5], self.B[8] = _D[8], _D[5], _D[2]
            else:
              # rotate like R
              self.U[2], self.U[5], self.U[8] = _F[2], _F[5], _F[8]
              self.D[2], self.D[5], self.D[8] = _B[8], _B[5], _B[2]
              self.F[2], self.F[5], self.F[8] = _D[2], _D[5], _D[8]
              self.B[2], self.B[5], self.B[8] = _U[8], _U[5], _U[2]
          if rotation in ['E', 'u', 'd']:
            if (rotation == 'u' and inverted) or (rotation != 'u' and not inverted):
              # rotate like D
              self.R[4], self.R[5], self.R[6] = _F[4], _F[5], _F[6]
              self.L[4], self.L[5], self.L[6] = _B[4], _B[5], _B[6]
              self.F[4], self.F[5], self.F[6] = _L[4], _L[5], _L[6]
              self.B[4], self.B[5], self.B[6] = _R[4], _R[5], _R[6]
              pass
            else:
              # rotate like U
              self.R[4], self.R[5], self.R[6] = _B[4], _B[5], _B[6]
              self.L[4], self.L[5], self.L[6] = _F[4], _F[5], _F[6]
              self.F[4], self.F[5], self.F[6] = _R[4], _R[5], _R[6]
              self.B[4], self.B[5], self.B[6] = _L[4], _L[5], _L[6]
              pass
          if rotation in ['S', 'f', 'b']:
            if (rotation == 'b' and inverted) or (rotation != 'b' and not inverted):
              # rotate like F
              self.R[2], self.R[5], self.R[8] = _U[4], _U[5], _U[6]
              self.L[2], self.L[5], self.L[8] = _D[4], _D[5], _D[6]
              self.U[4], self.U[5], self.U[6] = _L[8], _L[5], _L[2]
              self.D[4], self.D[5], self.D[6] = _R[8], _R[5], _R[2]
              pass
            else:
              # rotate like B
              self.R[2], self.R[5], self.R[8] = _D[6], _D[5], _D[4]
              self.L[2], self.L[5], self.L[8] = _U[6], _U[5], _U[4]
              self.U[4], self.U[5], self.U[6] = _R[2], _R[5], _R[8]
              self.D[4], self.D[5], self.D[6] = _L[2], _L[5], _L[8]
              pass

        if self.debug:
          _ = input('Press enter to continue...\n')
          print(self)

      except:
        print_exc()

if __name__ == '__main__':
  # test all rotations
  cube = Cube()
  cube.toggle_debug()
  cube.rotate('R')
  cube.rotate('Ri')
  cube.rotate('L')
  cube.rotate('Li')
  cube.rotate('U')
  cube.rotate('Ui')
  cube.rotate('D')
  cube.rotate('Di')
  cube.rotate('F')
  cube.rotate('Fi')
  cube.rotate('B')
  cube.rotate('Bi')
  cube.rotate('M')
  cube.rotate('Mi')
  cube.rotate('E')
  cube.rotate('Ei')
  cube.rotate('S')
  cube.rotate('Si')
  cube.rotate('r')
  cube.rotate('ri')
  cube.rotate('l')
  cube.rotate('li')
  cube.rotate('u')
  cube.rotate('ui')
  cube.rotate('d')
  cube.rotate('di')
  cube.rotate('f')
  cube.rotate('fi')
  cube.rotate('b')
  cube.rotate('bi')

  # checker pattern
  # cube = Cube()
  # cube.rotate('2R')
  # cube.rotate('2L')
  # cube.rotate('2E')
  # cube.rotate('2f')
  # cube.rotate('2b')
  # print(cube)
