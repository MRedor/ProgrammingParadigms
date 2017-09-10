import sys


def read_words(filename):
    words = []
    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())
    return words


def print_top(filename):
    words = read_words(filename)

    w_cnt = dict()
    for i in range(len(words)):
        words[i] = words[i].lower()
        if (words[i] in w_cnt):
            w_cnt[words[i]] += 1
        else:
            w_cnt[words[i]] = 1

    ans = []
    for key in w_cnt:
        ans.append([w_cnt[key], key])

    ans.sort(reverse=True)
    for i in range(min(20, len(ans))):
        print(ans[i][1], ans[i][0])


def print_words(filename):
    words = read_words(filename)
    for i in range(len(words)):
        words[i] = words[i].lower()
    words.sort()

    cnt = 1
    for i in range(1, len(words)):
        if (words[i] != words[i - 1]):
            print(words[i - 1], cnt)
            cnt = 1
        else:
            cnt += 1

    print(words[len(words) - 1], cnt)


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
