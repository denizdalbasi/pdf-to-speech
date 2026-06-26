# PDF Audio Reader

A versatile command-line Python utility that extracts text from a PDF document and reads it aloud or converts it into an MP3 audiobook using the `pyttsx3` text-to-speech engine.

---

## Features
* **PDF Parsing**: Uses `pypdf` to accurately extract text from PDF files.
* **On-the-Fly Customization**: Dynamically adjust speaking speed (`--rate`) and switch between available system voices (`--voice`) straight from the terminal.
* **Audiobook Generation**: Export your PDFs directly to high-quality `.mp3` files (`--save`) for offline listening.
* **Formatting Cleanup**: Automatically removes messy newlines and layout whitespaces from the PDF to ensure smooth, continuous speech.