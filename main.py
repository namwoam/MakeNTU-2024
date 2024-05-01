import ocr
import claude
import reconstruct_pos
import os
import cv2
import visualize


def main():
    # use opencv to take picture
    picture_path = os.path.join(os.path.dirname(
        __file__), "2211.11559.pdf_page_2.png")
    paragraph = ocr.scan(picture_path)
    paragraph.to_csv("./paragraph.csv")
    fragment = ocr.scan(picture_path, False)
    fragment.to_csv("./fragment.csv")
    content = ocr.extract(paragraph)
    with open(os.path.join(os.path.dirname(__file__), "content.txt"), "w") as writer:
        writer.write(content)
    claude_result = claude.extract(content)
    with open(os.path.join(os.path.dirname(__file__), "claude_respond.txt"), "w") as writer:
        writer.write(claude_result)
    sentences = claude.clean(claude_result)
    with open(os.path.join(os.path.dirname(__file__), "claude_sentences.txt"), "w") as writer:
        writer.writelines(sentence + '\n' for sentence in sentences)
    markers = reconstruct_pos.reconstruct(fragment, sentences)
    markers.to_csv("./markers.csv")
    markers = reconstruct_pos.refine(markers, sentences)
    image = cv2.imread(os.path.join(os.path.dirname(
        __file__), "2211.11559.pdf_page_2.png"))
    visualize.highlight_image(image, markers)
    cv2.imwrite("highlighted.png", image)


if __name__ == "__main__":
    main()
