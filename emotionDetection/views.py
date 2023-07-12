from django.shortcuts import render, HttpResponse, redirect
from .analysis import text_to_emotion, get_large_audio_transcription
from .models import UploadFile


# Create your views here.
def home(request):
    """
    Show the home page
    :param request: http headers
    :return: html object
    """
    data = {
        'title': 'Emotion Detection'
    }
    return render(request, 'index.html', context=data)


def text_input(request):
    """
    get the text from html and pass it to analysis.py file to detect the emotion
    :param request: http headers
    :return: html object
    """
    # print(request)
    if request.method == "POST":
        input_text = request.POST.get('text')
        # call emotion detection function and pass text
        results = text_to_emotion(input_text)

        data = {
            'title': 'Result of Emotion Detection',
            'results': results,
            'text': input_text,
            'top': results[0]
        }
        # print(data)
        return render(request, 'index.html', context=data)
        # return redirect('emotionDetection:home')
    return redirect('emotionDetection:home')


def audio_input(request):
    """
    get the audio file from html and pass it to analysis.py file to detect the emotion
    :param request: http headers
    :return: html object
    """
    # print(request)
    if request.method == "POST":
        # get file from html
        input_text = request.FILES.get('video-file-upload')
        # print(input_text)
        # save file as object in model
        file_obj = UploadFile()
        file_obj.file = input_text
        file_obj.save()
        # Get last objects from database
        new_f = UploadFile.objects.last()
        # url of file location
        add_url = str(new_f.file.url)
        # F=file location of audio
        print(f'E:/AudioTextA/{add_url[1:]}')
        path = f'E:/AudioTextA/{add_url[1:]}'
        # E:\AudioTextA\media\audio\english - conversation - practice - canceling - plans - ytmp4converter.com - en.mp3
        # pass file path to extract text from speech
        text = get_large_audio_transcription(path)
        # call emotion detection function and pass text
        results = text_to_emotion(text)
        data = {
            'title': 'Result of Emotion Detection',
            'results': results,
            'text': text,
            'top': results[0]
        }
        # print(data)
        # after processing delete the object and file
        new_f.delete()
        return render(request, 'index.html', context=data)
    return redirect('emotionDetection:home')

