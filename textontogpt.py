import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import pyperclip  # To interact with the clipboard

# Function to split the text into chunks by characters and create a cluster for the remainder
def split_into_chunks_and_cluster_by_chars(text, chars_per_chunk=10000):
    chunks = [text[i:i+chars_per_chunk] for i in range(0, len(text) - len(text) % chars_per_chunk, chars_per_chunk)]
    cluster = text[len(chunks) * chars_per_chunk:]  # The remaining text that doesn't fit into a chunk
    return chunks, cluster

# Function to handle copying the chunk or cluster to clipboard using Tkinter's clipboard
def copy_to_clipboard(chunk_text):
    root.clipboard_clear()  # Clear the clipboard
    root.clipboard_append(chunk_text)  # Append the chunk text to clipboard
    root.update()  # Now it is available for pasting

# Function to show chunks in the main window
def show_chunk(chunk_number, chunk_text, is_cluster=False):
    chunk_window_title = f"Cluster" if is_cluster else f"Chunk {chunk_number}"
    
    # Clear the previous content
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Create label for chunk title
    chunk_title = tk.Label(main_frame, text=chunk_window_title, font=("Arial", 16, "bold"), bg="black", fg="white")
    chunk_title.pack(pady=10)

    # Scrollable text widget to display chunk
    text_area = scrolledtext.ScrolledText(main_frame, width=100, height=25, wrap=tk.WORD, bg="black", fg="white")
    text_area.pack(padx=10, pady=10)
    
    # Display the chunk or cluster text
    text_area.insert(tk.END, chunk_text)
    text_area.config(state=tk.DISABLED)  # Disable editing

    # Copy button for the chunk/cluster
    copy_button = tk.Button(main_frame, text="Copy to Clipboard", command=lambda: copy_to_clipboard(chunk_text), bg="#800000", fg="white")  # Maroon Red
    copy_button.pack(pady=10)

    # Back to chunks menu button
    back_to_chunks_button = tk.Button(main_frame, text="Back to Chunks Menu", command=go_to_chunks_menu, bg="#800000", fg="white")  # Maroon Red
    back_to_chunks_button.pack(pady=10)

    # Back to main menu button
    back_to_main_menu_button = tk.Button(main_frame, text="Back to Main Menu", command=go_to_main_menu, bg="#800000", fg="white")  # Maroon Red
    back_to_main_menu_button.pack(pady=10)

# Function to go to the chunks menu (previous screen)
def go_to_chunks_menu():
    for widget in main_frame.winfo_children():
        widget.destroy()
    show_chunks_buttons()

# Function to go back to the main menu
def go_to_main_menu():
    for widget in main_frame.winfo_children():
        widget.destroy()
    initialize_gui()

# Function to open the file and load text
def load_from_file():
    file_path = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text = file.read()
        return text
    return ""

# Function to load text from the clipboard
def load_from_clipboard():
    text = pyperclip.paste()
    return text

# Function to initialize the GUI with options for file or clipboard input
def initialize_gui():
    title_label = tk.Label(main_frame, text="Choose Input Source", font=("Arial", 20, "bold"), bg="black", fg="white")
    title_label.pack(pady=30)
    
    # File option button
    file_button = tk.Button(main_frame, text="Load from File", command=lambda: load_and_split("file"), bg="#800000", fg="white")  # Maroon Red
    file_button.pack(pady=20, padx=20)
    
    # Clipboard option button
    clipboard_button = tk.Button(main_frame, text="Load from Clipboard", command=lambda: load_and_split("clipboard"), bg="#800000", fg="white")  # Maroon Red
    clipboard_button.pack(pady=20, padx=20)

# Function to load and split text based on user input
def load_and_split(source_type):
    if source_type == "file":
        text = load_from_file()
    elif source_type == "clipboard":
        text = load_from_clipboard()

    if text:
        global chunks, cluster
        chunks, cluster = split_into_chunks_and_cluster_by_chars(text)
        
        # Clear the main window and show buttons for each chunk
        for widget in main_frame.winfo_children():
            widget.destroy()

        show_chunks_buttons()
    else:
        messagebox.showerror("Error", "No text found to split.")

# Function to display buttons for each chunk and cluster
def show_chunks_buttons():
    # Create a label for the chunks menu
    chunks_label = tk.Label(main_frame, text="Chunks Menu", font=("Arial", 20, "bold"), bg="black", fg="white")
    chunks_label.pack(pady=30)
    
    # Create buttons for each chunk
    for i, chunk in enumerate(chunks):
        chunk_number = i + 1
        chunk_text = chunk
        
        chunk_button = tk.Button(main_frame, text=f"Show Chunk {chunk_number}", command=lambda cn=chunk_number, ct=chunk_text: show_chunk(cn, ct), bg="#800000", fg="white")  # Maroon Red
        chunk_button.pack(pady=5)

    # Create a button for the cluster if there are any remaining characters
    if cluster:
        cluster_text = cluster
        cluster_button = tk.Button(main_frame, text="Show Cluster (Remaining Text)", command=lambda: show_chunk(None, cluster_text, is_cluster=True), bg="#800000", fg="white")  # Maroon Red
        cluster_button.pack(pady=5)

    # Add a button to return to the main menu
    back_to_main_menu_button = tk.Button(main_frame, text="Back to Main Menu", command=go_to_main_menu, bg="#800000", fg="white")  # Maroon Red
    back_to_main_menu_button.pack(pady=10)

# Main application window
root = tk.Tk()
root.title("Text Splitter")
root.config(bg="black")
root.geometry("900x600")  # Resize the window to be larger

# Main frame for content
main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill=tk.BOTH, expand=True)

# Initialize the GUI with file or clipboard options
initialize_gui()

# Start the application
root.mainloop()
