import tkinter


class LobbyMenuFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#000000")
