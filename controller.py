from data_loader import load_audio
from data_cleaner import clean_audio
from analysis import calculate_rt60

class AppController:
    def __init__(self, gui):
        self.gui = gui

    def process_audio(self, file_path):
        try:
            wav_path = load_audio(file_path)
            audio_data, sample_rate = clean_audio(wav_path)
            rt60 = calculate_rt60(audio_data, sample_rate)
            return rt60
        except Exception as e:
            print(f"Error processing audio: {e}")
            return None
