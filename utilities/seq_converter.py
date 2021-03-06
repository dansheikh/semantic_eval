#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import gensim


def _main():
    """Converts target words from CoNLL formatted files to vectorized model representation."""
    parser = argparse.ArgumentParser(description='SeqConverter')
    parser.add_argument('-c', '--count', action='store', default=1, type=int)
    parser.add_argument('-l', '--length', action='store', default=100, type=int)
    parser.add_argument('-m', '--mode', action='store', required=True, choices=['cbow', 'skipgram'])
    parser.add_argument('-s', '--sep', action='store', default='\t')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-w', '--workers', action='store', default=1, type=int)
    parser.add_argument('data_path')
    parser.add_argument('save_path')
    args = parser.parse_args()

    BEG = '__BOS__'
    END = '__EOS__'
    sg = 0

    if args.mode == 'skipgram':
        sg = 1

    sentences = list()

    try:
        dir = None

        if os.path.isdir(args.data_path):
            dir = os.listdir(args.data_path)

        for file in dir:
            print('Reading ' + file)

            with open(os.path.join(args.data_path, file), mode='r') as input:
                sentence = None

                for idx, line in enumerate(input):
                    line = line.rstrip(os.linesep).split(args.sep)

                    if len(line) == 3 and line[2] == BEG:
                        sentence = list()  # Start new sentence.
                        sentence.append(line[1])

                    elif len(line) == 3 and line[2] == END:
                        sentence.append(line[1])
                        sentences.append(sentence)  # Add sentence to list of sentences.

                        if args.verbose:
                            output = " ".join(sentence[:-1])
                            output += sentence[-1]
                            print("\n" + output)

                    elif len(line) == 2:
                        sentence.append(line[1])

        msg = "\nBuilding {mode} vocabulary...".format(mode=args.mode)
        print(msg)
        model = gensim.models.Word2Vec(sentences, sg=sg, workers=args.workers, min_count=args.count, size=args.length)
        model.save(args.save_path)
        print('Vocabulary built.')

    except IOError as err:
        stmt = "File Operation Failed: {error}".format(error=err.strerror)
        print(stmt)


if __name__ == '__main__':
    _main()
