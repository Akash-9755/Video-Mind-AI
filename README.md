# 🎥 VideoMindAI – AI-Powered Video Summarizer & Chat Assistant

**Turn long videos into searchable knowledge with Generative AI.**

VideoMindAI is an AI-powered application that transforms YouTube videos and local video files into structured, easy-to-understand information. It automatically transcribes video content, generates intelligent summaries, extracts important insights, and allows users to interact with the video through a Retrieval-Augmented Generation (RAG) based chat system.

Instead of watching an entire video to find specific information, users can simply upload a video or paste a YouTube URL and ask questions about its content.

## 🌐 Live Demo

[**Try VideoMindAI here →**](https://video-mind-ai-aarxwc8ceghhvdm2bjaepp.streamlit.app/)

## ✨ Key Features

### 1. Multiple Video Input Options
- Paste a YouTube video URL.
- Upload local video and audio files.
- Supports formats such as MP4, MOV, MKV, AVI, WEBM, MP3, WAV, and M4A.

### 2. AI-Powered Transcription
- Uses OpenAI Whisper for English speech transcription.
- Uses Sarvam AI for Hindi/Hinglish speech-to-text translation into English.
- Processes audio in smaller chunks for transcription.

### 3. Intelligent Video Summarization
Automatically generates:
- AI-powered video titles.
- Concise video summaries.
- Important action items.
- Key decisions.
- Open questions.

### 4. Chat with Your Video (RAG)
- Ask questions about the uploaded video.
- Retrieve relevant information from the video transcript.
- Generate context-aware answers using an LLM.
- Avoid manually searching through lengthy transcripts.

### 5. Interactive Streamlit Interface
- Clean and interactive user interface.
- Separate sections for summaries, action items, decisions, open questions, and transcripts.
- Download generated video notes in Markdown format.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Speech Recognition | OpenAI Whisper |
| Hindi/Hinglish Transcription | Sarvam AI |
| Audio Processing | Pydub, FFmpeg |
| Video Download | yt-dlp |
| LLM Integration | LangChain |
| Generative AI | Groq / Gemini / configured LLM provider |
| RAG | Retrieval-Augmented Generation |
| Vector Database | ChromaDB |
| Embeddings | Hugging Face Sentence Transformers |
| API Integration | REST APIs |

## ⚙️ How It Works

The application follows an end-to-end AI processing pipeline.

```text
       YouTube URL / Local Video
                  |
                  ▼
          Audio Extraction
                  |
                  ▼
           Audio Chunking
                  |
                  ▼
        Speech-to-Text Engine
          /             \
         ▼               ▼
    OpenAI Whisper    Sarvam AI
      (English)     (Hinglish)
          \             /
           ▼           ▼
          Complete Transcript
                  |
                  ▼
           LLM Processing
                  |
          ┌───────┼────────┐
          ▼       ▼        ▼
       Summary  Insights  Questions
          |
          ▼
      RAG Pipeline
          |
          ▼
    Vector Embeddings
          |
          ▼
      ChromaDB
          |
          ▼
      User Questions
          |
          ▼
    Context-Aware Answers
```

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Akash-9755/Video-Mind-AI.git

cd Video-Mind-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

FFmpeg is required for audio processing.

Download it from:

https://ffmpeg.org/download.html

Make sure FFmpeg is added to your system PATH.

### 5. Configure Environment Variables

Create a `.env` file in the root directory.

Add the API keys required by your configured LLM provider and transcription service:

```env
SARVAM_API_KEY=your_sarvam_api_key

GROQ_API_KEY=your_groq_api_key
```

If your code uses another LLM provider, configure its corresponding API key as well.

**Important:** Never upload your `.env` file or expose API keys on GitHub.

### 6. Run the Application

```bash
streamlit run new_A.py
```

Open the local URL displayed in your terminal.

## 📁 Project Structure

```text
Video-Mind-AI/
│
├── core/
│   ├── transcriber.py
│   ├── summarize.py
│   ├── extractor.py
│   └── rag_engine.py
│
├── utile/
│   └── audio_processor.py
│
├── vector_db/
│
├── new_A.py
├── app.py
├── main.py
├── requirements.txt
├── logo.png
├── test.py
└── README.md
```

*Note: The structure above highlights the main application modules; additional files may exist in the repository.*

## 🎯 Use Cases

- Summarizing educational lectures and tutorials.
- Extracting important information from long YouTube videos.
- Understanding technical discussions and presentations.
- Generating notes from recorded meetings.
- Asking questions about video content without manually watching the entire video.

## 🔮 Future Improvements

- Support for additional regional Indian languages.
- Improved transcription accuracy.
- Better handling of long-duration videos.
- More advanced semantic retrieval.
- Conversation history and downloadable chat reports.

## 👨‍💻 Author

**Akash Kumar Saket**

B.Tech Computer Science & Engineering | AI/ML & Generative AI Enthusiast

- GitHub: [Akash-9755](https://github.com/Akash-9755)
- Project Repository: [VideoMindAI](https://github.com/Akash-9755/Video-Mind-AI)
- Live Application: [VideoMindAI Demo](https://video-mind-ai-aarxwc8ceghhvdm2bjaepp.streamlit.app/)

---

⭐ If you find this project interesting, consider giving the repository a star!

**Built with Python, Generative AI, and a passion for learning.**
