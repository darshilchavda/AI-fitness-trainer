"""
model/logic.py
==============
Rule-based AI components:
  1. BMI calculator
  2. Workout plan recommender (goal × BMI × age)
  3. Simple NLP chatbot (keyword matching)
  4. Diet recommendation system
  5. Weekly workout planner
  6. Exercise instruction library
"""

# ── 1. BMI Calculator ─────────────────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float):
    """Return (bmi_value, category_string)."""
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25.0:
        category = "Normal"
    elif bmi < 30.0:
        category = "Overweight"
    else:
        category = "Obese"

    return bmi, category


# ── 2. Rule-Based Workout Recommender ────────────────────────────────────────

def get_workout_plan(bmi: float, goal: str, age: int):
    """
    Returns a list of exercise dicts based on goal, BMI, and age.
    Each dict: {exercise, sets, reps, rest, tip}
    """

    # ---- Fat Loss Plans ----
    if goal == 'fat_loss':

        if bmi >= 30:  # Obese – low-impact start
            return [
                {"exercise": "Brisk Walking",      "sets": 1,  "reps": "30 min", "rest": "—",   "tip": "Keep heart rate at 60–70% max"},
                {"exercise": "Wall Push-ups",       "sets": 3,  "reps": 12,       "rest": "60s",  "tip": "Great for upper-body without stress"},
                {"exercise": "Chair Squats",         "sets": 3,  "reps": 15,       "rest": "60s",  "tip": "Stand up slowly for control"},
                {"exercise": "Seated Leg Raises",   "sets": 3,  "reps": 15,       "rest": "45s",  "tip": "Core engagement is key"},
                {"exercise": "Plank (Knee)",         "sets": 3,  "reps": "20s",    "rest": "30s",  "tip": "Build up to a full plank gradually"},
            ]

        elif bmi >= 25:  # Overweight – moderate cardio
            return [
                {"exercise": "Jogging",             "sets": 1,  "reps": "20 min", "rest": "—",   "tip": "Maintain a conversational pace"},
                {"exercise": "Jumping Jacks",        "sets": 3,  "reps": 25,       "rest": "45s",  "tip": "Full range of motion"},
                {"exercise": "Push-ups",             "sets": 3,  "reps": 15,       "rest": "45s",  "tip": "Chest touches floor each rep"},
                {"exercise": "Mountain Climbers",    "sets": 3,  "reps": 20,       "rest": "45s",  "tip": "Drive knees explosively"},
                {"exercise": "Plank",                "sets": 3,  "reps": "30s",    "rest": "30s",  "tip": "Hips level, breathe steadily"},
            ]

        else:  # Normal BMI – aggressive fat burn
            return [
                {"exercise": "Running",             "sets": 1,  "reps": "25 min", "rest": "—",   "tip": "Include 2-min sprint intervals"},
                {"exercise": "Burpees",              "sets": 4,  "reps": 15,       "rest": "40s",  "tip": "Explosive jump at the top"},
                {"exercise": "Push-ups",             "sets": 4,  "reps": 20,       "rest": "30s",  "tip": "Try diamond push-ups for variety"},
                {"exercise": "Box Jumps",            "sets": 3,  "reps": 12,       "rest": "45s",  "tip": "Land softly with bent knees"},
                {"exercise": "Plank",                "sets": 3,  "reps": "45s",    "rest": "30s",  "tip": "Add hip dips for core variety"},
            ]

    # ---- Muscle Gain Plans ----
    elif goal == 'muscle_gain':

        if age < 25:  # Young – higher volume
            return [
                {"exercise": "Push-ups",            "sets": 4,  "reps": 20,       "rest": "60s",  "tip": "Slow eccentric for growth"},
                {"exercise": "Pull-ups",             "sets": 4,  "reps": 10,       "rest": "60s",  "tip": "Full hang to chin-above-bar"},
                {"exercise": "Bodyweight Squats",    "sets": 4,  "reps": 20,       "rest": "60s",  "tip": "Pause at bottom for 1 sec"},
                {"exercise": "Dips (Chair)",         "sets": 3,  "reps": 15,       "rest": "60s",  "tip": "Elbows close to body"},
                {"exercise": "Plank",                "sets": 3,  "reps": "60s",    "rest": "30s",  "tip": "Squeeze glutes and abs hard"},
            ]

        else:  # 25+ – moderate volume, joint-friendly
            return [
                {"exercise": "Push-ups",            "sets": 3,  "reps": 15,       "rest": "75s",  "tip": "Wide grip for chest focus"},
                {"exercise": "Bodyweight Rows",      "sets": 3,  "reps": 12,       "rest": "75s",  "tip": "Under a table; chest to hands"},
                {"exercise": "Lunges",               "sets": 3,  "reps": 12,       "rest": "60s",  "tip": "Keep front knee over ankle"},
                {"exercise": "Pike Push-ups",        "sets": 3,  "reps": 10,       "rest": "60s",  "tip": "Targets shoulders & triceps"},
                {"exercise": "Plank",                "sets": 3,  "reps": "45s",    "rest": "30s",  "tip": "Neutral spine throughout"},
            ]

    # ---- General Fitness (default) ----
    else:
        return [
            {"exercise": "Jumping Jacks",           "sets": 3,  "reps": 25,       "rest": "30s",  "tip": "Full-body warm-up"},
            {"exercise": "Push-ups",                "sets": 3,  "reps": 15,       "rest": "45s",  "tip": "Elbows at 45° angle"},
            {"exercise": "Squats",                  "sets": 3,  "reps": 20,       "rest": "45s",  "tip": "Weight in heels"},
            {"exercise": "Plank",                   "sets": 3,  "reps": "30s",    "rest": "30s",  "tip": "Straight line head to heel"},
            {"exercise": "Walking Lunges",          "sets": 2,  "reps": 12,       "rest": "45s",  "tip": "Step forward, lower slowly"},
        ]


# ── 3. Rule-Based NLP Chatbot ─────────────────────────────────────────────────

# Each entry: (list_of_keywords, response_string)
# The first rule whose ANY keyword is found in the message wins.
_RULES = [
    (
        ['hello', 'hi', 'hey', 'greet'],
        "👋 Hey there! I'm your AI Fitness Coach. Ask me anything about workouts, diet, or health tips!"
    ),
    (
        ['help', 'what can you do', 'options'],
        "💡 I can help with: fat loss, muscle gain, abs, push-ups, squats, diet, protein, sleep, motivation, BMI, and more. Just ask!"
    ),
    (
        ['bmi', 'body mass'],
        "📊 BMI = Weight(kg) ÷ Height(m)². Ranges: <18.5 Underweight | 18.5–24.9 Normal | 25–29.9 Overweight | ≥30 Obese."
    ),
    (
        ['fat loss', 'lose fat', 'burn fat', 'weight loss', 'lose weight'],
        "🔥 Fat Loss Plan: ①  Caloric deficit of ~500 kcal/day ② 30 min cardio (run/cycle) 5×/week ③ Strength train 3×/week to preserve muscle ④ Drink 2–3 L water daily ⑤ Sleep 7–8 hours."
    ),
    (
        ['muscle', 'build muscle', 'gain muscle', 'bulk'],
        "💪 Muscle Gain Tips: ① Progressive overload – add reps/sets weekly ② Eat 1.6 g protein per kg of body weight ③ Compound moves: push-ups, squats, rows ④ Rest 48h between same muscle groups ⑤ Sleep is when muscles grow!"
    ),
    (
        ['abs', 'six pack', 'core', 'stomach'],
        "🎯 Best Core Exercises: Plank (3×45s), Crunches (3×20), Leg Raises (3×15), Mountain Climbers (3×30), Bicycle Crunches (3×20). Remember: abs are made in the kitchen too!"
    ),
    (
        ['push up', 'pushup', 'push-up'],
        "🤸 Push-up Form: Hands slightly wider than shoulders, body in a straight line, lower chest to floor, elbows at 45°. Variations: Wide, Diamond, Decline, Incline."
    ),
    (
        ['squat', 'leg day', 'legs'],
        "🦵 Squat Tips: Feet shoulder-width apart, toes slightly out, sit back into heels, keep chest tall, go below parallel. Great for quads, glutes & hamstrings!"
    ),
    (
        ['plank', 'core hold'],
        "🏋️ Plank: Forearms on floor, body straight as a board, hips level, breathe steadily. Start with 20s and build to 60s+ over weeks."
    ),
    (
        ['diet', 'food', 'eat', 'nutrition', 'meal'],
        "🥗 Fitness Diet Basics: ① Lean protein: eggs, chicken, lentils, paneer ② Complex carbs: oats, brown rice, sweet potato ③ Healthy fats: nuts, avocado ④ Avoid: sugary drinks, ultra-processed food ⑤ Eat every 3–4 hours."
    ),
    (
        ['protein', 'protein intake'],
        "🥚 Protein Sources: Eggs (6g/egg), Chicken breast (31g/100g), Lentils (9g/cup), Greek yoghurt (10g/100g), Paneer (11g/100g). Aim for 1.2–1.6 g/kg body weight."
    ),
    (
        ['sleep', 'recovery', 'rest'],
        "😴 Sleep & Recovery: Muscles repair during sleep. Aim for 7–9 hours. Avoid screens 1 hour before bed. Naps <30 min are ok. Under-sleeping raises cortisol and kills gains!"
    ),
    (
        ['beginner', 'start', 'new to', 'just started'],
        "🌱 Beginner Plan: 3 days/week. Day 1: Push-ups + Squats. Day 2: Rest or walk. Day 3: Plank + Lunges. Day 4: Rest. Day 5: Full-body. Increase intensity every 2 weeks."
    ),
    (
        ['warm up', 'warmup', 'stretch', 'cool down'],
        "🔄 Always warm up for 5–10 min: Jumping jacks, arm circles, leg swings, hip rotations. Cool down: 5 min light walk + full-body stretching. Prevents injury!"
    ),
    (
        ['motivat', 'give up', 'tired', 'lazy'],
        "🚀 Motivation Boost: Every expert was once a beginner. The workout you skip is the one you'll regret. Progress, not perfection. Just do 5 minutes – momentum will carry you. You've got this! 💪"
    ),
    (
        ['water', 'hydrat'],
        "💧 Hydration: Drink 2–3 L of water daily. Add an extra 500 ml per 30 min of exercise. Dehydration reduces performance by up to 20%!"
    ),
    (
        ['cardio', 'running', 'cycling', 'swimming'],
        "🏃 Cardio Tips: 150 min moderate or 75 min vigorous per week (WHO guideline). HIIT burns more fat in less time. Mix steady-state and intervals for best results."
    ),
]

def chatbot_response(message: str) -> str:
    """Return a fitness-related reply based on keyword matching."""
    msg = message.lower().strip()

    for keywords, response in _RULES:
        if any(kw in msg for kw in keywords):
            return response

    # Default fallback
    return ("🤔 Interesting question! Try asking me about: "
            "fat loss, muscle gain, abs, push-ups, squats, diet, protein, sleep, or motivation. "
            "I'm always here to help you get fit! 💪")


# ── 4. Diet Recommendation System ────────────────────────────────────────────

def get_diet_plan(goal: str, bmi: float, weight_kg: float):
    """
    Returns a full diet plan dict based on fitness goal and BMI.
    Includes daily calorie target, macros, and 5 meal suggestions.
    """

    # Estimate maintenance calories (simplified Harris-Benedict)
    maintenance = weight_kg * 33   # rough average for mixed activity

    if goal == 'fat_loss':
        calories   = int(maintenance - 500)   # 500 kcal deficit
        protein_g  = int(weight_kg * 1.8)     # preserve muscle
        carbs_g    = int(calories * 0.35 / 4)
        fats_g     = int(calories * 0.25 / 9)
        goal_label = "Fat Loss"
        meals = [
            {
                "time": "7:00 AM",
                "name": "Breakfast",
                "icon": "🌅",
                "items": ["Oats porridge (1 cup) with banana slices",
                          "2 boiled eggs or 1 cup low-fat yoghurt",
                          "1 glass of warm water with lemon"],
                "calories": 350,
            },
            {
                "time": "10:30 AM",
                "name": "Mid-Morning Snack",
                "icon": "🍎",
                "items": ["1 apple or handful of mixed nuts (20 g)",
                          "1 glass of green tea (no sugar)"],
                "calories": 180,
            },
            {
                "time": "1:00 PM",
                "name": "Lunch",
                "icon": "🥗",
                "items": ["Brown rice (½ cup) or 2 chapatis",
                          "Dal / grilled chicken / paneer (100 g)",
                          "Large salad: cucumber, tomato, onion",
                          "1 cup buttermilk"],
                "calories": 500,
            },
            {
                "time": "4:00 PM",
                "name": "Evening Snack",
                "icon": "🥜",
                "items": ["Roasted chana or sprouts (½ cup)",
                          "1 banana or any seasonal fruit"],
                "calories": 200,
            },
            {
                "time": "7:30 PM",
                "name": "Dinner",
                "icon": "🌙",
                "items": ["2 chapatis or 1 cup quinoa",
                          "Sabzi (vegetables) or grilled fish / chicken",
                          "Cucumber-tomato salad",
                          "Avoid heavy carbs after 8 PM"],
                "calories": 450,
            },
        ]
        tips = [
            "🚫 Avoid sugary drinks, white bread, and fried food",
            "💧 Drink 2.5–3 L of water daily — it suppresses hunger",
            "🕐 Eat every 3–4 hours to keep metabolism active",
            "🥦 Fill half your plate with non-starchy vegetables",
            "📵 Stop eating 2–3 hours before bedtime",
        ]
        avoid = ["White rice (large qty)", "Cold drinks & juices", "Chips & namkeen",
                 "Maida-based items", "Ice cream & sweets", "Late-night meals"]

    elif goal == 'muscle_gain':
        calories   = int(maintenance + 400)   # 400 kcal surplus
        protein_g  = int(weight_kg * 2.0)     # max protein for growth
        carbs_g    = int(calories * 0.45 / 4)
        fats_g     = int(calories * 0.25 / 9)
        goal_label = "Muscle Gain"
        meals = [
            {
                "time": "7:00 AM",
                "name": "Breakfast",
                "icon": "🌅",
                "items": ["4 egg whites + 1 whole egg scrambled",
                          "2 slices of whole-wheat toast with peanut butter",
                          "1 banana + 1 glass full-fat milk"],
                "calories": 550,
            },
            {
                "time": "10:30 AM",
                "name": "Pre-Workout Snack",
                "icon": "⚡",
                "items": ["Greek yoghurt (150 g) with honey",
                          "Handful of almonds (25 g)",
                          "1 cup black coffee (optional)"],
                "calories": 300,
            },
            {
                "time": "1:00 PM",
                "name": "Lunch",
                "icon": "🍽️",
                "items": ["White/brown rice (1 cup) or 3 chapatis",
                          "Chicken breast / paneer / rajma (150 g)",
                          "Mixed vegetables sabzi",
                          "1 cup curd"],
                "calories": 700,
            },
            {
                "time": "4:00 PM",
                "name": "Post-Workout Shake",
                "icon": "💪",
                "items": ["Protein shake or 1 cup milk + banana blended",
                          "Handful of mixed nuts",
                          "Dates (3–4) for quick carbs"],
                "calories": 350,
            },
            {
                "time": "7:30 PM",
                "name": "Dinner",
                "icon": "🌙",
                "items": ["3 chapatis or 1.5 cup rice",
                          "Dal + sabzi + salad",
                          "Chicken / fish / soya chunks (150 g)",
                          "1 glass warm milk before bed"],
                "calories": 700,
            },
        ]
        tips = [
            "💪 Eat within 30 min after your workout for best recovery",
            "🥚 Include protein in every single meal",
            "🍚 Don't fear carbs — they fuel your workouts",
            "😴 Your muscles grow during sleep, not during exercise",
            "📈 Increase calories by 100 each week if not gaining",
        ]
        avoid = ["Skipping meals", "Low-fat diets", "Alcohol", "Excessive cardio",
                 "Very spicy food (causes bloating)", "Energy drinks"]

    else:  # general
        calories   = int(maintenance)
        protein_g  = int(weight_kg * 1.4)
        carbs_g    = int(calories * 0.40 / 4)
        fats_g     = int(calories * 0.30 / 9)
        goal_label = "General Fitness"
        meals = [
            {
                "time": "7:00 AM",
                "name": "Breakfast",
                "icon": "🌅",
                "items": ["Oats or poha with vegetables",
                          "2 eggs (any style) or 1 cup paneer",
                          "1 glass of water or green tea"],
                "calories": 400,
            },
            {
                "time": "10:30 AM",
                "name": "Morning Snack",
                "icon": "🍌",
                "items": ["1 banana or seasonal fruit",
                          "Handful of roasted nuts"],
                "calories": 200,
            },
            {
                "time": "1:00 PM",
                "name": "Lunch",
                "icon": "🥗",
                "items": ["Rice / chapati (moderate)",
                          "Dal / sabzi / curd",
                          "Fresh salad with lemon dressing"],
                "calories": 550,
            },
            {
                "time": "4:00 PM",
                "name": "Evening Snack",
                "icon": "🥜",
                "items": ["Sprouts chaat or fruit salad",
                          "1 cup green tea or coconut water"],
                "calories": 180,
            },
            {
                "time": "7:30 PM",
                "name": "Dinner",
                "icon": "🌙",
                "items": ["Light dinner: soup + 2 chapatis",
                          "Vegetables + protein source",
                          "Avoid heavy carbs, eat 2 hrs before sleep"],
                "calories": 450,
            },
        ]
        tips = [
            "⚖️ Eat balanced — don't over-restrict or over-eat",
            "💧 Stay hydrated: 8–10 glasses of water daily",
            "🥦 Include vegetables in at least 2 meals daily",
            "🍎 Choose whole foods over processed whenever possible",
            "🕐 Maintain consistent meal timings every day",
        ]
        avoid = ["Ultra-processed food", "Excess sugar", "Skipping meals",
                 "Eating too fast", "Late-night heavy meals", "Too much screen time while eating"]

    return {
        "goal_label": goal_label,
        "calories": calories,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fats_g": fats_g,
        "meals": meals,
        "tips": tips,
        "avoid": avoid,
    }


# ── 5. Weekly Workout Planner ─────────────────────────────────────────────────

def get_weekly_planner(goal: str):
    """
    Returns a 7-day workout schedule list.
    Each entry: {day, focus, icon, exercises, intensity, duration}
    """
    if goal == 'fat_loss':
        return [
            {
                "day": "Monday",
                "short": "MON",
                "focus": "Full Body HIIT",
                "icon": "🔥",
                "intensity": "High",
                "duration": "40 min",
                "exercises": ["Burpees × 15", "Jumping Jacks × 30", "Push-ups × 20",
                              "Mountain Climbers × 30", "Squat Jumps × 20"],
                "color": "red",
            },
            {
                "day": "Tuesday",
                "short": "TUE",
                "focus": "Cardio",
                "icon": "🏃",
                "intensity": "Medium",
                "duration": "30 min",
                "exercises": ["Jogging / Cycling 20 min", "Jump Rope 5 min",
                              "Brisk Walk cool-down 5 min"],
                "color": "orange",
            },
            {
                "day": "Wednesday",
                "short": "WED",
                "focus": "Core & Abs",
                "icon": "🎯",
                "intensity": "Medium",
                "duration": "35 min",
                "exercises": ["Plank 3×45s", "Crunches 3×25", "Leg Raises 3×20",
                              "Bicycle Crunches 3×20", "Russian Twists 3×20"],
                "color": "yellow",
            },
            {
                "day": "Thursday",
                "short": "THU",
                "focus": "Active Rest",
                "icon": "🧘",
                "intensity": "Low",
                "duration": "20 min",
                "exercises": ["Light stretching", "Yoga / Walk", "Foam rolling"],
                "color": "green",
            },
            {
                "day": "Friday",
                "short": "FRI",
                "focus": "Upper Body",
                "icon": "💪",
                "intensity": "High",
                "duration": "40 min",
                "exercises": ["Push-ups 4×20", "Pike Push-ups 3×12", "Dips 3×15",
                              "Plank to Downward Dog 3×10", "Superman 3×15"],
                "color": "red",
            },
            {
                "day": "Saturday",
                "short": "SAT",
                "focus": "Lower Body",
                "icon": "🦵",
                "intensity": "High",
                "duration": "40 min",
                "exercises": ["Squats 4×20", "Lunges 3×12 each", "Glute Bridges 3×20",
                              "Calf Raises 3×25", "Wall Sit 3×45s"],
                "color": "blue",
            },
            {
                "day": "Sunday",
                "short": "SUN",
                "focus": "Complete Rest",
                "icon": "😴",
                "intensity": "Rest",
                "duration": "—",
                "exercises": ["Rest and recover", "Hydrate well", "Plan next week's meals"],
                "color": "grey",
            },
        ]

    elif goal == 'muscle_gain':
        return [
            {
                "day": "Monday",
                "short": "MON",
                "focus": "Chest & Triceps",
                "icon": "🏋️",
                "intensity": "High",
                "duration": "45 min",
                "exercises": ["Push-ups 4×20", "Wide Push-ups 3×15", "Diamond Push-ups 3×12",
                              "Dips 4×15", "Tricep Extensions 3×12"],
                "color": "red",
            },
            {
                "day": "Tuesday",
                "short": "TUE",
                "focus": "Back & Biceps",
                "icon": "💪",
                "intensity": "High",
                "duration": "45 min",
                "exercises": ["Pull-ups 4×10", "Bodyweight Rows 3×12", "Superman 3×15",
                              "Reverse Curls 3×15", "Chin-ups 3×8"],
                "color": "blue",
            },
            {
                "day": "Wednesday",
                "short": "WED",
                "focus": "Legs & Glutes",
                "icon": "🦵",
                "intensity": "High",
                "duration": "45 min",
                "exercises": ["Squats 4×20", "Lunges 3×15 each", "Glute Bridges 4×20",
                              "Wall Sit 3×60s", "Calf Raises 3×30"],
                "color": "orange",
            },
            {
                "day": "Thursday",
                "short": "THU",
                "focus": "Active Rest",
                "icon": "🧘",
                "intensity": "Low",
                "duration": "20 min",
                "exercises": ["Light stretching", "Foam rolling", "20 min walk"],
                "color": "green",
            },
            {
                "day": "Friday",
                "short": "FRI",
                "focus": "Shoulders & Core",
                "icon": "🎯",
                "intensity": "High",
                "duration": "45 min",
                "exercises": ["Pike Push-ups 4×12", "Lateral Raises 3×15", "Plank 3×60s",
                              "Leg Raises 3×20", "Mountain Climbers 3×30"],
                "color": "yellow",
            },
            {
                "day": "Saturday",
                "short": "SAT",
                "focus": "Full Body Power",
                "icon": "⚡",
                "intensity": "High",
                "duration": "50 min",
                "exercises": ["Burpees 3×12", "Jump Squats 3×15", "Clap Push-ups 3×10",
                              "Box Jumps 3×12", "Plank Row 3×12"],
                "color": "red",
            },
            {
                "day": "Sunday",
                "short": "SUN",
                "focus": "Complete Rest",
                "icon": "😴",
                "intensity": "Rest",
                "duration": "—",
                "exercises": ["Full rest for muscle repair", "Good nutrition & sleep",
                              "Prepare for next week"],
                "color": "grey",
            },
        ]

    else:  # general
        return [
            {
                "day": "Monday",
                "short": "MON",
                "focus": "Full Body",
                "icon": "⚡",
                "intensity": "Medium",
                "duration": "35 min",
                "exercises": ["Jumping Jacks 3×30", "Push-ups 3×15", "Squats 3×20",
                              "Plank 3×30s", "Mountain Climbers 3×20"],
                "color": "blue",
            },
            {
                "day": "Tuesday",
                "short": "TUE",
                "focus": "Cardio",
                "icon": "🏃",
                "intensity": "Medium",
                "duration": "30 min",
                "exercises": ["Brisk walk / jog 25 min", "Light stretching 5 min"],
                "color": "orange",
            },
            {
                "day": "Wednesday",
                "short": "WED",
                "focus": "Core & Flexibility",
                "icon": "🧘",
                "intensity": "Low-Medium",
                "duration": "30 min",
                "exercises": ["Plank 3×30s", "Crunches 3×20", "Yoga stretches 10 min",
                              "Hip circles & leg swings"],
                "color": "green",
            },
            {
                "day": "Thursday",
                "short": "THU",
                "focus": "Rest",
                "icon": "😴",
                "intensity": "Rest",
                "duration": "—",
                "exercises": ["Light walk", "Stay active — avoid sitting all day"],
                "color": "grey",
            },
            {
                "day": "Friday",
                "short": "FRI",
                "focus": "Upper & Lower Mix",
                "icon": "💪",
                "intensity": "Medium",
                "duration": "35 min",
                "exercises": ["Push-ups 3×15", "Lunges 3×12", "Dips 3×12",
                              "Glute Bridges 3×20", "Plank 3×30s"],
                "color": "blue",
            },
            {
                "day": "Saturday",
                "short": "SAT",
                "focus": "Outdoor Activity",
                "icon": "🌳",
                "intensity": "Medium",
                "duration": "45 min",
                "exercises": ["Walk / cycle / swim / sport", "Any physical activity you enjoy",
                              "Make it fun!"],
                "color": "yellow",
            },
            {
                "day": "Sunday",
                "short": "SUN",
                "focus": "Complete Rest",
                "icon": "😴",
                "intensity": "Rest",
                "duration": "—",
                "exercises": ["Full rest", "Meal prep for the week", "Sleep well"],
                "color": "grey",
            },
        ]


# ── 6. Exercise Instruction Library ──────────────────────────────────────────

def get_exercise_library():
    """
    Returns a list of exercise dicts with full instructions.
    Each: {name, category, muscles, difficulty, steps, tips, common_mistakes, icon}
    """
    return [
        {
            "id": "pushup",
            "name": "Push-Up",
            "category": "Upper Body",
            "icon": "🤸",
            "muscles": ["Chest", "Triceps", "Shoulders", "Core"],
            "difficulty": "Beginner",
            "sets_reps": "3 sets × 15 reps",
            "rest": "45 seconds",
            "steps": [
                "Start in a high plank: hands slightly wider than shoulders",
                "Keep body in a straight line from head to heels",
                "Slowly lower chest toward the floor (2–3 seconds)",
                "Pause briefly when chest is 2 cm from the ground",
                "Push explosively back to start position",
                "Breathe in on the way down, out on the way up",
            ],
            "tips": [
                "🔑 Keep your core tight throughout — don't let hips sag",
                "🔑 Elbows should be at 45°, not flaring out to 90°",
                "🔑 Look slightly ahead, not straight down",
            ],
            "mistakes": [
                "❌ Flaring elbows too wide (causes shoulder injury)",
                "❌ Dropping hips or arching back",
                "❌ Not going to full range of motion",
            ],
            "variations": ["Wide Push-up", "Diamond Push-up", "Incline Push-up", "Decline Push-up"],
        },
        {
            "id": "squat",
            "name": "Bodyweight Squat",
            "category": "Lower Body",
            "icon": "🦵",
            "muscles": ["Quads", "Glutes", "Hamstrings", "Calves"],
            "difficulty": "Beginner",
            "sets_reps": "3 sets × 20 reps",
            "rest": "45 seconds",
            "steps": [
                "Stand with feet shoulder-width apart, toes slightly turned out",
                "Extend arms forward for balance (parallel to ground)",
                "Begin sitting back and down as if into a chair",
                "Keep chest up and knees tracking over toes — don't cave in",
                "Lower until thighs are parallel to the floor (or below)",
                "Drive through heels to return to standing",
                "Squeeze glutes at the top",
            ],
            "tips": [
                "🔑 Keep weight in your heels, not your toes",
                "🔑 Chest tall — imagine balancing a book on your head",
                "🔑 Go below parallel for maximum glute activation",
            ],
            "mistakes": [
                "❌ Knees caving inward (valgus collapse)",
                "❌ Heels lifting off the ground",
                "❌ Rounding the lower back at the bottom",
            ],
            "variations": ["Jump Squat", "Sumo Squat", "Pulse Squat", "Wall Sit"],
        },
        {
            "id": "plank",
            "name": "Plank",
            "category": "Core",
            "icon": "🏋️",
            "muscles": ["Core", "Abs", "Shoulders", "Glutes"],
            "difficulty": "Beginner",
            "sets_reps": "3 sets × 30–60 seconds",
            "rest": "30 seconds",
            "steps": [
                "Place forearms on the ground, elbows directly under shoulders",
                "Extend legs behind you, resting on toes",
                "Body should form a straight line from head to heels",
                "Engage core — brace as if expecting a punch",
                "Squeeze glutes and thighs throughout",
                "Hold for the target duration while breathing steadily",
                "Don't hold your breath!",
            ],
            "tips": [
                "🔑 Imagine pulling your elbows toward your feet — activates more core",
                "🔑 Keep hips level — don't let them pike up or sag",
                "🔑 Gaze at the floor, not forward",
            ],
            "mistakes": [
                "❌ Hips too high (pike position) — reduces core challenge",
                "❌ Hips sagging — causes lower back pain",
                "❌ Holding breath",
            ],
            "variations": ["Side Plank", "Plank with Hip Dips", "Plank to Push-up", "RKC Plank"],
        },
        {
            "id": "lunge",
            "name": "Walking Lunge",
            "category": "Lower Body",
            "icon": "🚶",
            "muscles": ["Quads", "Glutes", "Hamstrings", "Balance"],
            "difficulty": "Beginner",
            "sets_reps": "3 sets × 12 reps each leg",
            "rest": "45 seconds",
            "steps": [
                "Stand tall with feet together, hands on hips or extended",
                "Step forward with right foot, about 2 feet in front",
                "Lower your body until both knees are at 90°",
                "Front knee should stay directly above ankle — not past toes",
                "Back knee hovers 2–3 cm above the ground",
                "Push off front foot to bring rear leg forward",
                "Alternate legs and walk forward",
            ],
            "tips": [
                "🔑 Keep your torso upright, don't lean forward",
                "🔑 Take a long enough step — short steps strain the knee",
                "🔑 Control the descent slowly",
            ],
            "mistakes": [
                "❌ Front knee going past toes",
                "❌ Torso leaning too far forward",
                "❌ Back knee slamming into the floor",
            ],
            "variations": ["Static Lunge", "Reverse Lunge", "Side Lunge", "Jump Lunge"],
        },
        {
            "id": "mountain_climber",
            "name": "Mountain Climbers",
            "category": "Cardio & Core",
            "icon": "🏔️",
            "muscles": ["Core", "Hip Flexors", "Shoulders", "Cardio"],
            "difficulty": "Intermediate",
            "sets_reps": "3 sets × 30 reps",
            "rest": "40 seconds",
            "steps": [
                "Start in a high push-up position: hands under shoulders",
                "Body forms a straight line, core tight",
                "Drive right knee toward chest as fast as possible",
                "Quickly switch — extend right leg back while driving left knee forward",
                "Alternate rapidly, as if running horizontally",
                "Keep hips level throughout — don't bounce up and down",
            ],
            "tips": [
                "🔑 The faster you go, the more cardio benefit",
                "🔑 Keep shoulders over wrists — don't shift forward",
                "🔑 Breathe rhythmically, don't hold breath",
            ],
            "mistakes": [
                "❌ Hips piking up (too high in the air)",
                "❌ Not driving knees far enough forward",
                "❌ Slowing down due to shoulder fatigue — check your position",
            ],
            "variations": ["Slow Mountain Climbers", "Cross-Body Mountain Climbers", "Spider Climbers"],
        },
        {
            "id": "burpee",
            "name": "Burpee",
            "category": "Full Body / Cardio",
            "icon": "🔥",
            "muscles": ["Full Body", "Chest", "Legs", "Core", "Cardio"],
            "difficulty": "Intermediate",
            "sets_reps": "3 sets × 10–15 reps",
            "rest": "60 seconds",
            "steps": [
                "Stand with feet shoulder-width apart",
                "Drop down — place hands on floor, jump or step feet back to push-up position",
                "Perform one push-up (optional for beginners)",
                "Jump or step both feet back toward hands",
                "Explosively jump up with arms overhead",
                "Land softly with bent knees and immediately repeat",
            ],
            "tips": [
                "🔑 Land with soft knees to protect joints",
                "🔑 Go at your own pace — quality over speed",
                "🔑 Modify by stepping instead of jumping if needed",
            ],
            "mistakes": [
                "❌ Sagging back during the push-up phase",
                "❌ Not fully extending at the top of the jump",
                "❌ Landing with locked knees",
            ],
            "variations": ["Half Burpee (no push-up)", "Burpee with Tuck Jump", "Single-leg Burpee"],
        },
        {
            "id": "glute_bridge",
            "name": "Glute Bridge",
            "category": "Lower Body / Core",
            "icon": "🍑",
            "muscles": ["Glutes", "Hamstrings", "Lower Back", "Core"],
            "difficulty": "Beginner",
            "sets_reps": "3 sets × 20 reps",
            "rest": "30 seconds",
            "steps": [
                "Lie on your back, knees bent, feet flat on floor hip-width apart",
                "Arms flat at sides, palms down",
                "Press through heels and squeeze glutes to lift hips off floor",
                "Drive hips up until body forms a straight line: shoulders to knees",
                "Hold at the top for 1–2 seconds, squeezing hard",
                "Slowly lower hips back down and repeat",
            ],
            "tips": [
                "🔑 Focus on squeezing glutes at the top — not just lifting",
                "🔑 Don't hyperextend your lower back at the top",
                "🔑 Feet should be close enough to touch with fingertips",
            ],
            "mistakes": [
                "❌ Using lower back instead of glutes to lift",
                "❌ Feet too far away — shifts load to hamstrings",
                "❌ Not holding the contraction at the top",
            ],
            "variations": ["Single-leg Bridge", "Elevated Bridge", "Banded Bridge", "Hip Thrust"],
        },
        {
            "id": "jumping_jacks",
            "name": "Jumping Jacks",
            "category": "Cardio / Warm-up",
            "icon": "⭐",
            "muscles": ["Full Body", "Calves", "Shoulders", "Cardio"],
            "difficulty": "Beginner",
            "sets_reps": "3 sets × 30 reps",
            "rest": "30 seconds",
            "steps": [
                "Stand with feet together, arms at sides",
                "Jump and simultaneously spread feet shoulder-width apart",
                "At the same time, raise arms out and overhead to clap",
                "Jump back to starting position: feet together, arms down",
                "Land softly with slightly bent knees",
                "Maintain a steady rhythm",
            ],
            "tips": [
                "🔑 Great warm-up — start slower and build speed",
                "🔑 Land softly to protect knees and ankles",
                "🔑 Keep core engaged throughout",
            ],
            "mistakes": [
                "❌ Landing with stiff, locked knees",
                "❌ Arms not fully extending overhead",
                "❌ Going too fast before properly warmed up",
            ],
            "variations": ["Star Jumps", "Low-Impact (step out)", "Cross Jacks"],
        },
    ]
