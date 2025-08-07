# Broke Meal Planner 🍜💰

A Flask web application that helps broke college students and budget-conscious people find cheap, delicious meal ideas based on their budget and available ingredients.

## Features

- 💰 **Budget-Based Meal Planning**: Enter your budget and get meal suggestions that fit
- 🥘 **Ingredient Integration**: Use what you already have in your fridge
- 🤖 **AI-Powered Suggestions**: GPT-powered meal recommendations (with fallback options)
- 📱 **Mobile-Friendly**: Responsive design that works on all devices
- 🎯 **SEO Optimized**: Built for high search engine visibility
- 💸 **Monetization Ready**: AdSense integration and affiliate link support

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
   git clone https://github.com/yourusername/broke-meal-planner.git
   cd broke-meal-planner
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
| `OPENAI_API_KEY` | OpenAI API key for GPT meal suggestions | No (fallback available) |
| `FLASK_ENV` | Flask environment (development/production) | No (defaults to production) |
| `PORT` | Port for the application | No (Railway sets automatically) |

## How It Works

1. **User Input**: Users enter their budget and available ingredients
2. **AI Processing**: OpenAI GPT analyzes the input and generates personalized meal suggestions
3. **Fallback System**: If GPT is unavailable, the app uses curated meal databases
4. **Results**: Users get 5 meal ideas with ingredients, costs, and cooking instructions

## Monetization Strategy

### Google AdSense
- Food and cooking related ads
- Budget management tool advertisements
- College student targeted content

### Affiliate Marketing
- **Grocery Delivery**: Instacart, Amazon Fresh, Walmart Grocery
- **Meal Kits**: HelloFresh, Blue Apron (budget options)
- **Kitchen Tools**: Amazon affiliate links for basic cooking equipment
- **Cookbooks**: Budget cookbook recommendations

### Target Keywords
- "cheap meals for college students"
- "budget meal planning"
- "broke recipe ideas"
- "meals under $5"
- "budget grocery shopping"

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
broke-meal-planner/
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
- `POST /get_meals` - Get meal suggestions based on budget and ingredients
- `GET /health` - Health check endpoint

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit: `git commit -am 'Add new feature'`
5. Push: `git push origin feature-name`
6. Create a Pull Request

## Future Enhancements

- [ ] User accounts and meal history
- [ ] Shopping list generation
- [ ] Nutritional information
- [ ] Meal prep planning
- [ ] Social sharing features
- [ ] Recipe ratings and reviews
- [ ] Multi-language support
- [ ] Mobile app version

## License

MIT License - feel free to use this project for your own purposes.

## Support

If you find this project helpful, consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 📢 Sharing with friends

---

Built with ❤️ for broke college students everywhere 🎓💸
