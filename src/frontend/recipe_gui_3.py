import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
        # get the recipe names
        recipe_names = self.db_parser.get_recipe_names()
        self.recipe_dropdown["values"] = [name for name in recipe_names]  # TODO: Load from backend
        self.recipe_dropdown.pack(pady=5)

        ttk.Button(self.root, text="Load Recipe", command=self.load_recipe_to_edit).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)

    def load_recipe_to_edit(self):
        self.clear_window()
        self.root.configure(bg="#fff3e0")
        ttk.Label(self.root, text=f"Editing: {self.selected_recipe.get()}", font=("Helvetica", 18, "bold")).pack(pady=10)

        recipe_ingredients = self.db_parser.get_recipe_for_edit(self.selected_recipe.get())

        if not recipe_ingredients:
            # Recipe is empty → show warning and only a Back button
            messagebox.showwarning("Empty Recipe", "This recipe has no ingredients.")
            ttk.Button(self.root, text="Back", command=self.edit_recipe_screen).pack(pady=10)
            return

        # Treeview with Position column
        self.table = ttk.Treeview(self.root, columns=("Ingredient", "Amount", "Unit", "Position"), show="headings")
        self.table.heading("Ingredient", text="Ingredient")
        self.table.heading("Amount", text="Amount")
        self.table.heading("Unit", text="Unit")
        self.table.heading("Position", text="Position")
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        for item in recipe_ingredients:
            self.table.insert(
                "", "end",
                values=(item["name"], item["amount"], item["unit"], item.get("position", 0))
            )

        ttk.Button(self.root, text="Save Changes", command=self.apply_changes).pack(pady=10)
        ttk.Button(self.root, text="Send to Grocery List", command=self.send_to_grocery_list_edit).pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.edit_recipe_screen).pack(pady=5)

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
        
        #    def edit_recipe(self, recipe_name: str, new_ingredients: dict):
        new_ingredients = {}
        
        # needs to get the info from the cells and put them in the new_ingredients dict
        for row in data:
            name, amount, unit, position = row  # unpack new Position column
            new_ingredients[name] = (float(amount), unit, float(position))

        
        self.db_parser.edit_recipe(self.selected_recipe.get(), new_ingredients)
        
        
        messagebox.showinfo("Changes Applied", "Recipe updated successfully!")

    def send_to_grocery_list_edit(self):
        recipe_name = self.selected_recipe.get()
        if not recipe_name:
            messagebox.showwarning("No Recipe Selected", "Please select a recipe first.")
            return
        # FRONTEND ONLY placeholder
        print(f"Sending '{recipe_name}' to grocery list from Edit screen...")
        messagebox.showinfo("Sent!", f"'{recipe_name}' sent to grocery list.")

     # ---------------------- View Recipes (Updated 2-Column Layout) ---------------------- #
    def view_recipes_screen(self):
        self.clear_window()
        self.root.configure(bg="#e1f5fe")

        ttk.Label(self.root, text="Current Recipes", font=("Helvetica", 18, "bold")).pack(pady=15)

        container = tk.Frame(self.root, bg="#e1f5fe")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Left Column ---------------------- #
        left_frame = tk.Frame(container, bg="#e1f5fe")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        ttk.Label(left_frame, text="Available Recipes", font=("Helvetica", 14, "bold")).pack(pady=5)

        self.all_recipes_listbox = tk.Listbox(left_frame, font=("Helvetica", 13), height=20)
        self.all_recipes_listbox.pack(fill="both", expand=True)

        # TODO: Replace with backend fetch--------------------------------------------------------------------½½½½½½½½½½½½½½-----------------------------
        # get recipes with db_parser
        # add them to self.recipes list
        
        self.recipes = self.db_parser.get_recipe_names()
        for recipe in self.recipes:
            self.all_recipes_listbox.insert("end", recipe)

        ttk.Button(left_frame, text="Add →", command=self.add_recipe_to_temp_list).pack(pady=10)


        # Middle Controls (Proportion Selector) ---------------------- #
        center_frame = tk.Frame(container, bg="#e1f5fe")
        center_frame.pack(side="left", fill="y", padx=10)

        ttk.Label(center_frame, text="Proportion", font=("Helvetica", 13, "bold")).pack(pady=5)

        self.proportion_var = tk.StringVar(value="1")
        proportion_box = ttk.Combobox(center_frame, textvariable=self.proportion_var, width=5)
        proportion_box["values"] = ("1", "2", "3", "Custom")
        proportion_box.current(0)
        proportion_box.pack(pady=5)

        ttk.Label(center_frame, text="(Amount multiplied on Add)", font=("Helvetica", 10)).pack(pady=5)


        # Right Column ---------------------- #
        right_frame = tk.Frame(container, bg="#e1f5fe")
        right_frame.pack(side="left", fill="both", expand=True, padx=10)

        ttk.Label(right_frame, text="Added Recipes", font=("Helvetica", 14, "bold")).pack(pady=5)

        self.added_listbox = tk.Listbox(right_frame, font=("Helvetica", 13), height=20)
        self.added_listbox.pack(fill="both", expand=True)

        ttk.Button(right_frame, text="← Remove", command=self.remove_recipe_from_temp_list).pack(pady=10)

        ttk.Button(right_frame, text="Save to Grocery List", command=self.finalize_grocery_list).pack(pady=5)

        ttk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)


    # Add recipe from left → right
    def add_recipe_to_temp_list(self):
        selection = self.all_recipes_listbox.curselection()
        if not selection:
            return

        recipe = self.all_recipes_listbox.get(selection[0])

        # Proportion handling
        proportion = self.proportion_var.get()
        if proportion == "Custom":
            proportion = simpledialog.askfloat("Custom multiplier", "Enter multiplier:", minvalue=0.1, maxvalue=10)
            if not proportion:
                return

        # TODO: Use backend to multiply ingredient amounts before adding to grocery list

        self.added_listbox.insert("end", f"{recipe}  (x{proportion})")


    # Remove from right → left
    def remove_recipe_from_temp_list(self):
        selection = self.added_listbox.curselection()
        if not selection:
            return
        self.added_listbox.delete(selection[0])


    # Final save of everything added on the right side
    def finalize_grocery_list(self):
        added_items = self.added_listbox.get(0, "end")

        if not added_items:
            messagebox.showwarning("Empty", "No recipes added.")
            return

        # TODO: Perform DB queries to fetch ingredients per recipe
        # Here we need to send recipes as a dict with recipe name and a list of recipe which can be accessed using db_parser get_recipe_for_edit()
        # We also need to send proportions as a dict with recipe name and proportion value
        # This can be gotten be using the proportion from added_items listbox and creating a new dict with the recipe name and its proportions
        recipes_dict = {}
        proportions_dict = {}
        for item in added_items:
            parts = item.split("  (x")
            recipe_name = parts[0]
            proportion = float(parts[1].replace(")", "")) if len(parts) > 1 else 1
            recipes_dict[recipe_name] = self.db_parser.get_recipe_for_edit(recipe_name)
            proportions_dict[recipe_name] = proportion
            
        # Now we can use db_parsers parse_groceries method to get the final grocery list
        final_grocery_list = self.db_parser.parse_groceries(recipes_dict, proportions_dict)
        print("Parsed grocery list:", final_grocery_list)
        
        # Now we need to send this to the To_do_list_connector to add the ingredients to the grocery list
        
        
        self.db_parser.add_ingredients_to_to_do_list(final_grocery_list)
        messagebox.showinfo("Saved!", "Recipes added to grocery list.")

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