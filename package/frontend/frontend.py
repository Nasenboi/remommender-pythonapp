import tkinter as tk


class Frontend:
    """
    The Frontend class
    """

    def __init__(self):
        """
        Initialize the Frontend class
        """
        self.root = tk.Tk()
        self.root.title("Recommender System")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.create_widgets()

    def mainloop(self):
        """
        Start the main loop of the frontend
        """
        self.root.mainloop()

    def create_widgets(self):
        """
        Create the widgets for the frontend
        """
        self.label = tk.Label(
            self.root, text="Welcome to the Recommender System", font=("Arial", 24)
        )
        self.label.pack(pady=20)
