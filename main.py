
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Create main application window
root = Tk()
root.geometry("500x600")
root.title("Advanced Image Encryption Tool")
root.configure(bg="#f0f0f0")

# Global variables
original_image = None
encrypted_image = None
preview_label = None


# Generate encryption key from password
def generate_key(password):
    # Use SHA-256 to generate a 32-byte key from the password
    return hashlib.sha256(password.encode()).digest()


# Pixel-based encryption (alternative method)
def pixel_encrypt_image(image_path, password):
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise Exception("Could not read image file")

        # Generate key from password
        key = generate_key(password)

        # Convert key to integer for pixel manipulation
        key_int = int.from_bytes(key[:4], byteorder='big')  # Use first 4 bytes

        # Get image dimensions
        height, width = img.shape[:2]

        # Create a copy of the image to encrypt
        encrypted_img = img.copy()

        # Encrypt each pixel using XOR with key
        for i in range(height):
            for j in range(width):
                # XOR each color channel with different parts of the key
                encrypted_img[i, j, 0] = img[i, j, 0] ^ ((key_int + i + j) % 256)  # Blue
                encrypted_img[i, j, 1] = img[i, j, 1] ^ ((key_int + i * j) % 256)  # Green
                encrypted_img[i, j, 2] = img[i, j, 2] ^ ((key_int + i - j) % 256)  # Red

        # Save encrypted image
        base_name, ext = os.path.splitext(image_path)
        encrypted_path = base_name + "_pixel_encrypted.png"

        cv2.imwrite(encrypted_path, encrypted_img)

        return encrypted_path, True

    except Exception as e:
        return f"Error: {str(e)}", False


# Pixel-based decryption
def pixel_decrypt_image(encrypted_path, password):
    try:
        # Read encrypted image
        encrypted_img = cv2.imread(encrypted_path)
        if encrypted_img is None:
            raise Exception("Could not read encrypted image file")

        # Generate key from password
        key = generate_key(password)

        # Convert key to integer for pixel manipulation
        key_int = int.from_bytes(key[:4], byteorder='big')  # Use first 4 bytes

        # Get image dimensions
        height, width = encrypted_img.shape[:2]

        # Create a copy of the image to decrypt
        decrypted_img = encrypted_img.copy()

        # Decrypt each pixel using XOR with key (same as encryption)
        for i in range(height):
            for j in range(width):
                # XOR each color channel with different parts of the key
                decrypted_img[i, j, 0] = encrypted_img[i, j, 0] ^ ((key_int + i + j) % 256)  # Blue
                decrypted_img[i, j, 1] = encrypted_img[i, j, 1] ^ ((key_int + i * j) % 256)  # Green
                decrypted_img[i, j, 2] = encrypted_img[i, j, 2] ^ ((key_int + i - j) % 256)  # Red

        # Save decrypted image
        base_name, ext = os.path.splitext(encrypted_path)
        if "_pixel_encrypted" in base_name:
            base_name = base_name.replace("_pixel_encrypted", "")
        decrypted_path = base_name + "_decrypted.png"

        cv2.imwrite(decrypted_path, decrypted_img)

        return decrypted_path, True

    except Exception as e:
        return f"Error: {str(e)}", False


# Function to handle encryption/decryption
def process_image():
    global original_image, encrypted_image

    # Get values from UI
    password = password_entry.get().strip()
    if not password:
        messagebox.showerror("Error", "Please enter a password")
        return

    method = method_var.get()
    operation = operation_var.get()

    # Process based on operation
    if operation == "encrypt":
        file_path = filedialog.askopenfilename(
            filetypes=[('Image Files', '*.jpg *.jpeg *.png *.bmp *.tiff')]
        )
        if not file_path:
            return

        # Show loading
        status_label.config(text="Encrypting...")
        progress['value'] = 0
        root.update_idletasks()

        # Encrypt based on method
        #if method == "aes":
            #result_path, success = encrypt_image(file_path, password)
        #else:  # pixel method
        result_path, success = pixel_encrypt_image(file_path, password)

        if success:
            status_label.config(text=f"Encrypted! Saved as: {os.path.basename(result_path)}")
            # Load and show encrypted image if it's a pixel encryption
            if method == "pixel":
                encrypted_image = cv2.imread(result_path)
                show_image(encrypted_image, "Encrypted Image")
        else:
            messagebox.showerror("Error", result_path)

    else:  # decrypt
        if method == "aes":
            file_types = [('Encrypted Files', '*.aes')]
        else:
            file_types = [('Image Files', '*.png *.jpg *.jpeg *.bmp *.tiff')]

        file_path = filedialog.askopenfilename(filetypes=file_types)
        if not file_path:
            return

        # Show loading
        status_label.config(text="Decrypting...")
        progress['value'] = 0
        root.update_idletasks()

        # Decrypt based on method
        '''if method == "aes":
            result_path, success = decrypt_image(file_path, password)
        else:  # pixel method'''
        result_path, success = pixel_decrypt_image(file_path, password)

        if success:
            status_label.config(text=f"Decrypted! Saved as: {os.path.basename(result_path)}")
            # Load and show decrypted image
            decrypted_image = cv2.imread(result_path)
            show_image(decrypted_image, "Decrypted Image")
        else:
            messagebox.showerror("Error", result_path)

    progress['value'] = 100


# Function to display image in GUI
def show_image(image, title):
    global preview_label

    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert to PIL Image
    pil_image = Image.fromarray(image_rgb)

    # Resize for display
    max_size = (300, 300)
    pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)

    # Convert to PhotoImage for Tkinter
    photo = ImageTk.PhotoImage(pil_image)

    # Create or update label
    if preview_label is None:
        preview_label = Label(image_frame, image=photo)
        preview_label.image = photo  # Keep a reference
        preview_label.pack(pady=10)
    else:
        preview_label.configure(image=photo)
        preview_label.image = photo  # Keep a reference

    # Update title
    image_title.config(text=title)


# Function to load and display original image
def load_original_image():
    global original_image

    file_path = filedialog.askopenfilename(
        filetypes=[('Image Files', '*.jpg *.jpeg *.png *.bmp *.tiff')]
    )
    if not file_path:
        return

    original_image = cv2.imread(file_path)
    if original_image is not None:
        show_image(original_image, "Original Image")
        status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
    else:
        messagebox.showerror("Error", "Could not load image")


# UI Elements
main_frame = Frame(root, bg="#f0f0f0")
main_frame.pack(pady=20)

# Title
title_label = Label(main_frame, text="Advanced Image Encryption Tool",
                    font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Password entry
Label(main_frame, text="Password:", bg="#f0f0f0").grid(row=1, column=0, sticky=E, pady=5)
password_entry = Entry(main_frame, width=30, show="*")
password_entry.grid(row=1, column=1, pady=5, padx=5)

# Method selection
Label(main_frame, text="Encryption Method:", bg="#f0f0f0").grid(row=2, column=0, sticky=E, pady=5)
method_var = StringVar(value="pixel")
method_frame = Frame(main_frame, bg="#f0f0f0")
method_frame.grid(row=2, column=1, pady=5, padx=5, sticky=W)
'''Radiobutton(method_frame, text="AES (Strong)", variable=method_var, value="aes", bg="#f0f0f0").pack(anchor=W)'''
Radiobutton(method_frame, text="Pixel-based (Visual)", variable=method_var, value="pixel", bg="#f0f0f0").pack(anchor=W)

# Operation selection
Label(main_frame, text="Operation:", bg="#f0f0f0").grid(row=3, column=0, sticky=E, pady=5)
operation_var = StringVar(value="encrypt")
operation_frame = Frame(main_frame, bg="#f0f0f0")
operation_frame.grid(row=3, column=1, pady=5, padx=5, sticky=W)
Radiobutton(operation_frame, text="Encrypt", variable=operation_var, value="encrypt", bg="#f0f0f0").pack(anchor=W)
Radiobutton(operation_frame, text="Decrypt", variable=operation_var, value="decrypt", bg="#f0f0f0").pack(anchor=W)

# Buttons
button_frame = Frame(main_frame, bg="#f0f0f0")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)
Button(button_frame, text="Load Image", command=load_original_image, width=12).pack(side=LEFT, padx=5)
Button(button_frame, text="Process", command=process_image, width=12, bg="#4CAF50", fg="white").pack(side=LEFT, padx=5)

# Progress bar
progress = ttk.Progressbar(main_frame, orient=HORIZONTAL, length=300, mode='determinate')
progress.grid(row=5, column=0, columnspan=2, pady=10)

# Status label
status_label = Label(main_frame, text="Ready", bg="#f0f0f0", fg="green")
status_label.grid(row=6, column=0, columnspan=2, pady=5)

# Image preview frame
image_frame = LabelFrame(root, text="Image Preview", padx=10, pady=10)
image_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

# Image title
image_title = Label(image_frame, text="No image loaded", font=("Arial", 10))
image_title.pack(pady=5)

# Information label
info_text = """
Pixel Encryption: Visual encryption, outputs image file

Note: For decryption, you must use the same method and password used for encryption.
"""
info_label = Label(root, text=info_text, justify=LEFT, bg="#f0f0f0", fg="gray")
info_label.pack(pady=10)

# Start the GUI
root.mainloop()


