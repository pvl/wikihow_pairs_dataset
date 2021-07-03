import re
import json
import argparse
import pandas as pd
from spacy.lang.en import English

nlp = English()
nlp.add_pipe(nlp.create_pipe("sentencizer"))


def extract_paragraphs(text, min_size=150):
    """ Split the text in sentences and include the first sentences 
    until the min_size number of characters is reached
    """
    if len(text) <= min_size:
        return text
    output = ""
    for sent in nlp(text).sents:
        output += sent.text + " "
        if len(output) >= min_size:
            break
    return output.strip()


def clean_title(txt):
    while txt[-1].isdigit():
        txt = txt[:-1]
    return txt


def preprocess(data):
    # only using overview text, remove the duplication
    data = data.drop_duplicates(subset='overview').copy()
    data = data.fillna("")
    # the intent lable is the title without the "How to" section
    data['title'] = data['title'].str.replace('How to', '').str.strip().apply(clean_title)
    # use only overview as summary for the title text
    data['overview'] = data.overview.apply(extract_paragraphs)
    data = data[(data.title != '') & (data.overview != '')]
    return data


def main(datapath, output, nrows=None):
    data = pd.read_csv(datapath, nrows=nrows)
    data = preprocess(data)
    lines = []
    for title, overview in data[["title", "overview"]].values:
        lines.append(json.dumps([title, overview]))
    with open(output, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess WikiHow")
    parser.add_argument("datapath", type=str, help="Path to the wikihowSep.csv file")
    parser.add_argument("--output", type=str, default="wikihow.jsonl",
                        help="Path to the output jsonl file")
    parser.add_argument("--nrows", type=int, default=-1, help="number of rows (-1 includes all rows)")
    args = parser.parse_args()
    if args.nrows == -1:
        args.nrows = None
    main(args.datapath, args.output, args.nrows)