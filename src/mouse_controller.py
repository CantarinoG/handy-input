import pyautogui

class MouseController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.has_clicked_left = False
        self.has_clicked_right = False
        self.frames_clicked_left = 0
        pyautogui.PAUSE = 0

    def move_cursor(self, x, y):
        x = (x - 0.2) / 0.6
        y = (y - 0.2) / 0.6

        x = max(1, min(x * self.screen_width, self.screen_width - 2))
        y = max(1, min(y * self.screen_height, self.screen_height - 2))
        pyautogui.moveTo(x, y)

    def left_button_down(self):
        self.frames_clicked_left += 1
        if not self.has_clicked_left:
            pyautogui.click()
            self.has_clicked_left = True
        if self.frames_clicked_left >= 10:
            pyautogui.mouseDown(button='left')

    def right_button_down(self):
        if not self.has_clicked_right:
            pyautogui.rightClick()
            self.has_clicked_right = True

    def buttons_up(self):
        self.has_clicked_right = False
        self.has_clicked_left = False
        self.frames_clicked_left = 0
        pyautogui.mouseUp(button='left')
