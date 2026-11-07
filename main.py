import sys
import SaveSystem
from QrGen import QrGen
import customtkinter as ct
from Settings import Settings
from PIL import Image, ImageTk
from UrlShortener import UrlShortener as Url

APP_NAME = "QRL"
APP_SIZE = (900, 600)
APP_RESISABLE = False

tabview: ct.CTkTabview = None
qrGenTab: QrGen = None
urlTab: Url = None
settingsTab: Settings = None

def RebuildUI():
    global tabview, settingsTab
    for tabName in list(tabview._tab_dict.keys()):
        tabview.delete(tabName)
    GenerateTabs()
    settingsTab.Focus(tabview)
    
def FocusDefaultTab():
    global qrGenTab, urlTab, settingsTab, tabview
    if(SaveSystem.GetSettings().defaultTab == SaveSystem.Tabs.QrGen):
        qrGenTab.Focus(tabview)
    elif(SaveSystem.GetSettings().defaultTab == SaveSystem.Tabs.UrlShortener):
        urlTab.Focus(tabview)
    elif(SaveSystem.GetSettings().defaultTab == SaveSystem.Tabs.Settings):
        settingsTab.Focus(tabview)

def GenerateTabs():
    global qrGenTab, urlTab, settingsTab, tabview
    qrGenTab = QrGen(tabview, "QR-Code Generator", APP_SIZE)
    urlTab = Url(tabview, "URL shortener", APP_SIZE)
    settingsTab = Settings(tabview, "Settings", APP_SIZE)

def main():
    global tabview, urlTab, qrGenTab, settingsTab
    app = ct.CTk()

    app.title(APP_NAME)
    app.geometry(SizeToStr(APP_SIZE))
    app.resizable(APP_RESISABLE, APP_RESISABLE)
    ct.deactivate_automatic_dpi_awareness()

    if(sys.platform == "win32"):
        app.iconbitmap("assets/python_sucks.ico")
    else:
        img = Image.open("assets/python_sucks.png")
        photo = ImageTk.PhotoImage(image=img)
        app.iconphoto(True, photo)

    tabview = ct.CTkTabview(master=app, anchor="n")
    tabview.pack(padx=0, pady=0, fill="both", expand=True)

    SaveSystem.SetRebuildCallback(RebuildUI)
    SaveSystem.SetMainRoot(app)
    SaveSystem.InitSaveSystem()
    SaveSystem.settings = SaveSystem.LoadSettings()

    GenerateTabs()

    FocusDefaultTab()

    app.mainloop()

def SizeToStr(size: tuple[int]) -> str:
    return f"{str(size[0])}x{str(size[1])}"

if(__name__ == "__main__"):
    main()