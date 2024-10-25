import pyautogui

class MouseController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.is_left_button_down = False
        self.is_right_button_down = False

    def move_cursor(self, x, y):
        x = max(1, min(x * self.screen_width, self.screen_width - 1))
        y = max(1, min(y * self.screen_height, self.screen_height - 1))
        pyautogui.moveTo(x, y)

    def left_button_down(self):
        if not self.is_left_button_down:
            pyautogui.mouseDown(button='left')
            self.is_left_button_down = True

    def right_button_down(self):
        if not self.is_right_button_down:
            pyautogui.mouseDown(button='right')
            self.is_right_button_down = True

    def buttons_up(self):
        if self.is_left_button_down:
            pyautogui.mouseUp(button='left')
            self.is_left_button_down = False
        if self.is_right_button_down:
            pyautogui.mouseUp(button='right')
            self.is_right_button_down = False
