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

@csrf_exempt
def index(request):
  if request.method == "POST":
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    request.session['user_id'] = body['data_id']
    apiResponse = {
      "Status": 200,
      "AI": "Active"
    }
    return JsonResponse(apiResponse)
  else:
    apiResponse = {
      "Status": 400,
      "AI": ""
    }
    return JsonResponse(apiResponse)
    
# Since theres no important data being passed no csrf_token is need
@csrf_exempt
def imgAiCreation(request):
  # The user must make a POST request in order to access DALL-E
  if request.method == "POST":
    # Parsing the request
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # The user must have a active session to access ai
    if body['prompt'] or body['data_id'] not in body:
      api_response = {
        "status": 500,
        "error":"No Match Found",
        'date': datetime.now().strftime("%m/%d/%Y %H:%M:%S %z") # the %z is for utc offset
      }
      return JsonResponse(api_response)
    else:
      if 'user_id' in request.session:
        # Request ID
        id = uuid.uuid1()
        # This ensure the user is the same as the backend session
        if request.session['user_id'] == body['data_id']:
          # Calling the OpenAi API
          response = openai.Image.create(
            prompt= '%s' % body['prompt'],
            n=1,
            size="1024x1024"
            )
          image_url = response['data'][0]['url']
          print(image_url)
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
          api_response = {
            "status": 400,
            "id": id,
            'error': 'User Not Valid',
            'date': datetime.now().strftime("%m/%d/%Y %H:%M:%S %z") # the %z is for utc offset
          }
          return  JsonResponse(api_response)
  else:
    # Front-End return package 
    api_response = {
      'status': 400,
      'id': id,
      'error': 'Bad Request',
      'date': datetime.now().strftime("%m/%d/%Y %H:%M:%S %z") # the %z is for utc offset
    }
    return JsonResponse(api_response)