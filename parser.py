from collections import Counter

class Analyzer:
    def __init__(self):
        self.data = {}

    def load(self):
        with open('dict.cc_nouns_with_gender.txt', encoding='utf8') as file:
            for line in file:
                word, gender = line.strip().split(' ')
                self.data[word] = gender
        return self

    def analyze_ending_frequencies(self, ending):
        return Counter([gender for word, gender in self.data.items() if word.endswith(ending)])


def main(endings):
    anal = Analyzer().load()
    print('\tder\tdie\tdas')
    for ending in endings:
        print(ending, end=', \t')
        count = anal.analyze_ending_frequencies(ending)
        total = sum(count.values())
        frequ = {k[1:2]: v / total for k, v in count.items()}
        for key in ['m', 'f', 'n']:
            if key not in frequ:
                frequ[key] = 0.0
        print('%.2f\t%.2f\t%.2f' % (frequ['m'] * 100, frequ['f'] * 100, frequ['n'] * 100))


if __name__ == '__main__':
    endings = [
        'ling', 'or', 'us', 'er',
        'e', 'ei', 'heit', 'keit', 'schaft', 'ung', 'tät', 'ik', 'ur', 'ion',
        'chen', 'lein', 'ment', 'nis', 'um', 'tum',
    ]
    main(endings)
