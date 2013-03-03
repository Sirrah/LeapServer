import Leap, sys
import json, zmq
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):

  def send(self, msg):
    print "Sending: " + msg
    #self.zmqSocket.send_json({
    #  "message" : msg
    #})
    self.zmqSocket.send(msg)
    

  def state_string(self, state):
    if state == Leap.Gesture.STATE_START:
      return "STATE_START"

    if state == Leap.Gesture.STATE_UPDATE:
      return "STATE_UPDATE"

    if state == Leap.Gesture.STATE_STOP:
      return "STATE_STOP"

    if state == Leap.Gesture.STATE_INVALID:
      return "STATE_INVALID"

  def on_init(self, controller):
    ctx = zmq.Context()
    #self.zmqSocket = ctx.socket(zmq.PUSH)
    self.zmqSocket = ctx.socket(zmq.PUB)
    self.zmqSocket.bind('tcp://127.0.0.1:3333')

    print "Initialized"

  def on_connect(self, controller):
    print "Connected"

    # Enable gestures
    controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
    controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
    controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

  def on_disconnect(self, controller):
    print "Disconnected"

  def on_frame(self, controller):
    # Get the most recent frame and report some basic information
    frame = controller.frame()
    
    #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
    #  frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

    data = {'frame' : {'id':frame.id, 'timestamp':frame.timestamp} }
    self.send(json.dumps(data))
    
    if not frame.hands.empty:
      # Get the first hand
      hand = frame.hands[0]

      # Check if the hand has any fingers
      fingers = hand.fingers
      if not fingers.empty:
        # Calculate the hand's average finger tip position
        avg_pos = Leap.Vector()
        for finger in fingers:
            avg_pos += finger.tip_position
        avg_pos /= len(fingers)
        msg = {'frame' : {'fingers' : len(fingers), 'avg_pos' : [avg_pos.x, avg_pos.y, avg_pos.z]}}
        self.send(json.dumps(msg))
        #print msg
        
        # Get the hand's sphere radius and palm position
        print "Hand sphere radius: %f mm, palm position: %s" % (
              hand.sphere_radius, hand.palm_position)

        # Get the hand's normal vector and direction
        normal = hand.palm_normal
        direction = hand.direction

        # Calculate the hand's pitch, roll, and yaw angles
        print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
          direction.pitch * Leap.RAD_TO_DEG,
          normal.roll * Leap.RAD_TO_DEG,
          direction.yaw * Leap.RAD_TO_DEG)

        # Gestures
        for gesture in frame.gestures():
          if gesture.type == Leap.Gesture.TYPE_CIRCLE:
            circle = CircleGesture(gesture)

            # Determine clock direction using the angle between the pointable and the circle normal
            if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
              clockwiseness = "clockwise"
            else:
              clockwiseness = "counterclockwise"

            # Calculate the angle swept since the last frame
            swept_angle = 0
            if circle.state != Leap.Gesture.STATE_START:
              previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
              swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

            print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
              gesture.id, self.state_string(gesture.state),
              circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

          if gesture.type == Leap.Gesture.TYPE_SWIPE:
            swipe = SwipeGesture(gesture)
            print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
              gesture.id, self.state_string(gesture.state),
              swipe.position, swipe.direction, swipe.speed)

          if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
            keytap = KeyTapGesture(gesture)
            print "Key Tap id: %d, %s, position: %s, direction: %s" % (
              gesture.id, self.state_string(gesture.state),
              keytap.position, keytap.direction )

          if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
            screentap = ScreenTapGesture(gesture)
            print "Screen Tap id: %d, %s, position: %s, direction: %s" % (
              gesture.id, self.state_string(gesture.state),
              screentap.position, screentap.direction )

def main():
  listener = SampleListener()
  controller = Leap.Controller()

  controller.add_listener(listener)

  print "Press Enter to quit..."
  sys.stdin.readline()

  controller.remove_listener(listener)

if __name__ == "__main__":
  main()
