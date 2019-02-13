import re
from os import walk
from os.path import join

import spacy


def get_filepaths(directory, desired_format):
    """
    This function will generate the file names in a directory tree by walking the tree either top-down or bottom-up.
    For each directory in the tree rooted at directory top (including top itself), it yields a 3-tuple
    (dirpath, dirnames, filenames).
    """
    file_paths = []
    for root, directories, files in walk(directory):
        for filename in files:
            if filename != 'log.txt':
                filepath = join(root, filename)
                regex = '.' + desired_format + '$'
                if re.search(regex, filepath.lower()) is not None:
                    file_paths.append(filepath)
    return file_paths


nlp = spacy.blank('ru')

if __name__ == "__main__":
    import argparse
    import logging
    import json
    from tqdm import tqdm

    from brat2spacy import brat2spacy

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('Converting brat to spaCy')
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', help='Path to the folder, containing brat annotation files.', required=True,
                        type=str)
    parser.add_argument('--output_path', help='Path for resulting file in json format', required=True, type=str)
    args = parser.parse_args()

    pairs = {}
    for file in get_filepaths(args.input_path, 'ann'):
        id_ = file.split('/')[-1].split('.')[0]
        pairs[id_] = {'text': file.replace('.ann', '.txt'), 'ann': file}

    train_data = []
    for k, v in tqdm(pairs.items(), total=len(pairs.keys())):
        with open(v['text'], 'r') as f:
            text = f.read()
        with open(v['ann'], 'r') as f:
            ann = f.read()
        if ann == '':
            continue
        gold = brat2spacy(tokenizer=nlp, ann=ann, text=text, corpus=False, newline_sentence=False)
        train_data.append(gold)

    with open(args.output_path, 'w') as f:
        f.write(json.dumps(train_data))
