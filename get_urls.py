import re
import json
import requests

def get_slide_urls(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Extract totalSlides
    match = re.search(r'"totalSlides":(\d+),', response.text)
    total_slides = int(match.group(1)) if match else 0
    print(f"total_slides:{total_slides}")

    # Extract slide information
    slide_data = re.search(r'"slides":\s*{(.*?)},"strippedTitle"', response.text, re.DOTALL).group(1)
    print(slide_data)
    slide_info = json.loads('{' + slide_data + '}')  # Parse as JSON

    host = slide_info['host']
    image_location = slide_info['imageLocation']
    image_sizes = slide_info['imageSizes']

    # Get best quality image details
    best_quality = max(image_sizes, key=lambda x: x['width'])
    quality = best_quality['quality']
    width = best_quality['width']
    # format = best_quality['format']
    format2 = "jpg"

    # Generate URLs for all slides
    # slide_urls = [
    #     f"{host}/{image_location}/{quality}/-{n}-{width}.{format2}"
    #     for n in range(1, total_slides + 1)
    # ]
    slide_urls = {}

    for n in range(1, total_slides + 1):
        slide_urls[n] = {}
        # "imageSizes":[{"quality":85,"width":320,"format":"jpg"},{"quality":85,"width":638,"format":"jpg"},{"quality":75,"width":2048,"format":"webp"}]
        for image_size in image_sizes:
            width = image_size['width']
            quality = image_size['quality']
            # ---
            url = f"{host}/{image_location}/{quality}/-{n}-{width}.{format2}"
            slide_urls[n][width] = url
    # ---
    return slide_urls

if __name__ == "__main__":
    url = "https://www.slideshare.net/amroraouf/12-139666387"# @param

    slide_urls = get_slide_urls(url)

    print(json.dumps(slide_urls, indent=2))
