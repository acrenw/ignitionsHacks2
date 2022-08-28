import random, string
from flask import Flask, render_template, request, session
import requests, json
from werkzeug.utils import secure_filename
from time import sleep
from googletrans import Translator, constants
from pprint import pprint
import os

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

ok_chars = string.ascii_letters + string.digits


@app.route('/')  # What happens when the user visits the site
def base_page():
	return render_template(
		'base.html'
	)


@app.route('/upload')
def upload_file():
  return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
  global uploaded_file_name, uploaded_file_type
  
  if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))

      split_tup = os.path.splitext(f.filename)
      uploaded_file_name = (f.filename).replace(" ", "_")
      uploaded_file_type = split_tup[1][1:]
      print(uploaded_file_name)
      callApi()
  return render_template("upload.html")
  
def callApi():
	print('callAPI check')
	global conversation_id, access_token
	if request.method == 'POST':
		if request.form.get('submit') == 'submit':
			# print('calleth')
			conversation_id = getAccessToken()
			print('gotteeem',conversation_id)
		# 	if request.form.get('translate') == 'Translate':
		# 		pass # do something else
		# else:
		# 		pass
	elif request.method == 'GET':
			return render_template('upload.html')
	print(str(request.method))
	return render_template("upload.html")

def getAccessToken():
	global access_token
	print('getAccess check')
	url = "https://api.symbl.ai/oauth2/token:generate"
	
	payload = {
	    "type": "application",
	    "appId": "4841486a5565723339476c556a396639453855365342344b30486a694d336972",
	    "appSecret": "6a2d624c78736538466135394467323345647633545966314e784d44344e35427133456a426565462d5f4a494b6b7135676563724463624d336d776d2d454d49"
	}
	headers = {
	    "Accept": "application/json",
	    "Content-Type": "application/json"
	}
	supported_audio = ['mp3','mpeg','wav','wave']
		
	response = requests.post(url, json=payload, headers=headers)
	access_token = response.json()['accessToken']
  # session['access_token'] = response.json()['accessToken']

	# print(access_token)
	sleep(15)
	print(uploaded_file_type)
	if uploaded_file_type in supported_audio:
		conversation_id = getConvoIDAudio(access_token)
		return conversation_id
		# return getConvoIDAudio(access_token)
	elif uploaded_file_type == 'mp4':
		conversation_id = getConvoIDVid(access_token)
		return conversation_id
		# return getConvoIDVid(access_token)
	else:
		print('filetype not supported')
		pass
		#error

def getConvoIDAudio(access_token):
  global conversation_id
  
  url = "https://api.symbl.ai/v1/process/audio"
  payload = None
  numberOfBytes = 0
  try:
    print(uploaded_file_name)
    audio_file = open(uploaded_file_name, 'rb')  # use (r"path/to/file") when using windows path
    payload = audio_file.read()
    numberOfBytes = len(payload)
  except FileNotFoundError:
    print("Could not read the file provided.")
    exit()

  headers = {
	    'Authorization': 'Bearer ' + access_token,
	    'Content-Length': str(numberOfBytes),  # This should correctly indicate the length of the request body in bytes.
	    'Content-Type': 'audio/' + uploaded_file_type #TODO: make drop down for file type
	}
	
  params = {
	  'name': "NAME",
	  'languageCode': 'en-US',
	  'enableSummary': True,
	};
	
  responses = {
	    400: 'Bad Request! Please refer docs for correct input fields.',
	    401: 'Unauthorized. Please generate a new access token.',
	    404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
	    429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
	    500: 'Something went wrong! Please contact support@symbl.ai'
	}
	
  response = requests.request("POST", url, headers=headers, data=payload)
	
  if response.status_code == 201:
    sleep(10)
    # Successful API execution
    # session['conversation_id'] = response.json()['conversationId']
    return response.json()['conversationId']
    
	    # print("conversationId => " + response.json()['conversationId'])  # ID to be used with Conversation API.
	    # print("jobId => " + response.json()['jobId'])  # ID to be used with Job API.
  elif response.status_code in responses.keys():
	    print(responses[response.status_code])  # Expected error occurred
  else:
	    print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
  # convoID = response.json()['conversationId']
  # print(convoID)
  exit()


def getConvoIDVid(access_token):
	global conversation_id
	print('getConvo check')
	url = "https://api.symbl.ai/v1/process/video"
	payload = None
	
	try:
			video_file = open(uploaded_file_name, 'rb')
			payload = video_file.read()
	except FileNotFoundError:
	    print("Could not find the file provided.")
	    exit()
	
	
	headers = {
	    'Authorization': 'Bearer ' + access_token,
	    'Content-Type': 'video/mp4'  # Describes the format and codec of the provided video. Accepted value video/mp4
	}
	
	params = {
	    'name': "test",
	    'confidenceThreshold': 0.6,
	}
  
	responses = {
	    400: 'Bad Request! Please refer docs for correct input fields.',
	    401: 'Unauthorized. Please generate a new access token.',
	    404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
	    429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
	    500: 'Something went wrong! Please contact support@symbl.ai'
	}
	
	response = requests.request("POST", url, headers=headers, data=payload)
	if response.status_code == 201:
		sleep(10)
	  # Successful API execution
    # session['conversation_id'] = response.json()['conversationId']
		print(response.json()['conversationId'])
		return response.json()['conversationId']
	    # print("conversationId => " + response.json()['conversationId'])  # ID to be used with Conversation API.
	    # print("jobId => " + response.json()['jobId'])  # ID to be used with Job API.
	elif response.status_code in responses.keys():
	    print(responses[response.status_code])  # Expected error occurred
	else:
	    print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
	
	exit()
	
@app.route('/summarize')  
def summarize():
	global conversation_id, access_token, result
  # conversation_id = session.get('conversation_id')
  # access_token = session.get('access_token')
	# print(conversation_id)
	# print(access_token)
	url="https://api.symbl.ai/v1/conversations/" + conversation_id + "/summary"
	headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
  }

	responses = {
      401: 'Unauthorized. Please generate a new access token.',
      404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
      500: 'Something went wrong! Please contact support@symbl.ai'
  }

	response = requests.request("GET", url, headers=headers)

	if response.status_code == 200:
		# print(response.json())
		# print(response.json()['summary'][0]['text'])
		result = response.json()['summary'][0]['text']
		return render_template(
		'upload.html',  # Template file path, starting from the templates folder. 
		summary = response.json()['summary'][0]['text'],
    translation = "undefined"
	)
	elif response.status_code in responses.keys():
		print(responses[response.status_code])  # Expected error occurred
	else:
		print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))

	exit()

@app.route('/translate' , methods = ['GET', 'POST'])
def callTranslate():
	trans_result = ''
	print('translate call check')
	if request.method == 'POST':
		if request.form.get('translate') == 'Translate':
			trans_result = translate()
		elif request.method == 'GET':
			return render_template('base.html')
	return render_template(
		'upload.html',  # Template file path, starting from the templates folder. 
		summary = result,
    translation_result = trans_result  
	)


def translate():
	tmpLang = {
	    'af': 'afrikaans',
	    'sq': 'albanian',
	    'am': 'amharic',
	    'ar': 'arabic',
	    'hy': 'armenian',
	    'az': 'azerbaijani',
	    'eu': 'basque',
	    'be': 'belarusian',
	    'bn': 'bengali',
	    'bs': 'bosnian',
	    'bg': 'bulgarian',
	    'ca': 'catalan',
	    'ceb': 'cebuano',
	    'ny': 'chichewa',
	    'zh-cn': 'chinese (simplified)',
	    'zh-tw': 'chinese (traditional)',
	    'co': 'corsican',
	    'hr': 'croatian',
	    'cs': 'czech',
	    'da': 'danish',
	    'nl': 'dutch',
	    'en': 'english',
	    'eo': 'esperanto',
	    'et': 'estonian',
	    'tl': 'filipino',
	    'fi': 'finnish',
	    'fr': 'french',
	    'fy': 'frisian',
	    'gl': 'galician',
	    'ka': 'georgian',
	    'de': 'german',
	    'el': 'greek',
	    'gu': 'gujarati',
	    'ht': 'haitian creole',
	    'ha': 'hausa',
	    'haw': 'hawaiian',
	    'iw': 'hebrew',
	    'he': 'hebrew',
	    'hi': 'hindi',
	    'hmn': 'hmong',
	    'hu': 'hungarian',
	    'is': 'icelandic',
	    'ig': 'igbo',
	    'id': 'indonesian',
	    'ga': 'irish',
	    'it': 'italian',
	    'ja': 'japanese',
	    'jw': 'javanese',
	    'kn': 'kannada',
	    'kk': 'kazakh',
	    'km': 'khmer',
	    'ko': 'korean',
	    'ku': 'kurdish (kurmanji)',
	    'ky': 'kyrgyz',
	    'lo': 'lao',
	    'la': 'latin',
	    'lv': 'latvian',
	    'lt': 'lithuanian',
	    'lb': 'luxembourgish',
	    'mk': 'macedonian',
	    'mg': 'malagasy',
	    'ms': 'malay',
	    'ml': 'malayalam',
	    'mt': 'maltese',
	    'mi': 'maori',
	    'mr': 'marathi',
	    'mn': 'mongolian',
	    'my': 'myanmar (burmese)',
	    'ne': 'nepali',
	    'no': 'norwegian',
	    'or': 'odia',
	    'ps': 'pashto',
	    'fa': 'persian',
	    'pl': 'polish',
	    'pt': 'portuguese',
	    'pa': 'punjabi',
	    'ro': 'romanian',
	    'ru': 'russian',
	    'sm': 'samoan',
	    'gd': 'scots gaelic',
	    'sr': 'serbian',
	    'st': 'sesotho',
	    'sn': 'shona',
	    'sd': 'sindhi',
	    'si': 'sinhala',
	    'sk': 'slovak',
	    'sl': 'slovenian',
	    'so': 'somali',
	    'es': 'spanish',
	    'su': 'sundanese',
	    'sw': 'swahili',
	    'sv': 'swedish',
	    'tg': 'tajik',
	    'ta': 'tamil',
	    'te': 'telugu',
	    'th': 'thai',
	    'tr': 'turkish',
	    'uk': 'ukrainian',
	    'ur': 'urdu',
	    'ug': 'uyghur',
	    'uz': 'uzbek',
	    'vi': 'vietnamese',
	    'cy': 'welsh',
	    'xh': 'xhosa',
	    'yi': 'yiddish',
	    'yo': 'yoruba',
	    'zu': 'zulu',
	}
	langDict = {v: k for k, v in tmpLang.items()}
	translator = Translator()
	lang = 'chinese (simplified)'.lower()
	translation = translator.translate(result, dest=langDict[lang])
	print(str(translation.text))
	return (str(translation.text))

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=5000,  # Randomly select the port the machine hosts on.
		debug=True
	)