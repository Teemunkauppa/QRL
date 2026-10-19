import sys
from PIL import Image, ImageTk
import customtkinter as ct
from QrGen import QrGen
from UrlShortener import UrlShortener as Url

APP_NAME = "QRL"
APP_SIZE = (900, 600)
APP_RESISABLE = False

def main():
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

    qrGenTab = QrGen(tabview, "QR-Code Generator", APP_SIZE)

    urlTab = Url(tabview, "URL shortener", APP_SIZE)

    qrGenTab.Focus(tabview)

    app.mainloop()

def SizeToStr(size: tuple[int]) -> str:
    return f"{str(size[0])}x{str(size[1])}"

if(__name__ == "__main__"):
    main()