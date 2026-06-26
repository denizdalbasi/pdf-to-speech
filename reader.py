import argparse
from pathlib import Path
import sys
from pypdf import PdfReader
import pyttsx3


def initialize_engine(rate=170, voice_index=0):
    """Configures the TTS engine."""
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    voices = engine.getProperty("voices")

    if voice_index < len(voices):
        engine.setProperty("voice", voices[voice_index].id)
    else:
        print(
            f"Warning: Voice index {voice_index} not found. Using default voice."
        )

    return engine


def process_text(text):
    """Cleans text to sound more natural."""
    if not text:
        return ""
    return " ".join(text.split())


def read_pdf(file_path, rate, voice, save_mp3):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' not found.")
        return

    engine = initialize_engine(rate=rate, voice_index=voice)
    reader = PdfReader(path)

    print(f"--- Starting: {path.name} ({len(reader.pages)} pages) ---")

    full_text = []
    try:
        for i, page in enumerate(reader.pages):
            text = process_text(page.extract_text())
            if text:
                full_text.append(text)

        complete_text = " ".join(full_text)

        if save_mp3:
            output_path = (
                save_mp3
                if save_mp3.endswith(".mp3")
                else f"{path.stem}_output.mp3"
            )
            print(f"Saving audio to file: {output_path}...")
            engine.save_to_file(complete_text, output_path)
            engine.runAndWait()
            print("--- Export Finished Successfully ---")

        else:
            print("Press Ctrl+C to stop reading.")
            for i, page_text in enumerate(full_text):
                print(f"Processing Page {i+1}...")
                engine.say(page_text)
                engine.runAndWait()
            print("--- Finished ---")

    except KeyboardInterrupt:
        print("\n--- Reading Interrupted by User ---")
        engine.stop()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        engine.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A CLI PDF Audio Reader and MP3 Converter."
    )

    parser.add_argument("file_path", help="Path to the PDF file you want to read")

    parser.add_argument(
        "--rate",
        type=int,
        default=170,
        help="Speaking speed rate (default: 170)",
    )
    parser.add_argument(
        "--voice",
        type=int,
        default=0,
        help="Voice index/type (0 for male, 1 for female depending on OS defaults)",
    )
    parser.add_argument(
        "--save",
        nargs="?",
        const="default.mp3",
        default=None,
        help="Save to an MP3 file instead of playing live. Optional: Specify a custom filename.",
    )

    args = parser.parse_args()

    read_pdf(
        file_path=args.file_path,
        rate=args.rate,
        voice=args.voice,
        save_mp3=args.save,
    )