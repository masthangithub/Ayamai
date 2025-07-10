import google.generativeai as genai
import os

# Best practice: Use an environment variable
# os.environ['GOOGLE_API_KEY'] = 'YOUR_API_KEY' 
# genai.configure()

# Or configure directly (less secure)
genai.configure(api_key="AIzaSyD94317UFjtBvLDslOgP0Brh7heA-8KAQU")

# Now, try to create the model
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content("Test")
    print("Success! API call worked.")
    print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")