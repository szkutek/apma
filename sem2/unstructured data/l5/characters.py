import pdfplumber
import nltk
import matplotlib.pyplot as plt


def extract_names_from_page_NNP(page):
    """
    :param page: page from pdf.pages
    :return: None if there is no text on the page
    or a list of tuples [(char_name, number_of_occurrences)]
    """
    if page.extract_text() is None:
        return None
    sample = page.extract_text().replace('\n', ' ')

    sentences = nltk.sent_tokenize(sample)
    tokens = nltk.tokenize.word_tokenize(sample)
    # print(tokens)
    tags = nltk.pos_tag(tokens)
    # print(tags)

    nnp = [t[0] for t in tags if t[1] == 'NNP' or t[1] == 'NNPS']  # get only proper nouns

    names = []
    name = ''
    for i, word in enumerate(nnp):
        if word == 'Mr.' or word == 'Mrs.' or word == 'Professor':
            name += word + ' '
        elif word != 'Mr.' and word != 'Mrs.':
            name += word
            names.append(name)
            name = ''

    d = {}
    for name in names:
        d[name] = d.get(name, 0) + 1

    sorted_d = sorted(d.items(), key=lambda item: item[1], reverse=True)
    return sorted_d


def compile_res_per_page(index, tuples, compiled_res):
    """
    :param index: page number
    :param tuples: [(char_name, number of occurrences per page)]
    :param compiled_res: dictionary of the form {char_name: {page_number: number_of_occurrences}}
    :return: None if the list of tuples is None
    """
    if tuples is None:
        return None
    for name, number in tuples:
        if name in compiled_res:
            compiled_res[name][index] = number
        else:
            compiled_res[name] = {index: number}
    return None


def ex1(res_per_char_per_page):
    marker_size = 15
    for name in res_per_char_per_page:
        x, y = zip(*res_per_char_per_page[name].items())
        plt.plot(x, y, 'o', MarkerSize=marker_size)
        marker_size -= 2
    plt.legend(res_per_char_per_page.keys())
    plt.xlabel('page number')
    plt.ylabel('number of occurrences')
    plt.title('Character mentions per page')
    plt.savefig('ex1-character-mentions-150.png')
    plt.clf()


def ex4(res_per_char_per_page):
    for name in res_per_char_per_page:
        for x in res_per_char_per_page[name].keys():
            plt.plot(x, name, 'b.', MarkerSize=5)
    plt.xlabel('page number')
    plt.ylabel('character')
    plt.title('Graph of co-occurrences')
    plt.savefig('ex4-cooccurrences-150.png')
    plt.clf()


if __name__ == '__main__':
    pdf = pdfplumber.open("HP.pdf")
    # create dictionary of the form {char_name: {page_number: number_of_occurrences}}
    compiled_res_per_char_per_page = {}
    for index, page in enumerate(pdf.pages[:150]):
        tuples = extract_names_from_page_NNP(page)
        compile_res_per_page(index, tuples, compiled_res_per_char_per_page)
    # print(compiled_res_per_char_per_page)

    # LIMIT RESULTS TO THE MOST COMMON CHARACTERS IN THE WHOLE BOOK
    # get number of occurrences in the whole book per character
    compiled_res_per_char = {}
    for name, occurrences in compiled_res_per_char_per_page.items():
        compiled_res_per_char[name] = sum(occurrences.values())
    # sort by number of occurrences in the whole book
    sorted_per_char = sorted(compiled_res_per_char.items(),
                             key=lambda item: item[1], reverse=True)
    # get only the most common characters
    limited_characters, numbers = zip(*sorted_per_char)

    # get the number of occurrences per page for limited number of characters
    limited_res_per_page = {ch: compiled_res_per_char_per_page[ch] for ch in limited_characters[:5]}
    print(limited_res_per_page)

    ex1(limited_res_per_page)
    ex4(limited_res_per_page)
