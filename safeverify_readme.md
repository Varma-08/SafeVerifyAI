# SafeVerifyAI - News Verification System

An academic proof-of-concept web application that uses Google Gemini AI to verify whether news content is Genuine, Fake, or Uncertain.

## 📋 Project Structure

```
safeverifyai/
│
├── app.py                  # Flask backend with Gemini integration
├── templates/
│   └── index.html         # Frontend UI
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up API Key

Set your Gemini API key as an environment variable:

**On Linux/Mac:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**On Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 4: Use the Application

1. Open your browser and go to `http://localhost:5000`
2. Paste news content in the textarea
3. Click "Verify News"
4. View the AI-powered analysis

## 🔧 How It Works

1. **User Input**: User enters news content on the frontend
2. **API Request**: Frontend sends POST request to `/verify` endpoint
3. **AI Processing**: Backend constructs prompt and sends to Google Gemini
4. **Classification**: Gemini analyzes and classifies as Genuine/Fake/Uncertain
5. **Response Display**: Frontend displays classification and explanation

## 🎯 Features

- ✅ **Multi-Modal Input Support**: Text, Image, and Audio
- ✅ Simple, clean academic interface with tabbed navigation
- ✅ Real-time AI verification using Google Gemini
- ✅ Drag-and-drop file upload
- ✅ Image preview and audio playback
- ✅ Color-coded results (Green/Red/Yellow)
- ✅ Detailed explanations for classifications
- ✅ Error handling and validation
- ✅ No database or authentication required

## 🧪 Example News to Test

### Text Examples:

**Genuine News:**
```
NASA successfully launched the James Webb Space Telescope, which has been sending back unprecedented images of distant galaxies.
```

**Fake News:**
```
Scientists confirm that drinking bleach cures all diseases according to a study published by Harvard.
```

**Uncertain News:**
```
A local resident claims to have seen mysterious lights in the sky last night.
```

### Image Examples:
- Upload a screenshot of a news article
- Upload a photo claiming to show a news event
- Upload a viral social media image with news claims

### Audio Examples:
- Record or upload a voice note claiming news information
- Upload a podcast segment discussing news
- Upload any audio file with news claims

## ⚠️ Important Notes

- This is an **academic project** for educational purposes
- Not intended for production use
- AI classifications should be verified with additional fact-checking
- No data is stored or tracked
- Requires active internet connection for Gemini API

## 📚 Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **AI**: Google Gemini API
- **No databases or authentication**

## 🔐 Security Notes

- Never commit your API key to version control
- Use environment variables for sensitive data
- For production, implement proper security measures

## 📄 License

This is an academic project for educational purposes.

## 🤝 Contributing

This is a simple academic project. For improvements:
1. Keep it simple
2. Document all changes
3. Follow the existing code style

---

**Academic Project** • Powered by Google Gemini AI