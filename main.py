import image2paragraph
import claude
import reconstruct_pos
import os


def main():
    # use opencv to take picture
    picture_path = os.path.join(os.path.dirname(
        __file__), "2211.11559.pdf_page_2.png")
    paragraph = image2paragraph.scan(picture_path)
    paragraph.to_csv("./paragraph.csv")
    fragment = image2paragraph.scan(picture_path, False)
    fragment.to_csv("./fragment.csv")
    content = image2paragraph.extract(paragraph)
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


if __name__ == "__main__":
    main()
