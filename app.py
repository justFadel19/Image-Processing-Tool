from tkinter import Tk, Button, Label, filedialog, Frame
from PIL import Image, ImageTk
from processing.histogram import apply_histogram, apply_histogram_equalization
from processing.color import convert_to_grayscale
from processing.threshold import apply_threshold
from processing.simple_edge_detection import edge_detection as simple_edge_detection
from processing.utils import reset_image
from processing.halftone import apply_halftone

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Project")
        self.root.geometry("800x600")  # Set the window size
        self.root.configure(bg="#2C3E50")  # Change window background color

        self.image = None
        self.original_image = None
        self.display_image = None

        # Frame for the image
        self.image_frame = Frame(root, bg="#34495E", bd=2, relief="groove")
        self.image_frame.place(x=50, y=50, width=500, height=400)

        self.image_label = Label(self.image_frame, bg="#34495E")
        self.image_label.pack(expand=True, fill="both")

        # Frame for the buttons
        self.button_frame = Frame(root, bg="#1ABC9C")
        self.button_frame.place(x=580, y=0, width=210, height=3000)

        # Upload image button
        self.upload_btn = Button(self.button_frame, text="Upload Image", command=self.upload_image,
                                 bg="#E74C3C", fg="white", font=("Arial", 12, "bold"))
        self.upload_btn.pack(pady=5, fill="x")

        # Operation buttons
        self.grayscale_btn = Button(self.button_frame, text="Grayscale", command=self.convert_to_grayscale,
                                    bg="#3498DB", fg="white", font=("Arial", 12))
        self.grayscale_btn.pack(pady=5, fill="x")

        self.threshold_btn = Button(self.button_frame, text="Threshold", command=self.apply_threshold,
                                    bg="#3498DB", fg="white", font=("Arial", 12))
        self.threshold_btn.pack(pady=5, fill="x")

        self.histogram_btn = Button(self.button_frame, text="Histogram", command=self.apply_histogram,
                                    bg="#3498DB", fg="white", font=("Arial", 12))
        self.histogram_btn.pack(pady=5, fill="x")

        self.hist_eq_btn = Button(self.button_frame, text="Histogram Equalization", command=self.histogram_equalization,
                                  bg="#3498DB", fg="white", font=("Arial", 12))
        self.hist_eq_btn.pack(pady=5, fill="x")

        self.halftone_btn = Button(self.button_frame, text="Halftone", command=self.apply_halftone,
                                   bg="#3498DB", fg="white", font=("Arial", 12))
        self.halftone_btn.pack(pady=5, fill="x")

        # Edge Detection buttons
        self.edge_detection_btn = Button(self.button_frame, text="Edge Detection (Sobel)",
                                         command=lambda: self.edge_detection(method="sobel"),
                                         bg="#9B59B6", fg="white", font=("Arial", 12))
        self.edge_detection_btn.pack(pady=5, fill="x")

        self.prewitt_btn = Button(self.button_frame, text="Edge Detection (Prewitt)",
                                  command=lambda: self.edge_detection(method="prewitt"),
                                  bg="#9B59B6", fg="white", font=("Arial", 12))
        self.prewitt_btn.pack(pady=5, fill="x")

        self.kirsch_btn = Button(self.button_frame, text="Edge Detection (Kirsch)",
                                 command=lambda: self.edge_detection(method="kirsch"),
                                 bg="#9B59B6", fg="white", font=("Arial", 12))
        self.kirsch_btn.pack(pady=5, fill="x")
        
        self.reset_btn = Button(self.button_frame, text="Reset Image", command=self.reset_image,
                                bg="#F1C40F", fg="black", font=("Arial", 12))
        self.reset_btn.pack(pady=5, fill="x")

    def upload_image(self):
        # Upload image
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.original_image = self.image.copy()  # Save a copy of the original image

            # Set the maximum image size (width × height)
            max_width, max_height = 500, 500  # You can adjust the size as needed

            # Resize the image to not exceed the specified size while maintaining the aspect ratio
            self.image.thumbnail((max_width, max_height))  # Resize while keeping the aspect ratio

            # Display the thumbnail image
            self.display_image = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.display_image)

    def convert_to_grayscale(self):
        if self.image:
            self.image = convert_to_grayscale(self.image)
            self.display_image = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.display_image)

    def apply_threshold(self):
        if self.image:
            self.image = apply_threshold(self.image)
            self.display_image = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.display_image)

    def apply_histogram(self):
        if self.image:
            apply_histogram(self.image)

    def histogram_equalization(self):
        if self.image:
            self.image = apply_histogram_equalization(self.image)
            self.display_image = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.display_image)

    def apply_halftone(self):
        if self.image:
            try:
                self.image = apply_halftone(self.image)
                self.display_image = ImageTk.PhotoImage(self.image)
                self.image_label.config(image=self.display_image)
            except Exception as e:
                print(f"Failed to apply halftone: {str(e)}")
        else:
            print("Please upload an image first")

    def reset_image(self):
        if hasattr(self, 'original_image') and self.original_image:
            self.image = reset_image(self.original_image)
            
            # Resize the image to fit the display area
            max_width, max_height = 500, 500
            self.image.thumbnail((max_width, max_height))
            
            self.display_image = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.display_image)

    def edge_detection(self, method="sobel"):
        if self.image:
            self.image = simple_edge_detection(self.image, method)
            self.display_image = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.display_image)

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
