import customtkinter as ctk


class Frontend:
    """
    The Frontend class
    """

    def __init__(self):
        """
        Initialize the Frontend class
        """
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
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
        self.label = ctk.CTkLabel(self.root, text="Welcome to the Recommender System")
        self.label.pack(pady=20)
