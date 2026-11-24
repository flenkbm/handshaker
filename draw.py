import cv2
import numpy as np
from .utils import *
from math import sqrt
from .classes import Point3D

PRESET1 = {# BGR colors
    "palm_col" : (0, 255, 255),
    "palm_infill" : 0.2,# opacity from 0 to 1
    "palm_w" : 4,
    "thumb_col" : (255, 255, 255),
    "index_col" : (0, 0, 255),
    "middle_col": (0, 255, 0),
    "ring_col"  : (255, 0, 0),
    "pinky_col" : (0, 0, 0),
    "finger_w" : 3
}
PRESET2 = {# BGR colors
    "palm_col" : (0, 250, 250),
    "palm_infill" : 0.3,# opacity from 0 to 1
    "palm_w" : 4,
    "thumb_col" : (130, 130, 130),
    "index_col" : (130, 130, 130),
    "middle_col": (130, 130, 130),
    "ring_col"  : (130, 130, 130),
    "pinky_col" : (130, 130, 130),
    "finger_w" : 3
}

def draw_finger(img, coords, color, width):
    img = cv2.polylines(img, np.array([coords], dtype=np.int32), False, color, int(width))
    for p in coords: img = cv2.circle(img, p, int(width*2.3), color, -1)
    return img

def draw_hand(img: np.ndarray, hand: dict[str,list[Point3D]], style=PRESET1, auto_w: float=False):# auto_w - palm surface % of the screen
    ret = img.copy()
    if auto_w:
        style = style.copy()
        sp = float(sqrt((hand["palm"][0].x - hand["palm"][1].x)**2 + (hand["palm"][0].y - hand["palm"][1].y)**2) \
            * sqrt((hand["palm"][0].x - hand["palm"][3].x)**2 + (hand["palm"][0].y - hand["palm"][3].y)**2))
        si = float(img.shape[0] * img.shape[1])
        k = sqrt(sp / si * 100 / float(auto_w))
        style["palm_w"] = max(float(style["palm_w"]) * k, 0.6)
        style["finger_w"] = max(float(style["finger_w"]) * k, 0.6)
    #
    # pre-fingers
    if hand["thumb"][-1].z > hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["thumb"]], style["thumb_col"], style["finger_w"])
    if hand["index"][-1].z > hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["index"]], style["index_col"], style["finger_w"])
    if hand["middle"][-1].z > hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["middle"]], style["middle_col"], style["finger_w"])
    if hand["ring"][-1].z > hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["ring"]], style["ring_col"], style["finger_w"])
    if hand["pinky"][-1].z > hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["pinky"]], style["pinky_col"], style["finger_w"])
    #
    # palm
    todraw = []
    for p in hand["palm"]: todraw.append(np.array([p.ix(), p.iy()], dtype=np.int32))
    todraw = np.array([todraw], np.int32)
    #
    cv2.polylines(ret, todraw, True, style["palm_col"], int(style["palm_w"]))
    #
    for p in todraw[0]: cv2.circle(ret, p, int(style["palm_w"]*2.2), style["palm_col"], -1)
    cv2.circle(ret, np.array((hand["wrist"][0].ix(), hand["wrist"][0].iy()), dtype=np.int32), int(style["palm_w"]*2.3), style["palm_col"], -1)
    #
    if style["palm_infill"] >= 0.01:
        adraw(ret, style["palm_infill"], cv2.fillPoly, todraw, style["palm_col"])
    #
    # post fingers
    if hand["thumb"][-1].z <= hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["thumb"]], style["thumb_col"], style["finger_w"])
    if hand["index"][-1].z <= hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["index"]], style["index_col"], style["finger_w"])
    if hand["middle"][-1].z <= hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["middle"]], style["middle_col"], style["finger_w"])
    if hand["ring"][-1].z <= hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["ring"]], style["ring_col"], style["finger_w"])
    if hand["pinky"][-1].z <= hand["palm"][1].z:
        draw_finger(ret, [np.array([p.ix(), p.iy()], dtype=np.int32) for p in hand["pinky"]], style["pinky_col"], style["finger_w"])
    return ret