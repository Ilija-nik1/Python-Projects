import tkinter as tk
from tkinter import messagebox, ttk
import random

# Color schemes for dark and light modes
DARK_MODE_COLORS = {
    "BACKGROUND_COLOR": "#282c34",
    "LABEL_COLOR": "white",
    "ENTRY_BACKGROUND": "white",
    "ENTRY_TEXT_COLOR": "black",
    "BUTTON_BACKGROUND": "#61afef",
    "BUTTON_TEXT_COLOR": "white",
    "ERROR_COLOR": "#e06c75"
}

LIGHT_MODE_COLORS = {
    "BACKGROUND_COLOR": "#f0f0f0",
    "LABEL_COLOR": "black",
    "ENTRY_BACKGROUND": "white",
    "ENTRY_TEXT_COLOR": "black",
    "BUTTON_BACKGROUND": "#d3d3d3",
    "BUTTON_TEXT_COLOR": "black",
    "ERROR_COLOR": "#ff0000"
}

MIN_SIDES = 1
DICE_FACES = [1, 2, 3, 4, 5, 6]
ANIMATION_ITERATIONS = 10
ANIMATION_DELAY = 100

class DiceRollerGUI(tk.Frame):
    def __init__(self, master=None, mode='dark'):
        super().__init__(master)
        self.master = master
        self.mode = mode
        self.colors = DARK_MODE_COLORS if mode == 'dark' else LIGHT_MODE_COLORS
        self.configure_gui()
        self.master.title("Dice Roller")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.create_menu()
        self.roll_history = []

    def configure_gui(self):
        self.config(bg=self.colors['BACKGROUND_COLOR'])
        self.master.config(bg=self.colors['BACKGROUND_COLOR'])
        self.master.geometry("500x400")  # Set initial size
        self.master.minsize(300, 200)    # Set minimum size

    def create_widgets(self):
        self.create_label_entry_button_widgets()
        self.create_result_label()
        self.create_history_widgets()
        self.layout_widgets()  # New method to manage layout

    def create_label_entry_button_widgets(self):
        self.sides_label = self.create_label("Number of sides:")
        self.sides_entry = self.create_entry(width=10)
        self.roll_button = self.create_button("Roll", self.roll_dice)
        self.clear_button = self.create_button("Clear", self.clear_fields)

    def create_result_label(self):
        self.result_label = self.create_label("", font=("Arial", 14, "bold"))
        self.history_label = self.create_label("Roll History:", anchor="w")
        self.create_history_widgets()

    def create_history_widgets(self):
        self.history_text = self.create_text(height=5, width=30)
        self.history_scrollbar = tk.Scrollbar(self, command=self.history_text.yview)
        self.history_scrollbar.grid(row=3, column=4, sticky="NS")
        self.history_text.config(yscrollcommand=self.history_scrollbar.set)

    def create_label(self, text, **kwargs):
        label = tk.Label(self, text=text, bg=self.colors['BACKGROUND_COLOR'], fg=self.colors['LABEL_COLOR'], **kwargs)
        label.grid(padx=5, pady=5, sticky="E")
        return label

    def create_entry(self, **kwargs):
        entry = tk.Entry(self, bg=self.colors['ENTRY_BACKGROUND'], fg=self.colors['ENTRY_TEXT_COLOR'], **kwargs)
        entry.grid(padx=5, pady=5)
        return entry

    def create_button(self, text, command, **kwargs):
        button = tk.Button(self, text=text, command=command, bg=self.colors['BUTTON_BACKGROUND'], fg=self.colors['BUTTON_TEXT_COLOR'], **kwargs)
        button.grid(padx=5, pady=5)
        return button

    def create_text(self, **kwargs):
        text = tk.Text(self, bg=self.colors['ENTRY_BACKGROUND'], fg=self.colors['ENTRY_TEXT_COLOR'], **kwargs)
        text.grid(padx=5, pady=5)
        return text

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        options_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Switch to Dark Mode", command=lambda: self.switch_mode('dark'))
        options_menu.add_command(label="Switch to Light Mode", command=lambda: self.switch_mode('light'))

    def switch_mode(self, mode):
        self.mode = mode
        self.colors = DARK_MODE_COLORS if mode == 'dark' else LIGHT_MODE_COLORS
        self.configure_gui()
        self.create_widgets()

    def roll_dice(self):
        try:
            num_sides = int(self.sides_entry.get())
            if num_sides < MIN_SIDES:
                raise ValueError("Number of sides must be greater than 0")
        except ValueError:
            self.show_error("Invalid input")
            return

        self.animate_dice_roll(num_sides, ANIMATION_ITERATIONS)

    def animate_dice_roll(self, num_sides, iterations):
        def update_dice_face():
            roll_result = random.choice(DICE_FACES)
            self.result_label.config(text=f"You rolled a {roll_result}!")

        def end_animation():
            roll_result = random.randint(1, num_sides)
            self.result_label.config(text=f"You rolled a {roll_result}!")
            self.roll_history.append(roll_result)
            self.update_history_text()

        def animation_loop(current_iteration):
            if current_iteration < iterations:
                update_dice_face()
                self.after(ANIMATION_DELAY, animation_loop, current_iteration + 1)
            else:
                end_animation()

        animation_loop(0)

    def clear_fields(self):
        if messagebox.askokcancel("Clear Fields", "Are you sure you want to clear the fields?"):
            self.sides_entry.delete(0, tk.END)
            self.result_label.config(text="")

    def update_history_text(self):
        self.history_text.delete(1.0, tk.END)
        for roll in self.roll_history:
            self.history_text.insert(tk.END, f"Roll: {roll}\n")
        self.history_text.see(tk.END)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def create_label_entry_button_widgets(self):
        self.sides_label = self.create_label("Number of sides:")
        self.sides_entry = self.create_entry(width=10)

        self.dice_label = self.create_label("Number of dice:")
        self.dice_entry = self.create_entry(width=10)

        self.roll_button = self.create_button("Roll", self.roll_dice)
        self.clear_button = self.create_button("Clear", self.clear_fields)

    def roll_dice(self):
        try:
            num_sides = int(self.sides_entry.get())
            num_dice = int(self.dice_entry.get())
            if num_sides < MIN_SIDES or num_dice < 1:
                raise ValueError("Number of sides and dice must be greater than 0")
        except ValueError:
            self.show_error("Invalid input for sides or dice")
            return

        self.animate_dice_roll(num_sides, num_dice, ANIMATION_ITERATIONS)

    def animate_dice_roll(self, num_sides, num_dice, iterations):
        def update_dice_face():
            roll_results = [random.choice(DICE_FACES) for _ in range(num_dice)]
            self.result_label.config(text=f"Rolling... {', '.join(map(str, roll_results))}")

        def end_animation():
            roll_results = [random.randint(1, num_sides) for _ in range(num_dice)]
            self.result_label.config(text=f"You rolled: {', '.join(map(str, roll_results))}")
            self.roll_history.extend(roll_results)
            self.update_history_text()

    def layout_widgets(self):
        # Grid configuration for dynamic resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Positioning the widgets with grid
        self.sides_label.grid(row=0, column=0, sticky="E")
        self.sides_entry.grid(row=0, column=1, sticky="W")
        self.dice_label.grid(row=1, column=0, sticky="E")
        self.dice_entry.grid(row=1, column=1, sticky="W")
        self.roll_button.grid(row=0, column=2, rowspan=2, sticky="EW")
        self.clear_button.grid(row=1, column=3, rowspan=2, sticky="EW")
        self.result_label.grid(row=2, column=0, columnspan=4)
        self.history_label.grid(row=3, column=0, columnspan=4, sticky="W")
        self.history_text.grid(row=4, column=0, columnspan=3, sticky="NSEW")
        self.history_scrollbar.grid(row=4, column=3, sticky="NS")

if __name__ == '__main__':
    root = tk.Tk()
    app = DiceRollerGUI(master=root, mode='dark')
    app.mainloop()