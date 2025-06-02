import customtkinter as ctk
from ..backend.backend import Backend, audio_driver_types


class Frontend:
    """
    The Frontend class
    """

    def __init__(self):
        """
        Initialize the Frontend class
        """
        self.backend = Backend()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        self.root.title("Recommender System")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.current_tmp_file = None
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
        self.label = ctk.CTkLabel(
            self.root,
            text="Welcome to the Recommender System",
        )
        self.label.pack(pady=20)

        self.driver_label = ctk.CTkLabel(
            self.root,
            text="Select Audio Driver:",
        )
        self.driver_label.pack(pady=10)
        self.driver_dropdown = ctk.CTkOptionMenu(
            self.root,
            values=["mic", "file", "browser"],
            command=self.set_audio_driver,
        )
        self.driver_dropdown.pack(pady=10)

        self.source_label = ctk.CTkLabel(
            self.root,
            text="Select Audio Source:",
        )
        self.source_label.pack(pady=10)
        self.source_dropdown = ctk.CTkOptionMenu(
            self.root,
            values=self.backend.list_audio_sources(),
            command=self.backend.set_audio_source,
        )
        self.source_dropdown.pack(pady=10)

        self.extract_single_button = ctk.CTkButton(
            self.root,
            text="Extract Single Audio",
            command=self.extract_single,
        )
        self.extract_single_button.pack(pady=20)

        self.current_tmp_file_label = ctk.CTkLabel(
            self.root,
            text="Current Temporary File: None",
        )
        self.current_tmp_file_label.pack(pady=10)

        self.send_single_button = ctk.CTkButton(
            self.root,
            text="Send Single Request",
            command=self.send_single_request,
        )
        self.send_single_button.pack(pady=20)
        self.response_label = ctk.CTkLabel(
            self.root,
            text="Response: None",
        )
        self.response_label.pack(pady=10)

    def set_audio_driver(self, audio_driver_type: audio_driver_types):
        """
        Set the audio driver for the backend
        :param audio_driver_type: Type of the audio driver
        """
        self.backend._set_audio_driver(audio_driver_type)
        self.source_dropdown.configure(values=self.backend.list_audio_sources())

    def extract_single(self):
        """
        Extract a single audio file and update the current temporary file
        """
        self.current_tmp_file = self.backend.extract_single()
        print(f"Extracted audio file: {self.current_tmp_file}")
        self.current_tmp_file_label.configure(
            text=f"Current Temporary File: {self.current_tmp_file}"
        )

    def send_single_request(self):
        """
        Send a single audio file to the backend API server and update the response
        """
        if self.current_tmp_file:
            response = self.backend.send_single_request(self.current_tmp_file)
            self.response_label.configure(text=f"Response: {response}")
        else:
            self.response_label.configure(text="No audio file to send.")
