import requests
import os
from requests.auth import HTTPBasicAuth


username = ''
password = ''

def get_access_token():
    token_url = "https://sh.dataspace.copernicus.eu/api/authenticate"

    response = requests.post(token_url, json={'username': username, 'password': password})
    
    if response.status_code == 200:
        return response.json().get("accessToken")
    else:
        print("Failed to obtain access token:", response.status_code, response.text)
        return None

def search_for_images(access_token, area_of_interest, date_start, date_end, max_results=20):
    base_url = "https://sh.dataspace.copernicus.eu/api/v1/catalog/1.0.0"

    search_query = f"{base_url}/search?format=json&areaOfInterest={area_of_interest}&dateStart={date_start}&dateEnd={date_end}&maxResults={max_results}"
    
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(search_query, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code, response.text)
        return None

token = get_access_token()

if token:
    area_of_interest = 'coordinates_of_your_area'
    date_start = '20240101'
    date_end = '20240131'
    results = search_for_images(token, area_of_interest, date_start, date_end)

def download_image(image_url, destination_folder):
    response = requests.get(image_url, auth=HTTPBasicAuth(username, password), stream=True)
    
    if response.status_code == 200:
        filename = image_url.split("/")[-1]
        filepath = os.path.join(destination_folder, filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded {filename}")
    else:
        print("Failed to download image:", response.status_code)

area_of_interest = 'coordinates_of_your_area'
date_start = '20240101'
date_end = '20240131'
results = search_for_images(area_of_interest, date_start, date_end)

if results:
    for image in results['features']:
        download_url = image['properties']['services']['download']['url']
        download_image(download_url, '/Users/oladejo/Desktop/images')
