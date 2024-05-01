import easyocr
import os
import pandas as pd
from pandas import DataFrame
import ast
import numpy as np
# this needs to run only once to load the model into memory
reader = easyocr.Reader(['ch_sim', 'en'])


def scan(file_path: str, full_text: bool = True):
    result = reader.readtext(file_path, paragraph=full_text)
    if full_text:
        df = pd.DataFrame(result, columns=["coords",  "content"])
    else:
        df = pd.DataFrame(result, columns=["coords",  "content", "conf"])
    coords = []
    for coord in df["coords"].values:
        try:
            coords.append(ast.literal_eval(str(coord)))
        except:
            pass
    coords = np.array(coords)
    print(df.shape)
    print(coords.shape)
    assert df.shape[0] == coords.shape[0]
    df["x1"] = coords[:,0,0]
    df["y1"] = coords[:,0,1]
    df["x2"] = coords[:,2,0]
    df["y2"] = coords[:,2,1]
    df.drop(columns=["content"])
    return df


def extract(df: DataFrame):
    clean_df = df[df["content"].str.len() > 30]
    # print(len(clean_df))
    return "\n".join(clean_df["content"].values.tolist())


if __name__ == "__main__":
    scan_result = scan(os.path.join(os.path.dirname(
        __file__), "2211.11559.pdf_page_2.png"), False)
    scan_result.to_csv("./test_fragment.csv")
