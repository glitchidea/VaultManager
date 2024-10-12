import os
import getpass  # Modülü içe aktarma
import platform
import sys
import json
import random
import string
import itertools
import pandas as pd
import concurrent.futures
import multiprocessing
from pykeepass import PyKeePass, create_database

#Reader
def clear_screen():
    """Terminal ekranını temizler"""
    os.system('cls' if os.name == 'nt' else 'clear')

def list_entries(kp):
    """Veritabanındaki girişleri listeler"""
    entries = kp.entries
    data = {
        'No': [i + 1 for i in range(len(entries))],
        'Title': [entry.title for entry in entries],
        'Username': [entry.username if entry.username else '-' for entry in entries],
        'Password': [entry.password[:2] + '*' * (len(entry.password) - 2) if entry.password else '-' for entry in entries],
        'URL': [entry.url if entry.url else '-' for entry in entries],
        'Notes': [entry.notes if entry.notes else '-' for entry in entries]
    }
    df = pd.DataFrame(data)
    clear_screen()
    print(df)


def add_entry(kp):
    """Yeni bir giriş ekler"""
    clear_screen()
    new_title = input("Yeni giriş başlığı: ")
    new_username = input("Yeni kullanıcı adı: ")
    new_password = getpass.getpass("Yeni şifre: ")
    new_url = input("Yeni URL: ")
    new_notes = input("Yeni notlar: ")

    default_group = kp.find_groups(name='Root')[0]
    kp.add_entry(default_group, title=new_title, username=new_username, password=new_password, url=new_url, notes=new_notes)
    kp.save()  # Değişiklikleri kaydet
    clear_screen()
    print(f"'{new_title}' başlığıyla yeni giriş başarıyla eklenmiştir.")

def edit_entry(kp):
    """Bir girişi düzenler"""
    entries = kp.entries
    list_entries(kp)
    try:
        entry_num = int(input("\nDüzenlemek istediğiniz girişin numarasını girin (q ile çıkış): "))
        if entry_num <= 0 or entry_num > len(entries):
            raise ValueError("Geçersiz giriş numarası!")
        
        entry = entries[entry_num - 1]
        clear_screen()
        print("Seçilen Giriş Bilgileri:")
        print(f"Başlık: {entry.title}")
        print(f"Kullanıcı Adı: {entry.username if entry.username else '-'}")
        print(f"Şifre: {entry.password if entry.password else '-'}")
        print(f"URL: {entry.url if entry.url else '-'}")
        print(f"Notlar: {entry.notes if entry.notes else '-'}")
        print("\nDüzenlemek istediğiniz bilgileri girin (Değiştirilecek olmayan alanları boş bırakın):")

        new_title = input(f"Yeni başlık ({entry.title}): ")
        new_username = input(f"Yeni kullanıcı adı ({entry.username if entry.username else '-'}): ")
        new_password = getpass(prompt=f"Yeni şifre ({entry.password if entry.password else '-'}): ")
        new_url = input(f"Yeni URL ({entry.url if entry.url else '-'}): ")
        new_notes = input(f"Yeni notlar ({entry.notes if entry.notes else '-'}): ")

        if new_title:
            entry.title = new_title
        if new_username:
            entry.username = new_username
        if new_password:
            entry.password = new_password
        if new_url:
            entry.url = new_url
        if new_notes:
            entry.notes = new_notes

        kp.save()  # Değişiklikleri kaydet
        clear_screen()
        print(f"Giriş başarıyla güncellendi.")
        input("Ana menüye dönmek için ENTER tuşuna basın.")

    except ValueError as ve:
        clear_screen()
        print(f"Hata: {ve}")
        input("Devam etmek için ENTER tuşuna basın.")

def delete_entry(kp):
    """Bir girişi siler"""
    entries = kp.entries
    list_entries(kp)
    try:
        entry_num = int(input("\nSilmek istediğiniz girişin numarasını girin (q ile çıkış): "))
        if entry_num <= 0 or entry_num > len(entries):
            raise ValueError("Geçersiz giriş numarası!")
        
        entry = entries[entry_num - 1]
        kp.delete_entry(entry)
        kp.save()  # Değişiklikleri kaydet
        clear_screen()
        print(f"Giriş başarıyla silindi.")
        input("Ana menüye dönmek için ENTER tuşuna basın.")

    except ValueError as ve:
        clear_screen()
        print(f"Hata: {ve}")
        input("Devam etmek için ENTER tuşuna basın.")

def import_data(kp):
    """Verileri içe aktarır"""
    clear_screen()
    try:
        file_path = input("İçe aktarmak istediğiniz KDBX dosyasının yolunu girin: ")
        new_kp = PyKeePass(file_path)

        # Mevcut veritabanındaki tüm girişleri yeni veritabanına kopyala
        for entry in kp.entries:
            default_group = new_kp.find_groups(name='Root')[0]
            new_kp.add_entry(default_group, title=entry.title, username=entry.username, password=entry.password, url=entry.url, notes=entry.notes)

        new_kp.save()  # Yeni veritabanını kaydet
        clear_screen()
        print("Veriler başarıyla içe aktarıldı.")
        input("Ana menüye dönmek için ENTER tuşuna basın.")

    except Exception as e:
        clear_screen()
        print(f"Hata: {e}")
        input("Devam etmek için ENTER tuşuna basın.")


def export_data(kp):
    """Verileri dışa aktarır"""
    clear_screen()
    try:
        export_format = input("Verileri dışa aktarmak için formatı seçin (CSV için 'csv', JSON için 'json'): ").strip().lower()

        if export_format not in ['csv', 'c', 'C', 'json', 'j', 'J']:
            raise ValueError("Geçersiz format seçimi! Lütfen 'csv' veya 'json' girin.")

        file_path = input("Dışa aktarılacak dosyanın yolunu girin (boş bırakılırsa varsayılan dosya adı kullanılır): ")
        
        if not file_path.strip():
            file_path = 'exported_data.' + export_format  # Varsayılan dosya adı
        
        if export_format in ['csv', 'c', 'C']:
            df = pd.DataFrame({
                'Title': [entry.title for entry in kp.entries],
                'Username': [entry.username if entry.username else '-' for entry in kp.entries],
                'Password': [entry.password for entry in kp.entries],
                'URL': [entry.url if entry.url else '-' for entry in kp.entries],
                'Notes': [entry.notes if entry.notes else '-' for entry in kp.entries]
            })
            df.to_csv(file_path, index=False)
        
        elif export_format in ['json', 'j', 'J']:
            data = [{
                'Title': entry.title,
                'Username': entry.username if entry.username else '-',
                'Password': entry.password,
                'URL': entry.url if entry.url else '-',
                'Notes': entry.notes if entry.notes else '-'
            } for entry in kp.entries]
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

        clear_screen()
        print(f"Veriler başarıyla '{file_path}' dosyasına dışa aktarıldı.")
        input("Ana menüye dönmek için ENTER tuşuna basın.")

    except Exception as e:
        clear_screen()
        print(f"Hata: {e}")
        input("Devam etmek için ENTER tuşuna basın.")


def generate_password():
    """Rastgele bir şifre oluşturur"""
    clear_screen()
    try:
        use_upper = input("Büyük harfler kullanılsın mı? (Evet için 'e', Hayır için başka bir tuş): ").lower() == 'e'
        use_lower = input("Küçük harfler kullanılsın mı? (Evet için 'e', Hayır için başka bir tuş): ").lower() == 'e'
        use_digits = input("Rakamlar kullanılsın mı? (Evet için 'e', Hayır için başka bir tuş): ").lower() == 'e'
        use_punctuation = input("Noktalama işaretleri kullanılsın mı? (Evet için 'e', Hayır için başka bir tuş): ").lower() == 'e'
        
        length = int(input("Şifrenin uzunluğunu girin: "))

        if not (use_upper or use_lower or use_digits or use_punctuation):
            raise ValueError("En az bir karakter türü seçilmelidir!")

        characters = ''
        if use_upper:
            characters += string.ascii_uppercase
        if use_lower:
            characters += string.ascii_lowercase
        if use_digits:
            characters += string.digits
        if use_punctuation:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        clear_screen()
        print(f"Oluşturulan şifre: {password}")
        input("Ana menüye dönmek için ENTER tuşuna basın.")

    except ValueError as ve:
        clear_screen()
        print(f"Hata: {ve}")
        input("Devam etmek için ENTER tuşuna basın.")

def show_password(kp):
    """Bir girişin şifresini gösterir"""
    entries = kp.entries
    list_entries(kp)
    try:
        entry_num = int(input("\nŞifresini görmek istediğiniz girişin numarasını girin (q ile çıkış): "))
        if entry_num <= 0 or entry_num > len(entries):
            raise ValueError("Geçersiz giriş numarası!")
        
        entry = entries[entry_num - 1]
        clear_screen()
        print(f"Başlık: {entry.title}")
        print(f"Kullanıcı Adı: {entry.username if entry.username else '-'}")
        print(f"Şifre: {entry.password if entry.password else '-'}")
        print(f"URL: {entry.url if entry.url else '-'}")
        print(f"Notlar: {entry.notes if entry.notes else '-'}")
        input("\nAna menüye dönmek için ENTER tuşuna basın.")

    except ValueError as ve:
        clear_screen()
        print(f"Hata: {ve}")
        input("Devam etmek için ENTER tuşuna basın.")

#Solvent
def open_kdbx(filepath, password):
    try:
        kp = PyKeePass(filepath, password=password)
        return kp
    except Exception:
        return None

def generate_passwords(charset, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(charset, repeat=length):
            yield ''.join(password)

def try_password(filepath, password):
    kp = open_kdbx(filepath, password)
    if kp:
        print(f"\nŞifre bulundu: {password}")
        return password
    return None

def try_passwords(filepath, passwords):
    found_password = None
    total_passwords = len(passwords)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        future_to_password = {executor.submit(try_password, filepath, password): password for password in passwords}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_password)):
            password = future_to_password[future]
            sys.stdout.write(f"\rDeneniyor ({i+1}/{total_passwords}): {password}")
            sys.stdout.flush()
            
            try:
                result = future.result()
                if result:
                    found_password = result
                    break
            except Exception as exc:
                continue

    if found_password:
        print(f"\nŞifre bulundu: {found_password}")
        return True
    else:
        print("\nŞifre bulunamadı.")
        return False
#Converter

def create_new_database():
    db_name = input("Yeni KDBX dosyasının tam yolunu girin (örneğin, C:\\Users\\mydatabase.kdbx): ")
    password = getpass.getpass("Veritabanı şifresini girin: ")
    confirm_password = getpass.getpass("Veritabanı şifresini tekrar girin: ")

    if password != confirm_password:
        print("Şifreler eşleşmiyor. Lütfen tekrar deneyin.")
        return

    try:
        kp = create_database(db_name, password)
        kp.save()
        print(f"Yeni veritabanı '{db_name}' başarıyla oluşturuldu.")
    except Exception as e:
        print(f"Veritabanı oluşturulurken hata oluştu: {e}")

def change_existing_password():
    db_path, _, _ = load_settings()  # Ayarları yükle
    if not db_path:
        print("Veritabanı yolu ayarlanmamış. Önce ayarları yapın.")
        return

    old_password = getpass.getpass("Mevcut veritabanı şifresini girin: ")
    try:
        kp = PyKeePass(db_path, password=old_password)
    except Exception as e:
        print(f"Dosya açılırken hata oluştu: {e}")
        return

    new_password = getpass.getpass("Yeni veritabanı şifresini girin: ")
    confirm_password = getpass.getpass("Yeni veritabanı şifresini tekrar girin: ")

    if new_password != confirm_password:
        print("Yeni şifreler eşleşmiyor. Lütfen tekrar deneyin.")
        return

    kp.password = new_password
    kp.save()
    print(f"Veritabanı '{db_path}' şifresi başarıyla değiştirildi.")

#Ayarlar
def load_settings():
    """Ayar dosyasını yükler ve mevcut ayarları döndürür."""
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
            return settings.get("db_path", None), settings.get("csv_path", None), settings.get("json_path", None)
    except FileNotFoundError:
        return None, None, None  # Dosya yoksa varsayılan değerler
    except json.JSONDecodeError:
        return None, None, None  # JSON hatası

def save_settings(db_path, csv_path, json_path):
    """Ayarları belirtilen dosyaya kaydeder."""
    settings = {
        "db_path": db_path,
        "csv_path": csv_path,
        "json_path": json_path
    }
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)


def settings_menu():
    """Ayarlar menüsünü gösterir ve dosya yolu ayarlarını günceller."""
    while True:
        clear_screen()
        print("Ayarlar Menüsü")
        
        # Mevcut ayarları yükle
        db_path, csv_path, json_path = load_settings()
        
        # Mevcut yolları göster
        print(f"Mevcut Veritabanı Dosya Yolu: {db_path if db_path else 'Belirtilmedi'}")
        print(f"Mevcut CSV Dosya Yolu: {csv_path if csv_path else 'Belirtilmedi'}")
        print(f"Mevcut JSON Dosya Yolu: {json_path if json_path else 'Belirtilmedi'}")
        
        print("\nKDBX yolu")
        print("\n1 - Veritabanı dosya yolunu ayarla")
        print("\nDışa Aktarma")
        print("\n2 - CSV dosya yolunu ayarla")
        print("3 - JSON dosya yolunu ayarla")
        print("4 - Mevcut ayarları göster")
        print("q - Çıkış")

        choice = input("Bir seçenek seçin: ")

        if choice == "1":
            new_db_path = input("Yeni veritabanı dosya yolunu girin: ")
            csv_path, json_path = load_settings()[1:3]  # Mevcut CSV ve JSON yollarını al
            save_settings(new_db_path, csv_path, json_path)
            print(f"Yeni veritabanı dosya yolu '{new_db_path}' olarak kaydedildi.")
            input("Devam etmek için ENTER'a basın...")
        elif choice == "2":
            new_csv_path = input("Yeni CSV dosya yolunu girin: ")
            db_path, json_path = load_settings()[0], load_settings()[2]  # Mevcut DB ve JSON yollarını al
            save_settings(db_path, new_csv_path, json_path)
            print(f"Yeni CSV dosya yolu '{new_csv_path}' olarak kaydedildi.")
            input("Devam etmek için ENTER'a basın...")
        elif choice == "3":
            new_json_path = input("Yeni JSON dosya yolunu girin: ")
            db_path, csv_path = load_settings()[0:2]  # Mevcut DB ve CSV yollarını al
            save_settings(db_path, csv_path, new_json_path)
            print(f"Yeni JSON dosya yolu '{new_json_path}' olarak kaydedildi.")
            input("Devam etmek için ENTER'a basın...")
        elif choice == "4":
            db_path, csv_path, json_path = load_settings()
            print(f"Mevcut veritabanı dosya yolu: {db_path if db_path else 'Belirtilmedi'}")
            print(f"Mevcut CSV dosya yolu: {csv_path if csv_path else 'Belirtilmedi'}")
            print(f"Mevcut JSON dosya yolu: {json_path if json_path else 'Belirtilmedi'}")
            input("Devam etmek için ENTER'a basın...")
        elif choice.lower() == "q":
            break
        else:
            print("Geçersiz seçenek, lütfen tekrar deneyin.")
            input("Devam etmek için ENTER'a basın...")
#Menü
def main():
    while True:
        clear_screen()
        print("1 - Listele ")
        print("2 - Yeni KDBX dosyası oluştur ")
        print("3 - Mevcut KDBX dosyasının şifresini değiştir ")
        print("4 - Şifre Kırma ")
        print("5 - Ayarlar ")
        print("q - Çıkış")

        choice = input("Bir seçenek seçin: ")

        if choice == "1":
            # Reader işlevi
            try:
                db_path, _, _ = load_settings()  # Ayarları yükle
                user_db_path = input("KeePass veritabanı dosyasının yolunu giriniz (Varsayılan): ")

                if not user_db_path:  # Kullanıcı boş bıraktıysa ayarlar kullanılsın
                    user_db_path = db_path
                    if not user_db_path:
                        raise ValueError("Ayar dosyasında veritabanı yolu tanımlanmamış.")

                password = getpass.getpass(prompt='KeePass veritabanı şifresini giriniz: ')
                kp = PyKeePass(user_db_path, password=password)

                while True:
                    clear_screen()
                    print("1- Listele")
                    print("2- Ekle")
                    print("3- Düzenle")
                    print("4- Sil")
                    print("5- Şifre Oluştur")
                    print("6- Şifre Göster")
                    print("q- Çıkış")

                    choice = input("\nİşlem seçin: ").strip().lower()

                    if choice == '1':
                        list_entries(kp)
                        input("\nDevam etmek için ENTER tuşuna basın...")
                    elif choice == '2':
                        add_entry(kp)
                    elif choice == '3':
                        edit_entry(kp)
                    elif choice == '4':
                        delete_entry(kp)
                    elif choice == '5':
                        generate_password()
                    elif choice == '6':
                        show_password(kp)
                    elif choice == 'q':
                        clear_screen()
                        print("İşlem tamamlandı. Programdan çıkılıyor...")
                        break
                    else:
                        clear_screen()
                        print("Geçersiz seçenek! Lütfen tekrar deneyin.")
                        input("\nDevam etmek için ENTER tuşuna basın...")
            except Exception as e:
                clear_screen()
                print(f"Bir hata oluştu: {str(e)}")
                input("\nDevam etmek için ENTER tuşuna basın...")

        elif choice == "2":
            clear_screen()
            create_new_database()
        elif choice == "3":
            clear_screen()
            change_existing_password()
        elif choice == "4":
            clear_screen()
            filepath = input("Lütfen KDBX dosyasının konumunu girin: ")
            use_password_file = input("Elinizde bir şifre dosyası var mı? (E/H): ").strip().lower() == 'e'
            if use_password_file:
                password_file = input("Lütfen şifre dosyasının konumunu girin: ")
                
                if not os.path.isfile(password_file):
                    print("Şifre dosyası bulunamadı.")
                    continue
                
                with open(password_file, 'r') as f:
                    passwords = f.read().splitlines()
                
                if input(f"{len(passwords)} adet şifre denenecek. Denemek ister misiniz? (E/H): ").strip().lower() == 'e':
                    if try_passwords(filepath, passwords):
                        print("Şifre doğru!")
                        continue
                    else:
                        print("\nŞifre dosyasındaki şifreler ile dosya açılamadı.")
            
            create_password_file = input("Kendi şifre dosyanızı oluşturmak ister misiniz? (E/H): ").strip().lower() == 'e'
            if create_password_file:
                charset = ""
                if input("Büyük harfler kullanılsın mı? (E/H): ").strip().lower() == 'e':
                    charset += string.ascii_uppercase
                if input("Küçük harfler kullanılsın mı? (E/H): ").strip().lower() == 'e':
                    charset += string.ascii_lowercase
                if input("Rakamlar kullanılsın mı? (E/H): ").strip().lower() == 'e':
                    charset += string.digits
                if input("ASCII karakterleri kullanılsın mı? (E/H): ").strip().lower() == 'e':
                    charset += string.punctuation
                
                if not charset:
                    print("Hiçbir karakter seti seçilmedi.")
                    continue
                
                min_length = int(input("Minimum şifre uzunluğu: "))
                max_length = int(input("Maximum şifre uzunluğu: "))
                
                generated_password_file = "generated_passwords.txt"
                with open(generated_password_file, 'w') as f:
                    for password in generate_passwords(charset, min_length, max_length):
                        f.write(password + '\n')
                print(f"Şifre dosyası oluşturuldu: {generated_password_file}")
                
                with open(generated_password_file, 'r') as f:
                    passwords = f.read().splitlines()
                
                print(f"Oluşturulan dosyada {len(passwords)} adet şifre var.")
                if input(f"Oluşturulan dosyadaki şifreleri denemek ister misiniz? (E/H): ").strip().lower() == 'e':
                    if try_passwords(filepath, passwords):
                        print("Şifre doğru!")
                        continue
                    else:
                        print("\nOluşturulan şifre dosyasındaki şifreler ile dosya açılamadı.")

        elif choice == "5":
            clear_screen()
            settings_menu() 
        elif choice.lower() == "q":
            break
        else:
            print("Geçersiz seçenek, lütfen tekrar deneyin.")

        input("\nAna menüye dönmek için Enter'a basın...")
if __name__ == "__main__":
    main()
