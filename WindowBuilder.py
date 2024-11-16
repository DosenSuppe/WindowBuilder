import customtkinter as ctk
from tkinter import StringVar, IntVar
from DraggableWindow import DraggableWindow
from utils import create_property_entry

class WindowBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Window Builder")
        self.geometry("1000x600")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill='both')

        self.left_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.left_frame.pack(side='left', fill='y')

        self.element_label = ctk.CTkLabel(self.left_frame, text="Elements")
        self.element_label.pack(pady=10)

        self.add_label_button = ctk.CTkButton(self.left_frame, text="Add Label", command=self.add_label)
        self.add_label_button.pack(pady=5)

        self.add_button_button = ctk.CTkButton(self.left_frame, text="Add Button", command=self.add_button)
        self.add_button_button.pack(pady=5)

        self.add_entry_button = ctk.CTkButton(self.left_frame, text="Add Entry", command=self.add_entry)
        self.add_entry_button.pack(pady=5)

        self.create_window_button = ctk.CTkButton(self.left_frame, text="Create Window", command=self.add_editor_window)
        self.create_window_button.pack(pady=5)
        self.create_window_button.pack_forget()  # Initially hide this button

        self.right_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.right_frame.pack(side='right', fill='y')

        self.property_label = ctk.CTkLabel(self.right_frame, text="Properties")
        self.property_label.pack(pady=10)

        self.window_title_var = StringVar(value="Editor Window")
        self.create_window_title_entry()

        self.properties = {}
        self.selected_element = None
        self.selection_frame = None

        self.editor_windows = []
        self.bind("<Configure>", lambda e: self.lift_editor_windows())
        self.add_editor_window()

    def create_window_title_entry(self):
        create_property_entry(self.right_frame, "Window Title:", self.window_title_var)
        self.window_title_var.trace_add("write", self.update_window_titles)

    def update_window_titles(self, *args):
        for window in self.editor_windows:
            if window.winfo_exists():
                window.set_title(self.window_title_var.get())

    def add_editor_window(self):
        editor_window = DraggableWindow(self)
        self.editor_windows.append(editor_window)
        editor_window.protocol("WM_DELETE_WINDOW", lambda win=editor_window: self.close_editor_window(win))

        # Show UI elements and hide the "Create Window" button
        self.show_ui_elements()
        self.create_window_button.pack_forget()

    def deselect_element(self, event=None):
        if self.selection_frame:
            self.selection_frame.destroy()
        if self.selected_element:
            self.selected_element.unbind("<B1-Motion>")
        self.selected_element = None
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.property_label = ctk.CTkLabel(self.right_frame, text="Properties")
        self.property_label.pack(pady=10)
        self.create_window_title_entry()

    def close_editor_window(self, win):
        if win in self.editor_windows:
            self.editor_windows.remove(win)
        win.destroy()

        # Hide UI elements and show the "Create Window" button
        self.hide_ui_elements()
        self.create_window_button.pack(pady=5)

    def lift_editor_windows(self):
        for win in self.editor_windows:
            if win.winfo_exists():
                win.lift()

    def update(self):
        super().update()
        self.lift_editor_windows()

    def add_label(self):
        label = ctk.CTkLabel(self.editor_windows[0], text="New Label")
        label.pack(padx=10, pady=10)
        label.bind("<Button-1>", lambda e: self.try_select_element(label))

    def add_button(self):
        button = ctk.CTkButton(self.editor_windows[0], text="New Button")
        button.pack(padx=10, pady=10)
        button.bind("<Button-1>", lambda e: self.try_select_element(button))

    def add_entry(self):
        entry = ctk.CTkEntry(self.editor_windows[0])
        entry.pack(padx=10, pady=10)
        entry.bind("<Button-1>", lambda e: self.try_select_element(entry))

    def try_select_element(self, element):
        self.after(1, lambda: self.select_element(element))

    def select_element(self, element):
        self.deselect_element()
        self.selected_element = element

        # Create a frame around the selected element with specific width and height
        self.selection_frame = ctk.CTkFrame(
            self.editor_windows[0], width=element.winfo_width() + 8, height=element.winfo_height() + 8,
            border_color="blue", border_width=2
        )
        self.selection_frame.place(x=element.winfo_x() - 4, y=element.winfo_y() - 4)
        element.lift()

        self.selected_element.bind("<B1-Motion>", self.on_drag)

        self.update_properties()

    def on_drag(self, event):
        x = self.selected_element.winfo_pointerx() - self.editor_windows[0].winfo_rootx() - self.selected_element.winfo_width() // 2
        y = self.selected_element.winfo_pointery() - self.editor_windows[0].winfo_rooty() - self.selected_element.winfo_height() // 2
        self.selected_element.place(x=x, y=y)
        self.selection_frame.place(x=x - 4, y=y - 4)

        self.update_property_vars(x, y, self.selected_element.winfo_width(), self.selected_element.winfo_height())

    def update_property_vars(self, x, y, width, height):
        self.x_var.set(x)
        self.y_var.set(y)
        self.width_var.set(width)
        self.height_var.set(height)
        self.selection_frame.configure(width=width + 8, height=height + 8)

    def update_properties(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        self.property_label = ctk.CTkLabel(self.right_frame, text="Properties")
        self.property_label.pack(pady=10)

        self.x_var = IntVar(value=self.selected_element.winfo_x())
        self.y_var = IntVar(value=self.selected_element.winfo_y())
        self.width_var = IntVar(value=self.selected_element.winfo_width())
        self.height_var = IntVar(value=self.selected_element.winfo_height())
        self.text_var = StringVar(value=self.selected_element.cget("text") if isinstance(self.selected_element, (ctk.CTkLabel, ctk.CTkButton)) else "")

        def on_change(*args):
            if self.selected_element:
                self.selected_element.place(x=self.x_var.get(), y=self.y_var.get())
                self.selection_frame.place(x=self.x_var.get() - 4, y=self.y_var.get() - 4)
                self.selected_element.configure(width=self.width_var.get(), height=self.height_var.get())
                self.selection_frame.configure(width=self.width_var.get() + 8, height=self.height_var.get() + 8)

                if isinstance(self.selected_element, (ctk.CTkLabel, ctk.CTkButton)) and self.text_var.get() is not None:
                    self.selected_element.configure(text=self.text_var.get())

        self.x_var.trace_add("write", on_change)
        self.y_var.trace_add("write", on_change)
        self.width_var.trace_add("write", on_change)
        self.height_var.trace_add("write", on_change)

        if isinstance(self.selected_element, (ctk.CTkLabel, ctk.CTkButton)):
            self.text_var.trace_add("write", on_change)

        create_property_entry(self.right_frame, "X Position:", self.x_var)
        create_property_entry(self.right_frame, "Y Position:", self.y_var)
        create_property_entry(self.right_frame, "Width:", self.width_var)
        create_property_entry(self.right_frame, "Height:", self.height_var)

        if isinstance(self.selected_element, ctk.CTkLabel) or isinstance(self.selected_element, ctk.CTkButton):
            create_property_entry(self.right_frame, "Text:", self.text_var)

    def show_ui_elements(self):
        self.add_label_button.pack(pady=5)
        self.add_button_button.pack(pady=5)
        self.add_entry_button.pack(pady=5)
        self.element_label.pack(pady=10)

    def hide_ui_elements(self):
        self.add_label_button.pack_forget()
        self.add_button_button.pack_forget()
        self.add_entry_button.pack_forget()
        self.element_label.pack_forget()
