# V2VlogAI

V2VlogAI is a simple web application that helps you turn YouTube videos into well-structured blog posts. Just paste a YouTube link, and the app will fetch the transcript, organize the content, and generate a readable blog article with clear sections and a conclusion.

## Features
- Converts YouTube video transcripts into blog posts
- Automatically organizes content into sections with subheadings
- Easy-to-use web interface
- Powered by Flask and Llama 3 (Ollama) for local AI text generation

## How It Works
1. Enter a YouTube video URL in the web interface.
2. The app fetches the transcript (if available).
3. The transcript is sent to a locally running Llama 3 model via Ollama.
4. The model generates a blog post, which is displayed in your browser.

## Requirements
- Python 3.8+
- Flask
- flask-cors
- youtube-transcript-api
- requests
- Ollama (with the Llama 3 model running locally)

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/V2VlogAI.git
   cd V2VlogAI
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Ollama with Llama 3:**
   Make sure Ollama is installed and running. Start the Llama 3 model:
   ```bash
   ollama run llama3
   ```
4. **Run the Flask app:**
   ```bash
   python app.py
   ```
5. **Open your browser:**
   Go to [http://localhost:5000](http://localhost:5000)

## Notes
- The app only works with YouTube videos that have transcripts enabled.
- Ollama and the Llama 3 model must be running locally for blog generation to work.
- If you encounter errors about transcripts, check if the video has captions enabled.

## Project Structure
```
V2VlogAI/
├── app.py            # Main Flask backend
├── requirements.txt  # Python dependencies
├── static/           # Frontend HTML files
│   ├── frontend.html
│   ├── about.html
│   └── contact.html
└── README.md         # This file
```

## License
This project is open source. Feel free to use and modify it for your own needs.
