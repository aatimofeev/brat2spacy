def spacy2brat(doc):
    tokens = []
    relations = []
    for token in doc:
        tokens.append("T{id}\t{tag} {start} {end}\t{text}".format(id=str(token.i),
                                                                  start=token.idx,
                                                                  end=token.idx + len(token),
                                                                  tag=token.pos_,
                                                                  text=token.text
                                                                  ))
        relations.append("R{id}\t{label}  Arg1:T{head} Arg2:T{dep}".format(id=str(token.i),
                                                                           label=token.dep_,
                                                                           head=token.head.i,
                                                                           dep=token.i
                                                                           ))

    entities = []
    for id_, entity in enumerate(doc.ents):
        entities.append("T{id}\t{type} {start} {end}\t{text}".format(id=id_,
                                                                     type=entity.label_,
                                                                     start=entity.start_char,
                                                                     end=entity.end_char,
                                                                     text=entity.text))
    return tokens, relations, entities
