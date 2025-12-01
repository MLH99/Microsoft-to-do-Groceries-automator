from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()#check this out

db = mysql.connector.connect(host=os.getenv("DB_HOST"),
                             user =os.getenv("DB_USER"),
                             passwd = os.getenv("DB_PASSWORD"),
                             database = os.getenv("DB_NAME"))

db.autocommit = True
mycursor = db.cursor(dictionary=True)

class DatabaseConnector():
    #---------------------- Getters ----------------------#
    def get_recipes(self): 
        """Return list of recipe names."""
        sql = "SELECT name FROM recipes ORDER BY name"
        mycursor.execute(sql)
        rows = mycursor.fetchall()
        return [r["name"] for r in rows]

    def get_recipe_for_edit(self, recipe_name: str):
        """
        Returns full ingredient info for one recipe.
        Output format:
        [
          {"name": "flour", "amount": 500, "unit": "g", "position": 1.0},
          ...
        ]
        """
        sql = """
        SELECT i.name, ri.amount, ri.unit, i.position
        FROM recipes r
        JOIN recipe_ingredients ri ON r.r_id = ri.r_id
        JOIN ingredients i ON i.i_id = ri.i_id
        WHERE r.name = %s
        ORDER BY i.position ASC
        """
        mycursor.execute(sql, (recipe_name,))
        return mycursor.fetchall()

    """Maybe unnecessary since it doesnt really do anything for us"""
    def get_ingredients(self, recipe_name: str):
        
        sql = "SELECT name, amount FROM ingredients where name = %s"
        
        mycursor.execute(sql, recipe_name)
        
        return [r[0] for r in mycursor.fetchall()]

    def get_recipe_ingredients(self):
        
        sql ="""
        SELECT r.name AS recipe_name,
        GROUP_CONCAT(i.name ORDER BY i.position SEPARATOR ', ') AS ingredients
        FROM recipes r
        JOIN recipe_ingredients ri ON r.r_id = ri.r_id
        JOIN ingredients i ON i.i_id = ri.i_id
        GROUP BY r.name
        ORDER BY r.name
        """
        
        mycursor.execute(sql)
        rows =  mycursor.fetchall()
        return rows
        

    # MIGHT BE UNNECCESSARY SINCE MYSQL TABLE ALREADY HAS UNIQUE ON RECIPE NAMES
    def check_recipe(self, recipe_name: str):
        sql = "SELECT name FROM recipes WHERE name = %s"
        mycursor.execute(sql, (recipe_name,))
        result = mycursor.fetchone()
        return bool(result)
    #---------------------- Inserts ----------------------#
    def insert_recipe(self, recipe_name: str):
        sql = "INSERT IGNORE INTO recipes (name) VALUES (%s)"  
        mycursor.execute(sql, (recipe_name,))

    def insert_ingredients(self, ingredients: dict):
        """
        parameter ingredient_positions = {name: position}
        """
        sql = "INSERT IGNORE INTO ingredients (name, position) VALUES (%s, %s)"
        ingredient_list = [(name, pos) for name, pos in ingredients.items()]
        mycursor.executemany(sql, ingredient_list)

    """ingredients should be a dict that contains dicts with the ingredient name as a key, then 
    the values should be a tuple with  amount as float, unit as a string and position as an float"""

    def insert_recipe_ingredients(self, recipe_name: str, ingredients: dict):
        """
        ingredients should be a dict that contains tuples with the ingredient name as a key,
        and the tuple contains: (amount as float, unit as str, position as float)
        """
        # Insert recipe first
        self.insert_recipe(recipe_name)
        
        # Insert ingredients with positions
        # Extract the position (3rd element in tuple) for insert_ingredients
        self.insert_ingredients({name: details[2] for name, details in ingredients.items()})
        
        # Prepare SQL to link recipe with ingredients
        sql = """
        INSERT INTO recipe_ingredients (r_id, i_id, amount, unit)
        VALUES (
            (SELECT r_id FROM recipes WHERE name = %s),
            (SELECT i_id FROM ingredients WHERE name = %s),
            %s,
            %s
        )
        ON DUPLICATE KEY UPDATE amount = VALUES(amount), unit = VALUES(unit)
        """
        
        # Prepare list of values for insertion
        recipe_ingredient_list = [
            (recipe_name, name, details[0], details[1])  # amount = details[0], unit = details[1]
            for name, details in ingredients.items()
        ]
        
        # Execute SQL for each ingredient
        for item in recipe_ingredient_list:
            mycursor.execute(sql, item)
        

    
    # ---------------------------- EDIT SYSTEM ---------------------------- #

    def delete_recipe_ingredients(self, recipe_name: str):
        """Remove existing ingredient links for a recipe."""
        sql = "SELECT r_id FROM recipes WHERE name = %s"
        mycursor.execute(sql, (recipe_name,))
        row = mycursor.fetchone()

        if not row:
            return False

        r_id = row["r_id"]

        del_sql = "DELETE FROM recipe_ingredients WHERE r_id = %s"
        mycursor.execute(del_sql, (r_id,))
        return True

    def edit_recipe(self, recipe_name: str, new_ingredients: dict):
        """
        Completely replaces a recipe's ingredients with new data.

        new_ingredients format:
            { "flour": (500, "g", 1.0), ... }
        """

        # 1. Remove old ingredient links
        self.delete_recipe_ingredients(recipe_name)

        # 2. Reinsert everything
        self.insert_recipe_ingredients(recipe_name, new_ingredients)

        return True