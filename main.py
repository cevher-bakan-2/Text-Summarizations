# -*- coding: utf-8 -*-

from datetime import datetime
import time
import nltk
from algorithmns.lex_rank import LexrankAlgorithm
from algorithmns.malatya_algorithm import MalatyaAlgorithm
from algorithmns.pagerank_algorithmn import PagerankAlgorithm
from algorithmns.textrank_algorithm import TextrankAlgorithm
from algorithmns.tfidf_algorithm import TfidfAlgorithm
from dataset.pubmed_dataset import PubmedDataset
from dataset.cnn import CNNDataset
from dataset.bbc import BBCDataset
from helpers import print_excel_rog_test, print_txt, progress_indicator, calculate_rouge_with_library
import xlsxwriter


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('punkt')



class TextSummarization:
    def __init__(self, dataset):
        dataset_classes = {
            "pubmed": PubmedDataset,
            "cnn": CNNDataset,
            "bbc": BBCDataset
        }

        if dataset.lower() in dataset_classes:
            self.dataset = dataset_classes[dataset.lower()]()
        else:
            raise ValueError(f"Unsupported dataset type: {dataset}")

        self.dataset = self.dataset.get_dataset()

    def main(self, dataset_name, algorithm_name):
        dataset = self.dataset
        algorithms = {
            "malatya-algorithm": MalatyaAlgorithm,
            "textrank-algorithm": TextrankAlgorithm,
            "pagerank-algorithm": PagerankAlgorithm,
            "lexrank-algorithm": LexrankAlgorithm,
            "tfidf-algorithm": TfidfAlgorithm,
        }

        if algorithm_name in algorithms:
            algorithm = algorithms[algorithm_name]()
        else:
            raise ValueError(f"Geçersiz algoritma adı: {algorithm_name}")

        date_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        base_directory = "Results/"+algorithm_name+'/'+date_time+"-"+dataset_name+"/"
        summarization_directory = base_directory+"summarizations-recommended/"
        reference_directory = base_directory+"summarizations-reference/"
        full_text_directory = base_directory+"full-text/"

        workbook = xlsxwriter.Workbook(base_directory+'/'+'RougeScore.xlsx')
        worksheets = [
            workbook.add_worksheet('ROUGE-1 Scores'),
            workbook.add_worksheet('ROUGE-2 Scores'),
            workbook.add_worksheet('ROUGE-L Scores')
        ]

        total_rouge_1_r, total_rouge_1_p, total_rouge_1_f = 0, 0, 0
        total_rouge_2_r, total_rouge_2_p, total_rouge_2_f = 0, 0, 0
        total_rouge_l_r, total_rouge_l_p, total_rouge_l_f = 0, 0, 0
        total_articles = 0
        i = 0
        total = len(dataset)

        print("Starting the summarization process with "+algorithm_name+"...")
        start_time = time.time()
        for article in dataset:
            if i >= total:
                break

            text = article["full_text"]
            summary = article["abstract"]
            generated_summary, total_words_count, words_count, sentence_count = algorithm.proccess(text)

            if sentence_count == 0:
                continue
            rouge_scores = calculate_rouge_with_library(summary, generated_summary)
            rouge_scores = rouge_scores[0]

            print_txt(summarization_directory, article["id"], generated_summary)
            print_txt(reference_directory, article["id"], summary)
            print_txt(full_text_directory, article["id"], text)

            print_excel_rog_test(worksheets, article["id"], rouge_scores, total_words_count, words_count)
            total_rouge_1_r += rouge_scores['rouge-1']['r']
            total_rouge_1_p += rouge_scores['rouge-1']['p']
            total_rouge_1_f += rouge_scores['rouge-1']['f']
            total_rouge_2_r += rouge_scores['rouge-2']['r']
            total_rouge_2_p += rouge_scores['rouge-2']['p']
            total_rouge_2_f += rouge_scores['rouge-2']['f']
            total_rouge_l_r += rouge_scores['rouge-l']['r']
            total_rouge_l_p += rouge_scores['rouge-l']['p']
            total_rouge_l_f += rouge_scores['rouge-l']['f']
            total_articles += 1
            i += 1
            progress_indicator(i / total)

        print("\nMethod run time: ", time.time() - start_time)
        print("\nSummarization process completed.")

        if total_articles > 0:
            print("\nAverage ROUGE-1 Scores:")
            print(f"  Recall (r): {total_rouge_1_r/total_articles:.4f}")
            print(f"  Precision (p): {total_rouge_1_p/total_articles:.4f}")
            print(f"  F-Score (f): {total_rouge_1_f/total_articles:.4f}\n")
            print("Average ROUGE-2 Scores:")
            print(f"  Recall (r): {total_rouge_2_r/total_articles:.4f}")
            print(f"  Precision (p): {total_rouge_2_p/total_articles:.4f}")
            print(f"  F-Score (f): {total_rouge_2_f/total_articles:.4f}\n")
            print("Average ROUGE-L Scores:")
            print(f"  Recall (r): {total_rouge_l_r/total_articles:.4f}")
            print(f"  Precision (p): {total_rouge_l_p/total_articles:.4f}")
            print(f"  F-Score (f): {total_rouge_l_f/total_articles:.4f}")

        workbook.close()


dataset_name = "pubmed"
text_summarization = TextSummarization(dataset_name)
text_summarization.main(dataset_name=dataset_name, algorithm_name="malatya-algorithm")
# text_summarization.main(dataset_name=dataset_name, algorithm_name="pagerank-algorithm")
# text_summarization.main(dataset_name=dataset_name, algorithm_name="textrank-algorithm")
# text_summarization.main(dataset_name=dataset_name, algorithm_name="lexrank-algorithm")
# text_summarization.main(dataset_name=dataset_name, algorithm_name="tfidf-algorithm")
