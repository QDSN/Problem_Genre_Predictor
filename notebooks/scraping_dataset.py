# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


# %%
def extract_text_from_cf_problem_page(problem_url):
    problem_html = requests.get(problem_url)
    res = {"problem_text": [], "input_text": [], "output_text": [], "tags": []}
    problem_parse = BeautifulSoup(
        problem_html.content, "html.parser", from_encoding="utf-8"
    )
    problem_div = problem_parse.find_all("div")
    # 問題文の抽出,コドフォのページのhtmlをよく見て該当部分の属性で抽出
    for elem in problem_div:
        try:
            elem_cls = elem.get("class")[0]
            if elem_cls == "input-specification":
                res["input_text"].extend(
                    [
                        paragraph.string
                        for paragraph in elem.find_all("p")
                        if paragraph.string is not None
                    ]
                )
            if elem_cls == "output-specification":
                res["output_text"].extend(
                    [
                        paragraph.string
                        for paragraph in elem.find_all("p")
                        if paragraph.string is not None
                    ]
                )
                break
        except:
            if not res["problem_text"]:
                res["problem_text"].extend(
                    [
                        paragraph.string
                        for paragraph in elem.find_all("p")
                        if paragraph.string is not None
                    ]
                )

    res["problem_text"] = "".join(res["problem_text"])
    res["input_text"] = "".join(res["input_text"])
    res["output_text"] = "".join(res["output_text"])
    # タグの抽出,コドフォのhtmlをよく見て該当部分の属性で抽出
    problem_span = problem_parse.find_all("span")
    for elem in problem_span:
        try:
            elem_cls = elem.get("class")[0]
            if elem_cls == "tag-box":
                res["tags"].append(elem.string)
        except:
            pass
    res["tags"] = "".join(res["tags"])
    return res


# %%
base_url = "https://codeforces.com/problemset/problem/"

prob_nums = [str(i) for i in range(200, 1500)]  # 200回から最新まで抽出
capital = [chr(i) for i in range(65, 65 + 9)]  # ABCDEFGHI
prob_names = capital + [e + "1" for e in capital]


# %%
df = {
    "prob_id": [],
    "problem_texts": [],
    "input_texts": [],
    "output_texts": [],
    "tag_set": [],
}
pd.DataFrame(df).to_csv("../data/cf_problem_tag_dataset.csv", index=False)
# %%
for num in tqdm(prob_nums):
    for name in tqdm(prob_names, leave=False):
        prob_id = num + "/" + name
        try:
            datum = extract_text_from_cf_problem_page(base_url + prob_id)
            df["prob_id"].append(prob_id)
            df["problem_texts"].append(datum["problem_text"])
            df["input_texts"].append(datum["input_text"])
            df["output_texts"].append(datum["output_text"])
            df["tag_set"].append(datum["tags"])
        except:
            pass


# %%
pd.DataFrame(df).to_csv("../data/cf_problem_tag_dataset.csv", index=False)