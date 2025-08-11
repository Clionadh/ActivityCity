import streamlit as st
import random
from pathlib import Path
from datetime import date, timedelta

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"

# Page reruns - change page on first click
# Redirect immediately if booking flag set
if st.session_state.get("go_to_checkout", False):
    st.session_state.page = "checkout"
    st.session_state.go_to_checkout = False
    st.rerun()

# helper function for booking buttons
def book_button(label, key, plan=None, filters=None):
    if st.button(label, key=key):
        if plan is not None:
            st.session_state.selected_plan = plan

        if filters is not None:
            st.session_state.booking_people = filters.get("people")
            st.session_state.booking_day = filters.get("day")
            st.session_state.booking_time = filters.get("time")

        st.session_state.page = "checkout"
        st.rerun()

def generate_match_percentage(is_featured=False):
    """Return a fake match %."""
    if is_featured:
        return random.randint(92, 98)  # Featured gets top match
    return random.randint(75, 90)      # Others get slightly lower

def generate_rating():
    """Return a fake rating (float) and star string."""
    rating_value = round(random.uniform(4.0, 5.0), 1)
    full_stars = int(rating_value)
    half_star = (rating_value - full_stars) >= 0.5
    stars = "★" * full_stars + ("⯨" if half_star else "")
    stars = stars.ljust(5, "☆")  # pad with empty stars
    return rating_value, stars

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="ActivityCity", page_icon="🎯", layout="wide")

# Palette
BLUE = "#81CAD6"      # soft sky blue, main brand colour
YELLOW = "#EDCD44"    # bright, warm yellow accent
RED = "#DC3E26"       # vibrant red accent

BG_LIGHT = "#E9E7E0"  # very light warm cream background to complement yellow
TEXT_DARK = "#A72218" # keep dark text for readability
TEXT_LIGHT = "#E3C5B2" # white for text on dark backgrounds

# Font styles (Streamlit markdown supports inline HTML styles)
HEADER_FONT = "font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 700;"
BODY_FONT = "font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 400;"

# Style overrides for buttons and headers
#background-color: #FFF9E5;  /* very light warm cream */
st.markdown(
    """
    <style>
    /* Page background */
    .main.css-1v3fvcr.egzxvld0 {
        background-color: #EDCD44
    }

    /* Hero container with yellow background */
    .hero-container {
        background-color: #EB6F46;  /* bright warm yellow */
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: #E9E7E0;  /* dark text for contrast */
        margin-bottom: 1.5rem;
    }

    /* Activity cards styling (white bubble) */
    .activity-card {
        background-color: #FFFFFF; /* white background for 'bubble' effect */
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Demo image pools (6 each - we cycle through these for the 100 items)
activity_images = [str(IMAGES_DIR / f"activity{i}.jpg") for i in range(1, 7)]
restaurant_images = [str(IMAGES_DIR / f"restaurant{i}.jpg") for i in range(1, 7)]
combo_images = [str(IMAGES_DIR / f"combo{i}.jpg") for i in range(1, 7)]

# Example allergens
allergens_list = ["Gluten", "Dairy", "Nuts", "Shellfish", "Soy", "Eggs", "Sesame"]

# -----------------------------
# DEMO DATA (50 activities, 50 restaurants)
# matched tags for 'competitive' / 'family friendly' and food features
# -----------------------------

# Activities (50) - adding only is_competitive and is_family_friendly for now as an e.g. 
# Would have full characteristic list for live partners
activities = [
    {"name": "Flight Club Darts", "img": activity_images[0 % len(activity_images)], "is_competitive": True,  "is_family_friendly": False},
    {"name": "Electric Shuffle",   "img": activity_images[1 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Urban Axe Throwing", "img": activity_images[2 % len(activity_images)], "is_competitive": True,  "is_family_friendly": False},
    {"name": "Life-Size Monopoly", "img": activity_images[3 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Escape Quest Rooms", "img": activity_images[4 % len(activity_images)], "is_competitive": True,  "is_family_friendly": False},
    {"name": "TopGolf Arena",      "img": activity_images[5 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Cosmic Bowling",     "img": activity_images[0 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "DNA VR World",       "img": activity_images[1 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Navrtar Battles",    "img": activity_images[2 % len(activity_images)], "is_competitive": True,  "is_family_friendly": False},
    {"name": "Chaos Karts",        "img": activity_images[3 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Electric Gamebox",   "img": activity_images[4 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Ice Rink Central",   "img": activity_images[5 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Curling Corner",     "img": activity_images[0 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "The Clay Bar",       "img": activity_images[1 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Junkyard Mini Golf", "img": activity_images[2 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Sixes Cricket Club", "img": activity_images[3 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Goal! Football Bar", "img": activity_images[4 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Strike Zone Bowling","img": activity_images[5 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Puppy Yoga Loft",   "img": activity_images[0 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "BYOB Pottery",       "img": activity_images[1 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Boozy Paint Nights", "img": activity_images[2 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "The Cauldron Experience", "img": activity_images[3 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Shakeeoke Karaoke",  "img": activity_images[4 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Bunga Bunga Show",   "img": activity_images[5 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Bongo's Bingo",      "img": activity_images[0 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Pub Quiz Palace",    "img": activity_images[1 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "VR Laser Tag",       "img": activity_images[2 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Zombie Escape VR",   "img": activity_images[3 % len(activity_images)], "is_competitive": True,  "is_family_friendly": False},
    {"name": "Mystery Puzzle Rooms","img": activity_images[4 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Adventure Climbing Wall","img": activity_images[5 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Skyline Zipline",    "img": activity_images[0 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Waterfront Kayaking","img": activity_images[1 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Urban Paddleboarding","img": activity_images[2 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "City Bike Tours",    "img": activity_images[3 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Historic Walking Tour","img": activity_images[4 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Foodie Tasting Walk", "img": activity_images[5 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Cocktail Masterclass","img": activity_images[0 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Wine & Cheese Night", "img": activity_images[1 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Craft Beer Trail",    "img": activity_images[2 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Chocolate Making Lab", "img": activity_images[3 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Murder Mystery Dinner","img": activity_images[4 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Theatre Improv Night", "img": activity_images[5 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Silent Disco Tour",    "img": activity_images[0 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Street Art Workshop",  "img": activity_images[1 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Photography Walk",     "img": activity_images[2 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Arcade Bar Blast",     "img": activity_images[3 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Trampoline Park",      "img": activity_images[4 % len(activity_images)], "is_competitive": False, "is_family_friendly": True},
    {"name": "Indoor Skydiving",     "img": activity_images[5 % len(activity_images)], "is_competitive": False, "is_family_friendly": False},
    {"name": "Laser Quest Arena",    "img": activity_images[0 % len(activity_images)], "is_competitive": True,  "is_family_friendly": True},
    {"name": "Surf Simulator",       "img": activity_images[1 % len(activity_images)], "is_competitive": False, "is_family_friendly": True}
]

# Restaurants (50) - each with gluten_free_friendly, vegan_friendly, vegetarian_friendly, meat_friendly, seafood_focused, allergens list
restaurants = [
    {"name": "La Vita Trattoria", "img": restaurant_images[0 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten", "Dairy"]},
    {"name": "The Sizzling Wok",  "img": restaurant_images[1 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": True,  "allergens": ["Soy", "Sesame"]},
    {"name": "Bistro Lumière",    "img": restaurant_images[2 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Dairy"]},
    {"name": "The Curry Pot",     "img": restaurant_images[3 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Dairy", "Nuts"]},
    {"name": "Tapas y Vino",      "img": restaurant_images[4 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": True,  "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten"]},
    {"name": "Ocean Catch Grill", "img": restaurant_images[5 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": True,  "allergens": ["Shellfish", "Fish"]},
    {"name": "Steakhouse Prime",  "img": restaurant_images[0 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": False, "allergens": ["Dairy"]},
    {"name": "Veggie Garden Cafe", "img": restaurant_images[1 % len(restaurant_images)], "gluten_free_friendly": True, "vegan_friendly": True,  "vegetarian_friendly": True,  "meat_friendly": False, "seafood_focused": False, "allergens": ["Nuts"]},
    {"name": "The Dumpling Den",  "img": restaurant_images[2 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten", "Soy"]},
    {"name": "Burger Republic",   "img": restaurant_images[3 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten", "Eggs"]},
    {"name": "Sakura Sushi House","img": restaurant_images[4 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": False, "seafood_focused": True,  "allergens": ["Fish", "Soy"]},
    {"name": "Tandoori Nights",   "img": restaurant_images[5 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Dairy"]},
    {"name": "The Greek Table",   "img": restaurant_images[0 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": True,  "allergens": ["Dairy"]},
    {"name": "El Camino Cantina", "img": restaurant_images[1 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten"]},
    {"name": "Pasta Fresca",      "img": restaurant_images[2 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten", "Dairy"]},
    {"name": "Seoul Kitchen BBQ", "img": restaurant_images[3 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": False, "allergens": ["Soy"]},
    {"name": "French Quarter Bistro","img": restaurant_images[4 % len(restaurant_images)], "gluten_free_friendly": True, "vegan_friendly": False, "vegetarian_friendly": True, "meat_friendly": True, "seafood_focused": False, "allergens": ["Dairy", "Gluten"]},
    {"name": "Spice Bazaar",      "img": restaurant_images[5 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Nuts"]},
    {"name": "Gourmet Vegan Co.", "img": restaurant_images[0 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": True,  "vegetarian_friendly": True,  "meat_friendly": False, "seafood_focused": False, "allergens": ["Nuts"]},
    {"name": "The Pizza Loft",    "img": restaurant_images[1 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten", "Dairy"]},
    {"name": "Riverside Brasserie","img": restaurant_images[2 % len(restaurant_images)], "gluten_free_friendly": True, "vegan_friendly": False, "vegetarian_friendly": True, "meat_friendly": True, "seafood_focused": True, "allergens": ["Fish", "Dairy"]},
    {"name": "The BBQ Pit",       "img": restaurant_images[3 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": False, "allergens": ["Dairy"]},
    {"name": "Coastal Catch",     "img": restaurant_images[4 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": True,  "allergens": ["Shellfish"]},
    {"name": "Urban Deli",        "img": restaurant_images[5 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten"]},
    {"name": "Rustic Oven",       "img": restaurant_images[0 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten", "Dairy"]},
    {"name": "Chili & Lime Cantina","img": restaurant_images[1 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten"]},
    {"name": "Mediterranean Mezze","img": restaurant_images[2 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": True,  "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": True,  "allergens": ["Sesame"]},
    {"name": "Pho Street Kitchen", "img": restaurant_images[3 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Soy"]},
    {"name": "Noodle House 88",    "img": restaurant_images[4 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Gluten", "Soy"]},
    {"name": "Lobster Shack",      "img": restaurant_images[5 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True,  "seafood_focused": True,  "allergens": ["Shellfish"]},
    {"name": "The Breakfast Club", "img": restaurant_images[0 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Eggs", "Dairy"]},
    {"name": "Farm to Fork",       "img": restaurant_images[1 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": True,  "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Nuts"]},
    {"name": "Harbour House Grill", "img": restaurant_images[2 % len(restaurant_images)], "gluten_free_friendly": True, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True, "seafood_focused": True, "allergens": ["Shellfish"]},
    {"name": "Soul Food Spot",      "img": restaurant_images[3 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True, "seafood_focused": False, "allergens": ["Dairy"]},
    {"name": "Kebab House Express", "img": restaurant_images[4 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True, "seafood_focused": False, "allergens": ["Gluten"]},
    {"name": "High Tea Lounge",     "img": restaurant_images[5 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": True, "meat_friendly": False, "seafood_focused": False, "allergens": ["Gluten", "Dairy"]},
    {"name": "The Chocolate Factory","img": restaurant_images[0 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": True, "meat_friendly": False, "seafood_focused": False, "allergens": ["Dairy", "Nuts"]},
    {"name": "Wine Cellar Bar",     "img": restaurant_images[1 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": False, "allergens": ["Dairy"]},
    {"name": "Oyster & Ale House",  "img": restaurant_images[2 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True, "seafood_focused": True, "allergens": ["Shellfish"]},
    {"name": "Plant-Based Paradise","img": restaurant_images[3 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": True,  "vegetarian_friendly": True,  "meat_friendly": False, "seafood_focused": False, "allergens": ["Nuts"]},
    {"name": "Meatball & Co.",      "img": restaurant_images[4 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True, "seafood_focused": False, "allergens": ["Gluten", "Dairy"]},
    {"name": "Fusion Street Eats",  "img": restaurant_images[5 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": True,  "vegetarian_friendly": True,  "meat_friendly": True, "seafood_focused": False, "allergens": ["Soy"]},
    {"name": "Pancake Parlour",     "img": restaurant_images[0 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": True, "meat_friendly": False, "seafood_focused": False, "allergens": ["Eggs", "Gluten"]},
    {"name": "Hotpot Heaven",       "img": restaurant_images[1 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True, "seafood_focused": True, "allergens": ["Soy", "Shellfish"]},
    {"name": "Dim Sum Delight",     "img": restaurant_images[2 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True, "seafood_focused": False, "allergens": ["Gluten", "Soy"]},
    {"name": "Tex-Mex Tavern",      "img": restaurant_images[3 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": False, "vegetarian_friendly": False, "meat_friendly": True, "seafood_focused": False, "allergens": ["Gluten"]},
    {"name": "The Ice Creamery",    "img": restaurant_images[4 % len(restaurant_images)], "gluten_free_friendly": False, "vegan_friendly": True,  "vegetarian_friendly": True,  "meat_friendly": False, "seafood_focused": False, "allergens": ["Dairy", "Nuts"]},
    {"name": "Sea Breeze Cafe",     "img": restaurant_images[5 % len(restaurant_images)], "gluten_free_friendly": True,  "vegan_friendly": False, "vegetarian_friendly": True,  "meat_friendly": True,  "seafood_focused": True,  "allergens": ["Shellfish"]},
    {"name": "Urban Taproom",       "img": restaurant_images[0 % len(restaurant_images)], "gluten_free_friendly": True, "vegan_friendly": False, "vegetarian_friendly": True, "meat_friendly": True, "seafood_focused": False, "allergens": ["Gluten"]}
]

# -----------------------------
# Filtering helpers (loose matching)
# -----------------------------
def filter_activities_by_vibe(vibe):
    """Loose matching: if vibe is 'Competitive' return activities that are competitive.
       For other vibes we return full pool (loose behaviour) to avoid over-restricting."""
    if vibe == "Competitive":
        return [a for a in activities if a.get("is_competitive")]
    # For 'Fun', 'Relaxed', 'Romantic' we keep broad results (loose filter)
    return activities.copy()

def filter_restaurants_by_pref(food_pref, allergens_selected):
    """Loose matching for food preference:
       - Vegetarian-friendly => vegetarian_friendly OR vegan_friendly
       - Vegan-friendly => vegan_friendly
       - Seafood => seafood_focused
       - Meat Lover => meat_friendly
       - Any => all restaurants
       Additionally filter out restaurants that list any of the selected allergens."""
    pool = restaurants.copy()
    if food_pref and food_pref != "Any":
        key = food_pref
        if key == "Vegetarian-friendly":
            pool = [r for r in pool if r.get("vegetarian_friendly") or r.get("vegan_friendly")]
        elif key == "Vegan-friendly":
            pool = [r for r in pool if r.get("vegan_friendly")]
        elif key == "Seafood":
            pool = [r for r in pool if r.get("seafood_focused")]
        elif key == "Meat Lover":
            pool = [r for r in pool if r.get("meat_friendly")]
    # Allergens: the user chooses allergens they want to avoid - exclude restaurants that list those allergens
    if allergens_selected:
        filtered = []
        for r in pool:
            r_allergens = [a.lower() for a in r.get("allergens", [])]
            avoid = False
            for a in allergens_selected:
                if a.lower() in r_allergens:
                    avoid = True
                    break
            if not avoid:
                filtered.append(r)
        pool = filtered
    return pool

# -----------------------------
# FUNCTIONS (generate_plan + booking flow)
# -----------------------------
def generate_plan(filters):
    """Generate a featured plan and explore_more list based on structured data and loose filters."""
    plan_type = filters.get("type", "Any")
    vibe = filters.get("vibe", "Any")
    food_pref = filters.get("food_pref", "Any")
    allergens = filters.get("allergens", []) or []

    # Prepare pools
    activity_pool = filter_activities_by_vibe(vibe)
    restaurant_pool = filter_restaurants_by_pref(food_pref, allergens)

    # If user picked Activity only
    if plan_type == "Activity":
        if not activity_pool:
            return None, []
        act = random.choice(activity_pool)
        featured = {
            "activity": act["name"],
            "activity_img": act["img"],
            "reasoning": f"You chose an activity-only plan, so here’s **{act['name']}** - an exciting experience just for you!"
        }
        explore_more = []
        # Build explore more from activity_pool (loose)
        candidates = random.sample(activity_pool, min(4, len(activity_pool)))
        for c in candidates:
            explore_more.append({"activity": c["name"], "img": c["img"]})
        return featured, explore_more

    # If user picked Food only
    if plan_type == "Food":
        if not restaurant_pool:
            return None, []
        rest = random.choice(restaurant_pool)
        featured = {
            "restaurant": rest["name"],
            "restaurant_img": rest["img"],
            "reasoning": f"You chose a food-only plan, so enjoy dining at **{rest['name']}**, a top restaurant pick!"
        }
        explore_more = []
        candidates = random.sample(restaurant_pool, min(4, len(restaurant_pool)))
        for c in candidates:
            explore_more.append({"restaurant": c["name"], "img": c["img"]})
        return featured, explore_more

    # Combo or Any: pick one activity and one restaurant from respective pools (loose)
    # If either pool empty, return None
    if not activity_pool or not restaurant_pool:
        return None, []
    act = random.choice(activity_pool)
    rest = random.choice(restaurant_pool)
    walk_time = random.randint(2, 12)
    reasoning = (
        f"You told us you’re looking for {vibe} vibes for {filters.get('occasion','a great day out')} occasion - "
        f"so we paired you with **{act['name']}**, just {walk_time} minutes from the buzzing **{rest['name']}**. "
        f"Start your day with this exciting experience, then stroll over for a great meal."
    )
    featured = {
        "activity": act["name"],
        "restaurant": rest["name"],
        "activity_img": act["img"],
        "restaurant_img": rest["img"],
        "combo_img": random.choice(combo_images),
        "reasoning": reasoning
    }

    # Explore more combos (loose)
    explore_more = []
    # create up to 4 combos mixing items from both pools
    for _ in range(min(4, len(activity_pool), len(restaurant_pool))):
        a = random.choice(activity_pool)
        r = random.choice(restaurant_pool)
        explore_more.append({"activity": a["name"], "restaurant": r["name"], "img": random.choice(combo_images)})

    return featured, explore_more

if "friends" not in st.session_state:
    st.session_state.friends = []

def booking_flow():
    st.subheader("🛒 Checkout")
    #st.write("Please confirm your booking details below.")
    #st.date_input("Date", value=date.today())
    #st.time_input("Time", key="booking_time")
    #st.number_input("Number of people", min_value=1, value=2)
    if st.button("Confirm Booking"):
        st.session_state.page = "home"
        st.write("Thank you for your booking. Have the best time!")
        #st.rerun()


def add_friends():
    st.subheader("👥 Invite Friends")
    email = st.text_input("Friend's email")
    if st.button("Add Friend") and email:
        st.session_state.friends.append(email)
        #st.rerun()
    if st.session_state.friends:
        st.write("Invited:", ", ".join(st.session_state.friends))
        if st.button("Continue to Preferences"):
            st.session_state.page = "friend_prefs"
            #st.rerun()

def friend_preferences():
    st.subheader("🎯 Friend Preferences")
    for friend in st.session_state.friends:
        st.write(f"Preferences for {friend}:")
        st.selectbox("Vibe", ["Fun", "Relaxed", "Competitive", "Romantic"], key=f"{friend}_vibe")
        st.multiselect("Food preferences", ["Vegetarian", "Vegan", "Meat Lover", "Seafood"], key=f"{friend}_food")
    if st.button("Generate Best Match"):
        st.session_state.page = "best_match"
        #st.rerun()

def best_match():
    st.subheader("✨ Your Group's Perfect Day")
    st.write("Based on everyone's preferences, here’s what we think you'll love:")
    st.image(random.choice(combo_images), use_container_width=True)
    st.markdown("**Activity:** " + random.choice([a["name"] for a in activities]))
    st.markdown("**Restaurant:** " + random.choice([r["name"] for r in restaurants]))
    if st.button("Confirm & Book"):
        st.session_state.page = "confirmation"
        #st.rerun()

def confirmation():
    st.success("🎉 Booking confirmed! Have an amazing day out!")
    st.balloons()

# -----------------------------
# APP FLOW (UI) - 
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "friends" not in st.session_state:
    st.session_state.friends = []

# Hero with gradient background & styled text
st.markdown(
    """
    <div class="hero-container">
        <h1 style="margin-bottom: 0;">🎯 ActivityCity</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem;">Plan and book your perfect day out in seconds - activities, restaurants, and everything in between.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Filters
st.subheader("🔍 Find Your Perfect Day")
cols = st.columns(5)
city = cols[0].selectbox("City", ["London", "Manchester", "Birmingham"])
people = cols[1].number_input("People", 1, 20, 2)
day = cols[2].date_input("Day", date.today())
time = cols[3].time_input("Time", key="filter_time")
atype = cols[4].selectbox("Type", ["Activity + Food","Activity", "Food"])

with st.expander("More Filters"):
    occasion = st.selectbox("Occasion", ["Any", "Birthday", "Date Night", "Team Event"])
    vibe = st.selectbox("Vibe", ["Any", "Fun", "Relaxed", "Competitive", "Romantic"])
    food_pref = st.selectbox("Food Preference", ["Any", "Vegetarian-friendly", "Vegan-friendly", "Seafood", "Meat Lover"])
    allergens = st.multiselect("Allergens", allergens_list)
    walk_dist = st.slider("Max Walking Distance (mins)", 1, 15, 5)

filters = {
    "city": city,
    "people": people,
    "day": day,
    "time": time,
    "type": atype,
    "occasion": occasion,
    "vibe": vibe,
    "food_pref": food_pref,
    "allergens": allergens,
    "walk_dist": walk_dist
}
if st.session_state.page == "home":
    
# Page logic

# -----------------------------
# Invite Friends & Combine Preferences
# -----------------------------

# Ensure session state variables exist
    if "friends" not in st.session_state:
        st.session_state.friends = []
    if "friends_prefs" not in st.session_state:
        st.session_state.friends_prefs = []

    with st.expander("👥 Invite friends"):
    
        st.markdown("### 👥 Invite friends for their preferences")
        contact_input = st.text_input("Friend's email or phone number")

        if st.button("Add Friend"):
            if contact_input and contact_input not in st.session_state.friends:
                st.session_state.friends.append(contact_input)
                st.success(f"📩 Request for preferences sent to {contact_input}")

                # Generate demo prefs once for this friend
                possible_vibes = ["Fun", "Relaxed", "Competitive", "Romantic"]
                possible_food = ["Vegetarian-friendly", "Vegan-friendly", "Seafood", "Meat Lover"]
                demo_vibe = random.choice(possible_vibes)
                demo_food = random.choice(possible_food)

                st.session_state.friends_prefs.append({
                    "name": contact_input,
                    "vibe": demo_vibe,
                    "food_pref": [demo_food]
                })

        if st.session_state.friends:
            st.write("Invited Friends:", ", ".join(st.session_state.friends))

            for fp in st.session_state.friends_prefs:
                st.info(f"Demo: {fp['name']} prefers {fp['vibe']} vibes and {fp['food_pref'][0]} food.")

            # Reset button for demo purposes
            if st.button("🔄 Reset Friends & Preferences"):
                st.session_state.friends = []
                st.session_state.friends_prefs = []
                st.rerun()

        # -----------------------------
        # Combine all preferences (user + friends)
        # -----------------------------
        friends_prefs = [{"vibe": f["vibe"], "food_pref": f["food_pref"]} for f in st.session_state.friends_prefs]

        combined_vibes = [filters["vibe"]] if filters["vibe"] != "Any" else []
        combined_food = [filters["food_pref"]] if filters["food_pref"] != "Any" else []

        for fp in friends_prefs:
            if fp["vibe"]:
                combined_vibes.append(fp["vibe"])
            combined_food.extend(fp["food_pref"])

        # Remove duplicates
        combined_vibes = list(set([v for v in combined_vibes if v]))
        combined_food = list(set([f for f in combined_food if f]))

        # -----------------------------
        # Decide whether to include friends' preferences
        # -----------------------------
        filters_to_use = filters.copy()

        if friends_prefs:
            use_friends_prefs = st.checkbox("✅ Include friends' preferences in results", value=True)
            if use_friends_prefs:
                if combined_vibes:
                    filters_to_use["vibe"] = combined_vibes[0]
                if combined_food:
                    filters_to_use["food_pref"] = combined_food[0]



        featured, explore_more = generate_plan(filters_to_use)
        
        # Save filters_to_use in session_state
    
    st.session_state.filters_to_use = filters_to_use
    match_pct = generate_match_percentage(is_featured=True)
    rating_value, rating_stars = generate_rating()

    # Featured Match display

    # Wrapper function to handle button clicks and state change with rerun

    st.markdown("## 🔥 Your Featured Match")

    if not featured:
        st.info("No matches found for your selected filters and friends' preferences. Try changing filters or friends preferences.")
    else:
        # Activity only
        if filters_to_use["type"] == "Activity":
            left_col, right_col = st.columns([1, 2])
            with left_col:
                st.image(featured["activity_img"], use_container_width=True, width=250)
            with right_col:
                st.markdown(f"### 🏆 {featured['activity']}")
                st.markdown(f"**🎯 Match:** {match_pct}% ")
                st.markdown(f"**💫 Rating:** {rating_value} {rating_stars}")
                st.markdown(f"💡 *Why we picked this for you:* {featured['reasoning']}")
                book_button("Book Now", key="featured_book", plan=featured, filters=filters_to_use)

        # Food only
        elif filters_to_use["type"] == "Food":
            left_col, right_col = st.columns([1, 2])
            with left_col:
                st.image(featured["restaurant_img"], use_container_width=True, width=250)
            with right_col:
                st.markdown(f"### 🏆 {featured['restaurant']}")
                st.markdown(f"**🎯 Match:** {match_pct}% ")
                st.markdown(f"**💫 Rating:** {rating_value} {rating_stars}")
                st.markdown(f"💡 *Why we picked this for you:* {featured['reasoning']}")
                book_button("Book Now", key="featured_book", plan=featured, filters=filters_to_use)

        # Combo or Any
        else:
            left_col, right_col = st.columns([1, 2])
            with left_col:
                st.image(featured["combo_img"], use_container_width=True, width=250)
            with right_col:
                st.markdown(f"### 🏆 {featured['activity']} + {featured['restaurant']}")
                st.markdown(f"**🎯 Match:** {match_pct}% ")
                st.markdown(f"**💫 Rating:** {rating_value} {rating_stars}")                
                st.markdown(f"💡 *Why we picked this for you:* {featured['reasoning']}")
                book_button("Book Now", key="featured_book", plan=featured, filters=filters_to_use)


        st.markdown("---")
        st.markdown("## 🔎 Explore More Options")

        cols = st.columns(4)
    for idx, plan in enumerate(explore_more):
        with cols[idx]:
            img = plan.get("img")
            if img:
                st.image(img, use_container_width=True)
            match_pct = generate_match_percentage(is_featured=False)
            rating_value, rating_stars = generate_rating()

            if filters_to_use["type"] == "Activity":
                st.markdown(f"**{plan['activity']}**")
                st.markdown(f"🎯 Match: {match_pct}% ")
                st.markdown(f"💫 Rating: {rating_value} {rating_stars}") 
                book_button(f"Book {idx}", f"book_more_{idx}", plan=plan,)
            elif filters_to_use["type"] == "Food":
                st.markdown(f"**{plan['restaurant']}**")
                st.markdown(f"🎯 Match: {match_pct}% ")
                st.markdown(f"💫 Rating: {rating_value} {rating_stars}") 
                book_button(f"Book {idx}", f"book_more_{idx}", plan=plan)
            else:
                st.markdown(f"**{plan['activity']} + {plan['restaurant']}**")       
                st.markdown(f"🎯 Match: {match_pct}% ")
                st.markdown(f"💫 Rating: {rating_value} {rating_stars}") 
                book_button(f"Book {idx}", f"book_more_{idx}", plan=plan)
        
    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.8rem; color:gray;'><em>""Disclaimer: All data and recommendations are for demonstration purposes only. "
        "Side effects may include spontaneous hunger, wanderlust, and an overwhelming urge to plan the best day ever. "
        "Proceed with caution. 🍕" "</em></p>",
        unsafe_allow_html=True
    )

elif st.session_state.page == "checkout":

    filters_to_use = st.session_state.get("filters_to_use")
    
    if filters_to_use is None:
        st.warning("Filters not set. Please go back and select your preferences.")
        st.stop()  # stops execution here

    if st.button("← Back to Search"):
        st.session_state.page = "home"
        st.rerun()

    plan = st.session_state.get("selected_plan")

    people = st.session_state.get("booking_people", 2)
    day = st.session_state.get("booking_day", date.today())
    time = st.session_state.get("booking_time", None)

    if plan:
        st.markdown(f"## Booking Details")
        st.write("Please confirm your booking details below.")
        if filters_to_use["type"] == "Activity":
            st.write(f"You are heading to: {plan.get('activity')}")
        elif filters_to_use["type"] == "Food":
            st.write(f"You are heading to: {plan.get('restaurant')}")
        else:
            st.write(f"You are heading to: {plan.get('activity')} + {plan.get('restaurant')}")

        st.write(f"Date: {day}")
        st.write(f"Time: {time}")
        st.write(f"People: {people}")

        booking_flow()
        st.markdown("---")
        st.markdown(
            "<p style='font-size:0.8rem; color:gray;'><em>""Disclaimer: All data and recommendations are for demonstration purposes only. "
            "Side effects may include spontaneous hunger, wanderlust, and an overwhelming urge to plan the best day ever. "
            "Proceed with caution. 🍕" "</em></p>",
            unsafe_allow_html=True
        )
    else:
        st.warning("No plan selected. Please go back and select a plan.")

