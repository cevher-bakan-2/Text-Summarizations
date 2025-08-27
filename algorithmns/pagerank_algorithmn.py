# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class PagerankAlgorithm:
    def pagerank_summary(self, sentences, similarity_matrix, num_summary_sentences=2, damping_factor=0.85, max_iterations=100):
        graph = nx.from_numpy_array(np.array(similarity_matrix))
        scores = nx.pagerank(graph, alpha=damping_factor, max_iter=max_iterations)

        ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        summary_sentences = [sentence for score, sentence in ranked_sentences[:num_summary_sentences]]

        return summary_sentences

    def proccess(self, text):
        sentences = sent_tokenize(text)
        vectorizer = CountVectorizer().fit_transform(sentences)
        similarity_matrix = cosine_similarity(vectorizer)

        summary_sentences = self.pagerank_summary(sentences, similarity_matrix)
        generated_summary = " ".join(summary_sentences)

        return generated_summary, len(text.split()), len(generated_summary.split()), len(sentences)
