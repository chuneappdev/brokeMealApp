# Fridge to Fork �✨

A Flask web application that helps people discover delicious recipe ideas based on ingredients they already have in their fridge or pantry.

## Features

- 🥘 **Ingredient-Based Recipes**: Enter your available ingredients and get personalized meal suggestions
- 🤖 **AI-Powered Suggestions**: GPT-powered recipe recommendations (with fallback options)
- 📱 **Mobile-Friendly**: Responsive design that works on all devices
- 🎯 **SEO Optimized**: Built for high search engine visibility
- 💸 **Monetization Ready**: AdSense integration and affiliate link support
- 🌟 **Smart Cooking**: Reduce food waste by using what you already have

## Live Demo

Visit the app at: [Your Railway URL here]

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI**: OpenAI GPT-3.5 Turbo
- **Deployment**: Railway
- **Monetization**: Google AdSense, Affiliate Links

## Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chuneappdev/brokeMealApp.git
   cd brokeMealApp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key (optional)
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Visit**: http://localhost:5000

### Deploy to Railway

1. **Connect your GitHub repository to Railway**
2. **Set environment variables** in Railway dashboard:
   - `OPENAI_API_KEY` (optional - for GPT suggestions)
   - `FLASK_ENV=production`
3. **Deploy** - Railway will automatically detect and deploy your Flask app

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT recipe suggestions | No (fallback available) |
| `FLASK_ENV` | Flask environment (development/production) | No (defaults to production) |
| `PORT` | Port for the application | No (Railway sets automatically) |

## How It Works

1. **User Input**: Users enter ingredients they have available
2. **AI Processing**: OpenAI GPT analyzes the ingredients and generates personalized recipe suggestions
3. **Fallback System**: If GPT is unavailable, the app uses curated recipe databases
4. **Results**: Users get 5 recipe ideas with ingredients and cooking instructions

## Monetization Strategy

### Google AdSense
- Cooking and recipe related ads
- Kitchen tool advertisements
- Food-related content

### Affiliate Marketing
- **Kitchen Tools**: Amazon affiliate links for cooking equipment
- **Cookbooks**: Recipe book recommendations
- **Ingredient Delivery**: Fresh ingredient delivery services
- **Meal Kits**: Cooking subscription services

### Target Keywords
- "recipe ideas with ingredients"
- "what to cook with"
- "fridge ingredients recipes"
- "cooking with what you have"
- "meal ideas from ingredients"

## Features for SEO

- Semantic HTML structure
- Meta tags for social sharing
- Mobile-responsive design
- Fast loading times
- Internal linking structure
- Recipe schema markup ready
- Content-rich pages

## File Structure

```
brokeMealApp/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
│
├── templates/
│   └── index.html        # Main application page
│
└── static/ (optional)
    ├── css/
    ├── js/
    └── images/
```

## API Endpoints

- `GET /` - Main application page
- `POST /get_meals` - Get recipe suggestions based on available ingredients
- `GET /health` - Health check endpoint

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit: `git commit -am 'Add new feature'`
5. Push: `git push origin feature-name`
6. Create a Pull Request

## Future Enhancements

- [ ] User accounts and recipe favorites
- [ ] Shopping list generation for missing ingredients
- [ ] Nutritional information
- [ ] Dietary restriction filters
- [ ] Recipe ratings and reviews
- [ ] Social sharing features
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Recipe photo uploads

## License

MIT License - feel free to use this project for your own purposes.

## Support

If you find this project helpful, consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 📢 Sharing with friends

---

Built with ❤️ for home cooks everywhere 👩‍��‍🍳
