#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#region Description
__author__ = 'Tamnd - NGUYEN DUC TAM'
__copyright__ = "Copyright ©2022 Tamnd <ductambka@gmail.com>"
__maintainer__ = "Tamnd"
__email__ = "ductambka@gmail.com"
__status__ = "Production"
# __date__ = 2022 - 08 - 10
#endregion

# __init__.py
import sys
import os
import time
import datetime
import json
import logging
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap3

class SampleListener(Leap3.Listener):

    def on_connect(self, controller):
        print("Connected")


    def on_frame(self, controller):
        frame = controller.frame()

        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap3.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()

# End of TFile



