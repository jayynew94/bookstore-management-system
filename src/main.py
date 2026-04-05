import tkinter as tk
from ui.login_window import LoginApp


def main():
    root = tk.Tk()
    root.title("Bookstore Management System")
    app = LoginApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()