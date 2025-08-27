# -*- coding: utf-8 -*-
import os
from rouge import Rouge


row = 0


def print_excel_rog_test(worksheets, file_name, rouge_scores, total_words_count, words_count):
    global row
    rouge_scores_dict = {}

    if row == 0:
        col = 0
        for worksheet in worksheets:
            for j, cell_data in enumerate(["Dosya Adi", "Recall", "Precision", "F-Score", "Total Words Count", "Words Count"]):
                worksheet.write(row, col + j, cell_data)

    row += 1

    rouge_scores_dict['rouge-1'] = {
        'r': rouge_scores['rouge-1']['r'],
        'p': rouge_scores['rouge-1']['p'],
        'f': rouge_scores['rouge-1']['f']
    }

    rouge_scores_dict['rouge-2'] = {
        'r': rouge_scores['rouge-2']['r'],
        'p': rouge_scores['rouge-2']['p'],
        'f': rouge_scores['rouge-2']['f']
    }

    rouge_scores_dict['rouge-l'] = {
        'r': rouge_scores['rouge-l']['r'],
        'p': rouge_scores['rouge-l']['p'],
        'f': rouge_scores['rouge-l']['f']
    }

    rog_1_scores = [file_name, rouge_scores_dict['rouge-1']['r'], rouge_scores_dict['rouge-1']['p'], rouge_scores_dict['rouge-1']['f'], total_words_count, words_count]
    col = 0
    for j, cell_data in enumerate(rog_1_scores):
        worksheets[0].write(row, col + j, cell_data)

    rog_2_scores = [file_name, rouge_scores_dict['rouge-2']['r'], rouge_scores_dict['rouge-2']['p'], rouge_scores_dict['rouge-2']['f'], total_words_count, words_count]
    col = 0
    for j, cell_data in enumerate(rog_2_scores):
        worksheets[1].write(row, col + j, cell_data)

    rog_l_scores = [file_name, rouge_scores_dict['rouge-l']['r'], rouge_scores_dict['rouge-l']['p'], rouge_scores_dict['rouge-l']['f'], total_words_count, words_count]
    col = 0
    for j, cell_data in enumerate(rog_l_scores):
        worksheets[2].write(row, col + j, cell_data)

    return rouge_scores_dict


def print_txt(directory, file_name, text):
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + file_name+'.txt', "w", encoding='utf-8') as file:
        file.write(text)


def progress_indicator(rate):
    bar_length = 100
    block = int(round(bar_length * rate))
    empty = bar_length - block
    progress_text = f"[{'=' * block}{' ' * empty}] {rate * 100:.2f}%"

    print(f"\r{progress_text}", end='')


def print_rouge_result(result):
    if result is None:
        print("Hata: result None değer döndürüyor")
    elif 'rouge-1' not in result:
        print("Hata: 'rouge-1' anahtarı result içerisinde yok")
    else:
        print("ROUGE-1 Scores:")
        print(f"  Recall (r): {result.get('rouge-1').get('r')}")
        print(f"  Precision (p): {result.get('rouge-1').get('p')}")
        print(f"  F-Score (f): {result.get('rouge-1').get('f')}")

        print("\nROUGE-2 Scores:")
        print(f"  Recall (r): {result.get('rouge-2').get('r')}")
        print(f"  Precision (p): {result.get('rouge-2').get('p')}")
        print(f"  F-Score (f): {result.get('rouge-2').get('f')}")

        print("\nROUGE-L Scores:")
        print(f"  Recall (r): {result.get('rouge-l').get('r')}")
        print(f"  Precision (p): {result.get('rouge-l').get('p')}")
        print(f"  F-Score (f): {result.get('rouge-l').get('f')}")


def calculate_rouge_with_library(reference, summary):
    rouge = Rouge()
    scores = rouge.get_scores(summary, reference)
    return scores
