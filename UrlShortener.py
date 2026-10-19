import requests
import validators
import pyperclip
import customtkinter as ct

class UrlShortener():
    name: str = ""
    tab: ct.CTkFrame = None
    textInput: ct.CTkEntry = None
    providerDropdown: ct.CTkComboBox = None
    shortenUrlButton: ct.CTkButton = None
    previewLink: ct.CTkLabel = None

    right: ct.CTkFrame = None
    messageText: ct.CTkLabel = None

    providerOptions = ["TinyURL"]
    selProvider = providerOptions[0]

    inputTextVar: ct.StringVar = None
    inputText: str = ""

    shortenedURL: str = ""

    providerToURL = {providerOptions[0] : "https://tinyurl.com/api-create.php"}

    def __init__(self, tabview: ct.CTkTabview, name: str, size: tuple[int]):
        self.tab = tabview.add(name)
        self.DrawUI(size)
        self.SetOptions()
        self.name = name

    def DrawUI(self, size: tuple[int]):
        self.inputTextVar = ct.StringVar()

        # Split into 2 columns
        self.tab.columnconfigure(0, weight=1)
        self.tab.columnconfigure(1, weight=1)
        self.tab.rowconfigure(1, weight=1)

        # Title
        title = ct.CTkLabel(master=self.tab, text=self.name, font=("ArialBold", 20))
        title.grid(row=0, column=0, columnspan=2, pady=(5, 5))

        # Left panel
        left = ct.CTkFrame(self.tab)
        left.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        # Options title
        leftTitle = ct.CTkLabel(master=left, text="Options", font=("Arial", 18))
        leftTitle.pack(pady=(5, 0), anchor="nw")

        # Input for shortener
        self.textInput = ct.CTkEntry(master=left, placeholder_text="Enter URL...", width=(size[0] / 2) - 50, height=30, textvariable=self.inputTextVar)
        self.textInput.pack(pady=(0, 0), anchor="nw")
        self.textInput.bind("<Return>", self.EventEnterPressed)

        # Generate button
        self.shortenUrlButton = ct.CTkButton(master=left, text="Shorten URL", command=self.EventShortenURL)
        self.shortenUrlButton.pack(pady=(10, 0), anchor="nw")
        
        # Shortener provider
        self.providerDropdown = ct.CTkComboBox(master=left, values=self.providerOptions, command=self.EventProviderDropdown)
        self.providerDropdown.pack(pady=(10, 0), anchor="nw")

        # Right panel
        self.right = ct.CTkFrame(self.tab)
        self.right.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.right.grid_columnconfigure(0, weight=1)

        # Preview title
        previewTitle = ct.CTkLabel(master=self.right, text="Preview", font=("Arial", 18))
        previewTitle.pack(pady=(10, 10), anchor="n")

        # Preview link
        self.previewLink = ct.CTkLabel(master=self.right, text="Shorten URL to see it here...", font=("Arial", 16))
        self.previewLink.pack(pady=(5, 0), anchor="n")

        # Copy to clipboard button
        cpToCpButton = ct.CTkButton(master=self.right, text="Copy to clipboard", command=self.EventCopyToClipboard, width=150)
        cpToCpButton.pack(pady=(10, 0), anchor="n")

        # Message text
        self.messageText = ct.CTkLabel(master=self.right, text="", font=("Arial", 16), justify="left", wraplength=350)
        self.messageText.pack(pady=(5, 0), anchor="n")

    def EventEnterPressed(self, *args):
        self.EventShortenURL()

    def EventShortenURL(self):
        longURL = self.inputText
        shortURL = ""

        if not longURL.startswith(("http://", "https://")):
            longURL = "https://" + longURL
    
        if validators.url(longURL):
            if self.URLExists(longURL):
                self.ShowMessage("green", "Valid URL. Shortening...", "")
            else:
                self.ShowMessage("red", "URL is not valid or it can not be reached:", "Check URL and try again")
                return
        else:
            self.ShowMessage("red", "Invalid URL:", "Check URL and try again")
            return
    
        response = requests.get(self.providerToURL.get(self.selProvider), params={"url": longURL})
    
        if response.status_code == 200:
            shortURL = response.text
            self.previewLink.configure(text=shortURL)
            self.HideMessage()
        else:
            self.ShowMessage("red", "Something went wrong: ", f"{response.status_code}")

        self.shortenedURL = shortURL

    def URLExists(self, url: str):
        headers = {'User-Agent': 'Mozilla/5.0 (compatible)'}
        try:
            response = requests.head(url, allow_redirects=True, timeout=5, headers=headers)

            if response.status_code == 405:
                response = requests.get(url, allow_redirects=True, timeout=5, headers=headers)

            if 200 <= response.status_code < 400:
                return True
            else:
                return False

        except requests.RequestException as e:
            self.ShowMessage("red", "Request Exception:", f"{e}")
            return False

    def ShowMessage(self, color: str, reason:str, text: str):
        self.messageText.configure(text=f"{reason}\n{text}", text_color=color)
        print(reason, "\n", text) 

    def HideMessage(self):
        self.messageText.configure(text="")

    def SetOptions(self):
        self.inputTextVar.trace_add('write', self.OnTextChangedEvent)
              
    def OnTextChangedEvent(self, *args):
        self.shortenedURL = ""
        self.previewLink.configure(text="Shorten URL to see it here...")
        self.inputText = self.textInput.get().strip()
  
    def EventProviderDropdown(self, option: str):
        self.selProvider = option

    def EventCopyToClipboard(self):
        if(self.shortenedURL != ""):
            pyperclip.copy(self.shortenedURL)
        else:
            self.ShowMessage("red", "No URL to copy:", "Shorten URL first to copy it to clipboard")

    def Focus(self, tabview: ct.CTkTabview):
        tabview.set(self.name)