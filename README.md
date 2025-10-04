# **Farmer Support Chatbot**

This is an intelligent, multilingual chatbot designed to provide support to farmers. It uses Google's Gemini API to understand and answer a wide range of agricultural questions in English, Hindi, and Marathi.

## **Features**

* **Intelligent Q\&A:** Leverages the Gemini 1.5 Flash model to provide accurate answers to complex farming-related questions.  
* **Multilingual Support:** Seamlessly communicates in English, Hindi, and Marathi.  
* **User-Friendly Interface:** A clean, modern, and responsive chat interface built with Flask and Tailwind CSS.  
* **Secure API Key Handling:** Uses a .env file to keep your Google API key safe and secure.  
* **Real-time Translation:** Translates user queries to English for the AI model and translates the AI's response back to the user's chosen language.

## **Project Setup and Installation**

Follow these steps to get the chatbot running on your local machine.

### **1\. Prerequisites**

* Python 3.7+  
* A Google account to get an API key.

### **2\. Clone the Repository (or Set Up Manually)**

If you have this project in a git repository, clone it:

git clone \<your-repository-url\>  
cd Farmer-ChatBot

If not, just make sure all the files (app.py, .env, templates/index.html) are in the correct folder structure.

### **3\. Create a Virtual Environment**

It's highly recommended to use a virtual environment to manage project dependencies.

\# Create the virtual environment  
python \-m venv venv

\# Activate it  
\# On Windows (Command Prompt):  
.\\venv\\Scripts\\activate  
\# On Windows (PowerShell):  
.\\venv\\Scripts\\Activate.ps1  
\# On macOS/Linux:  
source venv/bin/activate

You should see (venv) at the start of your terminal prompt.

### **4\. Get Your Gemini API Key**

1. Go to [Google AI Studio](https://aistudio.google.com/).  
2. Sign in and click **"Get API key"** \> **"Create API key in new project"**.  
3. Copy the generated API key.

### **5\. Install Dependencies and Set Up .env**

1. In the root of your project, create a file named .env.  
2. Add your API key to this file:  
   GEMINI\_API\_KEY=YOUR\_API\_KEY\_HERE

   Replace YOUR\_API\_KEY\_HERE with the key you copied.  
3. Install all the required Python packages:  
   pip install \-r requirements.txt

   *(Note: If you don't have a requirements.txt file, you can install the packages manually)*:  
   pip install Flask google-generativeai python-dotenv deep-translator

## **How to Run the Application**

1. Make sure your virtual environment is activated.  
2. Run the Flask application from the root directory:  
   python app.py

3. Open your web browser and navigate to:  
   http://127.0.0.1:5000

You can now interact with your chatbot\!

## **Technologies Used**

* **Backend:** Python, Flask  
* **Frontend:** HTML, Tailwind CSS, JavaScript  
* **AI & Translation:**  
  * Google Gemini API  
  * Deep-Translator Library  
* **Environment Management:** python-dotenv
