"""
Main Module
Launches the administrative application loop.
"""
import tkinter as tk
import database
from gui import FullApplicationEngine

def main():
    # Instantiate or connect to the target Postgre SQL schemas tables
    database.initialize_database()
    
    # Establish root environment instance setup window parameters
    root = tk.Tk()
    
    # Start app view loop
    app = FullApplicationEngine(root)
    root.mainloop()

if __name__ == "__main__":
    main()