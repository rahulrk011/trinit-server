from django.http import JsonResponse
import pymongo
from django.views.decorators.csrf import csrf_exempt
import base64
from pymongo import MongoClient,DESCENDING
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai
import PIL.Image


client = MongoClient("mongodb://localhost:27017/")
db = client['trinitt']
collection=db['data']

@csrf_exempt
def generate_content_view(request):
    if request.method == 'POST':
        # Load environment variables
        load_dotenv()
        gemini_key = os.getenv("GEMINI_API_KEY")

    # Configure GenAI with API key
        genai.configure(api_key=gemini_key)
        # Get the uploaded image
        image = request.FILES.get('file')
        
        # Open the image using PIL
        img = PIL.Image.open(image)
        
        # Generate content using the GenAI model
        model = genai.GenerativeModel('gemini-pro-vision')
        response1 = model.generate_content(["just retrun the coordinates only of the location corresponding to the image, nothing else", img])
        response2 = model.generate_content(["Describe about the location of the image", img])
        
        # Return generated content as JSON response
        return JsonResponse({'generated_content': [response1.text, response2.text]})
    else:
        # Return error response if no image file uploaded
        return JsonResponse({'error': 'No image file uploaded'}, status=400)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        image_bytes = uploaded_file.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        current_datetime = datetime.now()
        inserted_id = collection.insert_one({'image_bytes': base64_image, 'datetime': current_datetime , 'caption' : "this is caption :/"}).inserted_id
        return JsonResponse({'upload success -- inserted_id': str(inserted_id)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def get_history_data(request):
    # Retrieve history data from the collection in descending order of time
    history_data = list(collection.find().sort('datetime', pymongo.DESCENDING))
    # Convert image_bytes to hexadecimal format
    history = []
    for item in history_data:
        image_bytes = item['image_bytes']
        caption = item['caption']
        time=item['datetime']
        history.append((image_bytes,caption,time))
    return JsonResponse(history, safe=False)