from pykeepass import PyKeePass
from getpass import getpass
import pandas as pd
import random
import string
import os

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
        'Password': [entry.password if entry.password else '-' for entry in entries],
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
    new_password = getpass(prompt="Yeni şifre: ")
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

def main():
    kp = None
    try:
        database_path = input("KeePass veritabanı dosyasının yolunu giriniz: ")
        password = getpass(prompt='KeePass veritabanı şifresini giriniz: ')
        kp = PyKeePass(database_path, password=password)

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

    finally:
        if kp:
            kp.save()  # Değişiklikleri kaydet

if __name__ == "__main__":
    main()
