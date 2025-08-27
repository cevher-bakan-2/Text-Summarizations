# -*- coding: utf-8 -*-
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from nltk.tokenize import sent_tokenize


class TextrankAlgorithm:
    def textrank_summary(self, text, num_summary_sentences=2):
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()

        summary_sentences = summarizer(parser.document, num_summary_sentences)
        summary_sentences = [str(sentence) for sentence in summary_sentences]

        return summary_sentences

    def proccess(self, text):
        summary_sentences = self.textrank_summary(text)

        generated_summary = " ".join(summary_sentences)

        return generated_summary, len(text.split()), len(generated_summary.split()), len(sent_tokenize(text))
