# main.py
import tkinter as tk
from gui import DiaryApp

if __name__ == "__main__":
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()