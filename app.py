from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Fallback meal suggestions for when API is not available
FALLBACK_MEALS = {
    "under_5": [
        {"name": "Ramen Noodle Upgrade", "ingredients": ["instant ramen", "egg", "any vegetables"], "cost": "$2-3", "instructions": "Cook ramen, add beaten egg while hot, mix in any leftover vegetables"},
        {"name": "Rice & Bean Bowl", "ingredients": ["rice", "canned beans", "onion", "garlic"], "cost": "$3-4", "instructions": "Cook rice, sauté onion and garlic, mix with heated beans"},
        {"name": "Pasta with Garlic Oil", "ingredients": ["pasta", "garlic", "olive oil", "parmesan"], "cost": "$2-3", "instructions": "Cook pasta, sauté minced garlic in oil, toss with pasta"},
        {"name": "Egg Fried Rice", "ingredients": ["rice", "eggs", "soy sauce", "any vegetables"], "cost": "$3-4", "instructions": "Cook rice, scramble eggs, mix together with soy sauce"},
        {"name": "Grilled Cheese & Soup", "ingredients": ["bread", "cheese", "canned tomato soup"], "cost": "$4-5", "instructions": "Make grilled cheese sandwich, heat soup, enjoy together"}
    ],
    "under_10": [
        {"name": "Chicken Thigh Stir-fry", "ingredients": ["chicken thighs", "mixed vegetables", "rice", "soy sauce"], "cost": "$7-8", "instructions": "Cook chicken thighs, stir-fry with vegetables, serve over rice"},
        {"name": "Spaghetti with Meat Sauce", "ingredients": ["ground beef", "pasta", "tomato sauce", "onion"], "cost": "$8-9", "instructions": "Brown ground beef with onion, add tomato sauce, serve over pasta"},
        {"name": "Bean and Cheese Quesadilla", "ingredients": ["tortillas", "cheese", "canned beans", "salsa"], "cost": "$6-7", "instructions": "Fill tortillas with cheese and beans, cook until crispy, serve with salsa"},
        {"name": "Tuna Pasta Salad", "ingredients": ["pasta", "canned tuna", "mayo", "vegetables"], "cost": "$6-8", "instructions": "Cook pasta, mix with tuna, mayo, and chopped vegetables"},
        {"name": "Chicken Noodle Soup", "ingredients": ["chicken breast", "noodles", "carrots", "celery", "broth"], "cost": "$8-10", "instructions": "Simmer chicken with vegetables in broth, add noodles last 10 minutes"}
    ],
    "under_15": [
        {"name": "Beef Stir-fry with Vegetables", "ingredients": ["beef strips", "broccoli", "bell peppers", "rice"], "cost": "$12-14", "instructions": "Stir-fry beef until almost done, add vegetables, serve over rice"},
        {"name": "Salmon with Sweet Potato", "ingredients": ["salmon fillet", "sweet potato", "green beans"], "cost": "$13-15", "instructions": "Bake salmon and sweet potato, steam green beans, season all well"},
        {"name": "Chicken Parmesan", "ingredients": ["chicken breast", "breadcrumbs", "pasta", "marinara"], "cost": "$11-13", "instructions": "Bread and bake chicken, serve over pasta with marinara sauce"},
        {"name": "Pork Chops with Rice", "ingredients": ["pork chops", "rice", "green vegetables"], "cost": "$10-12", "instructions": "Pan-fry pork chops, serve with rice and steamed vegetables"},
        {"name": "Shrimp Pasta", "ingredients": ["shrimp", "pasta", "garlic", "white wine", "parmesan"], "cost": "$13-15", "instructions": "Sauté shrimp with garlic, deglaze with wine, toss with pasta"}
    ]
}

def get_budget_category(budget):
    """Determine budget category based on amount"""
    if budget < 5:
        return "under_5"
    elif budget < 10:
        return "under_10"
    else:
        return "under_15"

def generate_meal_suggestions_gpt(budget, ingredients):
    """Generate meal suggestions using OpenAI GPT"""
    try:
        if not openai.api_key:
            raise Exception("No OpenAI API key configured")
            
        prompt = f"""
        I have ${budget} to spend on a meal and these ingredients available: {', '.join(ingredients) if ingredients else 'none specific'}.
        
        Please suggest 5 cheap, practical meal ideas that fit this budget. For each meal, provide:
        1. Name of the dish
        2. Complete ingredient list with estimated costs
        3. Brief cooking instructions
        4. Total estimated cost
        
        Focus on simple, nutritious meals that a broke person can actually make. Be realistic about portions and costs.
        Format as JSON with this structure:
        {{
            "meals": [
                {{
                    "name": "dish name",
                    "ingredients": ["ingredient1", "ingredient2"],
                    "cost": "$X-Y",
                    "instructions": "step by step instructions"
                }}
            ]
        }}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that suggests budget-friendly meals."},
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
        category = get_budget_category(budget)
        return FALLBACK_MEALS[category]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_meals', methods=['POST'])
def get_meals():
    try:
        data = request.json
        budget = float(data.get('budget', 0))
        ingredients = data.get('ingredients', [])
        
        # Clean up ingredients list
        ingredients = [ing.strip() for ing in ingredients if ing.strip()]
        
        if budget <= 0:
            return jsonify({'error': 'Please enter a valid budget amount'}), 400
        
        # Generate meal suggestions
        meals = generate_meal_suggestions_gpt(budget, ingredients)
        
        return jsonify({
            'success': True,
            'budget': budget,
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
