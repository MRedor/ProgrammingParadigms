import sys


def read_words(filename):
    words = []
    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())
    return words


def make_dict(filename):
    words = read_words(filename)
    new_dict = dict()
    for word in words:
        word = word.lower()
        if word in new_dict:
            new_dict[word] += 1
        else:
            new_dict[word] = 1
    return new_dict


def make_countlist(filename):
    w_cnt = make_dict(filename)
    ans = list(w_cnt.items())
    return ans


def print_top(filename):
    ans = make_countlist(filename)
    ans.sort(key=lambda x: x[1], reverse=True)

    for word, count in ans[:20]:
        print(word, count)


def print_words(filename):
    ans = make_countlist(filename)
    ans.sort()

    for word, count in ans:
        print(word, count)


def main():
    if len(sys.argv) != 3:
        print('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print('unknown option: ' + option)
        sys.exit(1)

if __name__ == '__main__':
    main()
