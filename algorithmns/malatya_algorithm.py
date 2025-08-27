# -*- coding: utf-8 -*-
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx


class MalatyaAlgorithm:
    def MalatyaCentralityMethod(self, g):
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

    def FindMaxMalatyaCentralityValue(self, g):
        centrality_values, nodes, node_number = self.MalatyaCentralityMethod(g)
        if len(centrality_values) == 0:
            g.remove_node(node_number)
            return None

        maxIndex = centrality_values.index(max(centrality_values)) # En yüksek değere sahip düğümün indeksini bulur
        maxVertex = nodes[maxIndex] # En yüksek değere sahip düğümü bulur
        g.remove_node(maxVertex) # Seçilen en yüksek değere sahip düğümün kenarlarını siler

        return maxVertex

    def FindMinVertexCover(self, g):
        max_list = []
        while g.number_of_edges() != 0: # Grafın ulaşılmamış kenarı olduğu sürece çalışır
            maxVertex = self.FindMaxMalatyaCentralityValue(g)
            if maxVertex is not None:
                max_list.append(maxVertex) # En yüksek değere sahip düğümü listeye ekler
        return maxVertex, max_list

    def _create_graph(self, cumleler, kelime_tekrarlari):
        stop_words = set(stopwords.words("turkish"))  # Türkçe stopwords listesi
        en_stop_words = set(stopwords.words("english"))

        new_words = [
            ".", ",", "!","?",";",":","'","(",")","[","]","{","}","-","_","*","/",
            "\\","%","<",">","&","|","@","#","$","^","~","`","+","=","1","2","3",
            "4","5","6","7","8","9","0","\"","’","‘","“","”","–","…","•","·","»", 
            "«",">>","<<","%", "€", "£", " ", "a", "b", "c", "ç" "d", "e", "f",
            "g","ğ", "h","ı","i","j","k","l","m","n","o","p","r","s","t","u","ü","v",
            "y","z","x","w","q","1.","2.","3.","4.","5.","6.","7.","8.","9.","0."]

        stop_words.update(new_words)
        stop_words.update(en_stop_words)
        # Graf oluşturma
        G = nx.Graph()
        for i, cumle in enumerate(cumleler):
            G.add_node(i) # Her cümle için bir düğüm oluşturur
            for kelime, tekrar_sayisi in kelime_tekrarlari.items():
                if kelime in cumle.lower() and kelime not in stop_words:  # Kelime cümle içinde geçiyor ve stopwords listesinde değilse düğüme ekler
                    G.add_edge(i, kelime, weight=tekrar_sayisi)
            # self.draw_graph(G)
        return G

    def build_summary(self, cumleler, max_list):
        summary = ""
        words_count = 0
        sentence_count = 0
        total_words_count = 0
        for i in cumleler:
            total_words_count += len(i.split(" "))

        for j in cumleler:
            words_count += len(j.split(" "))
            if words_count > 80:
                if sentence_count == 0:
                    sentence_count = 1
                break
            sentence_count += 1

        for i in sorted(max_list[:sentence_count]):
            summary += cumleler[i] + " "

        return summary, total_words_count, words_count, sentence_count

    def draw_graph(self, G):
        pos = nx.spring_layout(G)  # Grafı düzenleme
        labels = {node: node for node in G.nodes()}  # Her düğümün etiketini kendisiyle aynı yapma
        nx.draw(G, pos, with_labels=True, labels=labels, font_size=17, font_color = "black", node_size=500, node_color='green')
        plt.show()

    def proccess(self, text):
        cumleler = sent_tokenize(text)
        kelime_tekrarlari = Counter(word_tokenize(text.lower()))
        G = self._create_graph(cumleler, kelime_tekrarlari)
        minCover, max_list = self.FindMinVertexCover(G)
        if minCover is None or len(max_list) == 0:
            return 0, 0, 0, 0

        return self.build_summary(cumleler, max_list)
