import pyperclip
import ctypes
import pyautogui
import time
from ctypes import wintypes

_user32 = ctypes.WinDLL('user32', use_last_error=True)
ctypes.wintypes.ULONG_PTR = wintypes.WPARAM

# ctypes code by https://gist.github.com/Aniruddha-Tapas/1627257344780e5429b10bc92eb2f52a

class _KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(_KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & 0x0004:
            self.wScan = _user32.MapVirtualKeyExW(self.wVk,
                                                 0, 0)

class _MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class _HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class _INPUT(ctypes.Structure):
    class __INPUT(ctypes.Union):
        _fields_ = (("ki", _KEYBDINPUT),
                    ("mi", _MOUSEINPUT),
                    ("hi", _HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", __INPUT))

_LPINPUT = ctypes.POINTER(_INPUT)
def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

_user32.SendInput.errcheck = _check_count
_user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             _LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

_kbd = 1

def PressKey(hexKeyCode):
    x = _INPUT(type=_kbd,
              ki=_KEYBDINPUT(wVk=hexKeyCode))
    _user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = _INPUT(type=_kbd,
              ki=_KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=0x0002))
    _user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def PressEnter():
    SendKey(0x0D)

def SendChat(text: str):
    PressEnter()
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    PressEnter()

def SendKey(hex: hex):
    PressKey(hex)
    ReleaseKey(hex)