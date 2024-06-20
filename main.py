from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

model = load_model('metadata.h5')

data_path = 'nutrition.csv'
nutrition_data = pd.read_csv(data_path)
nutrition_data['calories'] = pd.to_numeric(nutrition_data['calories'], errors='coerce')
nutrition_data.dropna(subset=['calories'], inplace=True)

def preprocess_input(user_weight, user_height, user_age, user_goal):
    # Konversi tinggi dari cm ke meter
    user_height_m = user_height / 100.0
    
    # Encode user_goal menjadi nilai numerik
    if user_goal == 'increase':
        goal_encoded = 1
    elif user_goal == 'decrease':
        goal_encoded = 2
    else:  # 'maintain'
        goal_encoded = 0
    
    # Kembalikan input yang telah diproses sebagai array numpy
    return np.array([[user_weight, user_height_m, user_age]])

def calculate_daily_calories(weight, height, age, goal_index):
    # Mengasumsikan jenis kelamin laki-laki untuk vere simplifyasi; sesuaikan jika diperlukan untuk perempuan
    BMR = 10 * weight + 6.25 * height - 5 * age + 5  # Tambahkan 5 untuk pria, kurangkan 161 untuk wanita

    # Sesuaikan BMR berdasarkan goal_index secara langsung
    if goal_index == 0:  # increase
        return BMR + 500
    elif goal_index == 1:  # decrease
        return BMR - 500
    else:  # maintain
        return BMR

def recommend_meals(data, daily_calories):
    meal_calories = daily_calories / 3
    suitable_foods = data[(data['calories'] >= 0.8 * meal_calories) & (data['calories'] <= 1.2 * meal_calories)]
    if suitable_foods.shape[0] >= 3:
        return suitable_foods.sample(3)
    else:
        print("Tidak cukup makanan yang sesuai ditemukan untuk direkomendasikan.")
        return pd.DataFrame()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Validasi input
    if 'weight' not in data or 'height' not in data or 'age' not in data or 'goal' not in data:
        return jsonify({'error': 'Input tidak valid. Harap berikan berat, tinggi, usia, dan goal.'}), 400
    
    weight = float(data['weight'])
    height_cm = float(data['height'])
    height = height_cm / 100.0  # Konversi tinggi dari cm ke meter
    age = int(data['age'])
    
    # Konversi goal dari string menjadi indeks float
    goals = {"increase": 0.0, "decrease": 1.0, "maintain": 2.0}
    goal_input = data['goal'].lower()
    if goal_input in goals:
        goal_index = goals[goal_input]
    else:
        return jsonify({'error': 'Goal tidak valid. Harap masukkan increase, decrease, atau maintain.'}), 400
    
    # Hitung kebutuhan kalori harian
    daily_calories_needed = calculate_daily_calories(weight, height, age, goal_index)
    
    # Dapatkan rekomendasi makanan
    recommended_meals = recommend_meals(nutrition_data, daily_calories_needed)
    
    if not recommended_meals.empty:
        meals_list = recommended_meals.to_dict(orient='records')
    else:
        meals_list = []
    
    # Format prediksi sebagai respons JSON
    response = {
        'daily_calories_needed': daily_calories_needed,
        'recommended_meals': meals_list
    }
    
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
