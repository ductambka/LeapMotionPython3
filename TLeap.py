#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# region Description
__author__ = 'Tamnd - NGUYEN DUC TAM'
__copyright__ = "Copyright ©2022 Tamnd <ductambka@gmail.com>"
__maintainer__ = "Tamnd"
__email__ = "ductambka@gmail.com"
__status__ = "Production"
# __date__ = 2022 - 08 - 11
# endregion
import sys
import os
import time
import datetime
import json
import logging
import sys
import os
import time
import datetime
import json
import logging
import websocket
import _thread
import time
import rel

import pyautogui
from pynput.keyboard import Key, Listener

from threading import Thread


# websocket.enableTrace(True)
# Pointables: Đầu ngón tay
#

ACTION_MAP = {

}
class TMouse:
    class TMouseHandler(Thread):
        def __init__(self):
            self.position = None
            self.last_position = None
            self.action_queues = []
            self.thread = Thread(target=self.mouse_handler, args=())
            self.thread.start()

        def mouse_handler(self):
            while True:
                self.position = pyautogui.position()
                if self.position != self.last_position:
                    print(f"Mouse position: {self.position}")
                    self.last_position = self.position
                if len(self.action_queues) > 0:
                    action = self.action_queues.pop(0)
                else:
                    time.sleep(0.1)

    # REf: https://www.geeksforgeeks.org/mouse-keyboard-automation-using-python/
    def __init__(self, *args, **kwargs):
        self.handler = self.TMouseHandler()
        self.screen_size = pyautogui.size()
        print(f"self.screen_size = {self.screen_size}")

        self.mouse_queues = []
        self.key_queues = []

        self.mouse_last_position = None
        self.mouse_position = pyautogui.position()

        self.mouse_thread = Thread(target=self.mouse_handler, args=())
        self.mouse_thread.start()

        self.key_thread = Thread(target=self.key_handler, args=())
        self.key_thread.start()

    def mouse_handler(self):
        while True:
            self.mouse_position = pyautogui.position()
            if self.mouse_position != self.mouse_last_position:
                print(f"Mouse position: {self.mouse_position}")
                self.mouse_last_position = self.mouse_position
            if len(self.mouse_queues) > 0:
                action = self.mouse_queues.pop(0)
            else:
                time.sleep(0.1)

    def key_handler(self):
        while True:
            if len(self.key_queues) > 0:
                action = self.key_queues.pop(0)
            else:
                time.sleep(0.1)
        pass

    def get_position(self):
        self.position = pyautogui.position()
        return self.position

    def moveTo(self, X, Y, duration=1):
        pyautogui.moveTo(X, Y, duration=duration)

    def moveRel(self, X, Y, duration=1):
        pyautogui.moveRel(X, Y, duration=duration)

    def click(self, X, Y):
        pyautogui.click(X, Y)

    # @TND: Must Recheck
    def dragRel(self, X1, Y1, X2, Y2):
        pyautogui.dragRel(0, 100, duration=1)

    def scroll(self, pixel=200):
        pyautogui.scroll(pixel)

    def typewrite(self, X, Y, message):
        pyautogui.click(X, Y)
        pyautogui.typewrite(message)

    def pressKeys(self, *keys):
        try:
            pyautogui.typewrite(keys)
        except Exception as xx:
            print(str(f"[pressKeys] {xx}"))

    def hotKey(self, *keys):
        try:
            pyautogui.hotkey(keys)
        except Exception as xx:
            print(str(f"[pressCombineKeys] {xx}"))

class TKey:
    class TKeyHandler(Thread):
        def __init__(self):
            self.key_actions = []

            self.key_humanize_queue = []

            self.listener_thread = Thread(target=self.key_listener, args=())
            self.listener_thread.start()

            self.handler_thread = Thread(target=self.key_handler, args=())
            self.handler_thread.start()

        def key_listener(self):
            # Collect events until released
            with Listener(
                    on_press=self.on_press,
                    on_release=self.on_release) as listener:
                listener.join()

        def key_handler(self):
            while True:
                if len(self.key_actions) > 0:
                    key = self.key_actions.pop(0)
                    # print(f"key action: {key}")
                    if key['action'] == "pressed" and len(self.key_actions) > 0:
                        next_key1 = self.key_actions.pop(0)
                        if next_key1['key'] == key['key']:
                            print(f"key: {key} clicked!")
                        elif next_key1['action'] == "pressed" and len(self.key_actions) > 0:
                            next_key2 = self.key_actions.pop(0)
                            if next_key2['key'] == next_key1['key']:
                                if next_key2['action'] == "release":
                                    print(f"combine keys: {key} + {next_key1} clicked!")
                                else:
                                    pass
                            elif len(self.key_actions) > 0:
                                next_key3 = self.key_actions.pop(0)
                                if next_key3['key'] == next_key2['key']:
                                    if next_key3['action'] == "release":
                                        print(f"combine keys: {key} + {next_key1} + {next_key2} clicked!")
                                    else:
                                        pass
                                else:
                                    if next_key3['action'] == "release":
                                        print(f"combine keys: {key} + {next_key1} + {next_key3} clicked!")
                                    else:
                                        pass
                else:
                    time.sleep(0.5)
        def on_press(self, key):
            # print('{0} pressed'.format(
            #     key))
            self.key_actions.append({
                "key": key,
                "action": "pressed"
            })
        def on_release(self, key):
            # print('{0} release'.format(
            #     key))
            self.key_actions.append({
                "key": key,
                "action": "release"
            })
            if key == Key.esc:
                # Stop listener
                return False

    # REf: https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
    def __init__(self, *args, **kwargs):
        self.handler = self.TKeyHandler()
        self.action_queues = []


class THand:
    # REf: https://developer-archive.leapmotion.com/documentation/javascript/api/Leap.Hand.html
    def __init__(self, *args, **kwargs):
        # Basis vectors fo the arm property specify the orientation of a arm:
        #
        # arm.basis[0] – the x-basis. Perpendicular to the longitudinal axis of the arm; exits laterally from the sides of the wrist.
        # arm.basis[1] – the y-basis or up vector. Perpendicular to the longitudinal axis of the arm; exits the top and bottom of the arm. More positive in the upward direction.
        # arm.basis[2] – the z-basis. Aligned with the longitudinal axis of the arm. More positive toward the elbow.
        # The bases provided for the right arm use the right-hand rule; those for the left arm use the left-hand rule. Thus, the positive direction of the x-basis is to the right for the right arm and to the left for the left arm. You can change from right-hand to left-hand rule by multiplying the basis vectors by -1.
        self.arm = None

        # number – a value in the range [0..1]
        # A low value indicates that there are significant discrepancies; finger positions, even hand identification could be incorrect. The significance of the confidence value to your application can vary with context.
        self.confidence = None

        self.fingers = []

        # The strength of a grab hand pose.
        #
        # The strength is zero for an open hand, and blends to 1.0 when a grabbing hand pose is recognized. The following example uses grabStrength to determine whether a hand is open or closed. The example also compares the current value to the average value from recent history to determine whether the hand is opening or closing (if the hand isn’t fully open or closed).
        self.grabStrength = None

        # The thumb finger of this Hand.
        self.thumb = None

        # The index finger of this Hand.
        self.indexFinger = None

        # The middle finger of this Hand.
        self.middleFinger = None

        # The pinky finger of this Hand.
        self.pinkyFinger = None

        # The ring finger of this Hand.
        self.ringFinger = None

        # "direction": [
        #                 0.469491,
        #                 0.132652,
        #                 -0.872915
        #             ],
        self.direction = []

        # "id": 8364,
        self.id = None

        # "palmNormal": [
        #                 -0.665152,
        #                 -0.579768,
        #                 -0.470576
        #             ],
        # The normal vector to the palm. If your hand is flat, this vector will point downward, or “out” of the front surface of your palm.
        # The direction is expressed as a unit vector pointing in the same direction as the palm normal (that is, a vector orthogonal to the palm).
        self.palmNormal = []

        # "palmPosition": [
        #                 16.0519,
        #                 212.918,
        #                 200.592
        #             ],
        # The center position of the palm in millimeters from the Leap origin.
        self.palmPosition = []

        # "palmVelocity": [
        #                 -897.436,
        #                 -210.251,
        #                 465.45
        #             ],
        # The rate of change of the palm position in millimeters/second.
        self.palmVelocity = []

        # The average outer width of the hand (not including fingers or thumb) in millimeters.
        self.palmWidth = None

        # The holding strength of a pinch hand pose.
        #
        # The strength is zero for an open hand, and blends to 1.0 when a pinching hand pose is recognized. Pinching can be done between the thumb and any other finger of the same hand.
        #
        # The following example compares the distances between the tip of the thumb and other fingers to determine which finger is pinching.
        self.pinchStrength = None

        # number[] – a 3-element array representing a position vector.
        # The center of a sphere fit to the curvature of this hand.
        self.sphereCenter = None

        # The radius of a sphere fit to the curvature of this hand, in millimeters.
        # This sphere is placed roughly as if the hand were holding a ball. Thus the size of the sphere decreases as the fingers are curled into a fist.
        self.sphereRadius = None

        # The list of Pointable objects (fingers) detected in this frame that are associated with this hand, given in arbitrary order. The list can be empty if no fingers associated with this hand are detected.
        #
        # The following example identifies each pointable by finger name.
        self.pointables = []

        # "r": [
        #                 [
        #                     0.948661,
        #                     -0.257454,
        #                     -0.183736
        #                 ],
        #                 [
        #                     0.314589,
        #                     0.707804,
        #                     0.632493
        #                 ],
        #                 [
        #                     -0.0327885,
        #                     -0.657823,
        #                     0.752458
        #                 ]
        #             ],
        self.r = []

        # "s": 0.491189,
        self.s = None

        # "sphereCenter": [
        #                 -19.8778,
        #                 200.187,
        #                 173.919
        #             ],
        self.sphereCenter = []

        # "sphereRadius": 36.9737,
        self.sphereRadius = None

        # "stabilizedPalmPosition": [
        #                 65.703,
        #                 215.803,
        #                 161.211
        #             ],
        self.stabilizedPalmPosition = []

        # "t": [
        #                 -40.4905,
        #                 5.8727,
        #                 -39.4453
        #             ],
        self.t = []

        # "timeVisible": 4.13225
        self.timeVisible = None

        # Notice Tools are deprecated in version 3.0.
        #
        # In version 2+, tools are not associated with hands. This list is always empty.
        #
        # The list of tools detected in this frame that are held by this hand, given in arbitrary order.
        self.tools = []

        # string – either “right” or “left”
        self._type = None

        # boolean
        #
        # Reports whether this is a valid Hand object.
        self.valid = None
        if kwargs:
            for k in kwargs:
                setattr(self, k, kwargs[k])
                # print(f"Set {k} = {kwargs[k]}")

    def is_chup(self):
        pass

    def pitch(self):
        pass

    def roll(self):
        pass

    def rotationAngle(self, sinceFrame):
        pass

    def rotationAxis(self, sinceFrame):
        pass

    def rotationMatrix(self, sinceFrame):
        pass

    # The scale factor derived from the hand’s motion between the current frame and the specified frame.
    #
    # The scale factor is always positive. A value of 1.0 indicates no scaling took place. Values between 0.0 and 1.0 indicate contraction and values greater than 1.0 indicate expansion.
    #
    # The Leap derives scaling from the relative inward or outward motion of a hand and its associated fingers (independent of translation and rotation).
    def scaleFactor(self, sinceFrame):
        pass

    # The change of position of this hand between the current frame and the specified frame
    #
    # The returned translation vector provides the magnitude and direction of the movement in millimeters.
    def translation(self, sinceFrame):
        pass


class TGesture:
    # REf: https://developer-archive.leapmotion.com/documentation/javascript/api/Leap.Pointable.html
    def __init__(self, *args, **kwargs):
        #  array of floats (vector) -- circle only
        self.center = []

        # "direction": [
        #                 0.469491,
        #                 0.132652,
        #                 -0.872915
        #             ],
        self.direction = []

        # "duration": integer microseconds
        self.duration = None

        # "handId": [836, 837]
        self.handIds = []

        # "id": 8364,
        # A unique ID assigned to this Pointable object, whose value remains the same across consecutive frames while the tracked finger remains visible. If tracking is lost (for example, when a finger is occluded by another finger or when it is withdrawn from the Leap field of view), the Leap may assign a new ID when it detects the entity in a future frame.
        # The anatomical name of this finger:
        #
        # 0 = THUMB
        # 1 = INDEX
        # 2 = MIDDLE
        # 3 = RING
        # 4 = PINKY

        self.id = None

        #     "normal": array of floats -- circle only
        self.normal = []

        self.pointableIds = []

        #     "type": string - one of "circle", "swipe", "keyTap", "screenTap"
        self._type = None

        #     "state": string - one of "start", "update", "stop"
        self.state = None

        #     "position": array of floats (vector) -- swipe, keyTap, screenTap only
        self.position = []

        #     "progress": float -- circle, keyTap, screenTap only
        self.progress = None

        #     "radius": float -- circle only
        self.radius = None

        #     "speed": float -- swipe only
        self.speed = None

        #     "startPosition": array of float (vector) -- swipe only
        self.startPosition = []

        if kwargs:
            for k in kwargs:
                setattr(self, k, kwargs[k])

    def get_type(self):
        return self._type

    def is_chup(self):
        pass


class TFinger:
    # REf: https://developer-archive.leapmotion.com/documentation/javascript/api/Leap.Pointable.html
    def __init__(self, *args, **kwargs):
        # "direction": [
        #                 0.469491,
        #                 0.132652,
        #                 -0.872915
        #             ],
        self.direction = []

        # "handId": 836,
        self.handId = None

        # "id": 8364,
        # A unique ID assigned to this Pointable object, whose value remains the same across consecutive frames while the tracked finger remains visible. If tracking is lost (for example, when a finger is occluded by another finger or when it is withdrawn from the Leap field of view), the Leap may assign a new ID when it detects the entity in a future frame.
        # The anatomical name of this finger:
        #
        # 0 = THUMB
        # 1 = INDEX
        # 2 = MIDDLE
        # 3 = RING
        # 4 = PINKY

        self.id = None

        self._type = None

        # "length": 48.4596,
        # The estimated length of the finger in millimeters.
        self.length = None

        # "stabilizedTipPosition": [
        #                 70.1756,
        #                 221.596,
        #                 45.7427
        #             ],
        # The tip position in millimeters from the Leap origin. Stabilized based on the velocity of the pointable to make precise positioning easier.
        self.stabilizedTipPosition = []

        # "timeVisible": 4.86518,
        # The amount of time this pointable has been continuously visible to the Leap Motion controller in seconds.
        self.timeVisible = None

        # "tipPosition": [
        #                 66.9785,
        #                 219.5,
        #                 42.7543
        #             ],
        # The tip position in millimeters from the Leap origin.
        self.tipPosition = []

        # "tipVelocity": [
        #                 -0.252702,
        #                 0.302651,
        #                 0.0104628
        #             ],
        # The rate of change of the tip position in millimeters/second.
        self.tipVelocity = []

        # "tool": false,
        # Whether or not the Pointable is believed to be a tool. Tools are generally longer, thinner, and straighter than fingers.
        #
        # If tool is false, then this Pointable must be a finger.
        self.tool = False

        # "touchDistance": 0.218685,
        # A value proportional to the distance between this Pointable object and the adaptive touch plane.
        self.touchDistance = None

        # "touchZone": "hovering",
        # The Leap Motion software computes the touch zone based on a floating touch plane that adapts to the user’s finger movement and hand posture. The Leap Motion software interprets purposeful movements toward this plane as potential touch points. When a Pointable moves close to the adaptive touch plane, it enters the “hovering” zone. When a Pointable reaches or passes through the plane, it enters the “touching” zone.
        # @Tnd: if distance from "pointable" --> "adaptive touch plane":
        # < 1 & > 0: --> Hovering
        # < 0 & > -1: --> Touching
        self.touchZone = ""

        # "width": 15.4054
        # The estimated width of the finger in millimeters.
        self.width = None
        if kwargs:
            for k in kwargs:
                setattr(self, k, kwargs[k])

    def get_type(self):
        _type = None
        if self.id[-1:] == "0":
            _type = "THUMB"
        elif self.id[-1:] == "1":
            _type = "INDEX"
        elif self.id[-1:] == "2":
            _type = "MIDDLE"
        elif self.id[-1:] == "3":
            _type = "RING"
        elif self.id[-1:] == "4":
            _type = "PINKY"
        self._type = _type
        return self._type

    def is_chup(self):
        pass


class TPointable:
    # REf: https://developer-archive.leapmotion.com/documentation/javascript/api/Leap.Pointable.html
    def __init__(self, *args, **kwargs):
        # "direction": [
        #                 0.469491,
        #                 0.132652,
        #                 -0.872915
        #             ],
        self.direction = []

        # "handId": 836,
        self.handId = None

        # "id": 8364,
        # A unique ID assigned to this Pointable object, whose value remains the same across consecutive frames while the tracked finger remains visible. If tracking is lost (for example, when a finger is occluded by another finger or when it is withdrawn from the Leap field of view), the Leap may assign a new ID when it detects the entity in a future frame.
        # The anatomical name of this finger:
        #
        # 0 = THUMB
        # 1 = INDEX
        # 2 = MIDDLE
        # 3 = RING
        # 4 = PINKY

        self.id = None

        self._type = None

        # "length": 48.4596,
        # The estimated length of the finger in millimeters.
        self.length = None

        # "stabilizedTipPosition": [
        #                 70.1756,
        #                 221.596,
        #                 45.7427
        #             ],
        # The tip position in millimeters from the Leap origin. Stabilized based on the velocity of the pointable to make precise positioning easier.
        self.stabilizedTipPosition = []

        # "timeVisible": 4.86518,
        # The amount of time this pointable has been continuously visible to the Leap Motion controller in seconds.
        self.timeVisible = None

        # "tipPosition": [
        #                 66.9785,
        #                 219.5,
        #                 42.7543
        #             ],
        # The tip position in millimeters from the Leap origin.
        self.tipPosition = []

        # "tipVelocity": [
        #                 -0.252702,
        #                 0.302651,
        #                 0.0104628
        #             ],
        # The rate of change of the tip position in millimeters/second.
        self.tipVelocity = []

        # "tool": false,
        # Whether or not the Pointable is believed to be a tool. Tools are generally longer, thinner, and straighter than fingers.
        #
        # If tool is false, then this Pointable must be a finger.
        self.tool = False

        # "touchDistance": 0.218685,
        # A value proportional to the distance between this Pointable object and the adaptive touch plane.
        self.touchDistance = None

        # "touchZone": "hovering",
        # The Leap Motion software computes the touch zone based on a floating touch plane that adapts to the user’s finger movement and hand posture. The Leap Motion software interprets purposeful movements toward this plane as potential touch points. When a Pointable moves close to the adaptive touch plane, it enters the “hovering” zone. When a Pointable reaches or passes through the plane, it enters the “touching” zone.
        # @Tnd: if distance from "pointable" --> "adaptive touch plane":
        # < 1 & > 0: --> Hovering
        # < 0 & > -1: --> Touching
        self.touchZone = ""

        # "width": 15.4054
        # The estimated width of the finger in millimeters.
        self.width = None
        if kwargs:
            for k in kwargs:
                setattr(self, k, kwargs[k])

    def get_type(self):
        _type = None
        if self.id[-1:] == "0":
            _type = "THUMB"
        elif self.id[-1:] == "1":
            _type = "INDEX"
        elif self.id[-1:] == "2":
            _type = "MIDDLE"
        elif self.id[-1:] == "3":
            _type = "RING"
        elif self.id[-1:] == "4":
            _type = "PINKY"
        self._type = _type
        return self._type

    def is_chup(self):
        pass


class TLeapSocket:
    class THandHandler(Thread):
        def __init__(self, actions=[], getures=[]):
            self.actions = actions
            self.getures = getures

            self.last_geture = None
            self.current_geture = None

            self.last_action = None
            self.current_action = None

            self.thread = Thread(target=self.hand_handler, args=())
            self.thread.start()

        def hand_handler(self):
            while True:
                if len(self.actions) > 0:
                    action = self.actions.pop(0)
                    self.current_action = action
                    if action != self.last_action:
                        # print(f"action = {action}")
                        self.last_action = action
                elif len(self.getures) > 0:
                    geture = self.getures.pop(0)
                    self.current_geture = geture
                    if geture != self.last_geture:
                        print(f"geture = {geture.type}")
                        self.last_geture = geture
                else:
                    time.sleep(0.1)

    def __init__(self, max_history=100):
        # self.ws = websocket.WebSocketApp(addr,
        #                       on_open=self.on_open,
        #                       on_message=self.on_message,
        #                       on_error=self.on_error,
        #                       on_close=self.on_close)
        self.handler = self.THandHandler()

        self.ws = websocket.WebSocketApp("ws://localhost:6437/",
                                         on_message=lambda ws, msg: self.on_message(ws, msg),
                                         on_error=lambda ws, msg: self.on_error(ws, msg),
                                         on_close=lambda ws: self.on_close(ws),
                                         on_open=lambda ws: self.on_open(ws))
        self.max_history = max_history

        self.histories = []

        self.actions = []
        self.last_action = None

        # Tay trái
        self.left_hand = None

        # Tay phải
        self.right_hand = None

        self.data = None

        self.id = None
        self.currentFrameRate = None
        self.devices = []

        self.last_geture = None
        self.data_gestures = []
        self.gestures = []

        # Các bàn tay
        self.last_hands_number = None
        self.data_hands = []
        self.hands = []

        self.interactionBox = {}

        # Các ngón tay
        self.last_pointables_number = None
        self.data_pointables = []
        self.pointables = []

        #
        self.last_fingers_number = None
        self.data_fingers = []
        self.fingers = []

        self.r = []
        self.s = None
        self.t = []
        self.timestamp = None

    def run(self):
        self.ws.run_forever(dispatcher=rel)
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()

    def on_message(self, ws, message):
        # print(message)
        self.data = json.loads(message)
        if 'id' in self.data:
            self.id = self.data['id']
        if 'currentFrameRate' in self.data:
            self.currentFrameRate = self.data['currentFrameRate']
        if 'devices' in self.data:
            self.devices = self.data['devices']

        if 'gestures' in self.data:
            self.data_gestures = self.data['gestures']
            self.gestures.clear()
            for geture in self.data_gestures:
                geture_obj = TGesture(**geture)
                self.gestures.append(geture_obj)
                # self.handler.gestures.append(geture)
                self.handler.gestures.append(geture_obj)

            if len(self.gestures) > 0:
                for geture in self.gestures:
                    if geture.state == "stop":
                        if geture.type != self.last_geture:
                            print(
                                f"geture = {geture.type} in {geture.duration} from {geture.startPosition} to {geture.position} at {datetime.datetime.now()}")
                            self.last_geture = geture.type
        if 'hands' in self.data:
            self.data_hands = self.data['hands']
            self.last_hands_number = len(self.data_hands)

            self.hands.clear()
            if len(self.data_hands) > 0:
                for hand in self.data_hands:
                    hand_obj = THand(**hand)
                    self.hands.append(hand_obj)
        else:
            self.hands.clear()

        if 'fingers' in self.data:
            self.data_fingers = self.data['fingers']
            self.last_fingers_number = len(self.data_fingers)
            self.fingers.clear()
            for finger in self.data_fingers:
                finger = TFinger(**finger)
                # for k in pointable:
                #     setattr(finger, k, pointable[k])
                self.fingers.append(finger)

        if 'pointables' in self.data:
            self.data_pointables = self.data['pointables']
            self.last_pointables_number = len(self.data_pointables)
            self.pointables.clear()

            if len(self.data['pointables']) >= 5:
                # print(json.dumps(self.data, indent=4))
                pass
            for pointable in self.data_pointables:
                pointable_obj = TPointable(**pointable)
                self.pointables.append(pointable_obj)

                for i in range(0, len(self.pointables)):
                    # for hand in self.hands:
                    if pointable_obj.handId == self.hands[i].id:
                        self.hands[i].pointables.append(pointable_obj)
                        break

                if str(pointable['touchZone']).lower() == "touching":
                    self.handler.actions.append(pointable['touchZone'])
                    break
                    # pass
                else:
                    is_outside = True
                    for pointable in self.data_pointables:
                        if str(pointable['touchZone']).lower() == "hovering":
                            is_outside = False
                            pass
                            # break
                    if is_outside == False:
                        self.handler.actions.append(pointable['touchZone'])
                # else:
                #     # self.handler.actions.append(pointable['touchZone'])
                #     pass
                #     # print(pointable['touchZone'])
        if (self.last_hands_number and len(self.data_hands) != self.last_hands_number) or (
                self.last_pointables_number and len(self.data_pointables) != self.last_pointables_number) or (
                self.last_fingers_number and len(self.data_fingers) != self.last_fingers_number):
            print(f"self.hands = {self.hands} Pointables: {len(self.pointables)} Fingers: {len(self.fingers)}")

        if 'interactionBox' in self.data:
            self.interactionBox = self.data['interactionBox']

        # if 'pointables' in self.data:
        #     self.data_pointables = self.data['pointables']

        # for pointable in self.data_pointables:
        #     self.data_fingers.append(pointable)
        #
        #     finger = TFinger(**pointable)
        #     # for k in pointable:
        #     #     setattr(finger, k, pointable[k])
        #     self.fingers.append(finger)
        #
        #     if str(pointable['touchZone']).lower() == "touching":
        #         self.handler.actions.append(pointable['touchZone'])
        #         break
        #         # pass
        #     else:
        #         is_outside = True
        #         for pointable in self.pointables:
        #             if str(pointable['touchZone']).lower() == "hovering":
        #                 is_outside = False
        #                 pass
        #                 # break
        #         if is_outside == False:
        #             self.handler.actions.append(pointable['touchZone'])
        #     # else:
        #     #     # self.handler.actions.append(pointable['touchZone'])
        #     #     pass
        #     #     # print(pointable['touchZone'])
        if 'r' in self.data:
            self.r = self.data['r']
        if 's' in self.data:
            self.s = self.data['s']
        if 't' in self.data:
            self.t = self.data['t']

        if 'timestamp' in self.data:
            self.timestamp = self.data['timestamp']

        # Check max history
        self.histories.append(self.data)
        if len(self.histories) > self.max_history:
            self.histories.pop(0)

        if len(self.actions) > self.max_history:
            self.actions.pop(0)

        # print(json.dumps(self.data, indent=4))

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### Closed ###")

    def on_open(self, ws):
        print("Opened connection")

# End of TFile
