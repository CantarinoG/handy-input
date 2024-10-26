from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer
from mouse_controller import MouseController

gesture_recognizer = GestureRecognizer()
mouse_controller = MouseController()

hand_tracker = HandTracker(gesture_recognizer, mouse_controller)
hand_tracker.run(is_debug=False)