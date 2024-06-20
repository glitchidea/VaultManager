[TR]

##VaultManager Solvent
### Özellikleri:

1. **KDBX Dosyası Açma**:
   - Kullanıcıdan alınan şifre ile belirtilen KDBX dosyasını açmayı deneme.
   - PyKeePass kütüphanesi kullanılarak dosya erişimi sağlanır.

2. **Paralel Şifre Deneme**:
   - Şifre deneme işlemlerini paralel olarak yürütme.
   - Birden fazla şifreyi aynı anda test ederek işlem hızını artırma.
   - `concurrent.futures` ve `multiprocessing` modülleri kullanılarak iş parçacıkları ile paralel deneme sağlanır.

3. **Şifre Oluşturma ve Deneme**:
   - Kullanıcıya isteğe bağlı olarak şifre dosyası oluşturma seçeneği sunma.
   - Belirtilen karakter setleri ve uzunluk aralıklarında rastgele şifreler üretme.
   - Üretilen şifreleri KDBX dosyasını açmak için test etme.

### Kullanımı:

1. **KDBX Dosyası Açma**:
   - Uygulama başlatıldığında, kullanıcıdan KDBX dosyasının yolunu ve şifresini girmesi istenir.
   - Dosya erişilebilirse, içeriği gösterilir veya şifrenin doğru olup olmadığı kontrol edilir.

2. **Elinizde Şifre Dosyası Varsa**:
   - Kullanıcı mevcut bir şifre dosyasının yolunu girebilir.
   - Bu dosyadaki şifreler paralel olarak denenebilir ve doğru şifre bulunduğunda işlem sonlandırılabilir.

3. **Kendi Şifre Dosyanızı Oluşturma**:
   - Kullanıcı isteğe bağlı olarak yeni bir şifre dosyası oluşturabilir.
   - Büyük harfler, küçük harfler, rakamlar ve özel karakterler gibi belirli karakter setlerini seçebilir.
   - Minimum ve maksimum şifre uzunluklarını belirleyebilir ve otomatik olarak şifreler üretilebilir.
   - Oluşturulan şifreler KDBX dosyasını açmak için denenebilir.

Uygulama, kullanıcı dostu bir arayüz sunarak, KeePass KDBX veritabanı dosyalarının güvenliğini artırmak ve şifre yönetimini kolaylaştırmak için geliştirilmiştir.



##VaultManager Converter

### Özellikleri:

1. **Yeni KDBX Dosyası Oluşturma**:
   - Kullanıcıdan dosyanın tam yolunu ve şifreyi girmesini isteyerek yeni bir KDBX veritabanı oluşturur.
   - `create_database` fonksiyonu kullanılarak veritabanı oluşturulur ve belirtilen yere kaydedilir.

2. **Mevcut KDBX Dosyasının Şifresini Değiştirme**:
   - Kullanıcıdan mevcut KDBX dosyasının yolunu ve mevcut şifreyi girmesini ister.
   - Dosya başarıyla açıldığında, kullanıcıya yeni bir şifre belirlemesi için işlem yapma imkanı sunar.
   - Yeni şifre belirlendikten sonra, dosyanın şifresi değiştirilir ve değişiklikler kaydedilir.

3. **Ekstra Özellikler**:
   - Terminal ekranını temizlemek için `clear_screen` fonksiyonu kullanılır.
   - `getpass` modülüyle şifre girişleri güvenli bir şekilde alınır.
   - Kullanıcıya ana menüde geçersiz bir seçenek girdiği durumda uygun geri bildirim sağlar.

### Kullanımı:

1. **Yeni KDBX Dosyası Oluşturma**:
   - Uygulama başlatıldığında, kullanıcıya bir ana menü sunulur.
   - Kullanıcı "1" tuşuna basarak yeni KDBX dosyası oluşturma seçeneğini seçer.
   - Dosya yolu ve şifre istenir, şifre doğrulandıktan sonra yeni KDBX dosyası oluşturulur.

2. **Mevcut KDBX Dosyasının Şifresini Değiştirme**:
   - Kullanıcı "2" tuşuna basarak mevcut KDBX dosyasının şifresini değiştirme seçeneğini seçer.
   - Dosya yolunu ve mevcut şifreyi girdikten sonra yeni şifre belirler.
   - Yeni şifre onaylandıktan sonra dosyanın şifresi değiştirilir ve değişiklikler kaydedilir.

3. **Çıkış**:
   - Kullanıcı "q" tuşuna basarak uygulamadan çıkış yapabilir.


##VaultManager Reader
### Özellikleri:

1. **Listeleme (`list_entries` fonksiyonu)**:
   - Veritabanındaki girişleri listeleyerek başlık, kullanıcı adı, şifre, URL ve notlar gibi bilgileri tablo halinde ekranda gösterir.
   - Pandas kütüphanesi kullanılarak veriler bir DataFrame'e dönüştürülüp terminal ekranına yazdırılır.

2. **Ekleme (`add_entry` fonksiyonu)**:
   - Kullanıcıdan yeni bir giriş için başlık, kullanıcı adı, şifre, URL ve notlar gibi bilgileri alarak veritabanına ekler.
   - `kp.add_entry` metoduyla belirtilen grup altına yeni giriş eklenir ve `kp.save()` ile değişiklikler kaydedilir.

3. **Düzenleme (`edit_entry` fonksiyonu)**:
   - Var olan bir girişin bilgilerini düzenlemek için kullanılır.
   - Kullanıcıdan değiştirilmek istenen bilgileri girmesi istenir ve `kp.save()` ile değişiklikler kaydedilir.

4. **Silme (`delete_entry` fonksiyonu)**:
   - Kullanıcıdan silmek istediği girişin numarasını alarak veritabanından girişi siler.
   - `kp.delete_entry` metodu kullanılarak giriş silinir ve `kp.save()` ile değişiklikler kaydedilir.

5. **Şifre Oluşturma (`generate_password` fonksiyonu)**:
   - Kullanıcıya isteğe bağlı olarak büyük harfler, küçük harfler, rakamlar ve noktalama işaretleri kullanarak rastgele bir şifre oluşturma imkanı sağlar.
   - `random.choice` fonksiyonuyla belirtilen karakter setinden rastgele karakterler seçilerek şifre oluşturulur.

6. **Şifre Gösterme (`show_password` fonksiyonu)**:
   - Belirtilen bir girişin tüm bilgilerini, özellikle şifresini gösterir.

7. **Ana Menü Yönetimi (`main` fonksiyonu)**:
   - Kullanıcıya ana menüyü gösterir ve seçilen işleme göre ilgili fonksiyonları çağırır.
   - `clear_screen` fonksiyonu ile ekran temizlenir ve kullanıcıya uygun geri bildirimler verilir.

### Kullanımı:

- Program başlatıldığında kullanıcıdan KeePass veritabanı dosyasının yolu ve şifresi istenir.
- Ana menüden seçilen işlem numarasına göre (`1`-`6`) ilgili işlem yapılır veya `q` girilerek programdan çıkılır.
- Her işlem sonrasında kullanıcıya gerekli geri bildirimler verilir ve işlem tamamlanır.
- Hata durumlarında kullanıcıya uygun hata mesajları gösterilir ve devam etmek için ENTER tuşuna basması istenir.

Bu betik, kullanıcıların KeePass veritabanı üzerindeki girişleri listelemelerini, eklemelerini, düzenlemelerini, silebilmelerini, rastgele şifre oluşturmalarını ve girişlerin detaylarını görebilmelerini sağlayarak günlük kullanım senaryolarına yönelik pratik bir araç sunar.

