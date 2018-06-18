import spacy

from brat2spacy import brat2spacy, spacy2brat


def test_brat2spacy():
    text = """ROOT Äktenskapet och familjen är en gammal institution , som funnits sedan 1800-talet ."""

    ann = """T1	ROOT 0 4	ROOT
T2	NN 5 16	Äktenskapet
T3	++ 17 20	och
T4	NN 21 29	familjen
T5	AV 30 32	är
T6	EN 33 35	en
T7	AJ 36 42	gammal
T8	NN 43 54	institution
T9	IK 55 56	,
T10	PO 57 60	som
T11	VV 61 68	funnits
T12	PR 69 74	sedan
T13	NN 75 85	1800-talet
T14	IP 86 87	.
R1	SS Arg1:T5 Arg2:T2
R2	++ Arg1:T4 Arg2:T3
R3	CC Arg1:T2 Arg2:T4
R4	ROOT Arg1:T1 Arg2:T5
R5	DT Arg1:T8 Arg2:T6
R6	AT Arg1:T8 Arg2:T7
R7	SP Arg1:T5 Arg2:T8
R8	IK Arg1:T8 Arg2:T9
R9	SS Arg1:T11 Arg2:T10
R10	ET Arg1:T8 Arg2:T11
R11	TA Arg1:T11 Arg2:T12
R12	PA Arg1:T12 Arg2:T13
R13	IP Arg1:T5 Arg2:T14"""
    nlp = spacy.blank('en')  # create blank Language class
    gold, text = brat2spacy(nlp, ann, text)
    assert len(gold.tags) == len(gold.words) == len(gold.labels) == len(gold.heads) == 14
    assert gold.heads[0] == 0
    assert gold.heads[1] == gold.heads[-1] == 4
    assert gold.labels[4] == 'ROOT'
    assert gold.heads[4] == 4


def test_spacy2brat():
    import spacy
    nlp = spacy.load('web_core_sm')
    text = "Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that " \
           "designs, develops, and sells consumer electronics, computer software, and online services. The " \
           "company's hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal " \
           "computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, " \
           "and the HomePod smart speaker. Apple's software includes the macOS and iOS operating systems, the iTunes " \
           "media player, the Safari web browser, and the iLife and iWork creativity and productivity suites, as well" \
           " as professional applications like Final Cut Pro, Logic Pro, and Xcode. Its online services include the " \
           "iTunes Store, the iOS App Store and Mac App Store, Apple Music, and iCloud."
    doc = nlp(text)
    tokens, relations, entities = spacy2brat(doc)
    return tokens, relations, entities
