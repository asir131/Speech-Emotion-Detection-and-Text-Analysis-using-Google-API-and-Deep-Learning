from django.urls import path
from .views import home, text_input, audio_input

app_name = 'emotionDetection'

urlpatterns = [
    path('', home, name='home'),
    path('text/', text_input, name='text_input'),
    path('audio/', audio_input, name='audio_input'),

]
