"""This class is for handling adding recipes backend. It should give options to add a recipe or 
change one. A screen should come up where they can choose what ingredients to add and
the amounts and unit. Unit should be a scroll menu with know measurements for cooking such
as ml or kg. the swedish version of "st" standing for styck but in english should also 
be a choice. After adding or chaing a recipe you can press OK to apply the changes and get
a message which tells you if it succeded or not. You should also have an option to see the current recipes.
So you can choose which one to view and edit. The editing should not be done one at a time.
Instead you should be able to click on a table and change its contents."""
from src.database_connector import DatabaseConnector

class DatabaseParser():

    def __init__(self):
        self.db_connector = DatabaseConnector()

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

        
    






