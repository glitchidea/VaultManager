[EN]
## VaultManager Solvent
### Features:

1. **Open KDBX File**:
   - Attempt to open the specified KDBX file with the password provided by the user.
   - Access to the file is facilitated using the PyKeePass library.

2. **Parallel Password Testing**:
   - Execute password testing operations in parallel.
   - Enhance processing speed by testing multiple passwords simultaneously.
   - Utilizes `concurrent.futures` and `multiprocessing` modules for parallel testing.

3. **Password Generation and Testing**:
   - Provide the option for users to generate a password file.
   - Generate random passwords using specified character sets and length ranges.
   - Test generated passwords to open a KDBX file.

### Usage:

1. **Open KDBX File**:
   - Upon starting the application, prompt the user to enter the path to the KDBX file and its password.
   - If access to the file is successful, display its contents or verify the correctness of the password.

2. **If You Have a Password File**:
   - Allow the user to input the path to an existing password file.
   - Test passwords from this file in parallel, ending the process upon finding the correct password.

3. **Create Your Own Password File**:
   - Optionally enable users to create a new password file.
   - Choose specific character sets like uppercase letters, lowercase letters, digits, and special characters.
   - Define minimum and maximum password lengths and automatically generate passwords.
   - Test the generated passwords to open a KDBX file.

The application is designed to provide a user-friendly interface for enhancing the security of KeePass KDBX database files and simplifying password management.

---

## VaultManager Converter

### Features:

1. **Create New KDBX File**:
   - Prompt the user to input the full path and password to create a new KDBX database.
   - Utilize the `create_database` function to create and save the database at the specified location.

2. **Change Password of Existing KDBX File**:
   - Prompt the user to input the path of the existing KDBX file and its current password.
   - Upon successful file access, allow the user to set a new password.
   - Change the file's password and save the changes.

3. **Additional Features**:
   - Utilize the `clear_screen` function to clear the terminal screen.
   - Securely retrieve password inputs using the `getpass` module.
   - Provide appropriate feedback when an invalid option is entered in the main menu.

### Usage:

1. **Create New KDBX File**:
   - Upon starting the application, present the user with a main menu.
   - User selects "1" to choose the option to create a new KDBX file.
   - Input the file path and password, verify the password, and create a new KDBX file.

2. **Change Password of Existing KDBX File**:
   - User selects "2" to choose the option to change the password of an existing KDBX file.
   - Input the file path and current password, then define a new password.
   - After confirming the new password, change the file's password and save the changes.

3. **Exit**:
   - User can exit the application by pressing "q".



---

## VaultManager Reader

### Features:

1. **Listing (`list_entries` function)**:
   - List entries in the database, displaying information such as title, username, password, URL, and notes in a tabular format.
   - Utilizes the Pandas library to convert data into a DataFrame and print it to the terminal.

2. **Adding (`add_entry` function)**:
   - Allow users to add a new entry by providing information such as title, username, password, URL, and notes.
   - Adds a new entry under the specified group using the `kp.add_entry` method and saves changes with `kp.save()`.

3. **Editing (`edit_entry` function)**:
   - Used to edit existing entry information.
   - Prompts users to input new information and saves changes with `kp.save()`.

4. **Deleting (`delete_entry` function)**:
   - Delete an entry from the database by prompting users for the entry number.
   - Deletes the entry using the `kp.delete_entry` method and saves changes with `kp.save()`.

5. **Password Generation (`generate_password` function)**:
   - Allows users to generate a random password using uppercase letters, lowercase letters, digits, and special characters.
   - Generates passwords using the `random.choice` function and prompts users to enter the desired password length.

6. **Password Display (`show_password` function)**:
   - Displays all information for a selected entry, particularly focusing on displaying passwords.

7. **Main Menu Management (`main` function)**:
   - Presents users with a main menu and calls relevant functions based on the selected operation.
   - Clears the screen with the `clear_screen` function and provides appropriate feedback to users.

### Usage:

- Upon starting the program, prompt users to enter the path to the KeePass database file and its password.
- Based on the selected operation number (`1`-`6`) from the main menu, perform the corresponding operation or exit by entering `q`.
- Provide appropriate feedback after each operation and ensure error messages are displayed when necessary, prompting users to press ENTER to continue.

This script offers users a practical tool for managing entries in KeePass KDBX database files, allowing them to list, add, edit, delete, generate passwords, and view entry details for everyday use scenarios.


---
---


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

