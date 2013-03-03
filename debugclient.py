#!/usr/bin/env python2.7
import sys, json, zmq

def main():
    context = zmq.Context()
    receiver = context.socket(zmq.SUB)
    receiver.connect("tcp://127.0.0.1:5557")
    receiver.setsockopt(zmq.SUBSCRIBE, "")

    gesture_receiver = context.socket(zmq.SUB)
    gesture_receiver.connect("tcp://127.0.0.1:5557")
    gesture_receiver.setsockopt(zmq.SUBSCRIBE, "gestures")

    fingers_receiver = context.socket(zmq.SUB)
    fingers_receiver.connect("tcp://127.0.0.1:5557")
    fingers_receiver.setsockopt(zmq.SUBSCRIBE, "fingers")

    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    poller.register(gesture_receiver, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())

        if socks.get(receiver) == zmq.POLLIN:
            print "EMPTY_FRAME: " + receiver.recv()
        if socks.get(gesture_receiver) == zmq.POLLIN:
            print "GESTURES: " + gesture_receiver.recv()
        if socks.get(fingers_receiver) == zmq.POLLIN:
            print "FINGERS: " + fingers_receiver.recv()

if __name__ == "__main__":
  main()
