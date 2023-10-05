import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# Function to apply syntax highlighting
def highlight_code(event):
    if current_text_widget is not None:  # Check if current_text_widget is set
        code = current_text_widget.get("1.0", "end-1c")
        highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())
        current_text_widget.delete("1.0", "end")
        current_text_widget.insert("1.0", highlighted_code)

# Create a function to set the current text widget
def set_current_text_widget(text_widget):
    global current_text_widget
    current_text_widget = text_widget
    current_text_widget.bind("<KeyRelease>", highlight_code)  # Bind the event here

def run_code():
    code = current_text_widget.get("1.0", "end-1c")
    output.delete("1.0", "end")
    try:
        # Execute the code without highlighting
        exec(code)
    except Exception as e:
        output.insert("1.0", str(e))

def save_code():
    code = current_text_widget.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(code)

def load_code():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
            current_text_widget.delete("1.0", "end")
            current_text_widget.insert("1.0", code)

def delete_tab():
    current_tab = notebook.select()
    if current_tab:
        notebook.forget(current_tab)

# Create the main window
window = tk.Tk()
window.title("Python Code Editor")

# Create a Notebook for multiple tabs
notebook = ttk.Notebook(window)
notebook.pack(fill=tk.BOTH, expand=True)

# Create a function to add a new tab and set the current text widget
def add_tab():
    new_tab = ttk.Frame(notebook)
    notebook.add(new_tab, text="Tab " + str(notebook.index("end")))
    new_code_text = tk.Text(new_tab, wrap=tk.WORD)
    new_code_text.pack(fill=tk.BOTH, expand=True)
    new_tab.bind("<FocusIn>", lambda event, text_widget=new_code_text: set_current_text_widget(text_widget))
    set_current_text_widget(new_code_text)  # Set the current text widget

# Add an initial tab and set it as the current text widget
add_tab()

# Create a menu
menu = tk.Menu(window)
window.config(menu=menu)

# Create a "File" submenu with options for loading and saving
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Add Tab", command=add_tab)
file_menu.add_command(label="Delete Tab", command=delete_tab)
file_menu.add_separator()
file_menu.add_command(label="Run", command=run_code)
file_menu.add_command(label="Save", command=save_code)
file_menu.add_command(label="Load", command=load_code)

# Create a text area for output
output = tk.Text(window, wrap=tk.WORD, height=6)
output.pack(fill=tk.BOTH)

# Start the Tkinter main loop
window.mainloop()
