# WikiHow dataset for sentence similarity

This dataset is extracted from WikiHow with goal of making matching pairs of similar sentences.

For more information on the original WikiHow dataset [check the repository](https://github.com/mahnazkoupaee/WikiHow-Dataset) and the paper on https://arxiv.org/abs/1810.09305. The source file need to run the extraction script is `wikihowSep.csv` and can be downloaded from this link below:

https://ucsb.box.com/s/7yq601ijl1lzvlfu4rjdbbxforzd2oag

To generate the `jsonl` file with pairs of texts using the python script in this repository, first install pandas and spacy and then run:

```
$ python extract.py <path to wikihowSep.csv> --output wikihow.jsonl
```

The compressed output file is also included in the repository.

