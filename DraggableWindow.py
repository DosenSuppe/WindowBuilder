import customtkinter as ctk

class DraggableWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Editor Window")
        self.geometry("400x300")
        self.bind_click_event()
    
    def set_title(self, new_title):
        self.title(new_title)
    
    def bind_click_event(self):
        self.bind("<Button-1>", self.on_click)
    
    def on_click(self, event):
        self.parent.deselect_element()
