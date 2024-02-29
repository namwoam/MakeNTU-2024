import easyocr
import os
import pandas as pd
from pandas import DataFrame
# this needs to run only once to load the model into memory
reader = easyocr.Reader(['ch_sim', 'en'])


def scan(file_path: str):
    result = reader.readtext(file_path, paragraph=True)
    df = pd.DataFrame(result, columns=["coords",  "content"])
    return df


def extract(df: DataFrame):
    # clean_df = df[df["conf"] > 0.6]
    # print(len(clean_df))
    return "\n".join(df["content"].values.tolist())


if __name__ == "__main__":
    scan_result = scan(os.path.join(os.path.dirname(
        __file__), "2212.10156.pdf_page_15.png"))
    text = extract(scan_result)
    print(text)
