import tkinter as tk
from tkinter import messagebox
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Function to extract YouTube video ID from URL
def get_video_id(url):
    try:
        query = urlparse(url)
        if query.hostname == 'youtu.be':  # Shortened URL (youtu.be/VIDEO_ID)
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):  # Full YouTube URL
            if query.path == '/watch':  # Standard YouTube URL (youtube.com/watch?v=VIDEO_ID)
                return parse_qs(query.query)['v'][0]
            if query.path[:7] == '/embed/':  # Embed URL (youtube.com/embed/VIDEO_ID)
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':  # Alternate URL (youtube.com/v/VIDEO_ID)
                return query.path.split('/')[2]
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Invalid URL: {e}")
        return None

# Function to fetch the transcript
def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ""
        for entry in transcript:
            transcript_text += entry['text'] + " "
        return transcript_text
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch transcript: {e}")
        return None

# Function to handle transcribe button click
def transcribe():
    video_url = entry.get()
    video_id = get_video_id(video_url)
    if video_id:
        transcript = fetch_transcript(video_id)
        if transcript:
            text_box.delete(1.0, tk.END)  # Clear the text box
            text_box.insert(tk.END, transcript)  # Insert new transcript

# Create the main window
root = tk.Tk()
root.title("YouTube Video Transcriber")

# URL input label
label = tk.Label(root, text="Enter YouTube Video URL:")
label.pack(pady=5)

# URL input field
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Transcribe button
button = tk.Button(root, text="Transcribe", command=transcribe)
button.pack(pady=10)

# Text box to display the transcript
text_box = tk.Text(root, wrap=tk.WORD, height=20, width=60)
text_box.pack(pady=10)

# Start the GUI event loop
root.mainloop()
