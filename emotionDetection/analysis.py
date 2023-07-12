from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import pipeline
import speech_recognition as sr
import os
import pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil

# create a speech recognition object
r = sr.Recognizer()
# To convert mp3 file format in WAV format we need ffmpeg for pydub
pydub.AudioSegment.ffmpeg = "C:\\Users\\h\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin"
# AudioSegment.converter = "C:\\Users\\h\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffmpeg.exe"
# AudioSegment.ffmpeg = "C:\\Users\\h\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffmpeg.exe"
# AudioSegment.ffprobe = "C:\\Users\\h\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffprobe.exe"


def text_to_emotion(text: str):
    """
    :param text: str
    :return: dict
    Creating pipeline from Huggingface transformers model emotion classification
    model and tokenizer used from Huggingface Hub
    """
    if len(text.split()) > 500:
        tem = text.split()
        text = ' '.join(tem[0:500])
    model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
    tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None)
    result = [{'label': str(r['label']).capitalize(), 'score': round((r['score'] * 100), 2)} for r in
              classifier(text)[0]]
    return result


# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    print(path)
    # with open(path, 'rb') as file:
    #     print(file.read())
    # sound = AudioSegment.from_mp3(path)
    try:
        sound = AudioSegment.from_file(path, "mp3")
    except:
        sound = AudioSegment.from_file(path, format="mp4")
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=500,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS - 14,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )
    folder_name = "./audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_data=audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                # text = f"{text.capitalize()}. "
                # print(chunk_filename, ":", text)
                whole_text += ' ' + str(text)
    # delete the directory that contains chucks of audio after processing
    if os.path.isdir(folder_name):
        shutil.rmtree(folder_name, ignore_errors=True)
    # return the text for all chunks detected
    return whole_text
