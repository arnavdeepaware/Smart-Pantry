'''
- list of ingredients ordered by expiry date
    - each ingredient has a name and expire date
- Add meal type and daily calorie intake
- add dietary restrictions
'''

#@title Use Google Gemini API
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('GEMINI_API_KEY')

def parse_recipe_response(response: dict) -> dict:
    """
    Parse the Gemini API response and clean up formatting
    Args:
        response (dict): Raw response from Gemini API
    Returns:
        dict: Cleaned recipe data or empty dict if parsing fails
    """
    try:
        # Extract the JSON string from the response
        json_text = response['candidates'][0]['content']['parts'][0]['text']
        
        # Clean up markdown, newlines, and whitespace
        clean_json = (json_text
            .replace('```json', '')  # Remove markdown JSON indicator
            .replace('```', '')      # Remove remaining markdown
            .strip()                 # Remove leading/trailing whitespace
            .replace('\n', ' ')      # Replace newlines with spaces
            .replace('  ', ' ')      # Remove double spaces
        )
        
        # Parse the JSON string
        recipe_data = json.loads(clean_json)
        
        # Clean up instructions and other text fields
        if 'recipes' in recipe_data:
            for recipe in recipe_data['recipes']:
                # Clean up instructions
                recipe['instructions'] = [
                    instruction.strip()
                    for instruction in recipe['instructions']
                ]
                
                # Clean up ingredient names and quantities
                for ingredient in recipe['ingredients_used']:
                    ingredient['name'] = ingredient['name'].strip()
                    ingredient['quantity'] = ingredient['quantity'].strip()
                
                # Clean up other text fields
                recipe['name'] = recipe['name'].strip()
                recipe['cooking_time'] = recipe['cooking_time'].strip()
                if 'total_calroies' in recipe:  # Handle typo in original format
                    recipe['total_calories'] = recipe.pop('total_calroies').strip()
        
        return recipe_data
        
    except Exception as e:
        print(f"Error parsing recipe response: {str(e)}")
        return {}

def get_recipe_instructions(list_of_ingredients, meal_type, daily_calorie_intake, dietary_restrictions):
    text_prompt = f'''
    Generate three detailed recipes that can be made with these ingredients. Prioritize the ingredients with coming expiry dates. Response must be in the following JSON format.
    If no recipe is possible, return an empty JSON object {{}}.

    Input parameters:
    - Ingredients with expiry dates: {list_of_ingredients}
    - Meal Type: {meal_type}
    - Daily Calorie Target: {daily_calorie_intake}
    - Dietary Restrictions: {dietary_restrictions}

    Required JSON Response Format:
    {{
        "recipes": [
            {{
                "name": "Recipe Name",
                "ingredients_used": [
                    {{
                        "name": "ingredient name",
                        "quantity": "amount needed",
                    }}
                ],
                "instructions": [
                    "step 1",
                    "step 2",
                    ...
                ],
                "total_calroies": "calories",
                "cooking_time": "minutes"
            }}
        ]
    }}
    '''

    print("Generating recipe instructions...")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'
    data = dict(contents=[dict(parts=[dict(text=text_prompt)])])
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    recipe_json = parse_recipe_response(response.json())
    return recipe_json

# Example test code
if __name__ == "__main__":
    # Test data with expiry dates
    test_ingredients = [
        {"name": "Eggs", "expiry_date": "2024-02-15"},
        {"name": "Milk", "expiry_date": "2024-02-12"},
        {"name": "Bread", "expiry_date": "2024-02-10"},
        {"name": "Rice", "expiry_date": "2024-03-01"},
        {"name": "Chicken", "expiry_date": "2024-02-11"},
        {"name": "Vegetables", "expiry_date": "2024-02-09"},
        {"name": "Soy Sauce", "expiry_date": "2024-05-01"},
        {"name": "Pasta", "expiry_date": "2024-04-01"}
    ]
    
    recipe = get_recipe_instructions(
        list_of_ingredients=test_ingredients,
        meal_type="Lunch",
        daily_calorie_intake=2000,
        dietary_restrictions="None"
    )
    
    if recipe and recipe.get('recipes'):
        print(json.dumps(recipe, indent=2, ensure_ascii=False))
    else:
        print("No recipes found or error parsing response")

