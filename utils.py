import customtkinter as ctk

def create_property_entry(parent, label_text, var):
    ctk.CTkLabel(parent, text=label_text).pack()
    entry = ctk.CTkEntry(parent, textvariable=var)
    entry.pack()
    return entry
