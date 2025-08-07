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
    {
        "name": "Classic Scrambled Eggs", 
        "ingredients": ["eggs", "butter", "salt", "pepper"], 
        "instructions": "Beat eggs, cook in butter over medium heat, stirring gently until fluffy",
        "detailed_instructions": "Prep Time: 2 minutes | Cook Time: 5 minutes | Serves: 2\n\n1. Crack 4-6 eggs into a bowl and beat with a fork until well combined\n2. Add a pinch of salt and pepper to taste\n3. Heat 1 tablespoon butter in a non-stick pan over medium-low heat\n4. Pour in beaten eggs and let sit for 20 seconds\n5. Using a spatula, gently stir and fold the eggs from the edges toward the center\n6. Continue stirring gently every 20-30 seconds until eggs are creamy and just set\n7. Remove from heat while slightly underdone (they'll continue cooking)\n8. Serve immediately\n\nTip: Low heat is key for creamy scrambled eggs!"
    },
    {
        "name": "Simple Pasta", 
        "ingredients": ["pasta", "garlic", "olive oil", "parmesan"], 
        "instructions": "Cook pasta, sauté minced garlic in oil, toss with pasta and cheese",
        "detailed_instructions": "Prep Time: 5 minutes | Cook Time: 12 minutes | Serves: 4\n\n1. Bring a large pot of salted water to boil\n2. Add 1 lb pasta and cook according to package directions until al dente\n3. While pasta cooks, heat 1/4 cup olive oil in a large pan over medium heat\n4. Add 4 minced garlic cloves and cook for 1-2 minutes until fragrant (don't brown)\n5. Reserve 1/2 cup pasta water before draining\n6. Drain pasta and add to the garlic oil pan\n7. Toss with pasta water as needed to create a silky sauce\n8. Remove from heat, add 1/2 cup grated parmesan\n9. Toss until cheese melts and coats pasta\n\nTip: Save pasta water - the starch helps bind the sauce!"
    },
    {
        "name": "Fried Rice", 
        "ingredients": ["rice", "eggs", "soy sauce", "vegetables"], 
        "instructions": "Cook rice, scramble eggs, mix together with soy sauce and any available vegetables",
        "detailed_instructions": "Prep Time: 10 minutes | Cook Time: 15 minutes | Serves: 4\n\n1. Use 3 cups of day-old cooked rice (or cool fresh rice completely)\n2. Heat 2 tbsp oil in a large wok or pan over high heat\n3. Beat 2-3 eggs and scramble in the pan, breaking into small pieces\n4. Remove eggs and set aside\n5. Add 1 tbsp more oil, then add diced vegetables (onions first, then harder veggies)\n6. Stir-fry vegetables for 2-3 minutes until tender-crisp\n7. Add rice, breaking up any clumps with a spatula\n8. Stir-fry for 3-4 minutes until rice is heated through\n9. Return eggs to pan, add 2-3 tbsp soy sauce\n10. Toss everything together and serve hot\n\nTip: Day-old rice works best - fresh rice can get mushy!"
    }
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
        3. Brief cooking instructions for the main display
        4. Detailed step-by-step cooking instructions for copying (include prep time, cook time, serving size, tips)
        
        Focus on practical, tasty meals that someone can actually make with these ingredients. Be creative with combinations.
        Format as JSON with this structure:
        {{
            "meals": [
                {{
                    "name": "dish name",
                    "ingredients": ["ingredient1", "ingredient2"],
                    "instructions": "brief cooking instructions for display",
                    "detailed_instructions": "detailed step-by-step instructions with prep time, cook time, serving size, and helpful tips"
                }}
            ]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional chef assistant that provides detailed, easy-to-follow cooking instructions. Always include prep time, cook time, serving size, and helpful tips in your detailed instructions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500,
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
