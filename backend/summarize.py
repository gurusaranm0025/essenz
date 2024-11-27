import requests
import warnings
from bs4 import BeautifulSoup

import yt_dlp
import speech_recognition as sr
from transformers import pipeline

warnings.filterwarnings('ignore')

PREFIX_TO_REMOVE = "CNN.com will feature iReporter photos in a weekly Travel Snapshots gallery. Please submit your best shots of the U.S. for next week. Visit CNN.com/Travel next Wednesday for a new gallery of snapshots. We will feature a selection of the best shots from across the globe."
AUDIO_PATH = "./video.wav"
YDL_OPTS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    'outtmpl': "."+'/video.%(ext)s',
}

def fetch_webpage(url: str):
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')
        content = "".join([p.get_text() for p in paragraphs])
        
        return content
    
    except Exception as e:
        print(f"Error fetching webpage: {e}")
        return None

def split_text_into_chunks(text: str, max_chunk_size: int = 1000):
    sentences = text.split(". ")
    chunks = []
    curr_chunk = []
    
    for sentence in sentences:
        if len(''.join(curr_chunk))+len(sentence) <= max_chunk_size:
            curr_chunk.append(sentence)
        else:
            chunks.append(''.join(curr_chunk)+'.')
            curr_chunk = [sentence]
        
    if curr_chunk:
        chunks.append(''.join(curr_chunk)+'.')
    
    return chunks

class Summarizer:
    def __init__(self) -> None:
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.recognizer = sr.Recognizer()
    
    def sumarize_webpage(self, url: str) -> str:
        """
            Summarizes the webpage of the given url.
            
            Parameters:
            url (str) - URL of the webpage to summarize.
            
            Returns:
            str - summarized content.
        """
        content = fetch_webpage(url)
        
        summary = self.summarize(content)
        
        return summary
    
    def transcribe(self, url: str) -> str:
        """
            Returns the transcription of the downloaded audio file.
            
            Parameters:
            url (str) - URL of the youtube video.
            
            Returns:
            str - transcription of the video.
        """
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            ydl.download([url])

        try:
            with sr.AudioFile(AUDIO_PATH) as source:
                print("\nLoading the audio file....")
                audio_data = self.recognizer.record(source)
            
            print("Transcribing...")
            text = self.recognizer.recognize_whisper(audio_data)
            
            return text
        except Exception as e:
            print(f"Error transcribing the audio {e.with_traceback()}.")
            return None
    
    def summarize_youtube_video(self, url: str) -> str:
        """
            Summarizes the youtube video fo the given URL.
            
            Parameters:
            url (str) - URL of the youtube video to summarize.
            
            Returns:
            str - summary of the youtube video.
        """
        transcription = self.transcribe(url)
        
        summary = self.summarize(transcription)
        
        return summary
        
    
    def summarize(self, text: str, max_chunk_size: int = 1000, max_length: int = 200, min_length: int = 50) -> str:
        """
            Summarizes the given text content.
            
            Parameters:
            text (str) - content to summarize.
            max_chunk_size (int) - maximum size of chunks, allowed.
            max_length (int) - minimum size of the summary.
            min_length(int) - minimum length of the summary.
            
            Returns:
            str - summary
        """
        print("\n Summarizing...")
        chunks = split_text_into_chunks(text, max_chunk_size=max_chunk_size)
        summaries = []

        for chunk in chunks:
            try:    
                summary = self.summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                summaries.append(summary[0]['summary_text'])
                
            except Exception as e:
                print(f"Error summarizing text: {e}")
                continue
        
        result = ''.join(summaries)
        
        if  result.startswith(PREFIX_TO_REMOVE):
            result = result.removeprefix(PREFIX_TO_REMOVE)
        
        return result.strip()
        

if __name__ == "__main__":
    summarizer = Summarizer()
    
    url = "https://medium.com/geekculture/youtube-video-summarization-with-python-52fc192a5004"
    print("\n WEBPAGE SUMMARY ==>")
    print(summarizer.sumarize_webpage(url))
    
    url = "https://www.youtube.com/watch?v=H-orCCxoE8I"
    print("\n YOUTUBE SUMMARY ==>")
    print(summarizer.summarize_youtube_video(url))
    
    