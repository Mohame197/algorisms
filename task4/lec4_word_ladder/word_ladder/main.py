import argparse

from word_ladder import load_words, word_ladder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("start")
    parser.add_argument("target")
    parser.add_argument("--words", default="data/words.txt")
    args = parser.parse_args()

    ladder = word_ladder(load_words(args.words), args.start, args.target)
    if ladder is None:
        print("no ladder")
        return
    print(" -> ".join(ladder))
    print(f"{len(ladder)} words = {len(ladder) - 1} changes")


if __name__ == "__main__":
    main()
