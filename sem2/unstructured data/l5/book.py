import pdfplumber
import nltk
import matplotlib.pyplot as plt


def extract_names_from_page_NNP(page):
    if page.extract_text() is None:
        return None
    sample = page.extract_text().replace('\n', ' ')

    sentences = nltk.sent_tokenize(sample)
    tokens = nltk.tokenize.word_tokenize(sample)
    tags = nltk.pos_tag(tokens)

    nnp = [t[0] for t in tags if t[1] == 'NNP']

    names = []
    name = ''
    for i, word in enumerate(nnp):
        if word == 'Mr.' or word == 'Mrs.' or word == 'Professor':
            name += word + ' '
        elif word != 'Mr.' and word != 'Mrs.':
            name += word
            names.append(name)
            name = ''

    d = {name: 0 for name in names}
    for name in names:
        d[name] += 1
    sorted_d = sorted([(k, v) for k, v in d.items() if v > 1], key=lambda item: item[1], reverse=True)
    # sorted_d = sorted([*d.items()], key=lambda item: item[1], reverse=True) # include one-time names
    # print(sorted_d)
    return sorted_d


def compile_res_per_page(index, tuples, compiled_res):
    if tuples is None:
        return
    for name, number in tuples:
        if name in compiled_res:
            compiled_res[name][index] = number
        else:
            compiled_res[name] = {index: number}
    return


if __name__ == '__main__':
    pdf = pdfplumber.open("HP.pdf")
    # res = [0] * len(pdf.pages[0:10])
    compiled_res_per_page = {}
    for index, page in enumerate(pdf.pages[0:10]):
        tuples = extract_names_from_page_NNP(page)
        compile_res_per_page(index, tuples, compiled_res_per_page)

    compiled_res_per_char = {}
    for name, occurences in compiled_res_per_page.items():
        compiled_res_per_char[name] = sum(occurences.values())
    sorted_per_char = sorted([(k, v) for k, v in compiled_res_per_char.items() if v > 5],
                             key=lambda item: item[1], reverse=True)
    limited_characters, numbers = zip(*sorted_per_char)

    limited_res = {compiled_res_per_page[ch] for ch in limited_characters}

    print(limited_res)

    # for i, r in enumerate(res):
    #     if r is not None:
    #         for k, v in r:
    #             plt.plot(i, v, '*')
    # plt.plot(numbers, chars, '*')
    # plt.show()
