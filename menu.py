"""
Upon the instruction "help me read this menu," the model will begin scanning an image of the menu.
If a letter is greater than the average size, it will recognize it as a header.
It will read the headers to the user, and the user will then say a header name they would like to hear items from.
"""

import cv2
import pytesseract
from pytesseract import Output
import statistics

def read_menu(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    d = pytesseract.image_to_data(gray, output_type=Output.DICT)

    headers = []
    header_sizes = []

    for i in range(len(d["level"])):
        if d["level"][i] == 2:
            header_sizes.append(d["height"][i])

    avg_size = statistics.mean(header_sizes)

    for i in range(len(d["level"])):
        if d["level"][i] == 2 and d["height"][i] > avg_size:
            headers.append(d["text"][i])

    return headers

def parse_items_from_header(image_path, header):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    d = pytesseract.image_to_data(gray, output_type=Output.DICT)

    items = []
    read_items = False

    for i in range(len(d["level"])):
        if d["level"][i] == 2 and d["text"][i] == header:
            read_items = True

        if read_items and d["level"][i] == 2 and d["text"][i] != header:
            break

        if read_items and d["level"][i] == 5:
            items.append(d["text"][i])

    return items

def main():
    image_path = "/Users/danielkim/Desktop/menu-template.jpg"
    print("Scanning menu...")
    headers = read_menu(image_path)
    print("Headers found:")
    for h in headers:
        print(h)

    chosen_header = input("Enter the header name you'd like to hear items from: ")
    items = parse_items_from_header(image_path, chosen_header)
    print(f"Items under {chosen_header}:")
    for item in items:
        print(item)

if __name__ == "__main__":
    main()
