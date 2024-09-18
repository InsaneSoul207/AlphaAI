import pyautogui
import time
def close(b):
        pyautogui.press("super")
        pyautogui.sleep(3)
        pyautogui.typewrite(b)
        pyautogui.sleep(3)
        pyautogui.press("enter")
        pyautogui.sleep(7)
        pyautogui.hotkey('alt', 'f4')