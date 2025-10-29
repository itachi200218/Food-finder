# from flask import Flask, request, jsonify, render_template
# import google.generativeai as genai

# app = Flask(__name__, template_folder='templetss', static_folder='frontend')

# # Replace with your actual Gemini API key
# API_KEY = "AIzaSyB0vF4ofeNImFAwR6l0n9sTUwmc_BC18Qg"

# # Configure Gemini
# genai.configure(api_key=API_KEY)

# # Create a generative model instance
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Serve main page
# @app.route("/")
# def index():
#     return render_template("index.html")

# # Serve ChatBot page
# @app.route("/chatbot")
# def chatbot():
#     return render_template("chatbot.html")

# # Gemini/OpenAI Chat API
# @app.route("/gemini-chat", methods=["POST"])
# def gemini_chat():
#     data = request.get_json()
#     user_input = data.get("prompt", "").strip()

#     if not user_input:
#         return jsonify({"reply": "Please provide some input."})

#     try:
#         # Start a chat session for each request
#         chat = model.start_chat()

#         # System instruction for food combos
#         system_prompt = (
#             "You are a helpful food recipe assistant. "
#             "Suggest dishes and combinations based on ingredients provided."
#         )
#         full_prompt = f"{system_prompt}\nUser input: {user_input}"

#         # Send message to Gemini
#         response = chat.send_message(full_prompt)

#         return jsonify({"reply": response.text})

#     except Exception as e:
#         return jsonify({"reply": f"Error: {str(e)}"}), 500

# if __name__ == "__main__":
#     # Run on port 5003
#     app.run(debug=True, port=5003)
