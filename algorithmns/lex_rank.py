# -*- coding: utf-8 -*-
from lexrank import LexRank


class LexrankAlgorithm:
    def proccess(self, text):
        sentences = text.split('.')

        lxr = LexRank(sentences)
        summary_sentences = lxr.get_summary(sentences, summary_size=2)
        generated_summary = " ".join(summary_sentences)

        return generated_summary, len(text.split()), len(generated_summary.split()), len(sentences)
