import pyttsx3
from pypdf import PdfReader
from pathlib import Path
import sys

def initialize_engine(rate=170, voice_index=0):
    """Configures the TTS engine."""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')
    if voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    return engine

def process_text(text):
    """Cleans text to sound more natural."""
    if not text:
        return ""
    
    return " ".join(text.split())

def read_pdf(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' not found.")
        return

    engine = initialize_engine()
    reader = PdfReader(path)
    
    print(f"--- Starting: {path.name} ({len(reader.pages)} pages) ---")
    print("Press Ctrl+C to stop reading.")

    try:
        for i, page in enumerate(reader.pages):
            text = process_text(page.extract_text())
            if text:
                print(f"Processing Page {i+1}...")
                engine.say(text)
                
                engine.runAndWait()
    except KeyboardInterrupt:
        print("\n--- Reading Interrupted by User ---")
        engine.stop()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        engine.stop()
        print("--- Finished ---")

if __name__ == "__main__":
    read_pdf('delete.pdf')