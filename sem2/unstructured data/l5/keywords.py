import pdfplumber
import nltk


# from nltk.corpus import stopwords


def extract_keywords(pdf):
    """
    :param pdf
    :return: a list of tuples [(word, number_of_occurrences)]
    """

    tokens = []
    for page in pdf.pages:
        if page.extract_text() is not None:
            sample = page.extract_text().replace('\n', ' ')
            tokens += nltk.tokenize.word_tokenize(sample)
    tokens = nltk.pos_tag(tokens)
    lemmatizer = nltk.stem.WordNetLemmatizer()
    wnpos = lambda e: ('a' if e[0].lower() == 'j' else e[0].lower()) if e[0].lower() in ['n', 'r', 'v'] else 'n'
    # tokens = [lemmatizer.lemmatize(word, wnpos(part)) for word, part in tokens if
    #           # part[0].isalpha()
    #           part == 'NN' or part == 'NNS' and "'" not in word]
    words = [word for word, part in tokens if (part == 'NN' or part == 'NNS') and "'" not in word]
    print(tokens)
    stopwords = nltk.corpus.stopwords.words('english')
    words = [t for t in words if t not in stopwords]
    d = {}
    for word in words:
        d[word] = d.get(word, 0) + 1

    sorted_words, _ = zip(*sorted(d.items(), key=lambda item: item[1], reverse=True))
    print(sorted_words[:20])
    # return sorted_d


if __name__ == '__main__':
    pdf = pdfplumber.open("HP.pdf")
    # keywords = extract_keywords(pdf)
    # print(keywords)
    extract_keywords(pdf)
