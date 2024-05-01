import cv2
import os
import pandas as pd
import ast

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
          (0, 255, 255), (255, 0, 255), (0, 255, 255)]


def build_marker(image, pt1, pt2, color=(0, 0, 0), thickness=10):
    cv2.rectangle(image, pt1, pt2, color, thickness)


def highlight_image(image, markers):
    for row in range(len(markers)):
        flag = markers.at[row, "flag"]
        pt1 = (int(markers.at[row , "x1"]) , int(markers.at[row , "y1"]))
        pt2 = (int(markers.at[row , "x2"]) , int(markers.at[row , "y2"]))
        if flag == -1:
            continue
        build_marker(image, pt1, pt2, colors[flag])


if __name__ == "__main__":
    image = cv2.imread(os.path.join(os.path.dirname(
        __file__), "2211.11559.pdf_page_2.png"))
    markers = pd.read_csv("./refined_markers.csv")
    highlight_image(image, markers)
    cv2.imwrite("refined_highlighted.png", image)
