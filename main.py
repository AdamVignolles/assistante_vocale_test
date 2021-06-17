import speech_recognition as sr
from gtts import gTTS
import os


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

run = True
while run:
	try:
		texte = reconize_voice()
		speak(f"j'ai compris YOUPI vous avez dit : {texte}")
	
	except TypeError:
		print('Desoler nous ne pouvons pas faire cela pour le moment')