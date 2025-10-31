from dotenv import load_dotenv
import os
import mysql.connector

db = mysql.connector.connect(host=os.getenv("DB_HOST"),
                             user =os.getenv("DB_USER"),
                             passwd = os.getenv("DB_PASSWORD"),
                             database = os.getenv("DB_NAME"))

db.autocommit = True
mycursor = db.cursor(dictionary=True)

def get_recipes():
    
    sql = "SELECT name FROM recipes"
    
    mycursor.execute(sql)
    
    return [r[0] for r in mycursor.fetchall()]


def get_ingredients():
    
    sql = "SELECT name FROM ingredients"
    
    mycursor.execute(sql)
    
    return [r[0] for r in mycursor.fetchall()]

def get_recipe_ingredients():
    
    sql = (
    "SELECT recipes.name AS recipe_name, "
    "GROUP_CONCAT(ingredients.name SEPARATOR ', ') AS ingredients "
    "FROM recipes "
    "JOIN recipe_ingredients ON recipes.r_id = recipe_ingredients.r_id "
    "JOIN ingredients ON ingredients.i_id = recipe_ingredients.i_id "
    "GROUP BY recipes.name"
    )
    
    mycursor.execute(sql)
    
    results =  mycursor.fetchall()
    
    return [{'recipe_name': r[0], 'ingredients': r[1]} for r in results]


# MIGHT BE UNNECCESSARY SINCE MYSQL TABLE ALREADY HAS UNIQUE ON RECIPE NAMES
def check_recipe(recipe_name: str):
    
    sql = "SELECT name FROM recipes WHERE name = %s"
    
    mycursor.execute(sql, (recipe_name,))
    
    result = mycursor.fetchone()
    
    return bool(result)

def insert_recipe(recipe_name: str):
    
    
    sql = "INSERT IGNORE INTO recipes (name) VALUES (%s)"
    
    mycursor.execute(sql, (recipe_name,))
    
    return

def insert_ingredients(ingredients: dict):
    
    sql = "INSERT IGNORE INTO ingredients (name, position) VALUES (%s, %s)"
    
    data = list(ingredients.items()) ## ask chat if this works instead
    mycursor.executemany(sql, data)
    
    return

"""ingredients should be a dict that contains dicts with the ingredient name as a key, then 
the values should be a tuple with  amount as float, unit as a string and position as an float"""

# currently has bugs below
def insert_recipe_ingredients(recipe_name: str, ingredients: dict):
    
    # start with inserting the recipe name in recipe table
    
    insert_recipe(recipe_name)
    
    # Then insert the ingredients in the ingredient list if they dont exist
    # i need to make the ingredient list a dict with name as key and position as value
    ingredient_list = dict()
    for ingredient in ingredients:
        ingredient_list[ingredient] = ingredients[ingredient][2]
    
    insert_ingredients(ingredient_list)
    
    # lastly insert all of it into recipe_ingredients
    
    # get recipe id (r_id) from recipe table
    
    sql = "SELECT r_id FROM recipes WHERE name = %s"
    
    mycursor.execute(sql, (recipe_name, ))
    
    r_id = mycursor.fetchone()["r_id"]
    

    # insert one ingredient at the time
    
    for ingredient in ingredients:
        # get amount
        ingredient_name = ingredient
        ingredient = ingredients[ingredient]
        amount = ingredient[0]
        # get unit
        unit = ingredient[1]
        
        # get i_id
        sql = "SELECT i_id FROM ingredients WHERE name = %s"
        
        mycursor.execute(sql, (ingredient_name, ))
        
        i_id = mycursor.fetchone()["i_id"]
        
        sql = "INSERT IGNORE INTO recipe_ingredients VALUES (%s, %s, %s, %s)"
        
        mycursor.execute(sql, (r_id, i_id, amount, unit))
        
    return

"""ingredients should be a dict that contains dicts with the ingredient name as a key, then 
the values should be a tuple with  amount as float, unit as a string and position as an float"""

ingredients = {
    "kol": (1, "huvud", 0.5),
    "nötfärs": (500, "gram", 1.2)
}

recipe_name = "koldolmar"

insert_recipe_ingredients(recipe_name, ingredients)