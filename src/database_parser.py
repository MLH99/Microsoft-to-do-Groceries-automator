"""This class is for handling adding recipes backend. It should give options to add a recipe or 
change one. A screen should come up where they can choose what ingredients to add and
the amounts and unit. Unit should be a scroll menu with know measurements for cooking such
as ml or kg. the swedish version of "st" standing for styck but in english should also 
be a choice. After adding or chaing a recipe you can press OK to apply the changes and get
a message which tells you if it succeded or not. You should also have an option to see the current recipes.
So you can choose which one to view and edit. The editing should not be done one at a time.
Instead you should be able to click on a table and change its contents."""
from src.database_connector import DatabaseConnector
from src.to_do_list_connector import To_Do_Connector

class DatabaseParser():

    def __init__(self):
        self.db_connector = DatabaseConnector()
        self.to_do_connector = To_Do_Connector()

    def get_recipe_names(self):
        # get names from database using recipe_automator

        recipe_names = self.db_connector.get_recipes()

        # return the info as a list

        return recipe_names
    
    def get_recipe_ingredients(self, recipe_name: str):
        
        recipe_ingredients = self.db_connector.get_recipe_ingredients(recipe_name)

        if recipe_ingredients:
            return recipe_ingredients
        else:
            return False
    
    def add_recipe(self, recipe_name: str, ingredients: dict):

        self.db_connector.insert_recipe_ingredients(recipe_name, ingredients)
        
    def get_recipe_for_edit(self, recipe_name: str):
        recipe_ingredients = self.db_connector.get_recipe_for_edit(recipe_name)

        if recipe_ingredients:
            return recipe_ingredients
        else:
            return False

    #---------------------- multiply recipes by proportion, add the ingredients from different recipe together and sort them -------------------#
    
    def multiply_by_proportion(self, recipe: str, proportion: int):
        recipe_ingredients = self.db_connector.get_recipe_for_edit(recipe)
        
        final_ingredients = []
        
        for ingredient in recipe_ingredients:
            ingredient["amount"] = ingredient["amount"] * proportion
            final_ingredients.append(ingredient)
        
        return final_ingredients

    def combine_same_ingredients(self, ingredients: dict):
        
        combined_ingredients = {}
        
        for name, items in ingredients.items():
            for item in items:
                amount = item["amount"]
                unit = item["unit"]
                
                key = (name, unit)
                
                if key in combined_ingredients:
                    combined_ingredients[key]["amount"] += amount
                else:
                    combined_ingredients[key] = {"amount": amount, "unit": unit}
        
        result = []
        for (name, unit), info in combined_ingredients.items():
            result.append({"name": name, "amount": info["amount"], "unit": unit, "position": info["position"] if "position" in info else 0})
        
        return result
    
    def sort_ingredients_by_position(self, ingredients: list):
        sorted_ingredients = sorted(ingredients, key=lambda x: x["position"], reverse=False)
        return sorted_ingredients
    
    def parse_groceries(self, recipes: dict, proportions: dict):
        
        all_ingredients = {}
        
        for recipe_name, ingredient_list in recipes.items():
            proportion = proportions.get(recipe_name, 1)
            multiplied_ingredients = self.multiply_by_proportion(recipe_name, proportion)
            
            for ingredient in multiplied_ingredients:
                name = ingredient["name"]
                
                if name not in all_ingredients:
                    all_ingredients[name] = []
                
                all_ingredients[name].append(ingredient)
        
        combined_ingredients = self.combine_same_ingredients(all_ingredients)
        
        sorted_ingredients = self.sort_ingredients_by_position(combined_ingredients)
        
        return sorted_ingredients
    
    
    #---------------------- Connectot to to_do_list connector and add the tasks to the to do list -------------------#
    def add_ingredients_to_to_do_list(self, ingredients: list):
        
        for ingredient in ingredients:
            title = f"{ingredient['name']} - {ingredient['amount']} {ingredient['unit']}"
            task_data = {
                "title": title,
                "body": f"Remember to buy {ingredient['amount']} {ingredient['unit']} of {ingredient['name']}."
            }
            self.to_do_connector.add_task(task_data["title"], task_data["body"])


    #---------------------- EDIT recipe -------------------#
    def edit_recipe(self, recipe_name: str, new_ingredients: dict):
        self.db_connector.edit_recipe(recipe_name, new_ingredients)