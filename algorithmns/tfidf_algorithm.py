# -*- coding: utf-8 -*-
import networkx as nx
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfAlgorithm:
    def tfidf_summary(self, sentences, num_summary_sentences=2):

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(sentences)

        sentence_scores = tfidf_matrix.sum(axis=1).flatten().tolist()[0]
        ranked_sentences = sorted(((score, s) for s, score in zip(sentences, sentence_scores)), reverse=True, key=lambda x: x[0])
        summary_sentences = [sentence for _, sentence in ranked_sentences[:num_summary_sentences]]

        return summary_sentences

    def proccess(self, text):
        sentences = sent_tokenize(text)

        summary_sentences = self.tfidf_summary(sentences)
        generated_summary = " ".join(summary_sentences)

        return generated_summary, len(text.split()), len(generated_summary.split()), len(sentences)
