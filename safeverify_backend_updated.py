"""
SafeVerifyAI - Flask Backend
A simple academic application for news verification using Google Gemini API
Supports text, image, and audio inputs
"""

from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
import base64
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure Google Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("=" * 60)
    print("⚠️  WARNING: GEMINI_API_KEY not found!")
    print("=" * 60)
    print("Please set your API key using one of these methods:")
    print()
    print("Method 1 (Recommended): Create a .env file")
    print("  1. Create a file named '.env' in this directory")
    print("  2. Add this line: GEMINI_API_KEY=your_api_key_here")
    print()
    print("Method 2: Set environment variable")
    print("  export GEMINI_API_KEY='your_api_key_here'")
    print("=" * 60)
else:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini API key loaded successfully!")

# System prompt for news verification
SYSTEM_PROMPT = """You are a Fake News Verification Assistant.
Analyze the given news content and classify it into one of the following categories:
1. Genuine – Information supported by reliable and credible sources.
2. Fake – False or misleading information with no credible backing.
3. Uncertain / Unverifiable – Information that cannot be conclusively verified.

Rules:
- Clearly state the classification at the top.
- Explain the reasoning in simple language.
- If classified as Genuine, mention credible source types (official news portals, government websites, reputed organizations).
- If Fake or Uncertain, explain why verification is not possible.
- Do NOT invent sources or links.
- For images: Analyze any text, context, or visual elements that might indicate authenticity.
- For audio: Analyze the transcribed content for verification.
"""


@app.route('/')
def home():
    """
    Render the main HTML page
    """
    return render_template('safeverify_frontend.html')


@app.route('/verify', methods=['POST'])
def verify_news():
    """
    API endpoint to verify news using Google Gemini
    Supports text, image, and audio inputs
    
    Expects form data or JSON:
    - text input: {"news": "news text here"}
    - file upload: multipart/form-data with 'file' field and optional 'news' field
    
    Returns JSON: {"classification": "...", "explanation": "...", "error": "..."}
    """
    try:
        news_text = ""
        file_data = None
        file_mime_type = None
        
        # Check if request has file upload
        if 'file' in request.files:
            file = request.files['file']
            
            if file and file.filename:
                # Read file data
                file_bytes = file.read()
                
                # Get MIME type
                file_mime_type = file.content_type
                
                # Convert to base64 for Gemini API
                file_data = base64.b64encode(file_bytes).decode('utf-8')
                
                print(f"📎 Received file: {file.filename} ({file_mime_type})")
            
            # Get optional text from form
            news_text = request.form.get('news', '').strip()
        else:
            # Handle JSON request (text only)
            data = request.get_json()
            
            if not data or 'news' not in data:
                return jsonify({
                    'error': 'Missing "news" field in request or no file uploaded'
                }), 400
            
            news_text = data['news'].strip()
        
        # Validate that we have either text or file
        if not news_text and not file_data:
            return jsonify({
                'error': 'Please provide either text content or upload a file'
            }), 400
        
        # Check if API key is configured
        if not GEMINI_API_KEY:
            return jsonify({
                'error': 'Gemini API key not configured. Please create a .env file with your GEMINI_API_KEY or set it as an environment variable.'
            }), 500
        
        # Initialize Gemini model (use vision model for multimodal support)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Prepare content for Gemini
        content_parts = []
        
        # Add text prompt
        prompt_text = f"{SYSTEM_PROMPT}\n\n"
        
        if file_data:
            # Handle different file types
            if file_mime_type.startswith('image/'):
                prompt_text += "Analyze the news content in this image.\n\n"
            elif file_mime_type.startswith('audio/'):
                prompt_text += "Analyze the transcribed audio content for news verification.\n\n"
            
            # Add file data
            content_parts.append({
                'mime_type': file_mime_type,
                'data': file_data
            })
        
        # Add user's text if provided
        if news_text:
            prompt_text += f"Additional context/text:\n{news_text}"
        
        content_parts.insert(0, prompt_text)
        
        print(f"🤖 Sending request to Gemini...")
        
        # Call Gemini API
        response = model.generate_content(content_parts)
        
        # Extract response text
        gemini_response = response.text
        
        print(f"✅ Received response from Gemini")
        
        # Parse classification from response
        classification = extract_classification(gemini_response)
        
        # Return structured response
        return jsonify({
            'classification': classification,
            'explanation': gemini_response
        })
    
    except Exception as e:
        # Handle any errors gracefully
        print(f"❌ Error occurred: {str(e)}")
        return jsonify({
            'error': f'An error occurred while processing your request: {str(e)}'
        }), 500


def extract_classification(response_text):
    """
    Extract classification category from Gemini's response
    Returns: 'Genuine', 'Fake', 'Uncertain', or 'Unknown'
    """
    response_lower = response_text.lower()
    
    # Check for classification keywords in order of priority
    if 'genuine' in response_lower[:200]:
        return 'Genuine'
    elif 'fake' in response_lower[:200]:
        return 'Fake'
    elif 'uncertain' in response_lower[:200] or 'unverifiable' in response_lower[:200]:
        return 'Uncertain'
    else:
        return 'Unknown'


if __name__ == '__main__':
    # Run Flask development server
    print("\n🚀 Starting SafeVerifyAI server...")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("✨ Now supports text, image, and audio inputs!")
    print("\n")
    app.run(debug=True, host='0.0.0.0', port=5000)