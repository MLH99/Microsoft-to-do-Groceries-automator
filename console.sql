CREATE database recipe_and_ingredients;

USE recipe_and_ingredients;

SHOW TABLES;

CREATE TABLE ingredients(
    i_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    position double
);
DROP TABLE recipes
DROP TABLE ingredients

CREATE TABLE recipes (
    r_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

drop table recipe_ingredients


CREATE TABLE recipe_ingredients(
    r_id INT,
    i_id INT,
    amount DOUBLE,
    unit VARCHAR(50),
    PRIMARY KEY (r_id, i_id),
    FOREIGN KEY (r_id) REFERENCES recipes(r_id) ON DELETE CASCADE,
    FOREIGN KEY (i_id) REFERENCES ingredients(i_id) ON DELETE CASCADE
);

INSERT INTO ingredients (name, position) VALUES ('yogurt', 1)

INSERT IGNORE INTO recipes (name) VALUE ('NAJS
')

INSERT INTO recipe_ingredients values (1, 1, 6, 'KG')

SELECT
    recipes.name as recipe_name,
    GROUP_CONCAT(ingredients.name SEPARATOR ', ') AS ingredients
from recipes
JOIN recipe_ingredients on recipes.r_id = recipe_ingredients.r_id
JOIN ingredients ON ingredients.i_id = recipe_ingredients.i_id
GROUP BY  recipes.name


