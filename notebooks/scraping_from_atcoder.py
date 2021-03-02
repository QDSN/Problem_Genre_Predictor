# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


# %%
def extract_text_from_atcoder_problem_page(problem_url):
    res = {"problem_text": "", "constraint": "", "input_text": "", "output_text": ""}
    problem_html = requests.get(problem_url)
    problem_parse = BeautifulSoup(
        problem_html.content, "html.parser", from_encoding="utf-8"
    )
    problem_span = problem_parse.find_all("span")
    for elem in problem_span:
        try:
            elem_cls = elem.get("class")[0]
            if elem_cls == "lang-en":
                (
                    res["problem_text"],
                    res["constraint"],
                    res["input_text"],
                    res["output_text"],
                ) = [paragraph.text for paragraph in elem.find_all("section")][:4]
        except:
            pass
    return res


# %%
base_url = "https://atcoder-tags.herokuapp.com/tag_search/"
tags_list = [
    "Easy",
    "Ad-Hoc",
    "Searching",
    "Greedy-Methods",
    "String",
    "Mathematics",
    "Technique",
    "Construct",
    "Graph",
    "Dynamic-Programming",
    "Data-Structure",
    "Game",
    "Flow-Algorithms",
    "Geometry",
]


# %%
df = {
    "urls": [],
    "problem_texts": [],
    "constraints": [],
    "input_texts": [],
    "output_texts": [],
    "tag": [],
}


# %%
atcoder_tags_url = base_url + tags_list[0]
atcoder_tags_html = requests.get(atcoder_tags_url)
atcoder_tags_parse = BeautifulSoup(
    atcoder_tags_html.content, "html.parser", from_encoding="utf-8"
)


# %%
for tag in tags_list:
    atcoder_tags_url = base_url + tag
    atcoder_tags_html = requests.get(atcoder_tags_url)
    atcoder_tags_parse = BeautifulSoup(
        atcoder_tags_html.content, "html.parser", from_encoding="utf-8"
    )
    prob_urls = [
        url.get("href")
        for url in atcoder_tags_parse.find_all("a")
        if url.get("href").startswith("http")
    ]
    for url in prob_urls:
        datum = extract_text_from_atcoder_problem_page(url)
        df["urls"].append(url)
        df["problem_texts"].append(datum["problem_text"])
        df["constraints"].append(datum["constraint"])
        df["input_texts"].append(datum["input_text"])
        df["output_texts"].append(datum["output_text"])
        df["tag"].append(tag)


# %%
pd.DataFrame(df).to_csv("../data/cf_problem_tag_dataset.csv", index=False)
