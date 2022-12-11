import os
from dotenv import load_dotenv
from django.shortcuts import render, HttpResponse
import firebase_admin
from firebase_admin import credentials 
from firebase_admin import firestore
import openai
load_dotenv()
openai.organization = os.getenv('ORGANIZATION_ID')
openai.api_key = os.getenv('AI_KEY')
# Use the application key
cred = credentials.Certificate('keys.json')
# Initialize the app.
app = firebase_admin.initialize_app(cred)
# Call the db
db = firestore.client()


# Create your views here.
def index(request):
  # doc_ref = db.collection(u'users').document(u'alovelace')
  # doc_ref.set({
  #   u'first': u'Ada',
  #   u'last': u'Lovelace',
  #   u'born': 1815
  # })
  if request.method == "GET":
    response = openai.Image.create(
    prompt='not a cat',
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    print(image_url)
    return HttpResponse(image_url)
  else:
    return HttpResponse('lo que dios quiera')