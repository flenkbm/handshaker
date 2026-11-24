import numpy as np
import mediapipe.python.solutions.hands as mph
import mediapipe as mp
from .classes import Point3D
from math import sqrt


def map_mediapipe(hand):
    hand = hand.landmark
    pdx = (hand[17].x - hand[5].x) / 2
    pdy = (hand[17].y - hand[5].y) / 2
    pdz = (hand[17].z - hand[5].z)
    return {
        "wrist" : [Point3D.ld(hand[0])],
        "thumb" : [Point3D.ld(i) for i in hand[1:5]],
        "index" : [Point3D.ld(i) for i in hand[5:9]],
        "middle": [Point3D.ld(i) for i in hand[9:13]],
        "ring"  : [Point3D.ld(i) for i in hand[13:17]],
        "pinky" : [Point3D.ld(i) for i in hand[17:22]],
        "palm"  : [Point3D(hand[0].x - pdx, hand[0].y - pdy, hand[0].z - pdz),
                   Point3D.ld(hand[5]), Point3D.ld(hand[17]),
                   Point3D(hand[0].x + pdx, hand[0].y + pdy, hand[0].z + pdz)]
                   # thumb base, index base, pinky base, wrist end (under the pinky)
    }

def multi_map_mediapipe(hands):
    res = []
    for hand in hands:
        res.append(map_mediapipe(hand))
    return res

def coords_from_mp_map(hand, imsize):
    res = dict()
    zk = sqrt(imsize[0] * imsize[1])
    for itm in hand.items():
        res[itm[0]] = [Point3D(l.x * imsize[1], l.y * imsize[0], l.z * zk) for l in itm[1]]
    return res

def multi_coords_from_mp_map(hands, imsize):
    res = []
    for hand in hands:
        res.append(coords_from_mp_map(hand, imsize))
    return res