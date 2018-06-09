from distutils.core import setup

setup(
    name="brat2spacy",
    version='0.1.0',
    description="brat ann to spacy and vice versa",
    long_description="Tool for converting brat *.ann files to spaCy GoldParse objects and spaCy Doc object to brat "
                     "*.ann files.",
    author="Anton Timofeev",
    author_email="aatimofeev@hse.ru",
    url="https://github.com/aatimofeev/brat2spacy/",
    keywords="brat spacy",
    packages=['brat2spacy'],
    install_requires=['spacy'],
    tests_require=['pytest'],
)
