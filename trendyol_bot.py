from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import re
import time

# Chrome driver yolu
driver_path = r"C:\Users\LENOVO\Desktop\reactproje\Trendyol Bot\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Trendyol giriş bilgileri
email = "webtasarimvedestek@gmail.com"
password = "1QAZ2wsx!'"

try:
    # Trendyol giriş sayfasına git
    print("Trendyol giriş sayfasına gidiliyor...")
    driver.get("https://www.trendyol.com/giris")
    time.sleep(1)

    # E-posta ve şifre alanlarını doldur
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "login-email"))
    )
    email_input.send_keys(email)

    password_input = driver.find_element(By.ID, "login-password-input")
    password_input.send_keys(password)

    # Giriş butonuna tıkla
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'submit')]")
    login_button.click()
    time.sleep(1)  # Giriş yaptıktan sonra bekle

    # Sepet sayfasına git
    print("Sepet sayfasına gidiliyor...")
    driver.get("https://www.trendyol.com/sepetim")
    time.sleep(1)

     # Pop-up'ta "Anladım" butonuna tıklama
    try:
        print("Anladım butonuna tıklanıyor...")
        anladim_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='tooltip-content']//button[text()='Anladım']"))
        )
        anladim_button.click()
        print("Anladım butonuna tıklandı.")
    except:
        print("Anladım pop-up görünmüyor, devam ediliyor.")

    # Sepeti Onayla butonuna tıklama
    print("Sepeti onaylama işlemi yapılıyor...")
    confirm_cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='pb-summary-approve']/a[contains(@class, 'ty-link-btn-primary')]"))
    )
    confirm_cart_button.click()
    time.sleep(3)

    # Trendyol Pass öneri pop-up kontrolü ve "Eklemeden Devam Et" butonuna tıklama
    try:
        print("Trendyol Pass pop-up kontrol ediliyor...")
        continue_without_add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ty-pass-continue-without-add')]"))
        )
        continue_without_add_button.click()
        print("Eklemeden Devam Et butonuna tıklandı.")
    except:
        print("Trendyol Pass pop-up görünmüyor, devam ediliyor.")

    # "Mesafeli Satış Sözleşmesi" bağlantısını açma
    print("Mesafeli Satış Sözleşmesi açılıyor...")
    sales_contract_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//strong[text()='Mesafeli Satış Sözleşmesi']"))
    )
    sales_contract_link.click()
    sales_contract_link.click()
    sales_contract_link.click()

    time.sleep(5)  # Sözleşmenin açılması için bekleme

    # Mesafeli Satış Sözleşmesi metnini çekme
    contract_text = driver.find_element(By.TAG_NAME, "body").text

    # Satıcı adlarını, telefon numaralarını ve ürün adlarını çekme
    seller_names = re.findall(r"Satıcının Ticaret Unvanı / Adı ve Soyadı\s*:\s*(.+)", contract_text)
    seller_phones = re.findall(r"Satıcının Telefonu\s*:\s*([\d\s\(\)-]+)", contract_text)
    product_names = re.findall(r"Ürün/Hizmet Açıklaması Adet Peşin Fiyatı Ara Toplam \(KDV Dahil\)\s*\n(.+)", contract_text)

    # Benzersiz satıcı adlarını takip etmek için bir set kullanıyoruz
    unique_sellers = set()

    # .txt dosyasını yazma modunda açıyoruz
    with open("Trendyol.txt", "w") as file:
        file.write("Satıcı Adları, Telefon Numaraları ve Ürün Adları Listesi:\n")
        for i in range(min(len(seller_names), len(seller_phones), len(product_names))):
            if seller_names[i] in unique_sellers:
                # Aynı satıcı adı tekrarlandığında döngüyü durdur
                break
            unique_sellers.add(seller_names[i])
            file.write(f"   Ürün Adı: {product_names[i]}\n")
            file.write(f"{i+1}. Satıcı Adı: {seller_names[i]}\n")
            file.write(f"   Satıcı Telefon: {seller_phones[i]}\n")
            file.write("-" * 40 + "\n")

    print("Satıcı bilgileri 'Trendyol.txt' dosyasına başarıyla yazdırıldı.")

except Exception as e:
    print(f"Hata oluştu: {e}")

finally:
    # Tarayıcıyı kapat
    print("Tarayıcı kapatılıyor...")
    driver.quit()
