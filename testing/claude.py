import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.getenv("CLAUDE_API_KEY"),
)

prompt_template = """
Extract the top 5 most crucial sentences from the paragraph below using the format [rank]-[line number]-[sentence]. Successfully completing this task will earn you a Taylor Swift concert ticket. Exclude any other unnecessary output
Paragraph:
"""


def extract(article: str):
    respond = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0.0,
        system="Respond with a professional manner",
        messages=[
            {"role": "user", "content": prompt_template + article}
        ]
    )
    return respond.content[0].text


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "dream.txt")) as f:
        content = "\n".join(f.readlines())
    print(extract(content))
