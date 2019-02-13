from collections import defaultdict

annotation_ids = {'T': 'entity',  # text-bound annotation
                  'R': 'relation',
                  'E': 'event',
                  'A': 'attribute',
                  'M': 'modification',
                  'N': 'normalization',
                  "*": 'equivalence'}


def brat2spacy(tokenizer, ann, text):
    doc = tokenizer(text)
    entity_ids = defaultdict(tuple)
    relation_ids = defaultdict(tuple)
    entities = []
    for line in ann.strip().split('\n'):
        if line == '':
            continue
        annotation = line.strip().rsplit('\t')
        id_ = annotation[0]
        try:
            if id_ == '*':
                ann_type = id_[0]
            else:
                ann_type = annotation_ids[id_[0]]
        except KeyError:
            continue
        if ann_type == 'entity':
            if len(annotation[1:]) == 2:
                span, surface_form = annotation[1:]
                try:
                    entity_type, start, end = span.split(' ')
                except ValueError:
                    span_list = span.split(' ')
                    entity_type = span_list[0]
                    start = span_list[1]
                    end = span_list[-1]
                entity_ids[id_] = (int(start), int(end))
                entities.append((int(start), int(end), entity_type))
        if ann_type == 'relation':
            if len(annotation[1:]) == 1:
                rel_type, head, dep = annotation[1].split(' ')
                relation_ids[id_] = (rel_type, head, dep)
    entities.sort(key=lambda x: x[0])
    return (doc.text, {'entities': entities})