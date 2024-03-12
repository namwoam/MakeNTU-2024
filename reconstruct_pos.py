import pylcs
from pandas import DataFrame

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
