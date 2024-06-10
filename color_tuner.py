import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class color_tuner_app:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Tuner")
        # self.root.attributes('-fullscreen', True)

        # Load the icon
        self.icon = ImageTk.PhotoImage(file="logo.png")
        self.root.iconphoto(True, self.icon)
        

        # Left Frame for the image
        self.left_frame = tk.Frame(root, width=root.winfo_screenwidth() // 2, height=root.winfo_screenheight())
        self.left_frame.grid(row=0, column=0)
        self.left_frame.grid_propagate(False)

        self.default_image = Image.open("logo.png").resize((800, 800))
        self.image_tk = ImageTk.PhotoImage(self.default_image)
        self.image_label = tk.Label(self.left_frame, image=self.image_tk)
        self.image_label.pack(expand=True)

        # self.browse_button = tk.Button(self.left_frame, text="Browse", command=self.browse_image)
        # self.browse_button.pack(side="bottom", fill="x")

        # Right Frame for controls
        self.right_frame = tk.Frame(root, width=root.winfo_screenwidth() // 2, height=root.winfo_screenheight(), bg="lightgrey")
        self.right_frame.grid(row=0, column=1)
        self.right_frame.grid_propagate(False)

        # Browse images Button
        self.browse_button = tk.Button(self.right_frame, text="Browse Image", command=self.browse_image)
        self.browse_button.pack(side="top", fill="x", pady=10)
        
        # Filter input sections
        self.low_hsv_label = tk.Label(self.right_frame, text="Current Low HSV", anchor="w")
        self.low_hsv_label.pack(anchor="w", padx=10, pady=5)
        self.low_hsv_input = tk.Entry(self.right_frame)
        self.low_hsv_input.pack(fill="x", padx=10)

        self.high_hsv_label = tk.Label(self.right_frame, text="Current High HSV", anchor="w")
        self.high_hsv_label.pack(anchor="w", padx=10, pady=5)
        self.high_hsv_input = tk.Entry(self.right_frame)
        self.high_hsv_input.pack(fill="x", padx=10)

        self.color_mask_label = tk.Label(self.right_frame, text="Color Mask", anchor="w")
        self.color_mask_label.pack(anchor="w", padx=10, pady=5)
        self.color_mask_input = tk.Entry(self.right_frame)
        self.color_mask_input.pack(fill="x", padx=10)

        # Add Filters and Browse Filters Buttons in the same row
        self.filters_frame = tk.Frame(self.right_frame, bg="lightgrey")
        self.filters_frame.pack(anchor="w", padx=10, pady=10, fill="x")

        self.add_filters_button = tk.Button(self.filters_frame, text="Add Filters", command=self.add_filters)
        self.add_filters_button.pack(side="left", padx=(0, 10))

        self.browse_filters_button = tk.Button(self.filters_frame, text="Browse Filters", command=self.browse_filters)
        self.browse_filters_button.pack(side="left")

        # Dropdown for filter positions
        self.filter_var = tk.StringVar()
        self.filter_dropdown = ttk.Combobox(self.filters_frame, textvariable=self.filter_var, state="readonly")
        self.filter_dropdown.bind("<<ComboboxSelected>>", self.update_sliders_and_apply)
        self.filter_dropdown.pack(fill="x", padx=(10, 0), expand=True, side="left")

        # Sliders for HSV range
        self.slider_frame = tk.Frame(self.right_frame, bg="lightgrey")
        self.slider_frame.pack(anchor="w", padx=10, pady=10, fill="both", expand=True)

        self.h_low_slider = tk.Scale(self.slider_frame, from_=0, to=179, length=400, orient=tk.HORIZONTAL, label="Hue Low", command=self.on_slider_change)
        self.s_low_slider = tk.Scale(self.slider_frame, from_=0, to=255, length=400, orient=tk.HORIZONTAL, label="Saturation Low", command=self.on_slider_change)
        self.v_low_slider = tk.Scale(self.slider_frame, from_=0, to=255, length=400, orient=tk.HORIZONTAL, label="Value Low", command=self.on_slider_change)
        self.h_high_slider = tk.Scale(self.slider_frame, from_=0, to=179, length=400, orient=tk.HORIZONTAL, label="Hue High", command=self.on_slider_change)
        self.s_high_slider = tk.Scale(self.slider_frame, from_=0, to=255, length=400, orient=tk.HORIZONTAL, label="Saturation High", command=self.on_slider_change)
        self.v_high_slider = tk.Scale(self.slider_frame, from_=0, to=255, length=400, orient=tk.HORIZONTAL, label="Value High", command=self.on_slider_change)

        self.h_low_slider.grid(row=0, column=0, padx=10, pady=5)
        self.s_low_slider.grid(row=1, column=0, padx=10, pady=5)
        self.v_low_slider.grid(row=2, column=0, padx=10, pady=5)
        self.h_high_slider.grid(row=0, column=1, padx=10, pady=5)
        self.s_high_slider.grid(row=1, column=1, padx=10, pady=5)
        self.v_high_slider.grid(row=2, column=1, padx=10, pady=5)

        # Update Filter and Reset Buttons in the same row
        self.buttons_frame = tk.Frame(self.right_frame, bg="lightgrey")
        self.buttons_frame.pack(anchor="w", padx=10, pady=10, fill="x")

        self.update_filter_button = tk.Button(self.buttons_frame, text="Update Filter", command=self.update_filter)
        self.update_filter_button.pack(side="left", padx=(0, 10))

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_image)
        self.reset_button.pack(side="left")

        # Latest HSV values display
        self.latest_values_frame = tk.Frame(self.right_frame, bg="lightgrey")
        self.latest_values_frame.pack(anchor="w", padx=10, pady=10, fill="both", expand=True)

        self.latest_low_hsv_label = tk.Label(self.latest_values_frame, text="Latest Low HSV", anchor="w")
        self.latest_low_hsv_label.pack(anchor="w", padx=10, pady=(5, 2))

        self.latest_low_hsv_text = tk.Entry(self.latest_values_frame, state="readonly", width=60)
        self.latest_low_hsv_text.pack(fill="x", padx=10, pady=(0, 5))

        self.latest_high_hsv_label = tk.Label(self.latest_values_frame, text="Latest High HSV", anchor="w")
        self.latest_high_hsv_label.pack(anchor="w", padx=10, pady=(5, 2))

        self.latest_high_hsv_text = tk.Entry(self.latest_values_frame, state="readonly", width=60)
        self.latest_high_hsv_text.pack(fill="x", padx=10, pady=(0, 5))

        # Apply all filters button
        self.apply_all_button = tk.Button(self.right_frame, text="Apply All Filters", command=self.apply_all_filters)
        self.apply_all_button.pack(side="bottom", pady=(0, 10))

        self.original_image = None
        self.current_image = None
        self.filters = []

        self.updating_slider = False  # Add a flag to indicate when sliders are being updated programmatically

    def browse_image(self):
        global file_path
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.reset_image()

    def reset_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.update_image()


    def update_image(self):
        if self.current_image is not None:
            image_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            image_pil.thumbnail((800, 800))  # Resize image to fit in the frame
            self.image_tk = ImageTk.PhotoImage(image_pil)  # Store as instance variable
            self.image_label.config(image=self.image_tk)
            self.image_label.image = self.image_tk
            self.root.update()  # Update the GUI

    def browse_filters(self):
        # Open the PDF file
        import webbrowser
        webbrowser.open_new("filter.pdf")

    def add_filters(self):
        try:
            low_hsv = eval(self.low_hsv_input.get())
            high_hsv = eval(self.high_hsv_input.get())
            color_mask = eval(self.color_mask_input.get())

            if len(low_hsv) == len(high_hsv) == len(color_mask):
                # Convert color mask to BGR order for OpenCV
                color_mask = [list(reversed(mask)) for mask in color_mask]
                self.filters = list(zip(low_hsv, high_hsv, color_mask))
                filter_positions = [f"Color {i+1}" for i in range(len(self.filters))]
                self.filter_dropdown['values'] = filter_positions

                if filter_positions:
                    self.filter_dropdown.current(0)
                    self.update_sliders_and_apply(None)
        except Exception as e:
            print(f"Error adding filters: {e}")

    def update_sliders_and_apply(self, event):
        self.updating_slider = True  # Set the flag to indicate sliders are being updated
        filter_index = self.filter_dropdown.current()
        if filter_index >= 0:
            low_h, low_s, low_v = self.filters[filter_index][0]
            high_h, high_s, high_v = self.filters[filter_index][1]

            self.h_low_slider.set(low_h)
            self.s_low_slider.set(low_s)
            self.v_low_slider.set(low_v)
            self.h_high_slider.set(high_h)
            self.s_high_slider.set(high_s)
            self.v_high_slider.set(high_v)

            self.apply_filter_with_current_settings()
        self.updating_slider = False  # Reset the flag after sliders are updated

    def on_slider_change(self, event):
        if not self.updating_slider:  # Only apply the filter if not in the middle of updating sliders
            self.apply_filter_with_current_settings()

    def apply_filter_with_current_settings(self):
        if self.original_image is None:
            return

        # Reset to the original image before applying filters
        self.current_image = self.original_image.copy()

        h_low = self.h_low_slider.get()
        h_high = self.h_high_slider.get()
        s_low = self.s_low_slider.get()
        s_high = self.s_high_slider.get()
        v_low = self.v_low_slider.get()
        v_high = self.v_high_slider.get()

        hsv_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2HSV)
        lower_color = np.array([h_low, s_low, v_low])
        upper_color = np.array([h_high, s_high, v_high])

        mask = cv2.inRange(hsv_image, lower_color, upper_color)
        filtered = self.current_image.copy()
        color_mask = self.filters[self.filter_dropdown.current()][2]
        filtered[mask > 0] = color_mask

        self.current_image = filtered
        self.update_image()

    def update_filter(self):
        filter_index = self.filter_dropdown.current()
        if filter_index >= 0:
            low_h = self.h_low_slider.get()
            low_s = self.s_low_slider.get()
            low_v = self.v_low_slider.get()
            high_h = self.h_high_slider.get()
            high_s = self.s_high_slider.get()
            high_v = self.v_high_slider.get()

            self.filters[filter_index] = ([low_h, low_s, low_v], [high_h, high_s, high_v], self.filters[filter_index][2])

            self.latest_low_hsv_values = [list(f[0]) for f in self.filters]
            self.latest_high_hsv_values = [list(f[1]) for f in self.filters]

            self.update_text_widget(self.latest_low_hsv_text, self.latest_low_hsv_values)
            self.update_text_widget(self.latest_high_hsv_text, self.latest_high_hsv_values)

    def update_text_widget(self, text_widget, values):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(0, tk.END)
        formatted_values = ", ".join(str(val) for val in values)
        text_widget.insert(0, formatted_values)
        text_widget.config(state=tk.NORMAL)

    def apply_all_filters(self):
        if self.original_image is None:
            return

        image_copy = self.original_image.copy()

        for low_hsv, high_hsv, color_mask in self.filters:
            hsv_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2HSV)
            lower_color = np.array(low_hsv)
            upper_color = np.array(high_hsv)
            mask = cv2.inRange(hsv_image, lower_color, upper_color)
            image_copy[mask > 0] = color_mask

        self.show_filtered_image(image_copy)

    def show_filtered_image(self, image):
        filtered_image_window = tk.Toplevel(self.root)
        filtered_image_window.title("Filtered Image")

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil.thumbnail((800, 800))
        image_tk = ImageTk.PhotoImage(image_pil)

        label = tk.Label(filtered_image_window, image=image_tk)
        label.image = image_tk
        label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = color_tuner_app(root)
    root.mainloop()
