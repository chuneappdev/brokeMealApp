from flask import Flask, render_template, request, jsonify, redirect
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

# Configure for Railway deployment
app.config['SERVER_NAME'] = None  # Let Railway handle the domain
if os.getenv('RAILWAY_ENVIRONMENT') == 'production':
    app.config['PREFERRED_URL_SCHEME'] = 'https'

# Configure OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None
    print("Warning: OPENAI_API_KEY not found. App will use fallback meals only.")

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
    },
    {
        "name": "Grilled Cheese Sandwich", 
        "ingredients": ["bread", "cheese", "butter"], 
        "instructions": "Butter bread, add cheese, cook in pan until golden and cheese melts",
        "detailed_instructions": "Prep Time: 3 minutes | Cook Time: 6 minutes | Serves: 1\n\n1. Heat a non-stick pan or skillet over medium heat\n2. Butter one side of each bread slice generously\n3. Place one slice butter-side down in the pan\n4. Add your favorite cheese on top (cheddar, swiss, or american work great)\n5. Top with second bread slice, butter-side up\n6. Cook for 2-3 minutes until golden brown on bottom\n7. Flip carefully with spatula and cook 2-3 minutes more\n8. Remove when both sides are golden and cheese is melted\n9. Let cool for 1 minute, then cut diagonally\n\nTip: Medium heat prevents burning while ensuring the cheese melts completely!"
    },
    {
        "name": "Basic Stir-fry", 
        "ingredients": ["vegetables", "oil", "garlic", "soy sauce"], 
        "instructions": "Heat oil, add garlic, stir-fry vegetables until tender, season with soy sauce",
        "detailed_instructions": "Prep Time: 8 minutes | Cook Time: 8 minutes | Serves: 3-4\n\n1. Prep all vegetables by cutting into similar-sized pieces\n2. Heat 2 tbsp oil in a large wok or pan over high heat\n3. Add 2-3 minced garlic cloves, stir for 30 seconds\n4. Add harder vegetables first (carrots, bell peppers, broccoli)\n5. Stir-fry for 2-3 minutes until slightly tender\n6. Add softer vegetables (zucchini, mushrooms, greens)\n7. Continue stir-frying for 2-3 minutes more\n8. Add 2-3 tbsp soy sauce and toss to coat\n9. Taste and adjust seasoning\n10. Serve immediately over rice or noodles\n\nTip: Keep ingredients moving in the pan for even cooking!"
    },
    {
        "name": "Vegetable Omelet", 
        "ingredients": ["eggs", "cheese", "vegetables", "butter"], 
        "instructions": "Beat eggs, pour into heated pan, add fillings, fold in half when set",
        "detailed_instructions": "Prep Time: 5 minutes | Cook Time: 8 minutes | Serves: 2\n\n1. Beat 4-6 eggs in a bowl with salt and pepper\n2. Prep vegetables: dice onions, bell peppers, mushrooms, etc.\n3. Heat 1 tbsp butter in a non-stick pan over medium heat\n4. Sauté vegetables for 2-3 minutes until softened\n5. Pour beaten eggs over vegetables\n6. Let eggs set on bottom for 2 minutes without stirring\n7. Add cheese to one half of the omelet\n8. Using a spatula, gently fold omelet in half\n9. Cook 1-2 minutes more until cheese melts\n10. Slide onto plate and serve hot\n\nTip: Don't overfill or the omelet will be hard to fold!"
    }
]

def generate_meal_suggestions_gpt(ingredients):
    """Generate meal suggestions using OpenAI GPT based on available ingredients"""
    try:
        if not client or not client.api_key:
            print("No OpenAI API key configured, using fallback meals")
            return FALLBACK_MEALS[:5]  # Return first 5 fallback meals
            
        prompt = f"""
        I have these ingredients available: {', '.join(ingredients) if ingredients else 'basic pantry staples'}.
        
        Please suggest exactly 5 meal ideas I can make with these ingredients. 
        
        IMPORTANT: Respond ONLY with valid JSON in this exact format (no extra text):
        {{
            "meals": [
                {{
                    "name": "dish name",
                    "ingredients": ["ingredient1", "ingredient2"],
                    "instructions": "brief cooking instructions for display",
                    "detailed_instructions": "Prep Time: X minutes | Cook Time: X minutes | Serves: X\\n\\n1. Step one\\n2. Step two\\n3. Step three\\n\\nTip: helpful cooking tip"
                }}
            ]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant. Respond ONLY with valid JSON in the exact format requested. No additional text or explanations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        print(f"OpenAI Response: {content[:200]}...")  # Debug print
        
        # Clean up common JSON issues
        if content.startswith('```json'):
            content = content.replace('```json', '').replace('```', '').strip()
        elif content.startswith('```'):
            content = content.replace('```', '').strip()
            
        # Try to parse JSON from the response
        try:
            result = json.loads(content)
            meals = result.get("meals", [])
            if len(meals) > 0:
                print(f"Successfully got {len(meals)} AI-generated meals")
                return meals
            else:
                raise Exception("No meals in response")
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw content: {content}")
            raise Exception("Invalid JSON response from API")
            
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        print("Falling back to predefined suggestions")
        # Fall back to predefined suggestions
        return FALLBACK_MEALS[:5]

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

@app.before_request
def force_https():
    """Force HTTPS on Railway production"""
    if os.getenv('RAILWAY_ENVIRONMENT') == 'production':
        if request.headers.get('X-Forwarded-Proto') == 'http':
            return redirect(request.url.replace('http://', 'https://'), code=301)

@app.after_request
def after_request(response):
    """Add security headers for production"""
    if os.getenv('RAILWAY_ENVIRONMENT') == 'production':
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    # Railway provides PORT environment variable
    port = int(os.environ.get('PORT', 5001))  # Default to 5001 for local development
    debug_mode = os.getenv('FLASK_ENV') == 'development' or os.getenv('RAILWAY_ENVIRONMENT') != 'production'
    
    print(f"Starting Fridge 2 Plate on port {port}")
    if os.getenv('RAILWAY_ENVIRONMENT') == 'production':
        print("Running in Railway production mode")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
