"""
Allows for parsing of a stream, so that it may give useful object detection observations verbally for the visually
impaired. It should have navigation capabilities such as crossing a street when the pedestrian light is on, and
ensuring that the impaired will not walk into a wall.
"""

import os
import cv2
import openai
import menu

# Set up your OpenAI API key
openai.api_key = os.environ["KEY"]

# Your YOLO model and configurations should be set up here
YOLO_MODEL = "path/to/yolo/model"
YOLO_CONFIG = "path/to/yolo/config"
YOLO_CLASSES = "path/to/yolo/classes"


def detect_objects(image):
    # Load the YOLO model and configuration
    net = cv2.dnn.readNet(YOLO_MODEL, YOLO_CONFIG)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Preprocess the image
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform object detection
    detections = net.forward(output_layers)

    # Extract class IDs, confidences, and bounding boxes
    class_ids, confidences, boxes = [], [], []
    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype("int")
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes, confidences, class_ids


def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Perform object detection
        boxes, confidences, class_ids = detect_objects(frame)

        # Generate a textual description of the scene
        prompt = "Describe the following scene with useful object detection observations for the visually impaired: "
        for box, class_id in zip(boxes, class_ids):
            class_name = YOLO_CLASSES[class_id]
            prompt += f"A {class_name} is detected. "
        prompt += "End of scene."

        description = generate_text(prompt)
        print(description)

        # Check for user input
        user_input = input("Enter command: ").strip()

        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "help me read this menu":
            image_path = input("Enter the path to the menu image: ").strip()
            menu.main(image_path)
        elif user_input.lower().startswith("navigate to "):
            destination = user_input[len("navigate to "):]
            prompt = f"Provide navigation instructions for a visually impaired person to reach {destination}: "
            instructions = generate_text(prompt)
            print(instructions)
        else:
            prompt = f"User asked: {user_input}. Answer: "
            response = generate_text(prompt)
            print(response)

        # Release the video capture
        cap.release()

        if name == "main":
            main()


