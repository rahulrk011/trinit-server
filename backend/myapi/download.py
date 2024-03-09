import requests

# URL of the image
url = "https://images.pexels.com/photos/18776367/pexels-photo-18776367/free-photo-of-colorful-houses-line-the-canal-in-burano-italy.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save the image to a file
    with open("landscape.jpg", "wb") as f:
        f.write(response.content)
    print("Image downloaded successfully.")
else:
    print("Failed to download image:", response.status_code)
