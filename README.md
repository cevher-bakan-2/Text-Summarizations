MalatyaCentralityMethod fonksiyonu, bir grafın düğümlerini gezerek Malatya merkezlilik değerini hesaplar. Her bir düğümün derecesini (Vdegree) ve komşularının derecesini (AdjacentDegree) toplar ve bunları kullanarak bir değer hesaplar. Eğer AdjacentDegree sıfırdan farklı ise, Vdegree / AdjacentDegree işlemi gerçekleştirilir, aksi takdirde değer sıfır atanır. Hesaplanan değer MalatyaCentralityValue değişkenine atılır ve ekrana yazdırılır. Son olarak, bu değer döndürülür.

FindMaxMalatyaCentralityValue fonksiyonu, verilen bir graf üzerinde MalatyaCentralityMethod fonksiyonunu kullanarak en yüksek Malatya merkezlilik değerine sahip düğümü bulur. Bu fonksiyon, max fonksiyonunu kullanarak en yüksek değere sahip düğümü belirler ve graf üzerinden bu düğümü kaldırır. Son olarak, en yüksek değere sahip düğümü ve kalan kenar sayısını döndürür.

FindMinVertexCover fonksiyonu, verilen bir graf üzerinde minimum düğüm kaplamasını bulur. Grafın kenar sayısı sıfır olana kadar en yüksek Malatya merkezlilik değerine sahip düğümü bulur ve bu düğümü graf üzerinden kaldırır. Bu işlemi tekrarlayarak minimum düğüm kaplamasını elde eder. Son olarak, en yüksek değere sahip düğümü ve kalan kenar sayısını döndürür.

Metin özetlemesi için örnek bir metin tanımlanır. Bu metin, üzerinde metin özetleme işlemi gerçekleştirilecek metni temsil eder.
Metin, sent_tokenize fonksiyonu kullanılarak cümlelere ayrılır ve cumleler listesine atanır.

word_tokenize fonksiyonu ve Counter sınıfı kullanılarak metindeki kelimelerin tekrar sayıları bulunur. Bu, metindeki kelime tekrarlarını belirlemek için kullanılır.
networkx kütüphanesi kullanılarak bir graf oluşturulur. Her cümle için bir düğüm oluşturulur ve kelime tekrarları için kenarlar eklenir. Kenarların ağırlığı, kelimenin tekrar sayısı olarak belirlenir.

FindMinVertexCover fonksiyonu kullanılarak minimum düğüm kaplaması bulunur. Bu adım, en etkili cümleyi belirlemek için gerekli olan işlemi gerçekleştirir.
En etkili cümle, cumleler listesindeki ilgili indeks kullanılarak belirlenir ve ekrana yazdırılır.
Bu şekilde, verilen metin içindeki en etkili cümleyi bulmak için Malatya merkezlilik yöntemi kullanılarak bir metin özetleme işlemi gerçekleştirilir.
