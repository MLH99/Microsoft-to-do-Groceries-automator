import tkinter as tk
from tkinter import ttk, messagebox
from src.database_parser import DatabaseParser

# ---------------------- Custom Styles ---------------------- #
def setup_styles():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton",
                    font=("Helvetica", 14, "bold"),
                    padding=10,
                    foreground="white",
                    background="#4CAF50",
                    borderwidth=0)
    style.map("TButton", background=[("active", "#45a049")])
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TCombobox", padding=5, font=("Helvetica", 12))
    style.configure("Treeview", font=("Helvetica", 12), rowheight=30)
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

# ---------------------- GUI Class ---------------------- #
class RecipeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍳 Automatic Recipe Adder")
        self.root.geometry("950x700")
        self.root.configure(bg="#fdf6e3")

        self.db_parser = DatabaseParser()
        setup_styles()
        self.create_main_menu()

    # ---------------------- Main Menu ---------------------- #
    def create_main_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#fdf6e3")
        frame.pack(expand=True)

        title = tk.Label(frame, text="Automatic Recipe Adder", font=("Helvetica", 24, "bold"), bg="#fdf6e3", fg="#FF5722")
        title.pack(pady=20)

        ttk.Button(frame, text="Add Recipe", command=self.add_recipe_screen, width=20).pack(pady=15)
        ttk.Button(frame, text="Edit Recipe", command=self.edit_recipe_screen, width=20).pack(pady=15)
        ttk.Button(frame, text="View Recipes", command=self.view_recipes_screen, width=20).pack(pady=15)

    # ---------------------- Add Recipe ---------------------- #
    def add_recipe_screen(self):
        self.clear_window()
        self.root.configure(bg="#e8f5e9")
        ttk.Label(self.root, text="Add a New Recipe", font=("Helvetica", 18, "bold")).pack(pady=15)

        form_frame = tk.Frame(self.root, bg="#e8f5e9")
        form_frame.pack(pady=10)

        # Recipe Name
        ttk.Label(form_frame, text="Recipe Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.recipe_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.recipe_name_var, width=40).grid(row=0, column=1, padx=5, pady=5, columnspan=4)

        # Ingredients Frame (headers + entries inside this frame)
        self.ingredients_frame = tk.Frame(form_frame, bg="#e8f5e9")
        self.ingredients_frame.grid(row=1, column=0, columnspan=5, pady=10)

        # Header row
        ttk.Label(self.ingredients_frame, text="Ingredient", width=20).grid(row=0, column=0, padx=3, pady=2)
        ttk.Label(self.ingredients_frame, text="Amount", width=10).grid(row=0, column=1, padx=3, pady=2)
        ttk.Label(self.ingredients_frame, text="Unit", width=10).grid(row=0, column=2, padx=3, pady=2)
        ttk.Label(self.ingredients_frame, text="Position", width=10).grid(row=0, column=3, padx=3, pady=2)

        self.ingredient_entries = []
        self.add_ingredient_row()

        ttk.Button(form_frame, text="Add Another Ingredient", command=self.add_ingredient_row).grid(
            row=2, column=3, pady=10, sticky="e"
        )

        ttk.Button(self.root, text="OK", command=self.save_recipe).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)



    def add_ingredient_row(self):
        row = len(self.ingredient_entries) + 1  # +1 because row 0 is header
        ingredient_name = tk.StringVar()
        amount = tk.StringVar()
        unit = tk.StringVar()
        position = tk.StringVar()

        ttk.Entry(self.ingredients_frame, textvariable=ingredient_name, width=20).grid(row=row, column=0, padx=3, pady=2)
        ttk.Entry(self.ingredients_frame, textvariable=amount, width=10).grid(row=row, column=1, padx=3, pady=2)

        unit_combo = ttk.Combobox(self.ingredients_frame, textvariable=unit, width=10)
        unit_combo["values"] = ("ml", "l", "g", "kg", "st")
        unit_combo.current(0)
        unit_combo.grid(row=row, column=2, padx=3, pady=2)

        ttk.Entry(self.ingredients_frame, textvariable=position, width=10).grid(row=row, column=3, padx=3, pady=2)

        self.ingredient_entries.append((ingredient_name, amount, unit, position))


    def save_recipe(self):
        recipe_name = self.recipe_name_var.get()

        ingredients = []
        for name, amount, unit, position in self.ingredient_entries:
            pos = position.get()
            try:
                pos_val = float(pos) if pos else 0.0
            except ValueError:
                messagebox.showerror("Invalid position", "Position must be a number.")
                return

            ingredients.append({
                "name": name.get(),
                "amount": amount.get(),
                "unit": unit.get(),
                "position": pos_val
            })

        ingredients_dict = {}
        for ing in ingredients:
            ingredients_dict[ing["name"]] = (float(ing["amount"]), ing["unit"], float(ing["position"]))
            
        # TODO: Replace this with backend integration

        self.db_parser.add_recipe(recipe_name, ingredients_dict)
        
        
        
        # This is where you would save 'recipe_name' and 'ingredients' to your database or file
        print("Saving recipe:", recipe_name)
        print("Ingredients:", ingredients)

        # use database_parser class to send the info to the database
        
        # wait for answer by controlling the database with databaseparser where you controll
        # the recipe name and the ingredients

        # if above is true set success to true otherwise to false

        success = True  # placeholder
        if success:
            messagebox.showinfo("Success", f"Recipe '{recipe_name}' saved successfully!")
        else:
            messagebox.showerror("Error", "Failed to save recipe.")



    # ---------------------- Edit Recipe ---------------------- #
    def edit_recipe_screen(self):
        self.clear_window()
        self.root.configure(bg="#fff3e0")
        ttk.Label(self.root, text="Edit Existing Recipes", font=("Helvetica", 18, "bold")).pack(pady=15)

        ttk.Label(self.root, text="Select Recipe:").pack()
        self.selected_recipe = tk.StringVar()
        self.recipe_dropdown = ttk.Combobox(self.root, textvariable=self.selected_recipe, width=30)
        self.recipe_dropdown["values"] = ["Pancakes", "Spaghetti Bolognese", "Chocolate Cake"]  # TODO: Load from backend
        self.recipe_dropdown.pack(pady=5)

        ttk.Button(self.root, text="Load Recipe", command=self.load_recipe_to_edit).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)

    def load_recipe_to_edit(self):
        self.clear_window()
        self.root.configure(bg="#fff3e0")
        ttk.Label(self.root, text=f"Editing: {self.selected_recipe.get()}", font=("Helvetica", 18, "bold")).pack(pady=10)

        self.table = ttk.Treeview(self.root, columns=("Ingredient", "Amount", "Unit"), show="headings")
        self.table.heading("Ingredient", text="Ingredient")
        self.table.heading("Amount", text="Amount")
        self.table.heading("Unit", text="Unit")
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        example_data = [("Flour", "500", "g"), ("Milk", "2", "dl")]  # TODO: Replace with backend
        for item in example_data:
            self.table.insert("", "end", values=item)

        ttk.Button(self.root, text="Save Changes", command=self.apply_changes).pack(pady=10)
        ttk.Button(self.root, text="Send to Grocery List", command=self.send_to_grocery_list_edit).pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)

        self.table.bind("<Double-1>", self.edit_cell)

    def edit_cell(self, event):
        item = self.table.identify_row(event.y)
        column = self.table.identify_column(event.x)
        if not item or not column:
            return
        x, y, width, height = self.table.bbox(item, column)
        column_index = int(column.replace("#", "")) - 1
        value = self.table.item(item, "values")[column_index]

        entry = ttk.Entry(self.table)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event):
            new_value = entry.get()
            values = list(self.table.item(item, "values"))
            values[column_index] = new_value
            self.table.item(item, values=values)
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def apply_changes(self):
        data = [self.table.item(item, "values") for item in self.table.get_children()]
        # TODO: Send updated data to backend
        messagebox.showinfo("Changes Applied", "Recipe updated successfully!")

    def send_to_grocery_list_edit(self):
        recipe_name = self.selected_recipe.get()
        if not recipe_name:
            messagebox.showwarning("No Recipe Selected", "Please select a recipe first.")
            return
        # FRONTEND ONLY placeholder
        print(f"Sending '{recipe_name}' to grocery list from Edit screen...")
        messagebox.showinfo("Sent!", f"'{recipe_name}' sent to grocery list.")

    # ---------------------- View Recipes ---------------------- #
    def view_recipes_screen(self):
        self.clear_window()
        self.root.configure(bg="#e1f5fe")
        ttk.Label(self.root, text="Current Recipes", font=("Helvetica", 18, "bold")).pack(pady=15)

        # Example recipe list, replace with backend fetch
        self.recipes = ["Pancakes", "Spaghetti Bolognese", "Chocolate Cake"]
        self.selected_recipe_view = tk.StringVar()

        self.listbox = tk.Listbox(self.root, font=("Helvetica", 14), height=15)
        for recipe in self.recipes:
            self.listbox.insert("end", recipe)
        self.listbox.pack(fill="both", expand=True, padx=30, pady=20)
        self.listbox.bind("<<ListboxSelect>>", self.on_recipe_select_view)

        self.send_button_view = ttk.Button(self.root, text="Send to Grocery List", command=self.send_to_grocery_list_view, state="disabled")
        self.send_button_view.pack(pady=10)

        ttk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def on_recipe_select_view(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.selected_recipe_view.set(self.listbox.get(selection[0]))
            self.send_button_view.config(state="normal")
        else:
            self.send_button_view.config(state="disabled")

    def send_to_grocery_list_view(self):
        recipe_name = self.selected_recipe_view.get()
        if not recipe_name:
            messagebox.showwarning("No Recipe Selected", "Please select a recipe first.")
            return
        # FRONTEND ONLY placeholder
        print(f"Sending '{recipe_name}' to grocery list from View screen...")
        messagebox.showinfo("Sent!", f"'{recipe_name}' sent to grocery list.")

    # ---------------------- Utility ---------------------- #
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------------- Run App ---------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeGUI(root)
    root.mainloop()
x