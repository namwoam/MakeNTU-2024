import cv2
import os
import pandas as pd
import ast

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
          (0, 255, 255), (255, 0, 255), (0, 255, 255)]


def build_marker(image, box, color=(0, 0, 0), thickness=10):
    for i, pt in enumerate(box):
        box[i] = [round(n) for n in pt]
    pt1 = box[0]
    pt2 = box[2]
    cv2.rectangle(image, pt1, pt2, color, thickness)


def highlight_image(image, markers):
    for row in range(len(markers)):
        box = ast.literal_eval(markers.at[row, "coords"])
        flag = markers.at[row, "flag"]
        if flag == -1:
            continue
        build_marker(image, box, colors[flag])


if __name__ == "__main__":
    image = cv2.imread(os.path.join(os.path.dirname(
        __file__), "2211.11559.pdf_page_2.png"))
    markers = pd.read_csv("./markers.csv")
    highlight_image(image, markers)
    cv2.imwrite("highlighted.png", image)
