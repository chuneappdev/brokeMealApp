from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

# Configure OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Fallback meal suggestions based on common ingredients
FALLBACK_MEALS = [
    {"name": "Classic Scrambled Eggs", "ingredients": ["eggs", "butter", "salt", "pepper"], "instructions": "Beat eggs, cook in butter over medium heat, stirring gently until fluffy"},
    {"name": "Simple Pasta", "ingredients": ["pasta", "garlic", "olive oil", "parmesan"], "instructions": "Cook pasta, sauté minced garlic in oil, toss with pasta and cheese"},
    {"name": "Fried Rice", "ingredients": ["rice", "eggs", "soy sauce", "vegetables"], "instructions": "Cook rice, scramble eggs, mix together with soy sauce and any available vegetables"},
    {"name": "Grilled Cheese Sandwich", "ingredients": ["bread", "cheese", "butter"], "instructions": "Butter bread, add cheese, cook in pan until golden and cheese melts"},
    {"name": "Basic Stir-fry", "ingredients": ["vegetables", "oil", "garlic", "soy sauce"], "instructions": "Heat oil, add garlic, stir-fry vegetables until tender, season with soy sauce"},
    {"name": "Simple Soup", "ingredients": ["broth", "vegetables", "noodles"], "instructions": "Heat broth, add chopped vegetables, simmer until tender, add noodles if available"},
    {"name": "Omelet", "ingredients": ["eggs", "cheese", "vegetables"], "instructions": "Beat eggs, pour into heated pan, add fillings, fold in half when set"},
    {"name": "Pasta Salad", "ingredients": ["pasta", "vegetables", "oil", "vinegar"], "instructions": "Cook pasta, cool, mix with chopped vegetables and simple oil-vinegar dressing"},
    {"name": "Rice Bowl", "ingredients": ["rice", "protein", "vegetables"], "instructions": "Cook rice, prepare protein and vegetables, serve together in a bowl"},
    {"name": "Sandwich", "ingredients": ["bread", "protein", "vegetables"], "instructions": "Layer ingredients between bread slices, customize with available items"}
]

def generate_meal_suggestions_gpt(ingredients):
    """Generate meal suggestions using OpenAI GPT based on available ingredients"""
    try:
        if not client.api_key:
            raise Exception("No OpenAI API key configured")
            
        prompt = f"""
        I have these ingredients available in my fridge/pantry: {', '.join(ingredients) if ingredients else 'basic pantry staples like salt, pepper, oil'}.
        
        Please suggest 5 delicious meal ideas I can make with these ingredients. For each meal, provide:
        1. Name of the dish
        2. Complete ingredient list (using what I have + basic pantry staples)
        3. Step-by-step cooking instructions
        
        Focus on practical, tasty meals that someone can actually make with these ingredients. Be creative with combinations.
        Format as JSON with this structure:
        {{
            "meals": [
                {{
                    "name": "dish name",
                    "ingredients": ["ingredient1", "ingredient2"],
                    "instructions": "step by step cooking instructions"
                }}
            ]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant that suggests creative meals based on available ingredients."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        # Try to parse JSON from the response
        try:
            result = json.loads(content)
            return result.get("meals", [])
        except json.JSONDecodeError:
            # If JSON parsing fails, use fallback
            raise Exception("Invalid JSON response from API")
            
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        # Fall back to predefined suggestions
        return FALLBACK_MEALS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_meals', methods=['POST'])
def get_meals():
    try:
        data = request.json
        ingredients = data.get('ingredients', [])
        
        # Clean up ingredients list
        ingredients = [ing.strip() for ing in ingredients if ing.strip()]
        
        if not ingredients:
            return jsonify({'error': 'Please enter at least one ingredient'}), 400
        
        # Generate meal suggestions
        meals = generate_meal_suggestions_gpt(ingredients)
        
        return jsonify({
            'success': True,
            'ingredients': ingredients,
            'meals': meals
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
