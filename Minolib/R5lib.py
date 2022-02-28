import pyperclip
import ctypes
import pyautogui
import time
from ctypes import wintypes


_KEYEVENTF_KEYUP       = 0x0002
_KEYEVENTF_UNICODE     = 0x0004
wintypes.ULONG_PTR = wintypes.WPARAM
_user32 = ctypes.WinDLL('user32', use_last_error=True)

class _KEYBDINPUT(ctypes.Structure):

    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(_KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & _KEYEVENTF_UNICODE:
            self.wScan = _user32.MapVirtualKeyExW(self.wVk, 0, 0)

class _INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", _KEYBDINPUT),)
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

_LPINPUT = ctypes.POINTER(_INPUT)
_user32.SendInput.argtypes = (wintypes.UINT, _LPINPUT, ctypes.c_int)

def PressKey(hex):
    x = _INPUT(type=1, ki=_KEYBDINPUT(wVk=hex))_user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hex):
    x = _INPUT(type=1,
            ki=_KEYBDINPUT(wVk=hex, dwFlags=_KEYEVENTF_KEYUP))_user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def PressEnter():
    PressKey(0x0D)
    time.sleep(0.001)
    ReleaseKey(0x0D)

def SendChat(text: str):
    PressEnter()
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    PressEnter()

def SendKey(hex: hex):
    PressKey(hex)
    ReleaseKey(hex)