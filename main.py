import speech_recognition as sr
from gtts import gTTS
import os
import requests
import json




def reconize_voice():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Parlez -->")
		audio = r.listen(source)

		try:
			sayed = r.recognize_google(audio, language='fr-Fr')
			print(f'vous avez dit: {sayed}')
			return sayed
		except sr.UnknownValueError:
			print("Pouvez vous repeter")
		except sr.RequestError as e:
			print('Le service Google API ne fonctione plus'+ format(e))

def speak(text):
	mytext = text
	language = 'fr'
	output = gTTS(text=mytext, lang=language, slow=False)
	output.save('last_output.mp3')
	os.system('cvlc --play-and-exit last_output.mp3')

def get_meteo_day(ville):
	url_weather = "http://api.openweathermap.org/data/2.5/weather?q="+ville+",fr&APPID=beb97c1ce62559bba4e81e28de8be095"

	r_weather = requests.get(url_weather)
	data = r_weather.json()

	try:
		t = data['main']['temp']       
		speak("La température moyenne est de {} degrés Celsius".format(round(t-273.15)))
		
		t_min = data['main']['temp_min']
		t_max = data['main']['temp_max']
		speak("Les températures varient entre {}".format(round(t_min-273.15)) + " a {} degrés Celsius".format(round(t_max-273.15)))
		
		humidite = data['main']['humidity']
		speak("Taux d'humidité de {}".format(humidite) + "%")	
		
		temps = data['weather'][0]['description']
		speak("Conditions climatiques : {}".format(temps))
	except KeyError:
		speak('nous ne prenons pas en charge cette ville désolé')

print("lancement de l'assistant vocal")
run = True
while run:
	try:
		texte = reconize_voice()
		speak(f"j'ai compris YOUPI vous avez dit : {texte}")
		if 'météo' in texte or 'température' in texte or 'humidité' in texte:
			speak('pouvez vous donner le nom de la ville française que vous rechercher')
			while True:
				try:
					ville = reconize_voice()
					get_meteo_day(ville)
					break
				except TypeError:
					speak('pouvez vous répéter')
		elif 'lance le robot' in texte:
			os.system('bash bot_start.sh')
		
		elif 'mets en ligne' in texte:
			os.system('bash git_command.sh')
			
	
	except TypeError:
		print('Desoler nous ne pouvons pas faire cela pour le moment')