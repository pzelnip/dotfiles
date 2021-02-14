#!/usr/bin/env python3

import sys
import string


def map_letter(letter):
    return (
        {letter: f":alphabet-white-{letter}:" for letter in string.ascii_lowercase}
        | {letter: f":alphabet-yellow-{letter}:" for letter in string.ascii_uppercase}
        | {
            "#": ":alphabet-yellow-hash:",
            "!": ":alphabet-yellow-exclamation:",
            "@": ":alphabet-yellow-at:",
            "?": ":alphabet-yellow-question:",
        }
    ).get(letter, letter)


def main():
    print("enter string, ctrl+d (EOF) to stop", file=sys.stderr)
    input_str = "".join(sys.stdin.readlines())
    print("".join(map_letter(letter) for letter in input_str))


if __name__ == "__main__":
    exit(main())
