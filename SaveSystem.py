import os
import sys
import json
import base64
import hashlib
import threading
import tkinter as tk
from pathlib import Path
from main import RebuildUI
import customtkinter as ct
import CTkColorPicker as ctkcp
from dataclasses import dataclass
from cryptography.fernet import Fernet, InvalidToken

@dataclass
class Tabs():
    QrGen: str = "QrGen"
    UrlShortener: str = "UrlShortener"
    Settings: str = "Settings"

    def Get(self) -> list:
        return [self.QrGen, self.UrlShortener, self.Settings]

@dataclass
class SettingsData():
    fgColor: str = "#2D2D2D"
    bgColor: str = "transparent"
    hoverColor: str = "#4A9FD8"
    buttonHoverColor: str = "#4A9FD8"
    borderColor: str = "#454545"
    textColor: str = "#FFFFFF"
    checkmarkColor: str = "#FFFFFF"
    progressColor: str = "#3B82C7"
    buttonColor: str = "#5EA1E0"
    dropdownFgColor: str = "#3A3A3A"
    dropdownTextColor: str = "#C0C0C0"
    placeholderTextColor: str = "#666666"
    textColorDisabled: str = "#666666"
    enableAdv: bool = False
    defaultTab: str = Tabs.QrGen

    def GetFgColor(self) -> str:
        return self.fgColor

    def GetBgColor(self) -> str:
        return self.bgColor

    def GetHoverColor(self) -> str:
        return self.hoverColor

    def GetButtonHoverColor(self) -> str:
        return self.buttonHoverColor

    def GetBorderColor(self) -> str:
        return self.borderColor

    def GetTextColor(self) -> str:
        return self.textColor

    def GetCheckmarkColor(self) -> str:
        return self.checkmarkColor

    def GetProgressColor(self) -> str:
        return self.progressColor

    def GetButtonColor(self) -> str:
        return self.buttonColor

    def GetDropdownFgColor(self) -> str:
        return self.dropdownFgColor

    def GetDropdownTextColor(self) -> str:
        return self.dropdownTextColor

    def GetPlaceholderTextColor(self) -> str:
        return self.placeholderTextColor

    def GetTextColorDisabled(self) -> str:
        return self.textColorDisabled

    def IsAdvancedEnabled(self) -> bool:
        return self.enableAdv

    def GetDefaultTab(self) -> Tabs:
        return self.defaultTab

    def ToDict(self):
        return vars(self)

    @classmethod
    def FromDict(cls, data: dict) -> 'SettingsData':
        return cls(**data)


DEBOUNCE_DELAY_MS = 1000
settings: SettingsData = None
updateTimer: threading.Timer = None
settingsFilename: str = "QRL.data"
settingsFile: Path = ""
cwd: str = ""
rebuildUI: bool = False

rebuildCallback = None 
mainRoot: tk.Misc = None

def SetRebuildCallback(callback):
    global rebuildCallback
    rebuildCallback = callback

def SetMainRoot(root: tk.Misc):
    global mainRoot
    mainRoot = root

def InitSaveSystem():
    global settingsFile, settingsFilename, cwd
    cwd = GetCWD()
    settingsFile = Path(cwd / settingsFilename)
    InitTimer()

def InitTimer():
    global updateTimer
    updateTimer = None
    
def QueueSave(uiRebuild: bool = False, *args):
    global updateTimer, DEBOUNCE_DELAY_MS, rebuildUI
    
    # Update flag if rebuild not queued
    if(not rebuildUI):
        rebuildUI = uiRebuild

    # Cancel pending timer
    if updateTimer and updateTimer.is_alive():
        updateTimer.cancel()

    # Start ner timer
    updateTimer = threading.Timer(DEBOUNCE_DELAY_MS / 1000, SaveSettings)
    updateTimer.daemon = True
    updateTimer.start()

def GetSettings() -> SettingsData:
    global settings
    return settings

def GetCWD() -> Path:
    if "__compiled__" in globals():
        # Running under Nuitka (standalone or onefile)
        exeDir = os.path.dirname(os.path.abspath(sys.argv[0]))
    elif getattr(sys, 'frozen', False):
        # PyInstaller etc.
        exeDir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        # Plain script
        exeDir = os.path.dirname(os.path.abspath(__file__))
    return Path(exeDir)

def SaveSettings() -> bool:
    global settingsFile, settings, rebuildUI
    data = settings.ToDict()

    if isinstance(data['defaultTab'], Tabs):
        data['defaultTab'] = data['defaultTab'].value

    jsonData = json.dumps(data).encode("utf-8")
    with open(settingsFile, 'wb') as file:
        file.write(Encrypt(jsonData))

    if rebuildUI and rebuildCallback is not None:
        if mainRoot is not None:
            mainRoot.after(0, rebuildCallback)
        else:
            rebuildCallback()

    rebuildUI = False

def LoadSettings() -> SettingsData:
    global settingsFile
    if not settingsFile.exists():
        print("Settings file not found! Setting default settings")
        return LoadDefaultSettings()
    try:
        with open(settingsFile, 'rb') as f:
            jsonData = Decrypt(f.read())

        data = json.loads(jsonData.decode("utf-8"))
        return SettingsData.FromDict(data)
    except (json.JSONDecodeError, TypeError, UnicodeDecodeError, InvalidToken):
        print("Settings file corrupted! Using defaults")
        return LoadDefaultSettings()

def LoadDefaultSettings():
    global settings
    settings = SettingsData()
    SaveSettings()
    return settings

def GetKey() -> bytes:
    digest = hashlib.sha256(b"Thi$_I$_4_V3rY_RaNdoM_QRL_D4t4_3ncrypt10n_striG").digest()
    return base64.urlsafe_b64encode(digest)

def Encrypt(data: bytes) -> bytes:
    return Fernet(GetKey()).encrypt(data)

def Decrypt(token: bytes) -> bytes:
    return Fernet(GetKey()).decrypt(token)