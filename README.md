https://web-production-42dc6.up.railway.app/ website host on railway

https://hindu-panchang.onrender.com/ host on render

 
 हिन्दू पंचांग (Hindu Panchang) Website

A comprehensive web application that displays Hindu calendar (Panchang) information including tithis, nakshatras, yogas, karanas, and festivals based on dates.

## Enhanced Features

- **Advanced Panchang Elements**:
  - Tithi calculation with completion percentage
  - Nakshatra information with completion percentage
  - Yoga and Karana details
  - Paksha (Shukla/Krishna) information

- **Extensive Festival Database**:
  - Major Hindu festivals throughout the year
  - Festival notifications and upcoming festival list
  - Festival highlights in calendar view

- **Improved UI/UX**:
  - Beautiful responsive design with animations
  - Tab-based navigation for better organization
  - Interactive calendar with detailed day information
  - Progress bars for tithi and nakshatra completion
  - Informational section about panchang elements

- **Technical Improvements**:
  - More accurate astronomical calculations
  - Optimized API endpoints
  - Better data organization

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Flask (Python)
- **Dependencies**: python-dateutil, requests
- **UI Components**: Font Awesome icons, Google Fonts

## Setup Instructions

1. Clone this repository
```
git clone https://github.com/indianhacker12/hindu-panchang.git
cd hindu-panchang
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the Flask application:
```
python app.py
```

4. Open your browser and navigate to `http://127.0.0.1:5000`

## Deployment Options

### Deploying to Heroku
1. Create a Heroku account and install Heroku CLI
2. Create a `Procfile` in the root directory with:
```
web: gunicorn app:app
```
3. Add gunicorn to requirements.txt
4. Deploy to Heroku:
```
heroku login
heroku create hindu-panchang
git push heroku main
```

### Deploying to PythonAnywhere
1. Create a PythonAnywhere account
2. Upload your code or clone from GitHub
3. Set up a web app with Flask
4. Configure the WSGI file to point to your app.py

### Deploying to Vercel
1. Create a `vercel.json` file:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```
2. Deploy using Vercel CLI or connect your GitHub repository

## Panchang Calculation Method

This application uses a simplified astronomical algorithm for calculating panchang elements:

- **Tithi**: Based on the angular distance between the moon and sun (each tithi = 12 degrees)
- **Nakshatra**: Based on the moon's position in the sky (each nakshatra = 13°20')
- **Yoga**: Based on the sum of the longitudes of the sun and moon
- **Karana**: Half of a tithi (6 degrees of angular distance)

For production applications, consider integrating with professional ephemeris libraries like Swiss Ephemeris for even more accurate calculations.

## Future Improvements

- Add Rashi (zodiac) information
- Include Vara (weekday) significance
- Add muhurta (auspicious timing) functionality
- Support for different regional calendars (North/South Indian)
- Multi-language support (Hindi, Tamil, Telugu, etc.)
- Dark mode theme
- User accounts to save important dates
- Printable monthly panchang

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License

## Credits

Created with ❤️ for the Hindu community#   h i n d u - p a n c h a n g 
 
 #   h i n d u - p a n c h a n g 
 
 
