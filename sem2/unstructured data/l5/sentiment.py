import pdfplumber
import matplotlib.pyplot as plt
import requests
import concurrent.futures


def get_sentiment(t):
    i, text = t
    try:
        req = requests.post(url, "text=" + text)
        # print(req)
        if req.status_code < 300:
            json = req.json()
            # return index, {'neg': -1, 'neutral': 0, 'pos': 1}[json['label']]
            return i, json['label']
    except:
        print("ERROR")
    return i, 'none'


if __name__ == '__main__':
    url = 'http://text-processing.com/api/sentiment/'
    pdf = pdfplumber.open("HP.pdf")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=64)

    sentiments = []
    texts = []
    futures = []

    for i, page in enumerate(pdf.pages):
        if page.extract_text() is not None:
            texts.append((i, page.extract_text().replace('\n', ' ')))
    for t in texts:
        futures.append(executor.submit(get_sentiment, t))

    completed_futures = concurrent.futures.as_completed(futures)  # wait for all processes to end
    for future in completed_futures:
        res = future.result()
        print(res)
        if res[1] != 'none':
            sentiments.append(res)

    x, y = zip(*sentiments)
    plt.plot(x, y, 'o')
    plt.xlabel('page number')
    plt.ylabel('sentiment')
    plt.title('Sentiment of every page')
    # plt.show()
    plt.savefig('sentiment.png')

    pdf.close()
