import os
import getpass
import platform
from pykeepass import PyKeePass, create_database

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def create_new_database():
    db_name = input("Yeni KDBX dosyasının tam yolunu girin (örneğin, C:\\Users\\yilan\\OneDrive\\Desktop\\Yedek projeler\\mydatabase.kdbx): ")
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
    db_name = input("Şifresini değiştirmek istediğiniz KDBX dosyasının tam yolunu girin (örneğin, C:\\Users\\yilan\\OneDrive\\Desktop\\Yedek projeler\\mydatabase.kdbx): ")
    old_password = getpass.getpass("Mevcut veritabanı şifresini girin: ")

    try:
        kp = PyKeePass(db_name, password=old_password)
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
    print(f"Veritabanı '{db_name}' şifresi başarıyla değiştirildi.")

def main():
    while True:
        clear_screen()
        print("1 - Yeni KDBX dosyası oluştur")
        print("2 - Mevcut KDBX dosyasının şifresini değiştir")
        print("q - Çıkış")

        choice = input("Bir seçenek seçin: ")

        if choice == "1":
            clear_screen()
            create_new_database()
        elif choice == "2":
            clear_screen()
            change_existing_password()
        elif choice.lower() == "q":
            break
        else:
            print("Geçersiz seçenek, lütfen tekrar deneyin.")

        input("\nAna menüye dönmek için Enter'a basın...")

if __name__ == "__main__":
    main()
