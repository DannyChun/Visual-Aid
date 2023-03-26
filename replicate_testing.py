import replicate
replicate.api_key = "55c893ae89896258fe6a887a7c1ff098fc86a735"
model = replicate.models.get("salesforce/blip")
version = model.versions.get("2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")

# https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#input
inputs = {
    # Input image
    # 'image': open("path/to/file", "rb"),

    # Choose a task.
    'task': "image_captioning",

    # Type question for the input image for visual question answering
    # task.
    # 'question': ...,

    # Type caption for the input image for image text matching task.
    # 'caption': ...,
}

# https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#output-schema
output = version.predict(**inputs)
print(output)