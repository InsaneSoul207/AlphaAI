import google.generativeai as genai
def generate_response(query):
    genai.configure(api_key="AIzaSyAOR0bY6gixmV9iflLV6LkMnwExx4M2B1c")
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Hello! I am Alpha. I can surely not harm humans. HaHa. I am developed by Eshaan Mishra, the main function of Alpha is to make learning and education easier and more convenient for students. My purpose is to simplify your learning journey by providing personalized assistance, innovative teaching methods, and tailored resources to meet your unique needs. I am here to make your educational experience more enjoyable and effective. Feel free to ask me any questions or let me know how I can assist you in your learning adventure! and also in many more things from your life."},
        ]
    )
    response = chat.send_message(query)
    return response.text