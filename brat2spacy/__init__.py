from collections import defaultdict

from spacy.gold import biluo_tags_from_offsets, offsets_from_biluo_tags, GoldParse

annotation_ids = {'T': 'entity',  # text-bound annotation
                  'R': 'relation',
                  'E': 'event',
                  'A': 'attribute',
                  'M': 'modification',
                  'N': 'normalization',
                  "*": 'equivalence'}


def brat2spacy(tokenizer, ann, text):
    doc = tokenizer(text)
    words = [i.text for i in doc]
    entity_ids = defaultdict(tuple)
    relation_ids = defaultdict(tuple)
    entities = []
    for line in ann.strip().split('\n'):
        annotation = line.strip().rsplit('\t')
        id_ = annotation[0]
        if id_ == '*':
            ann_type = id_[0]
        else:
            ann_type = annotation_ids[id_[0]]
        if ann_type == 'entity':
            if len(annotation[1:]) == 2:
                span, surface_form = annotation[1:]
                entity_type, start, end = span.split(' ')
                entity_ids[id_] = (int(start), int(end))
                entities.append((int(start), int(end), entity_type))
        if ann_type == 'relation':
            if len(annotation[1:]) == 1:
                rel_type, head, dep = annotation[1].split(' ')
                relation_ids[id_] = (rel_type, head, dep)
    entities.sort(key=lambda x: x[0])
    tags = biluo_tags_from_offsets(doc, entities)
    if relation_ids:
        # mapping from brat ids to doc's id
        brat_doc_ids_map = {}
        for entity in entity_ids:
            span = doc.char_span(*entity_ids[entity])
            if span.end - span.start == 1:
                brat_doc_ids_map[entity] = span.start
            else:
                # raise Warning("Tokenization mismatch, more than 1 spaCy token in ann token span")
                brat_doc_ids_map[entity] = span.start
        ids = range(len(doc))
        heads = defaultdict(int)
        deps = defaultdict(int)
        for rel_id, rel in relation_ids.items():
            dep, token, head = rel
            token, head = brat_doc_ids_map[token.split(':')[1]], brat_doc_ids_map[head.split(':')[1]]
            heads[head] = token
            deps[head] = dep
        heads = [i[1] if i[1] > 0 else i[0] for i in [(i, heads[i]) for i in ids]]
        deps = [i[1] if i[1] != 0 else 'ROOT' for i in [(i, deps[i]) for i in ids]]
        assert len(words) == len(heads) == len(deps) == len(tags)
        return GoldParse(doc, words=words, heads=heads, tags=tags, deps=deps, entities=entities), text
    else:
        assert len(words) == len(tags)
        return GoldParse(doc, words=words, tags=tags, entities=offsets_from_biluo_tags(doc, tags)), text
