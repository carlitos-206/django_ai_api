# PYTHON IMPORTS
import os
from dotenv import load_dotenv
import uuid
import json

# DJANGO IMPORTS
from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

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
# Call the db
db = firestore.client()


# Since theres no important data being passed no csrf_token is need
@csrf_exempt
def index(request):
  if request.method == "POST":
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    response = openai.Image.create(
      prompt= '%s' % body['prompt'],
      n=1,
      size="1024x1024"
      )
    image_url = response['data'][0]['url']
    id = uuid.uuid1()
    doc_ref = db.collection(u'openAI_img_request').document(u'{}'.format(id))
    doc_ref.set({
      # The old school literal templates is required by firebase
      # sample: 'hello %s' %s world ---> hello world
      # the u is from firebase sdk
      u'URL': u'%s' % image_url,
      # 
      u'id': u'{}'.format(id),
      u'data_id': u'{}'.format(body['data_id']),
      u'prompt': u'%s' % body['prompt']
    })
    return redirect("http://localhost:3000/")
  else:
    return HttpResponse('lo que dios quiera')