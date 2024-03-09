from django.http import JsonResponse
import pymongo
from django.views.decorators.csrf import csrf_exempt
import base64
from pymongo import MongoClient,DESCENDING
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client['trinitt']
collection=db['data']

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