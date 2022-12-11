# PYTHON IMPORTS
import os
from dotenv import load_dotenv
import uuid
import json
from datetime import datetime

# DJANGO IMPORTS
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# FIREBASE PACKAGE
import firebase_admin
from firebase_admin import credentials 
from firebase_admin import firestore

# OPEN AI PACKAGE
import openai

# This mounts the env file
load_dotenv()

openai.organization = os.getenv('ORGANIZATION_ID')
openai.api_key = os.getenv('AI_KEY')

# Use the application keys and set to ignore it on the .gitignore
cred = credentials.Certificate('keys.json')
# Initialize the app.
app = firebase_admin.initialize_app(cred)
# Call the Firbase DB
db = firestore.client()

def index(request):
  # I will create a session to ensure the user has agreed to the cookies to acces the ai
  return HttpResponse('set the session')
# Since theres no important data being passed no csrf_token is need
@csrf_exempt
def imgAiCreation(request):
  # The user must make a POST request in order to access DALL-E
  if request.method == "POST":
    # Parsing the request
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # Request ID
    id = uuid.uuid1()
    
    # Calling the OpenAi API
    response = openai.Image.create(
      prompt= '%s' % body['prompt'],
      n=1,
      size="1024x1024"
      )
    image_url = response['data'][0]['url']

    # Adding the data to Firebase
    doc_ref = db.collection(u'openAI_img_request').document(u'{}'.format(id))
    doc_ref.set({
      u'URL': u'%s' % image_url, 
      u'id': u'{}'.format(id),
      u'data_id': u'{}'.format(body['data_id']),
      u'prompt': u'%s' % body['prompt'],
      u'date': u'{}'.format(datetime.now().strftime("%m/%d/%Y %H:%M:%S %z"))
    })
    
    # Front-End return package 
    api_response = {
      'status':200,
      'id': id,
      'Prompt': '%s' % body['prompt'],
      'OpenAi_url': image_url,
      'date': datetime.now().strftime("%m/%d/%Y %H:%M:%S %z") # the %z is for utc offset
    }
    return JsonResponse(api_response)
  else:
    # Front-End return package 
    api_response = {
      'status': 400,
      'type': 'Bad Request',
      'date': datetime.now().strftime("%m/%d/%Y %H:%M:%S %z") # the %z is for utc offset
    }
    return JsonResponse(api_response)