import tkinter as tk

def refresh_window():
    # Redraw the window
    window.update()
    window.update_idletasks()
    print("Refresh completed.")

# Create the main window
window = tk.Tk()
window.geometry("300x300")
window.title("PythonExamples.org")

label = tk.Label(window, text="Click the below button to refresh the window.")
label.pack()

button = tk.Button(window, text="Refresh", command=refresh_window)
button.pack()

# Run the application
window.mainloop()