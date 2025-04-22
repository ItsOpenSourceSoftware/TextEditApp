import tkinter as tk
from tkinter import filedialog, messagebox
import os

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.root.geometry("800x600")

        self.filename = None

        # Create the Text widget with undo functionality enabled
        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Create a scrollbar and attach it to the text area
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_editor)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Bind keyboard shortcuts
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-S>", lambda event: self.save_as())

        # Track text modification (for prompting save on exit)
        self.text_area.edit_modified(False)

    def new_file(self):
        if self.prompt_save_changes():
            self.text_area.delete(1.0, tk.END)
            self.filename = None
            self.root.title("Simple Text Editor - New File")
            self.text_area.edit_modified(False)

    def open_file(self):
        if self.prompt_save_changes():
            file_path = filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        contents = f.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, contents)
                    self.filename = file_path
                    self.root.title(f"Simple Text Editor - {os.path.basename(file_path)}")
                    self.text_area.edit_modified(False)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open file:\n{e}")

    def save_file(self):
        if self.filename:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.filename, "w", encoding="utf-8") as f:
                    f.write(content)
                self.root.title(f"Simple Text Editor - {os.path.basename(self.filename)}")
                self.text_area.edit_modified(False)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.filename = file_path
            self.save_file()

    def exit_editor(self):
        if self.prompt_save_changes():
            self.root.destroy()

    def prompt_save_changes(self):
        """If there are unsaved changes, prompt the user before proceeding."""
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes?")
            if response:  # Yes, so save before proceeding
                self.save_file()
                # Return True only if save was successful (or not needed)
                return True
            elif response is None:  # Cancel; do not proceed
                return False
            else:  # No need to save
                return True
        return True

if __name__ == '__main__':
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
