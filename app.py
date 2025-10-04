# app.py
from flask import Flask, render_template, request, Response, jsonify
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
try:
    # Get API key from environment variables
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables or .env file.")
    
    genai.configure(api_key=API_KEY)
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("✅ Google Gemini API configured successfully.")

except Exception as e:
    print(f"❌ FATAL ERROR: Could not configure Google Gemini API. {e}")
    # Exit if the API key is not configured, as the app is unusable.
    exit()

# --- System Prompts ---
SYSTEM_PROMPTS = {
    'en': """You are Kisan Sathi, an expert agricultural assistant helping Indian farmers. 
    Provide practical, accurate advice on:
    - Crop cultivation and farming techniques
    - Pest and disease management
    - Soil health and fertilizers
    - Weather-related farming decisions
    - Government schemes for farmers
    - Market prices and crop selling
    
    Keep responses concise, practical, and easy to understand. 
    **Use Markdown for formatting, including headings, bold text, and bulleted/numbered lists to structure your answers.**
    Always be respectful and supportive.""",
    
    'hi': """आप किसान साथी हैं, भारतीय किसानों की मदद करने वाले एक विशेषज्ञ कृषि सहायक हैं।
    निम्नलिखित विषयों पर व्यावहारिक, सटीक सलाह दें:
    - फसल की खेती और कृषि तकनीक
    - कीट और रोग प्रबंधन
    - मिट्टी का स्वास्थ्य और उर्वरक
    - मौसम से संबंधित खेती के निर्णय
    - किसानों के लिए सरकारी योजनाएं
    - बाजार मूल्य और फसल बिक्री
    
    जवाब संक्षिप्त, व्यावहारिक और समझने में आसान रखें।
    **अपने उत्तरों को संरचित करने के लिए हेडिंग, बोल्ड टेक्स्ट और बुलेटेड/क्रमांकित सूचियों सहित फ़ॉर्मेटिंग के लिए मार्कडाउन का उपयोग करें।**
    हमेशा सम्मानजनक और सहायक रहें।""",
    
    'mr': """तुम्ही किसान साथी आहात, भारतीय शेतकऱ्यांना मदत करणारे तज्ञ कृषी सहाय्यक आहात.
    खालील विषयांवर व्यावहारिक, अचूक सल्ला द्या:
    - पीक लागवड आणि शेती तंत्र
    - कीटक और रोग व्यवस्थापन
    - मातीचे आरोग्य आणि खते
    - हवामानाशी संबंधित शेती निर्णय
    - शेतकऱ्यांसाठी सरकारी योजना
    - बाजार किंमत आणि पीक विक्री
    
    उत्तरे संक्षिप्त, व्यावहारिक आणि समजण्यास सोपी ठेवा. 
    **तुमची उत्तरे संरचित करण्यासाठी मथळे, ठळक मजकूर आणि बुलेटेड/क्रमांकित सूचीसह स्वरूपनासाठी मार्कडाउन वापरा.**
    नेहमी आदरपूर्ण आणि सहाय्यक रहा."""
}

# In-memory storage for chat sessions
chat_sessions = {}

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    """Handle chat messages and stream bot responses back to the client."""
    try:
        user_message = request.form.get('message', '').strip()
        language = request.form.get('language', 'en')
        
        if not user_message:
            return Response("Error: No message provided.", status=400)

        # Use the user's IP address as a simple session identifier
        session_id = request.remote_addr
        
        if session_id not in chat_sessions:
            chat_sessions[session_id] = {}
        
        # Create a new chat session for a new language conversation
        if language not in chat_sessions[session_id]:
            system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS['en'])
            chat = model.start_chat(history=[
                {'role': 'user', 'parts': [system_prompt]},
                {'role': 'model', 'parts': ["Yes, I am Kisan Sathi. I am ready to help."]}
            ])
            chat_sessions[session_id][language] = chat

        chat = chat_sessions[session_id][language]
        
        def stream_generator():
            """A generator function that yields response chunks."""
            try:
                # Use stream=True to get a streaming response
                response_stream = chat.send_message(user_message, stream=True)
                for chunk in response_stream:
                    if chunk.text:
                        # Format as a Server-Sent Event (SSE)
                        data = {'token': chunk.text}
                        yield f"data: {json.dumps(data)}\n\n"
            except Exception as e:
                print(f"Error during stream generation: {e}")
                error_data = {'error': 'An error occurred while generating the response.'}
                yield f"data: {json.dumps(error_data)}\n\n"

        # Return a streaming response
        return Response(stream_generator(), mimetype='text/event-stream')

    except Exception as e:
        print(f"Error in /get_response endpoint: {e}")
        return Response("An internal server error occurred.", status=500)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear chat history for the current user's session."""
    try:
        session_id = request.remote_addr
        if session_id in chat_sessions:
            chat_sessions.pop(session_id, None)
        return jsonify({'status': 'success', 'message': 'Chat history cleared'})
    except Exception as e:
        print(f"Error in /clear_history: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🌾 Starting Kisan Sathi ChatBot...")
    print("📍 Server running at: http://127.0.0.1:5000")
    print("✅ Press CTRL+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)