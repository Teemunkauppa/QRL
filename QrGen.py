import os
import io
import sys
import qrcode
import Helpers
import SaveSystem
import tkinter as tk
import customtkinter as ct
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk

# NOTES: If further data mode (numeric/alphabetical/binary/kanji) is needed then switch qrcode to segno

class QrGen():
    ENABLE_LIVE_PREVIEW_BY_DEFAULT = True
    DEBOUNCE_DELAY_MS = 500
    PREVIEW_SIZE = 300

    name: str = ""
    tab: ct.CTkFrame = None
    textInput: ct.CTkEntry = None
    livePreviewToggle: ct.CTkCheckBox = None
    advancedOptionsToggle: ct.CTkCheckBox = None
    versionSlider: ct.CTkSlider = None
    versionSliderValue: ct.CTkLabel = None
    ecDropdown: ct.CTkComboBox = None
    maskSlider: ct.CTkSlider = None
    maskSliderValue: ct.CTkLabel = None
    generateCodeButton: ct.CTkButton = None
    blockSizeSlider: ct.CTkSlider = None
    blockSizeSliderValue: ct.CTkLabel = None
    borderSlider: ct.CTkSlider = None
    borderSliderValue: ct.CTkLabel = None

    right: ct.CTkFrame = None
    qrDisplayFrame: ct.CTkFrame = None
    qrCanvas: ct.CTkCanvas = None
    errorText: ct.CTkLabel = None

    currentPilImage: Image = None
    displayedImage: ImageTk = None

    inputTextVar: ct.StringVar = None
    updateJob: str = None

    ecOptions = ["Auto", "Level L (~7%)", "Level M (~15%)", "Level Q (~25%)", "Level H (~30%)"]

    livePreview = False
    selLevel = 0
    selEc = ecOptions[0]
    selMask = 0
    selBlockSize = 0
    selBorder = 0

    def __init__(self, tabview: ct.CTkTabview, name: str, size: tuple[int]):
        self.tab = tabview.add(name)
        self.name = name
        self.InitTimer()
        self.DrawUI(size)
        self.SetOptions()
        self.ShowAdvanced(SaveSystem.GetSettings().enableAdv)

    def InitTimer(self):
        self.inputTextVar = ct.StringVar()
        self.updateTimer = None

    def DrawUI(self, size: tuple[int]):
        # Split into 2 columns
        self.tab.columnconfigure(0, weight=1)
        self.tab.columnconfigure(1, weight=1)
        self.tab.rowconfigure(1, weight=1)

        # Title
        title = Helpers.GenerateTitle(master=self.tab, text=self.name, font=("ArialBold", 20)) 
        title.grid(row=0, column=0, columnspan=2, pady=(5, 5))

        # Left panel
        left = Helpers.GenerateFrame(self.tab)
        left.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        # Options title
        leftTitle = Helpers.GenerateTitle(master=left, text="Options", font=("Arial", 18))
        leftTitle.pack(pady=(5, 0), anchor="nw")

        # Input for QR
        self.textInput = Helpers.GenerateEntry(master=left, placeholder_text="Enter text...", width=int((size[0] / 2) - 50), height=30, textvariable=self.inputTextVar)
        self.textInput.pack(pady=(0, 0), anchor="nw")
        self.textInput.bind("<Return>", self.EventEnterPressed)

        # Live preview toggle
        self.livePreviewToggle = Helpers.GenerateCheckbox(master=left, text="Live preview", font=("Arial", 16), command=self.EventLivePreview)
        self.livePreviewToggle.pack(pady=(10, 0), anchor="nw")

        # Generate button
        self.generateCodeButton = Helpers.GenerateButton(master=left, text="Generate QR-Code", command=self.GenerateCode)
        self.generateCodeButton.pack(pady=(10, 0), anchor="nw")

        # Advaced options toggle
        self.advancedOptionsToggle = Helpers.GenerateCheckbox(master=left, text="Advanced options", font=("Arial", 16), checked=SaveSystem.GetSettings().enableAdv, command=self.EventAdvancedOptions)
        self.advancedOptionsToggle.pack(pady=(10, 0), anchor="nw")

        # Version slider
        versionSliderTuple = Helpers.CreateSlider(left, 0, 40, "Version: ", self.EventSliderVersion)
        self.versionSlider = versionSliderTuple[0]
        self.versionSliderValue = versionSliderTuple[1]

        # Error correcton dropdown
        self.ecDropdown = Helpers.GenerateDropdown(left, "Error correction level", self.ecOptions, self.ecOptions[0], self.EventEcDropdown)

        # Mask slider
        maskSliderTuple = Helpers.CreateSlider(left, 0, 8, "Mask: ", self.EventSliderMask)
        self.maskSlider = maskSliderTuple[0]
        self.maskSliderValue = maskSliderTuple[1]

        # Block size slider
        blockSizeSliderTuple = Helpers.CreateSlider(left, 1, 50, "Block size (px):", self.EventSliderBlockSize)
        self.blockSizeSlider = blockSizeSliderTuple[0]
        self.blockSizeSliderValue = blockSizeSliderTuple[1]

        # Border slider
        borderSliderTuple = Helpers.CreateSlider(left, 4, 20, "Border (px):", self.EventSliderBorder)
        self.borderSlider = borderSliderTuple[0]
        self.borderSliderValue = borderSliderTuple[1]

        # Right panel
        self.right = Helpers.GenerateFrame(self.tab)
        self.right.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.right.grid_columnconfigure(0, weight=1)

        # Preview title
        previewTitle = Helpers.GenerateTitle(master=self.right, text="Preview", font=("Arial", 18))
        previewTitle.pack(pady=(10, 10), anchor="n")

        # Canvas for image
        self.qrCanvas = Helpers.GenerateCanvas(master=self.right, width=self.PREVIEW_SIZE, height=self.PREVIEW_SIZE)
        self.qrCanvas.pack(padx=(10, 10), pady=(10, 10))

        # Buttons row
        buttonRow: ct.CTkFrame = Helpers.GenerateFrame(self.right, transparent=True)
        buttonRow.pack(fill="x", pady=(15, 5))
        buttonRow.grid_columnconfigure(0, weight=1)
        buttonRow.grid_columnconfigure(1, weight=1)

        # Button for saving the qr
        saveButton = Helpers.GenerateButton(master=buttonRow, text="Save as file", command=self.EventSaveCode, width=150)
        saveButton.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        # Button for copying to clipboard
        cpToCpButton = Helpers.GenerateButton(master=buttonRow, text="Copy to clipboard", command=self.EventCopyToClipboard, width=150)
        cpToCpButton.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        # Label for error messages
        self.errorText = Helpers.GenerateTitle(master=self.right, text="", font=("Arial", 12), text_color="red", justify="left", wraplength=350)
        self.errorText.pack(pady=(0, 0), anchor="nw")

    def EventEnterPressed(self, *args):
        self.GenerateCode()

    def GenerateCode(self):
        if(self.textInput.get() == ""):
            self.HideCode()
            return

        try:
            # EC mapping
            ecMapping = {
                self.ecOptions[0]: None,
                self.ecOptions[1]: qrcode.constants.ERROR_CORRECT_L,
                self.ecOptions[2]: qrcode.constants.ERROR_CORRECT_M,
                self.ecOptions[3]: qrcode.constants.ERROR_CORRECT_Q,
                self.ecOptions[4]: qrcode.constants.ERROR_CORRECT_H
            }

            # Get level and EC level
            ecLevel = ecMapping.get(self.selEc, None)
            version = None if self.selLevel == 0 else self.selLevel

            # Generate QR-Code
            qr: qrcode.QRCode = qrcode.QRCode(version=version, box_size=self.selBlockSize, border=self.selBorder)

            # Error correction level
            if(ecLevel != None):
                qr.error_correction = ecLevel

            # Mask pattern if set
            if(self.selMask > 0):
                qr.mask_pattern = self.selMask - 1

            # Add data to qrcode and generate it
            qr.add_data(self.textInput.get())
            qr.make(fit=False)

            # Create PIL image
            img: Image = qr.make_image(fill_color="black", back_color="white")

            # Save for later use
            self.currentPilImage = img

            # Resize to fit canvas
            resisedImg = img.resize((self.PREVIEW_SIZE, self.PREVIEW_SIZE), Image.Resampling.NEAREST)

            # Convert image to tkintern image
            tkImg: ImageTk = ImageTk.PhotoImage(resisedImg)

            # Dispaly code
            self.DisplayCode(tkImg)

        except qrcode.exceptions.DataOverflowError:
            self.ShowError("Data Too Long", "Content exceeds QR code capacity for current settings. Try:\n• Lowering error correction level\n• Using shorter text\n• Increasing version number")
        except ValueError as e:
            self.ShowError("Invalid Parameter", f"Configuration error: {str(e)}")
        except Exception as e:
            self.ShowError("Generation Failed", f"Unexpected error: {type(e).__name__}: {str(e)}")

    def DisplayCode(self, code: ImageTk):
        self.HideError()
        self.qrCanvas.delete("all")
        self.displayedImage = code
        self.qrCanvas.create_image(self.PREVIEW_SIZE / 2, self.PREVIEW_SIZE / 2, image=code, anchor="center")

    def HideCode(self):
        self.currentPilImage = None
        self.displayedImage = None
        self.qrCanvas.delete("all")

    def ShowError(self, reason:str, text: str):
        self.HideCode()
        self.errorText.configure(text=f"{reason}:\n{text}")
        print(reason, text) 

    def HideError(self):
        self.errorText.configure(text="")

    def SetOptions(self):
        self.inputTextVar.trace_add('write', self.OnTextChangedEvent)

        self.livePreviewToggle.set(self.ENABLE_LIVE_PREVIEW_BY_DEFAULT)

        self.EventLivePreview()

        self.versionSlider.set(0)
        self.EventSliderVersion(0)

        self.ecDropdown.set(self.ecOptions[0])
        self.EventEcDropdown(self.ecOptions[0])

        self.maskSlider.set(0)
        self.EventSliderMask(0)

        self.blockSizeSlider.set(10)
        self.EventSliderBlockSize(10)

        self.borderSlider.set(4)
        self.EventSliderBorder(4)

    def ShowAdvanced(self, show: bool):
        state = tk.DISABLED
        if(show):
            state = tk.NORMAL

        self.versionSlider.configure(state=state)
        self.ecDropdown.configure(state=state)
        self.maskSlider.configure(state=state)
        self.blockSizeSlider.configure(state=state)
        self.borderSlider.configure(state=state)

    def EventSaveCode(self):
        filetypes = [("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"),("All files", "*.*")]
        filepath = filedialog.asksaveasfilename(title="Save QR code as...", defaultextension=".png", filetypes=filetypes, initialfile="qrcode.png")

        if filepath:
            dir = os.path.dirname(filepath)
            filename = os.path.basename(filepath)
            
            try:
                if(self.currentPilImage == None):
                    self.ShowError("Failed to save QR Code:", "No QR Code to save")
                    return

                ext = os.path.splitext(filename)[1].lower()

                if(ext in [".jpg", ".jpeg"]):
                    rgbImg = self.currentPilImage.convert("RGB")
                    rgbImg.save(filepath)
                else:
                    self.currentPilImage.save(filepath)
            except Exception as e:
                self.ShowError("Saving Failed", f"Unexpected error: {type(e).__name__}: {str(e)}")
                
    def EventCopyToClipboard(self):
        if(self.currentPilImage == None):
            self.ShowError("Failed to copy to clipboard", "No QR Code to copy")
            return
        try:
            if(sys.platform == "win32"):
                self.CopyToWindows()
            elif(sys.platform == "darwin"):
                self.CopyToMAC()
            elif(sys.platform == "linux"):
                self.CopyToLinux()
            else:
                self.ShowError("OS not supported", "Failed to identify OS for copying to clipboard")
        except Exception as e:
            self.ShowError("Copying to Clipboard Failed:", f"Unexpected error: {type(e).__name__}: {str(e)}")

    def CopyToWindows(self):
        import win32clipboard
        import win32con

        bmpBuf = io.BytesIO()
        self.currentPilImage.convert("RGB").save(bmpBuf, format="BMP")
        dibData = bmpBuf.getvalue()[14:]

        pngBuf = io.BytesIO()
        self.currentPilImage.save(pngBuf, format="PNG")

        pngFormat = win32clipboard.RegisterClipboardFormat("PNG")

        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_DIB, dibData)
            win32clipboard.SetClipboardData(pngFormat, pngBuf.getvalue())
        finally:
            win32clipboard.CloseClipboard()

    def CopyToMAC(self):
        from AppKit import NSPasteboard, NSImage

        buffer = io.BytesIO()
        self.currentPilImage.save(buffer, format="PNG")
        pngBytes = buffer.getvalue()

        nsimage = NSImage.alloc().initWithData_(pngBytes)
        if nsimage is None or not nsimage.isValid():
            raise RuntimeError("Could not build NSImage from PNG bytes")

        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()
        if not pasteboard.writeObjects_([nsimage]):
            raise RuntimeError("Pasteboard refused the image")

    def CopyToLinux(self):
        import subprocess
    
        # Try wl-clipboard first (Wayland)
        buffer = io.BytesIO()
        self.currentPilImage.save(buffer, format='PNG')
        buffer.seek(0)
        
        try:
            # Wayland (wl-paste / wl-copy)
            proc = subprocess.Popen(["wl-copy", "--type", "image/png"], stdin=subprocess.PIPE)
            proc.communicate(buffer.read())
        except FileNotFoundError:
            try:
                # Fallback to xclip (X11)
                proc = subprocess.Popen(["xclip", "-selection", "clipboard", "-t", "image/png"], stdin=subprocess.PIPE)
                proc.communicate(buffer.read())
            except FileNotFoundError:
                raise Exception("Install wl-clipboard or xclip")

    def OnTextChangedEvent(self, *args):
        if not self.livePreview:
            return

        self.QueueQrGeneration()

    def QueueQrGeneration(self):
        if self.updateJob is not None:
            self.tab.after_cancel(self.updateJob)
        self.updateJob = self.tab.after(self.DEBOUNCE_DELAY_MS, self.GenerateCode)

    def EventSliderBlockSize(self, value: int):
        self.selBlockSize = value
        self.blockSizeSliderValue.configure(text=str(int(value)))
        self.QueueQrGeneration()

    def EventSliderBorder(self, value: int):
        self.selBorder = value
        self.borderSliderValue.configure(text=str(int(value)))
        self.QueueQrGeneration()

    def EventEcDropdown(self, option: str):
        self.selEc = option
        self.QueueQrGeneration()

    def EventAdvancedOptions(self):
        if(self.advancedOptionsToggle.get()):
            self.ShowAdvanced(True)
        else:
            self.ShowAdvanced(False)

    def EventLivePreview(self):
        self.livePreview = self.livePreviewToggle.get()

        if(not self.livePreview):
            self.generateCodeButton.configure(state=tk.NORMAL)
        else:
            self.generateCodeButton.configure(state=tk.DISABLED)

        self.QueueQrGeneration()

    def EventSliderVersion(self, value: int):
        self.selLevel = int(value)

        if(value == 0):
            self.versionSliderValue.configure(text="Auto")
        else:
            self.versionSliderValue.configure(text=str(int(value)))
        self.QueueQrGeneration()

    def EventSliderMask(self, value: int):
        self.selMask = int(value)

        if(value == 0):
            self.maskSliderValue.configure(text="Auto")
        else:
            self.maskSliderValue.configure(text=str(int(value) - 1))
        self.QueueQrGeneration()

    def Focus(self, tabview: ct.CTkTabview):
        tabview.set(self.name)