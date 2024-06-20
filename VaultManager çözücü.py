# KDBX CRACK AMA PARALEL OLARAK DENER VE AKLINDA TUTMADAN DOSYA YOLUNDAN SÜREKLİ OLARAK ÇEKER- HIZLIDIR

import itertools
import string
from pykeepass import PyKeePass
import os
import sys
import concurrent.futures
import multiprocessing

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

def main():
    filepath = input("Lütfen KDBX dosyasının konumunu girin: ")
    
    use_password_file = input("Elinizde bir şifre dosyası var mı? (E/H): ").strip().lower() == 'e'
    if use_password_file:
        password_file = input("Lütfen şifre dosyasının konumunu girin: ")
        
        if not os.path.isfile(password_file):
            print("Şifre dosyası bulunamadı.")
            return
        
        with open(password_file, 'r') as f:
            passwords = f.read().splitlines()
        
        if input(f"{len(passwords)} adet şifre denenecek. Denemek ister misiniz? (E/H): ").strip().lower() == 'e':
            if try_passwords(filepath, passwords):
                return
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
            return
        
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
                return
            else:
                print("\nOluşturulan şifre dosyasındaki şifreler ile dosya açılamadı.")

if __name__ == "__main__":
    main()
