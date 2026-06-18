# pdf-to-speech# PDF Audio Reader

A simple Python utility that takes text from a PDF document and reads it aloud using the `pyttsx3` text-to-speech engine.

---

## Features
* **PDF Parsing**: Uses `pypdf` to accurately extract text from PDF files.
* **Speech Synthesis**: Converts extracted text into natural-sounding speech.
* **Formatting Cleanup**: Automatically removes unnecessary newlines and whitespace from the PDF layout to ensure smooth, continuous speech.
* **Configurable**: Easily adjust speech rate and voice selection.

## Prerequisites
```bash
pip install pypdf pyttsx3