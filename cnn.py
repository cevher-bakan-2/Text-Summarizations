# -*- coding: utf-8 -*-

import os
from datetime import datetime
import networkx as nx
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.request import urlopen
from rouge import Rouge
import PyPDF2
import xlsxwriter
from datasets import load_dataset


row = 0

# NLTK toolkit indirmeleri
nltk.download('punkt')
nltk.download('stopwords')


# Malatya merkezlilik değeri hesaplama
def MalatyaCentralityMethod(g):
    VertexList = list(g.nodes()) # Grafın düğümlerini diziye atar
    centrality_values = []
    nodes = []
    node_number = 0
    Value = 0
    for i in VertexList:
        if type(i) == int:
            node_number = i
            Vdegree = g.degree[i]  # i. düğümün derecesi, yani i. düğümün komşu düğümleri sayısı 
            AdjacentDegree = sum(g.degree[neighbor] for neighbor in g.neighbors(i)) # mevcut düğümün komşu düğümlerinin derecelerinin toplamı
            AdjacentDegree = AdjacentDegree - Vdegree # mevcut düğümün komşu düğümlerinin derecelerinin toplamından mevcut düğümün derecesini çıkarır
            if AdjacentDegree != 0: # Eğer komşu düğüm sayısı dereceleri toplamı 0 değilse
                Value = Vdegree / AdjacentDegree # i. düğümün derecesi / i. düğümün komşu düğümlerinin derecelerinin toplamı
            else: # eğer komşu düğüm sayısı dereceleri toplamı 0 ise
                Value = 0
            centrality_values.append(Value)
            nodes.append(i)

    return centrality_values, nodes, node_number


def NewMalatyaCentralityMethod(g):
    centrality_values = []
    nodes = []
    node_number = 0
    for i in list(g.nodes()): # Grafın düğümlerini diziye atar
        if type(i) == int:
            node_number = i
            Vdegree = g.degree[i]  # i. düğümün derecesi, yani i. düğümün komşu düğümleri sayısı
            centrality_value = 0
            for neighbor in g.neighbors(i):
                if g.degree[neighbor] != 0:
                    centrality_value += (Vdegree/g.degree[neighbor])

            centrality_values.append(centrality_value)
            nodes.append(i)

    return centrality_values, nodes, node_number


def FindMaxMalatyaCentralityValue(g):
    centrality_values, nodes, node_number = NewMalatyaCentralityMethod(g)
    if len(centrality_values) == 0:
        g.remove_node(node_number)
        return None

    maxIndex = centrality_values.index(max(centrality_values)) # En yüksek değere sahip düğümün indeksini bulur
    maxVertex = nodes[maxIndex] # En yüksek değere sahip düğümü bulur
    g.remove_node(maxVertex) # Seçilen en yüksek değere sahip düğümün kenarlarını siler

    return maxVertex


def FindMinVertexCover(g):
    max_list = []
    while g.number_of_edges() != 0: # Grafın ulaşılmamış kenarı olduğu sürece çalışır
        maxVertex = FindMaxMalatyaCentralityValue(g)
        if maxVertex is not None:
            max_list.append(maxVertex) # En yüksek değere sahip düğümü listeye ekler
    return maxVertex, max_list


def _read_from_file(name):
    with open(name, "r", encoding='ISO-8859-9') as f:
        return f.read()


def _read_from_web(url):
    all_text=''
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    for el in soup.find_all('p'):
        all_text+=el.get_text()

    return all_text


def _read_from_pdf(file_path):
    all_text = ""
    with open(file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            all_text += page.extract_text()

    return all_text


def _create_graph(cumleler, kelime_tekrarlari):
    stop_words = set(stopwords.words("turkish"))  # Türkçe stopwords listesi
    en_stop_words = set(stopwords.words("english"))

    new_words = [
        ".", ",", "!","?",";",":","'","(",")","[","]","{","}","-","_","*","/",
        "\\","%","<",">","&","|","@","#","$","^","~","`","+","=","1","2","3",
        "4","5","6","7","8","9","0","\"","’","‘","“","”","–","…","•","·","»", 
        "«",">>","<<","%", "€", "£", " ", "a", "b", "c", "ç" "d", "e", "f",
        "g","ğ", "h","ı","i","j","k","l","m","n","o","p","r","s","t","u","ü","v",
        "y","z","x","w","q","1.","2.","3.","4.","5.","6.","7.","8.","9.","0."]
    #print(en_stop_words)
    stop_words.update(new_words)
    stop_words.update(en_stop_words)
    # Graf oluşturma
    G = nx.Graph()
    for i, cumle in enumerate(cumleler):
        G.add_node(i) # Her cümle için bir düğüm oluşturur
        for kelime, tekrar_sayisi in kelime_tekrarlari.items():
            if kelime in cumle.lower() and kelime not in stop_words:  # Kelime cümle içinde geçiyor ve stopwords listesinde değilse düğüme ekler
                G.add_edge(i, kelime, weight=tekrar_sayisi)
        #draw_graph(G)
    return G


def draw_graph(G):
    pos = nx.spring_layout(G)  # Grafı düzenleme
    labels = {node: node for node in G.nodes()}  # Her düğümün etiketini kendisiyle aynı yapma
    nx.draw(G, pos, with_labels=True, labels=labels, font_size=17, font_color = "black", node_size=500, node_color='green')  # Grafı çizdirme
    plt.show()  # Çizimi görüntüleme    


def calculate_rouge_with_library(reference, summary):
    rouge = Rouge()
    scores = rouge.get_scores(summary, reference)
    return scores  # İlk ROUGE metriği puanlarını döndürür


def ilerleme_gostergesi(rate):
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


def create_directory():
    now_time = datetime.now()
    time = now_time.strftime("%d-%m-%Y-%H-%M-%S")
    directory = f"result_summaries-{time}/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def main():
    date_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    # Veri setini ve Excel kitabını yükleme
    dataset = load_dataset("cnn_dailymail", "3.0.0")
    workbook = xlsxwriter.Workbook('Rouge_Scores.xlsx')
    worksheet1 = workbook.add_worksheet('ROUGE-1 Scores')
    worksheet2 = workbook.add_worksheet('ROUGE-2 Scores')
    worksheet3 = workbook.add_worksheet('ROUGE-L Scores')
    worksheets = [worksheet1, worksheet2, worksheet3]

    # Initialize cumulative scores for averages
    total_rouge_1_r, total_rouge_1_p, total_rouge_1_f = 0, 0, 0
    total_rouge_2_r, total_rouge_2_p, total_rouge_2_f = 0, 0, 0
    total_rouge_l_r, total_rouge_l_p, total_rouge_l_f = 0, 0, 0
    total_articles = 0  # Total processed articles

    i = 0
    total = 1000  # Örneğin, işlenecek toplam dosya sayısı
    for article in dataset["test"]:
        if i >= total:
            break

        text = article["article"]
        summary = article["highlights"]
        cumleler = sent_tokenize(text)
        kelime_tekrarlari = Counter(word_tokenize(text.lower()))
        G = _create_graph(cumleler, kelime_tekrarlari)
        minCover, max_list = FindMinVertexCover(G)

        if minCover is None or len(max_list) == 0:
            continue

        generated_summary, total_words_count, words_count = build_summary(cumleler, max_list)
        rouge_scores = calculate_rouge_with_library(summary, generated_summary)

        print_txt(date_time+'/'+"cnn-summarizations-recommended", article["id"], generated_summary)
        print_txt(date_time+'/'+"cnn-summarizations-reference", article["id"], summary)
        print_txt(date_time+'/'+"cnn-articles", article["id"], text)

        print_excel_rog_test(worksheets, "test", article["id"], summary, generated_summary, total_words_count, words_count)

        # Update cumulative scores
        total_rouge_1_r += rouge_scores[0]['rouge-1']['r']
        total_rouge_1_p += rouge_scores[0]['rouge-1']['p']
        total_rouge_1_f += rouge_scores[0]['rouge-1']['f']
        total_rouge_2_r += rouge_scores[0]['rouge-2']['r']
        total_rouge_2_p += rouge_scores[0]['rouge-2']['p']
        total_rouge_2_f += rouge_scores[0]['rouge-2']['f']
        total_rouge_l_r += rouge_scores[0]['rouge-l']['r']
        total_rouge_l_p += rouge_scores[0]['rouge-l']['p']
        total_rouge_l_f += rouge_scores[0]['rouge-l']['f']
        total_articles += 1

        # İlerleme göstergesi güncellemesi
        i += 1
        ilerleme_gostergesi(i / total)

    # Calculate and print average ROUGE scores
    if total_articles > 0:  # Avoid division by zero
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

    # Excel dosyasını kapatma
    workbook.close()


def print_rog_test(subject, dosya_adi, referans_metin, en_etkin_cumle):
    scores = calculate_rouge_with_library(referans_metin, en_etkin_cumle)
    scores.insert(0, dosya_adi)
    text_file = subject+"-veriler.txt"

    with open(text_file, "a") as file:
        file.write(','.join(map(str, scores)) + "\n")

    print(scores)


def print_excel_rog_test(worksheets, subject, dosya_adi, referans_metin, en_etkin_cumle, total_words_count, words_count):
    global row
    rouge_scores_dict = {}

    if row != 0:
        dosya_adi = subject + "-" + dosya_adi
        scores = calculate_rouge_with_library(referans_metin, en_etkin_cumle)

        item = scores[0]

        rouge_scores_dict['rouge-1'] = {
            'r': item['rouge-1']['r'],
            'p': item['rouge-1']['p'],
            'f': item['rouge-1']['f']
        }

        rouge_scores_dict['rouge-2'] = {
            'r': item['rouge-2']['r'],
            'p': item['rouge-2']['p'],
            'f': item['rouge-2']['f']
        }

        rouge_scores_dict['rouge-l'] = {
            'r': item['rouge-l']['r'],
            'p': item['rouge-l']['p'],
            'f': item['rouge-l']['f']
        }

        rog_1_scores = [dosya_adi, rouge_scores_dict['rouge-1']['r'], rouge_scores_dict['rouge-1']['p'], rouge_scores_dict['rouge-1']['f'], total_words_count, words_count]
        col = 0
        for j, cell_data in enumerate(rog_1_scores):
            worksheets[0].write(row, col + j, cell_data)

        rog_2_scores = [dosya_adi, rouge_scores_dict['rouge-2']['r'], rouge_scores_dict['rouge-2']['p'], rouge_scores_dict['rouge-2']['f'], total_words_count, words_count]
        col = 0
        for j, cell_data in enumerate(rog_2_scores):
            worksheets[1].write(row, col + j, cell_data)

        rog_l_scores = [dosya_adi, rouge_scores_dict['rouge-l']['r'], rouge_scores_dict['rouge-l']['p'], rouge_scores_dict['rouge-l']['f'], total_words_count, words_count]
        col = 0
        for j, cell_data in enumerate(rog_l_scores):
            worksheets[2].write(row, col + j, cell_data)
    
    else:
        col = 0
        for worksheet in worksheets:
            for j, cell_data in enumerate(["Dosya Adi", "Recall", "Precision", "F-Score", "Total Words Count", "Words Count"]):
                worksheet.write(row, col + j, cell_data)

    row += 1
    
    return rouge_scores_dict


def build_summary(cumleler, max_list):
    summary = ""
    words_count = 0
    sentence_count = 0
    total_words_count = 0

    for i in cumleler:
        total_words_count+=len(i.split(" "))

    for j in cumleler:
        words_count+=len(j.split(" "))
        if words_count > 100:
            break
        sentence_count+=1

    for i in sorted(max_list[:sentence_count]):
        summary += cumleler[i] + " "

    return summary, total_words_count, words_count


def print_txt(directory, file_name, text):
    directory = directory+'/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + file_name, "w") as file:
        file.write(text)


main()
