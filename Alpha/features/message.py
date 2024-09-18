import pyautogui
import time

def messages(num,mess):
        pyautogui.press("super")
        pyautogui.sleep(3)
        pyautogui.typewrite("Whatsapp")
        pyautogui.sleep(5)
        pyautogui.press("enter")
        pyautogui.sleep(5)
        pyautogui.typewrite(num)
        time.sleep(2)
        pyautogui.press("down")
        pyautogui.press("enter")
        time.sleep(5)
        pyautogui.typewrite(mess)
        pyautogui.press('enter')
        return
