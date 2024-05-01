from pandas import DataFrame
import numpy as np
import pandas as pd

threshold = 0.6


def compute_lwcs(short_str, long_str):
    s1 = short_str.split(" ")
    s2 = long_str.split(" ")
    m = len(s1)
    n = len(s2)
    L = [[None]*(n+1) for i in range(m+1)]

    # Following steps build L[m+1][n+1] in bottom up fashion
    # Note: L[i][j] contains length of LCS of X[0..i-1]
    # and Y[0..j-1]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif s1[i-1] == s2[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]


def reconstruct(df: DataFrame, sentences: list[str]):
    result_df = df.copy()
    result_df["flag"] = -1
    for row in range(len(df)):
        text = df.loc[row].at["content"]
        for k in range(len(sentences)):
            lwcs = compute_lwcs(text, sentences[k])
            if len(text.split(" "))*threshold < lwcs:
                result_df.at[row, "flag"] = k
                print("lwcs:", lwcs, "s1:", text, "s2:", sentences[k])
                break
    return result_df


def refine(df: DataFrame, sentences: list[str]):
    result_df = df.copy()
    for k in range(len(sentences)):
        py_fragments = []
        for row in range(len(df)):
            if result_df.at[row, "flag"] == k:
                x_center = (result_df.at[row, "x1"]+result_df.at[row, "y1"])/2
                y_center = (result_df.at[row, "x2"]+result_df.at[row, "y2"])/2
                mass = abs((result_df.at[row, "x1"] - result_df.at[row, "x2"])
                           * (result_df.at[row, "y1"] - result_df.at[row, "y2"]))
                py_fragments.append((row, x_center, y_center, mass))
        fragments = np.array(py_fragments)
        # print(fragments.shape)
        x_com = np.average(fragments[:, 1], weights=fragments[:, 3])
        y_com = np.average(fragments[:, 2], weights=fragments[:, 3])
        dist = np.sqrt((fragments[:, 1] - x_com) **
                       2 + (fragments[:, 2] - y_com)**2)
        std = np.std(dist)
        # print(dist)
        # print(std)
        for i,  el in enumerate(py_fragments):
            if dist[i] > 2.5*std:
                result_df.at[el[0], "flag"] = -1
    # x_center , y_center =
    return result_df


if __name__ == "__main__":
    markers = pd.read_csv("./markers.csv", index_col=0)
    sentences = []
    with open("./claude_sentences.txt", "r") as reader:
        sentences = reader.read().split("\n")[:-1]
    markers = refine(markers, sentences)
    markers.to_csv("./refined_markers.csv")
