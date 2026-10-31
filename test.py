from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
from core.transcriber import transcribe_all
from utile.audio_processor import process_input


source = "https://www.youtube.com/watch?v=84vvYxibR0U"
language = "hinglish"

chunks = process_input(source)

transcript = transcribe_all(chunks , language=language)

print("\n\n----------------Final Transcript----------------\n\n")
print(transcript)