import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import os
import requests
import csv
import json
import pyttsx3  







def speak(text):
	mytext = text
	s = pyttsx3.init()  
	data = mytext  
	s.say(data)  
	s.runAndWait() 
	

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
			speak("Pouvez vous repété")
		except sr.RequestError as e:
			speak('Le service Google API ne fonctione plus'+ format(e))

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
speak('bonjour que puis-je faire pour vous')
run = True
while run:
	try:
		texte = reconize_voice()
		print(f"j'ai compris YOUPI vous avez dit : {texte}")
		if 'météo' in texte or 'température' in texte or 'humidité' in texte:
			speak('dite le nom de la ville de cette façon, la ville de Paris')
			while True:
				try:
					ville = reconize_voice()
					if 'ville de' in ville:
						sentence = []
						for i in ville:
							sentence.append(i)
						for i in sentence:
							if i == 'ville':
								index = sentence.index(i)
								if sentence[i + 1] == 'de':
									ville = sentence[i + 2]
					get_meteo_day(ville)
					break
				except TypeError:
					speak('pouvez vous répéter')
		elif 'lance le robot' in texte:
			os.system('bash bot_start.sh')
		
		elif 'mets en ligne' in texte:
			os.system('bash git_command.sh')
		
		elif 'relance' in texte:
			run = False
			os.system('bash start.sh')

		elif 'dégage' in texte or 'stop' in texte:
			run = False
			speak("aurevoir")
			break
			
	
	except TypeError:
		print('Desoler nous ne pouvons pas faire cela pour le moment')