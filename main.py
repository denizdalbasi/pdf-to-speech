import argparse
from pathlib import Path
import sys
import os
import speech_recognition as sr
from pypdf import PdfReader
import pyttsx3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class AudioAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice & Document Processor")
        self.root.geometry("600x500")
        self.root.configure(bg="#f5f6fa")

        # Custom Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 11), padding=6)
        self.style.configure("Primary.TButton", background="#007BFF", foreground="white")
        self.style.configure("Speech.TButton", background="#28A745", foreground="white")
        
        # Initialize Audio Engines
        self.recognizer = sr.Recognizer()
        
        self.create_widgets()

    def create_widgets(self):
        # Title Banner - FIXED: Changed 'padding' to 'pady' to fix the Tkinter crash
        title = tk.Label(self.root, text="Audio & PDF Control Center", font=("Arial", 16, "bold"), bg="#1e272e", fg="white", pady=12)
        title.pack(fill=tk.X)

        # Main Container
        main_frame = tk.Frame(self.root, bg="#f5f6fa", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- SECTION 1: VOICE / SETTINGS ---
        settings_frame = tk.LabelFrame(main_frame, text=" Engine Settings ", font=("Arial", 10, "bold"), bg="#f5f6fa", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=10)

        tk.Label(settings_frame, text="Speech Speed (Rate):", bg="#f5f6fa").grid(row=0, column=0, sticky="w", padx=5)
        self.rate_scale = tk.Scale(settings_frame, from_=100, to=250, orient=tk.HORIZONTAL, bg="#f5f6fa", bd=0)
        self.rate_scale.set(170)
        self.rate_scale.grid(row=0, column=1, sticky="ew", padx=5)
        
        tk.Label(settings_frame, text="Voice Accent:", bg="#f5f6fa").grid(row=0, column=2, sticky="w", padx=10)
        self.voice_var = tk.StringVar(value="Default (0)")
        self.voice_combo = ttk.Combobox(settings_frame, textvariable=self.voice_var, values=["Male / Default (0)", "Female (1)"], state="readonly", width=18)
        self.voice_combo.current(0)
        self.voice_combo.grid(row=0, column=3, padx=5)

        # --- SECTION 2: ACTIONS ---
        actions_frame = tk.Frame(main_frame, bg="#f5f6fa")
        actions_frame.pack(fill=tk.X, pady=15)

        # Button 1: Speech to Text
        speech_btn = ttk.Button(actions_frame, text="🎵 Process Speech (WAV File)", style="Speech.TButton", command=self.process_wav_file)
        speech_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Button 2: Read PDF Aloud
        pdf_read_btn = ttk.Button(actions_frame, text="📄 Read PDF Aloud", style="Primary.TButton", command=self.process_pdf_live)
        pdf_read_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Button 3: Convert PDF to MP3
        pdf_save_btn = ttk.Button(actions_frame, text="💾 Export PDF to MP3", command=self.process_pdf_save)
        pdf_save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # --- SECTION 3: CONSOLE / TEXT LOG OUTPUT ---
        log_frame = tk.LabelFrame(main_frame, text=" Live Console Output ", font=("Arial", 10, "bold"), bg="#f5f6fa")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_box = tk.Text(log_frame, wrap=tk.WORD, font=("Consolas", 10), bg="#2f3640", fg="#f5f6fa", bd=0, padx=10, pady=10)
        self.log_box.pack(fill=tk.BOTH, expand=True)
        
    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        self.log_box.delete("1.0", tk.END)

    def get_configured_engine(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", self.rate_scale.get())
        voices = engine.getProperty("voices")
        voice_idx = self.voice_combo.current()
        if voice_idx < len(voices):
            engine.setProperty("voice", voices[voice_idx].id)
        return engine

    def process_wav_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if not file_path:
            return
        
        self.clear_log()
        self.log(f"Loading speech audio file: {os.path.basename(file_path)}")
        
        engine = self.get_configured_engine()
        
        with sr.AudioFile(file_path) as source:
            self.log("Reading audio waves...")
            audio_data = self.recognizer.record(source)

        try:
            self.log("Sending data payload to Google Engine API...")
            text = self.recognizer.recognize_google(audio_data)
            
            self.log("\n=== Transcribed Text Output ===")
            self.log(text)
            self.log("===============================\n")

            response = f"I heard you say: {text}. Processing complete."
            self.log("Sounding response out loud...")
            engine.say(response)
            engine.runAndWait()
            
        except sr.UnknownValueError:
            self.log("Result Error: Audio was unclear or unrecognized.")
            engine.say("Sorry, I could not understand the audio.")
            engine.runAndWait()
        except sr.RequestError:
            self.log("Result Error: Network unreachable. Is your internet active?")
        finally:
            engine.stop()

    def extract_pdf_text(self, file_path):
        reader = PdfReader(file_path)
        full_text = []
        for page in reader.pages:
            raw_text = page.extract_text()
            if raw_text:
                full_text.append(" ".join(raw_text.split()))
        return " ".join(full_text), reader.pages

    def process_pdf_live(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Documents", "*.pdf")])
        if not file_path:
            return
        
        self.clear_log()
        self.log(f"Reading file: {os.path.basename(file_path)}")
        
        try:
            complete_text, pages = self.extract_pdf_text(file_path)
            self.log(f"Found {len(pages)} pages. Preparing narrator stream...")
            
            engine = self.get_configured_engine()
            self.log("Playing document text live...")
            engine.say(complete_text)
            engine.runAndWait()
            self.log("--- Playback Finished ---")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read PDF file:\n{str(e)}")

    def process_pdf_save(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Documents", "*.pdf")])
        if not file_path:
            return
            
        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Audio Files", "*.mp3")])
        if not save_path:
            return

        self.clear_log()
        self.log(f"Reading: {os.path.basename(file_path)}")
        
        try:
            complete_text, _ = self.extract_pdf_text(file_path)
            self.log(f"Synthesizing audiobook file track directly to disk...")
            
            engine = self.get_configured_engine()
            engine.save_to_file(complete_text, save_path)
            engine.runAndWait()
            
            self.log(f"\nSuccess! File saved cleanly to:\n{save_path}")
            messagebox.showinfo("Export Complete", "Your MP3 audiobook has been compiled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed saving track export:\n{str(e)}")


def initialize_engine(rate=170, voice_index=0):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    voices = engine.getProperty("voices")
    if voice_index < len(voices):
        engine.setProperty("voice", voices[voice_index].id)
    return engine

def handle_speech_recognition(file_path, engine):
    recognizer = sr.Recognizer()
    path = Path(file_path)
    if not path.exists():
        print(f"Error: Audio file '{file_path}' not found.")
        return
    with sr.AudioFile(str(path)) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        print(f"\n=== Recognized Text ===\n{text}\n=======================")
        engine.say("I heard you say: " + text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")

def read_pdf(file_path, rate, voice, save_mp3):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' not found.")
        return
    engine = initialize_engine(rate=rate, voice_index=voice)
    reader = PdfReader(path)
    full_text = [page.extract_text() for page in reader.pages if page.extract_text()]
    complete_text = " ".join(full_text)
    if save_mp3:
        engine.save_to_file(complete_text, save_mp3)
        engine.runAndWait()
    else:
        engine.say(complete_text)
        engine.runAndWait()


if __name__ == "__main__":
    # If no terminal parameters are given, load up the beautiful button window interface!
    if len(sys.argv) == 1:
        root = tk.Tk()
        app = AudioAppGUI(root)
        root.mainloop()
    else:
        # CLI fallback structure
        parser = argparse.ArgumentParser(description="CLI Tools package.")
        parser.add_argument("file_path", help="Path to file")
        parser.add_argument("--speech", action="store_true", help="Speech mode")
        parser.add_argument("--rate", type=int, default=170)
        parser.add_argument("--voice", type=int, default=0)
        parser.add_argument("--save", nargs="?", default=None)
        
        args = parser.parse_args()
        if args.speech:
            handle_speech_recognition(args.file_path, initialize_engine(args.rate, args.voice))
        else:
            read_pdf(args.file_path, args.rate, args.voice, args.save)