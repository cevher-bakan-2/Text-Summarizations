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

row = 0


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
    bar_length = 30
    block = int(round(bar_length * rate))
    empty = bar_length - block
    progress_text = f"[{'=' * block}{' ' * empty}] {rate * 100:.2f}%"

    print(f"\r{progress_text}", end='')

def calculet_with_multi_files(worksheets, texts_source, summaries_source):
    rouge_1_r = 0
    rouge_1_p = 0
    rouge_1_f = 0
    rouge_2_r = 0
    rouge_2_p = 0
    rouge_2_f = 0
    rouge_l_r = 0
    rouge_l_p = 0
    rouge_l_f = 0
    total_files = 0
    subjects = ["business", "entertainment", "politics", "sport", "tech"]
    directory = create_directory()
    
    for subject in subjects:
        index=0
        for dosya_adi in os.listdir(texts_source+subject+'/'):
            sub_total_files = len(os.listdir(texts_source+subject))
            print('\n')
            index+=1
            rate = index/sub_total_files
            ilerleme_gostergesi(rate)
            print('\n')
            print('dosya adı:', dosya_adi)
            dosya_yolu = os.path.join(texts_source+subject+'/', dosya_adi)
            metin = _read_from_file(dosya_yolu) # metin.txt dosyasından metni okur
            print("\n")
            print('-----------------------------------------------')
            print("subject:", subject)
            print("Dosya adı:", dosya_adi)

            # Metni cümlelere ayır
            cumleler = sent_tokenize(metin)
            # Cümlelerdeki kelime tekrarlarını bulur
            #print(metin)
            kelime_tekrarlari = Counter(word_tokenize(metin.lower()))

            G = _create_graph(cumleler, kelime_tekrarlari)
            # Minimum Vertex Cover'ı bulma
            minCover, max_list = FindMinVertexCover(G)
            if minCover is None or len(max_list) == 0:
                return False

            # En etkili cümleyi bulma
            #en_etkin_cumle = cumleler[minCover]
            #print("En etkili cümle:", en_etkin_cumle)
            summary, total_words_count, words_count = build_summary(cumleler, max_list)
            print_result_summary(directory, "recommended", subject, dosya_adi, summary)
            #print("#######Metin:")
            #print(metin)
            #print("\n")
            #print("#######Özet:")
            #print(summary)
            print('-----------------------------------------------')
            print("\n")
            dosya_yolu = os.path.join(summaries_source+subject+'/', dosya_adi)
            referans_metin = _read_from_file(dosya_yolu)
            result = print_excel_rog_test(worksheets, subject, dosya_adi, referans_metin, summary, total_words_count, words_count)
            #print_rouge_result(result)
            if result is None:
                print("Hata: result None değer döndürüyor")
            elif 'rouge-1' not in result:
                print("Hata: 'rouge-1' anahtarı result içerisinde yok")
            else:
                rouge_1_r += result.get('rouge-1').get('r')
                rouge_1_p += result.get('rouge-1').get('p')
                rouge_1_f += result.get('rouge-1').get('f')
                rouge_2_r += result.get('rouge-2').get('r')
                rouge_2_p += result.get('rouge-2').get('p')
                rouge_2_f += result.get('rouge-2').get('f')
                rouge_l_r += result.get('rouge-l').get('r')
                rouge_l_p += result.get('rouge-l').get('p')
                rouge_l_f += result.get('rouge-l').get('f')
        total_files += sub_total_files
    print("\n")
    print("AVARAGE ROUGE-1 Scores:")
    print(f"  Recall (r): {rouge_1_r/total_files}")
    print(f"  Precision (p): {rouge_1_p/total_files}")
    print(f"  F-Score (f): {rouge_1_f/total_files}")

    print("\nAVARAGE ROUGE-2 Scores:")
    print(f"  Recall (r): {rouge_2_r/total_files}")
    print(f"  Precision (p): {rouge_2_p/total_files}")
    print(f"  F-Score (f): {rouge_2_f/total_files}")

    print("\nAVARAGE ROUGE-L Scores:")
    print(f"  Recall (r): {rouge_l_r/total_files}")
    print(f"  Precision (p): {rouge_l_p/total_files}")
    print(f"  F-Score (f): {rouge_l_f/total_files}")

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
    directory = f"bbcdataset/result_summaries-{time}/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory

def main():
    now_time = datetime.now()
    time = now_time.strftime("%d-%m-%Y-%H-%M-%S")

    base_directory = "rouge-results"
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    time_directory = os.path.join(base_directory, time)
    if not os.path.exists(time_directory):
        os.makedirs(time_directory)

    workbooks = []
    worksheets = []
    texts_source = "bbcdataset/news_articles/"
    summaries_source = "bbcdataset/summaries/"

    workbooks.append(xlsxwriter.Workbook(f'{time_directory}/recommended_rouge1.xlsx'))
    workbooks.append(xlsxwriter.Workbook(f'{time_directory}/recommended_rouge2.xlsx'))
    workbooks.append(xlsxwriter.Workbook(f'{time_directory}/recommended_rougel.xlsx'))

    for workbook in workbooks:
        worksheets.append(workbook.add_worksheet("Main Sheet"))
    
    calculet_with_multi_files(worksheets, texts_source, summaries_source)

    for workbook in workbooks:
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
        if words_count > 180:
            break
        sentence_count+=1

    for i in sorted(max_list[:sentence_count]):
        summary += cumleler[i] + " "

    return summary, total_words_count, words_count

def print_result_summary(directory, alg, subject, file_name, summary):
    directory = directory+alg+'/'+subject+'/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + file_name, "w") as file:
        file.write(summary)


main()
