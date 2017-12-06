import argparse
from collections import Counter, defaultdict


class GenderStat:
    def __init__(self, m=0, f=0, n=0):
        self.dict = {
            'm': m,
            'f': f,
            'n': n,
        }

    def add(self, gender):
        self.dict[gender] += 1
        return self

    def count(self):
        return sum(self.dict.values())

    def most_freq(self):
        total = sum(self.dict.values())
        return max([v / total for v in self.dict.values()])

    def most_freq_key(self):
        return max(self.dict.items(), key=lambda x: x[1])[0]


class Analyzer:
    def __init__(self):
        self.data = {}
        self.endings = defaultdict(GenderStat)

    def load(self):
        with open('dict.cc_nouns_with_gender.txt', encoding='utf8') as file:
            for line in file:
                word, gender = line.strip().split(' ')
                self.data[word] = gender
        return self

    def analyze_ending_frequencies(self, ending):
        return Counter([gender for word, gender in self.data.items() if word.endswith(ending)])

    def extract_endings(self, max_length=5):
        for word, gender in self.data.items():
            for i in range(1, max_length + 1):
                ending = word[-i:]
                self.endings[ending].add(gender[1:2])
        return self


def main(endings):
    anal = Analyzer().load()
    print('\tder\tdie\tdas')
    for ending in endings:
        count = anal.analyze_ending_frequencies(ending)
        total = sum(count.values())
        frequ = {k[1:2]: v / total for k, v in count.items()}
        for key in ['m', 'f', 'n']:
            if key not in frequ:
                frequ[key] = 0.0
        print('%s\t%.2f\t%.2f\t%.2f' % (ending, frequ['m'] * 100, frequ['f'] * 100, frequ['n'] * 100))


def main2(n_m, n_f, n_n, sort_method, min_freq, min_count, suffix_free=False):
    anal = Analyzer().load().extract_endings(10)
    freq = [(word, gs) for word, gs
            in anal.endings.items()
            if gs.most_freq() > min_freq and gs.count() > min_count]
    if sort_method == 'COUNT':
        freq.sort(key=lambda x: x[1].most_freq(), reverse=True)
        freq.sort(key=lambda x: x[1].count(), reverse=True)
    if sort_method == 'FREQ':
        freq.sort(key=lambda x: x[1].count(), reverse=True)
        freq.sort(key=lambda x: x[1].most_freq(), reverse=True)
    freq_m = list(filter(lambda x: x[1].most_freq_key() == 'm', freq))
    freq_f = list(filter(lambda x: x[1].most_freq_key() == 'f', freq))
    freq_n = list(filter(lambda x: x[1].most_freq_key() == 'n', freq))

    def free_suffix(l, count=50):
        result = []
        words = set()
        for word, gs in l:
            if not any([word.endswith(previous_word) for previous_word in words]):
                result.append((word, gs))
                words.add(word)
                if len(result) >= count:
                    return result
        return result

    if suffix_free:
        freq_m = free_suffix(freq_m)
        freq_f = free_suffix(freq_f)
        freq_n = free_suffix(freq_n)
    for word, gs in (freq_m[:n_m] + freq_f[:n_f] + freq_n[:n_n]):
        total = gs.count()
        print('-{:9s} & {:3.2f} & {:3.2f} & {:3.2f} & {} \\\\'.format(
            word, 100 * gs.dict['m'] / total, 100 * gs.dict['f'] / total, 100 * gs.dict['n'] / total, gs.count()))


if __name__ == '__main__':
    cmdline_parser = argparse.ArgumentParser('parser')
    cmdline_parser.add_argument('-m', default=10, help='number of masculine to show', type=int)
    cmdline_parser.add_argument('-f', default=10, help='number of feminine to show', type=int)
    cmdline_parser.add_argument('-n', default=10, help='number of neuter to show', type=int)
    cmdline_parser.add_argument('-s', '--sort', choices=['COUNT', 'FREQ'], default='COUNT')
    cmdline_parser.add_argument('-d', '--defaults', type=bool, help='show stats for default endings')
    cmdline_parser.add_argument('-e', '--endings', type=str, nargs='+', help='endings to extract info about')
    cmdline_parser.add_argument('--min-count', type=int, default=5)
    cmdline_parser.add_argument('--min-freq', type=float, default=0.8)
    cmdline_parser.add_argument('-x', '--suffix-free', type=bool)

    args, unknowns = cmdline_parser.parse_known_args()

    if args.defaults:
        endings = [
            'ling', 'or', 'us', 'er',
            'e', 'ei', 'heit', 'keit', 'schaft', 'tät', 'ung', 'ik', 'ur', 'ion',
            'chen', 'lein', 'ment', 'nis', 'um', 'tum',
        ]
        main(endings)

    if args.endings is not None:
        main(args.endings)

    main2(args.m, args.f, args.n, args.sort, args.min_freq, args.min_count, args.suffix_free)
