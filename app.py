from flask import Flask, render_template, request, jsonify
import datetime
import json
import os
import math
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

# Hindu months
HINDU_MONTHS = [
    "Chaitra", "Vaisakha", "Jyeshtha", "Ashadha", 
    "Shravana", "Bhadrapada", "Ashwin", "Kartika", 
    "Margashirsha", "Pausha", "Magha", "Phalguna"
]

# Tithis
TITHIS = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima", "Amavasya"
]

# Nakshatras
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", 
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", 
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", 
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", 
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", 
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Yogas
YOGAS = [
    "Vishkumbha", "Preeti", "Ayushman", "Saubhagya", "Shobhana", 
    "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda", 
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", 
    "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva", 
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", 
    "Indra", "Vaidhriti"
]

# Karanas
KARANAS = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", 
    "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
]

# Extended festivals data
FESTIVALS = {
    "1-1": ["Hindu New Year"],
    "1-9": ["Ram Navami"],
    "2-3": ["Akshaya Tritiya"],
    "3-10": ["Ganga Dussehra"],
    "3-15": ["Vat Purnima"],
    "4-11": ["Devshayani Ekadashi"],
    "5-4": ["Nag Panchami"],
    "5-8": ["Raksha Bandhan"],
    "5-14": ["Janmashtami"],
    "6-3": ["Ganesh Chaturthi"],
    "6-7": ["Onam"],
    "7-1": ["Navratri Begins"],
    "7-9": ["Dussehra"],
    "7-15": ["Sharad Purnima"],
    "8-1": ["Diwali"],
    "8-2": ["Govardhan Puja"],
    "8-5": ["Bhai Dooj"],
    "8-11": ["Devutthana Ekadashi"],
    "9-15": ["Makar Sankranti"],
    "10-5": ["Vasant Panchami"],
    "10-14": ["Maha Shivaratri"],
    "11-15": ["Holi Purnima"],
    "11-16": ["Holika Dahan"],
    "12-9": ["Rama Navami"],
    "12-15": ["Hanuman Jayanti"]
}

def get_lunar_angle(date):
    """
    More accurate algorithm to calculate lunar angle
    This is still a simplified version but more accurate than the previous one
    """
    # Base date for calculation (known position)
    base_date = datetime.date(2023, 1, 1)  # New moon on Jan 1, 2023
    
    # Days since base date
    days_diff = (date - base_date).days
    
    # Lunar month is approximately 29.53 days
    lunar_month = 29.53
    
    # Calculate lunar angle (0 to 360 degrees)
    # One complete lunar cycle is 360 degrees
    lunar_angle = (days_diff % lunar_month) * (360 / lunar_month)
    
    return lunar_angle

def get_solar_angle(date):
    """Calculate solar angle based on day of year"""
    day_of_year = date.timetuple().tm_yday
    return (day_of_year - 1) * (360 / 365.25)

def get_tithi(date):
    """
    Calculate tithi based on lunar angle
    Tithi is the angular distance between the moon and the sun divided by 12 degrees
    """
    lunar_angle = get_lunar_angle(date)
    solar_angle = get_solar_angle(date)
    
    # Calculate the angular distance between moon and sun
    angle_diff = (lunar_angle - solar_angle) % 360
    
    # Each tithi is 12 degrees of angular distance
    tithi_index = int(angle_diff / 12)
    
    # Determine paksha (Shukla or Krishna)
    if tithi_index < 15:
        paksha = "Shukla Paksha"
    else:
        paksha = "Krishna Paksha"
        tithi_index = tithi_index % 15
    
    # Calculate the Hindu month
    # This is a simplified calculation
    solar_month = int((solar_angle / 30) % 12)
    lunar_month = (solar_month + (1 if angle_diff > 180 else 0)) % 12
    
    return {
        "month": HINDU_MONTHS[lunar_month],
        "tithi": TITHIS[tithi_index],
        "paksha": paksha,
        "tithi_index": tithi_index + 1,  # 1-indexed for display
        "completion": (angle_diff % 12) / 12 * 100  # Percentage of tithi completed
    }

def get_nakshatra(date):
    """
    Calculate nakshatra based on lunar angle
    Each nakshatra spans 13°20' (13.33 degrees) of the ecliptic
    """
    lunar_angle = get_lunar_angle(date)
    
    # Each nakshatra is 13.33 degrees
    nakshatra_index = int((lunar_angle % 360) / (360 / 27))
    
    # Calculate completion percentage
    completion = ((lunar_angle % (360 / 27)) / (360 / 27)) * 100
    
    return {
        "nakshatra": NAKSHATRAS[nakshatra_index],
        "index": nakshatra_index + 1,  # 1-indexed for display
        "completion": completion
    }

def get_yoga(date):
    """
    Calculate yoga based on the sum of lunar and solar angles
    Each yoga spans 13°20' (13.33 degrees)
    """
    lunar_angle = get_lunar_angle(date)
    solar_angle = get_solar_angle(date)
    
    # Sum of angles
    sum_angle = (lunar_angle + solar_angle) % 360
    
    # Each yoga is 13.33 degrees
    yoga_index = int(sum_angle / (360 / 27))
    
    return {
        "yoga": YOGAS[yoga_index],
        "index": yoga_index + 1  # 1-indexed for display
    }

def get_karana(date):
    """
    Calculate karana based on lunar angle
    Each karana spans 6 degrees of the ecliptic (half of a tithi)
    """
    lunar_angle = get_lunar_angle(date)
    solar_angle = get_solar_angle(date)
    
    # Calculate the angular distance between moon and sun
    angle_diff = (lunar_angle - solar_angle) % 360
    
    # Each karana is 6 degrees (half of a tithi)
    karana_index = int(angle_diff / 6) % 11
    
    return {
        "karana": KARANAS[karana_index],
        "index": karana_index + 1  # 1-indexed for display
    }

def get_festivals(date):
    """Get festivals for a given date"""
    month_day = f"{date.month}-{date.day}"
    return FESTIVALS.get(month_day, [])

@app.route('/')
def index():
    today = datetime.date.today().strftime('%Y-%m-%d')
    return render_template('index.html', today=today)

@app.route('/api/panchang', methods=['POST'])
def get_panchang():
    data = request.json
    date_str = data.get('date')
    
    try:
        # Parse date from string (format: YYYY-MM-DD)
        year, month, day = map(int, date_str.split('-'))
        date = datetime.date(year, month, day)
        
        # Get panchang elements
        tithi_info = get_tithi(date)
        nakshatra_info = get_nakshatra(date)
        yoga_info = get_yoga(date)
        karana_info = get_karana(date)
        festivals = get_festivals(date)
        
        return jsonify({
            "success": True,
            "date": date_str,
            "hindu_month": tithi_info["month"],
            "tithi": tithi_info["tithi"],
            "tithi_number": tithi_info["tithi_index"],
            "tithi_completion": round(tithi_info["completion"], 2),
            "paksha": tithi_info["paksha"],
            "nakshatra": nakshatra_info["nakshatra"],
            "nakshatra_number": nakshatra_info["index"],
            "nakshatra_completion": round(nakshatra_info["completion"], 2),
            "yoga": yoga_info["yoga"],
            "yoga_number": yoga_info["index"],
            "karana": karana_info["karana"],
            "karana_number": karana_info["index"],
            "festivals": festivals
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/calendar', methods=['POST'])
def get_calendar():
    data = request.json
    year = int(data.get('year', datetime.datetime.now().year))
    month = int(data.get('month', datetime.datetime.now().month))
    
    # Get first day of month
    first_day = datetime.date(year, month, 1)
    
    # Get last day of month
    if month == 12:
        last_day = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
    
    # Generate calendar data
    calendar_data = []
    current_date = first_day
    
    while current_date <= last_day:
        tithi_info = get_tithi(current_date)
        nakshatra_info = get_nakshatra(current_date)
        festivals = get_festivals(current_date)
        
        calendar_data.append({
            "date": current_date.day,
            "tithi": tithi_info["tithi"],
            "paksha": tithi_info["paksha"],
            "nakshatra": nakshatra_info["nakshatra"],
            "festivals": festivals
        })
        
        current_date += datetime.timedelta(days=1)
    
    return jsonify({
        "success": True,
        "year": year,
        "month": month,
        "days": calendar_data
    })

@app.route('/api/upcoming-festivals', methods=['GET'])
def upcoming_festivals():
    # Get next 60 days
    festivals_list = []
    start_date = datetime.date.today()
    
    for i in range(60):
        current_date = start_date + datetime.timedelta(days=i)
        festivals = get_festivals(current_date)
        
        if festivals:
            festivals_list.append({
                "date": current_date.strftime('%Y-%m-%d'),
                "formatted_date": current_date.strftime('%d %b %Y'),
                "festivals": festivals
            })
    
    return jsonify({
        "success": True,
        "festivals": festivals_list[:10]  # Return only next 10 festivals
    })

if __name__ == '__main__':
    app.run(debug=True) 