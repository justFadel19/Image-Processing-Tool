import tkinter as tk
from tkinter import ttk, filedialog, Toplevel, Label, messagebox
from PIL import Image, ImageTk
from processing.color import convert_to_grayscale
from processing.threshold import calculate_threshold
from processing.halftone import simple_halftone, error_diffusion_halftoning
from processing.histogram import show_histogram, histogram_equalization
from processing.simple_edge_detection import apply_sobel, apply_prewitt, apply_kirsch
from processing.advanced_edge_detection import ( homogeneity_operator, difference_operator, difference_of_gaussians, 
                                                    contrast_based_edge_detection, variance_operator, range_operator )
from processing.filtering import apply_highpass, apply_lowpass, apply_median
from processing.image_operations import invert_image, add_image_and_copy, subtract_image_and_copy
from processing.utils import reset_image

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Tool")
        
        # Set gray theme colors
        bg_color = "#E8E8E8"  # Light gray for background
        button_color = "#D0D0D0"  # Slightly darker gray for buttons
        frame_color = "#F0F0F0"  # Very light gray for frames
        
        # Configure root background
        self.root.configure(bg=bg_color)
        
        # Configure style for buttons and frames
        style = ttk.Style()
        style.configure('TButton', background=button_color)
        style.configure('TFrame', background=frame_color)
        style.configure('TLabelframe', background=frame_color)
        style.configure('TLabelframe.Label', background=frame_color)
        
        self.setup_window()
        self.create_menu()
        self.create_frames()
        self.create_buttons()
        self.create_status_bar()
        self.initialize_variables()

    def setup_window(self):
        self.root.geometry("1400x900")
        # Make the window resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.load_image)
        file_menu.add_command(label="Save Processed Image", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Theory", command=self.show_theory)

    def create_frames(self):
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.grid(row=0, column=0, sticky="nsew")

        # Left sidebar for buttons
        self.buttons_frame = ttk.Frame(main_container)
        self.buttons_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        
        # Right frame for images
        self.image_frame = ttk.Frame(main_container)
        self.image_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Configure weights for resizing
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # Create frames for original and processed images
        self.create_image_frames()

    def create_image_frames(self):
        # Frame for original image
        self.original_frame = ttk.Label(self.image_frame, relief="solid", borderwidth=1)
        self.original_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Frame for processed image
        self.processed_frame = ttk.Label(self.image_frame, relief="solid", borderwidth=1)
        self.processed_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Configure grid weights for image frames
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(1, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)

    def create_buttons(self):
        # Main control buttons
        control_frame = ttk.Frame(self.buttons_frame)
        control_frame.grid(row=0, column=0, pady=5, sticky="ew")

        self.upload_button = ttk.Button(
            control_frame, text="Open Image", command=self.load_image
        )
        self.upload_button.grid(row=0, column=0, padx=2, pady=2)

        self.save_button = ttk.Button(
            control_frame, text="Save Image", command=self.save_image, 
            state=tk.DISABLED
        )
        self.save_button.grid(row=0, column=1, padx=2, pady=2)

        self.reset_button = ttk.Button(
            control_frame, text="Reset", command=self.reset_image,
            state=tk.DISABLED
        )
        self.reset_button.grid(row=0, column=2, padx=2, pady=2)

        # Basic operations
        row = 1
        basic_ops = [
            ("Grayscale", convert_to_grayscale),
            ("Threshold", calculate_threshold),
            ("Simple Halftone", simple_halftone),
            ("Advanced Halftone", error_diffusion_halftoning),
            ("Histogram", show_histogram),
            ("Histogram Equalization", histogram_equalization)
        ]

        for text, func in basic_ops:
            btn = ttk.Button(
                self.buttons_frame, text=text,
                command=lambda f=func: self.process_image(f),
                state=tk.DISABLED
            )
            btn.grid(row=row, column=0, padx=5, pady=2, sticky="ew")
            row += 1

        # Edge Detection Menu
        edge_frame = ttk.LabelFrame(self.buttons_frame, text="Edge Detection")
        edge_frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        row += 1

        edge_ops = [
            ("Sobel", apply_sobel),
            ("Prewitt", apply_prewitt),
            ("Kirsch", apply_kirsch)
        ]

        for i, (text, func) in enumerate(edge_ops):
            btn = ttk.Button(
                edge_frame, text=text,
                command=lambda f=func: self.process_image(f),
                state=tk.DISABLED
            )
            btn.grid(row=0, column=i, padx=2, pady=2)

        # Advanced Edge Detection Menu
        advanced_edge_frame = ttk.LabelFrame(self.buttons_frame, text="Advanced Edge Detection")
        advanced_edge_frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        row += 1

        advanced_edge_ops = [
            ("Homogeneity", homogeneity_operator),
            ("Difference", difference_operator),
            ("DoG", difference_of_gaussians),
            ("Contrast", contrast_based_edge_detection),
            ("Variance", variance_operator),
            ("Range", range_operator)
        ]

        # Loop to create buttons and arrange them in a 2x3 grid
        for i, (text, func) in enumerate(advanced_edge_ops):
            btn = ttk.Button(
                advanced_edge_frame, text=text,
                command=lambda f=func: self.process_image(f),
                state=tk.DISABLED
            )
            
            # Determine the row and column for the grid
            row_position = i // 3  # Integer division for rows (0, 1, 2)
            col_position = i % 3   # Modulo for columns (0, 1, 2)
            
            btn.grid(row=row_position, column=col_position, padx=2, pady=2)



        # Filtering Menu
        filter_frame = ttk.LabelFrame(self.buttons_frame, text="Filtering")
        filter_frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        row += 1

        filter_ops = [
            ("High Pass", apply_highpass),
            ("Low Pass", apply_lowpass),
            ("Median", apply_median)
        ]

        for i, (text, func) in enumerate(filter_ops):
            btn = ttk.Button(
                filter_frame, text=text,
                command=lambda f=func: self.process_image(f),
                state=tk.DISABLED
            )
            btn.grid(row=0, column=i, padx=2, pady=2)

        # Image Operations Menu
        img_ops_frame = ttk.LabelFrame(self.buttons_frame, text="Image Operations")
        img_ops_frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        row += 1

        img_ops = [
            ("Invert", invert_image),
            ("Add & Copy", add_image_and_copy),
            ("Sub & Copy", subtract_image_and_copy)
        ]

        for i, (text, func) in enumerate(img_ops):
            btn = ttk.Button(
                img_ops_frame, text=text,
                command=lambda f=func: self.process_image(f),
                state=tk.DISABLED
            )
            btn.grid(row=0, column=i, padx=2, pady=2)

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self.root, textvariable=self.status_var, relief="sunken", padding=(5, 2)
        )
        status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    def initialize_variables(self):
        self.image = None
        self.original_image = None
        self.processed_image = None
        self.theory_answers = []

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    self.processed_image.save(file_path)
                    self.status_var.set(f"Image saved to {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {str(e)}")

    def show_about(self):
        about_text = """Image Processing Tool
Version 1.0

A comprehensive tool for image processing operations including:
- Basic image operations
- Edge detection
- Filtering
- Advanced processing

Created for educational purposes."""

        messagebox.showinfo("About", about_text)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        
        if file_path:
            try:
                self.image = Image.open(file_path)
                self.original_image = self.image.copy()
                self.processed_image = self.image.copy()
                
                # Display both original and processed images
                self.display_image(self.original_image, self.original_frame)
                self.display_image(self.processed_image, self.processed_frame)
                
                # Enable operation buttons
                self.enable_buttons()
                
                self.status_var.set("Image loaded successfully")
            except Exception as e:
                self.status_var.set(f"Error loading image: {str(e)}")
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def display_image(self, img, frame):
        # Calculate scaling factor to fit in frame
        display_size = (400, 300)
        img.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Convert image for display
        tk_image = ImageTk.PhotoImage(img)
        frame.config(image=tk_image)
        frame.image = tk_image  # Keep a reference

    def reset_image(self):
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.display_image(self.processed_image, self.processed_frame)
            self.status_var.set("Image reset to original")

    def enable_buttons(self):
        # Enable buttons in the buttons frame
        for widget in self.buttons_frame.winfo_children():
            if isinstance(widget, ttk.Frame):  # For the control frame
                for button in widget.winfo_children():
                    if isinstance(button, ttk.Button):
                        button.config(state=tk.NORMAL)
            elif isinstance(widget, ttk.Button):  # For operation buttons
                widget.config(state=tk.NORMAL)
            elif isinstance(widget, ttk.LabelFrame):  # For menus
                for button in widget.winfo_children():
                    if isinstance(button, ttk.Button):
                        button.config(state=tk.NORMAL)

    def process_image(self, operation):
        if self.processed_image:
            try:
                self.status_var.set(f"Processing image...")
                self.root.update()
                
                result = operation(self.processed_image)
                
                if isinstance(result, Image.Image):
                    self.processed_image = result
                    self.display_image(self.processed_image, self.processed_frame)
                    self.status_var.set("Processing complete")
                else:
                    self.status_var.set("Operation complete")
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")

    def show_theory(self):
        if not self.theory_answers:
            messagebox.showinfo("Theory", "No theory content available yet.")
            return
            
        theory_window = Toplevel(self.root)
        theory_window.title("Image Processing Theory")
        theory_window.geometry("600x400")
        
        # Create a scrolled text widget
        text_widget = tk.Text(theory_window, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(theory_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        scrollbar.pack(side="right", fill="y")
        text_widget.pack(side="left", fill="both", expand=True)
        
        # Insert theory content
        for answer in self.theory_answers:
            text_widget.insert(tk.END, answer + "\n\n")
        text_widget.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
