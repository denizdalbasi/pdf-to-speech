import pypdf
import pyttsx3

def smooth_read(pdf_path):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    
    # Optional: Select a specific voice if the default is silent
    voices = engine.getProperty('voices')
    # Try changing index [0] to [1] if you hear nothing
    engine.setProperty('voice', voices[0].id) 
    
    try:
        reader = pypdf.PdfReader(pdf_path)
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                # Clean up: Replace newlines with spaces to prevent word-splitting
                clean_text = " ".join(text.split())
                
                print(f"--- Processing Page {i+1} ---")
                print(f"Reading: {clean_text}")
                
                # Add the whole page to the queue
                engine.say(clean_text)
                
                # Run the queue for this page
                # This will wait for the page to finish and then release 
                # control back to the loop for the next page
                engine.runAndWait()
                
    except Exception as e:
        print(f"J.A.R.V.I.S. Error Report: {e}")

smooth_read('delete.pdf')