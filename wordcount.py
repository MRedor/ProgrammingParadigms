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
    for i in range(len(words)):
        words[i] = words[i].lower()
        if (words[i] in new_dict):
            new_dict[words[i]] += 1
        else:
            new_dict[words[i]] = 1
    return new_dict


def print_top(filename):
    w_cnt = make_dict(filename)

    ans = []
    for key in w_cnt:
        ans.append([key, w_cnt[key]])

    ans.sort(key=lambda x: x[1], reverse=True)

    for word, count in ans[:20]:
        print(word, count)


def print_words(filename):
    w_cnt = make_dict(filename)

    ans = []
    for key in w_cnt:
        ans.append([key, w_cnt[key]])

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
