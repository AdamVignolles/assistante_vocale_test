import speech_recognition as sr
from gtts import gTTS


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

run = True
while run:
	try:
		texte = reconize_voice()
	
	except TypeError:
		print('Desoler nous ne pouvons pas faire cela pour le moment')