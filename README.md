# LeapServer

This is a python based server to push events from a [Leap Motion](https://www.leapmotion.com) device through a [0mq](http://www.zeromq.org) server to remote devices.
The server is made for my own use to provide the output of the Leap Motion device for development on Linux and Android.

## Requirements

The server is based on the Leap Motion Python [sample application](https://developer.leapmotion.com/documentation/guide/Sample_Python_Tutorial#running-the-sample) and requires the following files from the Leap SDK to be available from the working directory:

 - Leap.py
 - Leap.dll
 - LeapPython.pyd

In addition to the Leap SDK you will need the following:

 - [Python 2.7](http://www.python.org/download/releases/2.7) (v2.7 is required for the Leap SDK)
 - [0mq](http://www.zeromq.org)
 - [Python bindings](http://www.zeromq.org/bindings:python) for 0mq

## Usage

1. Start the Leap software as usual
2. run `leapserver.py`
3. (optional) run `debugclient.py`

## Thanks

Thanks to the Leap Motion team for sending me a developer toolkit.
