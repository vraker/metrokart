import sys

# Başlanğıc dəyişənlər
pin = "1234"
balans = 0.0
borc = 0.0
limit = 100.0
gedis_sayi = 0
emeliyyatlar = []
rejim = "Normal" # Normal, Telebe, Pensiyaci
gunluk_artim = 0.0
gunluk_odenis = 0.0
gunluk_endirim = 0.0

def pin_yoxla():
    cehd = 3
    while cehd > 0:
        daxil_edilen = input(f"PIN daxil edin (Cəhd: {cehd}): ")
        if daxil_edilen == pin:
            print("Giriş uğurludur!")
            return True
        else:
            cehd -= 1
            print("Yanlış PIN!")
    print("3 dəfə səhv daxil etdiniz. Proqram dayandırılır.")
    return False

def menu_goster():
    print(f"\n--- METROKART MENYU (Rejim: {rejim}) ---")
    print(f"Balans: {balans:.2f} AZN | Borc: {borc:.2f} AZN")
    print("1) Balansı göstər")
    print("2) Balans artır")
    print("3) Gediş et (Turniket)")
    print("4) Son əməliyyatlara bax")
    print("5) Günlük statistika")
    print("6) Parametrlər")
    print("0) Çıxış")

if not pin_yoxla():
    sys.exit()

while True:
    menu_goster()
    secim = input("Seçim edin: ")

    if secim == "1":
        print(f"Cari balansınız: {balans:.2f} AZN")
        if borc > 0:
            print(f"Ödənilməli borc: {borc:.2f} AZN")

    elif secim == "2":
        try:
            mebleg = float(input("Artırılacaq məbləği daxil edin: "))
            if mebleg <= 0:
                print("Məbləğ müsbət olmalıdır!")
            elif gunluk_artim + mebleg > limit:
                print(f"Limit aşıldı! Günlük qalan limit: {limit - gunluk_artim:.2f} AZN")
            else:
                gunluk_artim += mebleg
                if borc > 0:
                    if mebleg >= borc:
                        mebleg -= borc
                        print(f"{borc:.2f} AZN borc silindi.")
                        borc = 0
                    else:
                        borc -= mebleg
                        print(f"Borcun bir hissəsi silindi. Qalan borc: {borc:.2f} AZN")
                        mebleg = 0
                balans += mebleg
                emeliyyatlar.append(f"Artırma: +{gunluk_artim:.2f} AZN, Yeni Balans: {balans:.2f}")
                print("Balans uğurla artırıldı.")
        except ValueError:
            print("Zəhmət olmasa rəqəm daxil edin.")

    elif secim == "3":
        # Qiymət hesablama
        qiymet = 0.40
        endirim = 0.0
        
        if rejim == "Telebe":
            qiymet = 0.20
        elif rejim == "Pensiyaci":
            qiymet = 0.15
        else: # Normal rejim
            gedis_sayi += 1
            if 2 <= gedis_sayi <= 4:
                endirim = 0.40 * 0.10
                qiymet = 0.40 - endirim
            elif gedis_sayi >= 5:
                endirim = 0.40 * 0.25
                qiymet = 0.40 - endirim

        if balans >= qiymet:
            balans -= qiymet
            gunluk_odenis += qiymet
            gunluk_endirim += endirim
            emeliyyatlar.append(f"Gediş: -{qiymet:.2f} AZN, Endirim: {endirim:.2f}, Balans: {balans:.2f}")
            print(f"Keçid uğurludur! Qiymət: {qiymet:.2f} AZN")
        elif 0.30 <= balans < qiymet and borc == 0:
            cavab = input("Balans azdır. 'Təcili keçid' (10 qəpik borc) istifadə edilsin? (h/y): ")
            if cavab.lower() == 'h':
                balans = 0
                borc = 0.10
                gunluk_odenis += 0.30
                print("Təcili keçid istifadə edildi. Borcunuz yaranmışdır.")
                emeliyyatlar.append("Təcili keçid (0.10 AZN borc)")
        else:
            print("Balans yetərsizdir! Zəhmət olmasa artırın.")

    elif secim == "4":
        try:
            n = int(input("Son neçə əməliyyatı görmək istəyirsiniz? "))
            for e in emeliyyatlar[-n:]:
                print(f"-> {e}")
        except ValueError:
            print("Düzgün say daxil edin.")

    elif secim == "5":
        print(f"--- GÜNLÜK STATİSTİKA ---")
        print(f"Ümumi gediş: {gedis_sayi}")
        print(f"Ümumi ödəniş: {gunluk_odenis:.2f} AZN")
        print(f"Toplam endirim: {gunluk_endirim:.2f} AZN")
        print(f"Toplam artırma: {gunluk_artim:.2f} AZN")

    elif secim == "6":
        print("1) Limiti dəyiş\n2) Rejimi dəyiş")
        p_secim = input("Seçim: ")
        if p_secim == "1":
            limit = float(input("Yeni günlük limit: "))
        elif p_secim == "2":
            print("1-Normal, 2-Tələbə, 3-Pensiyaçı")
            r_secim = input("Seçim: ")
            rejim = "Normal" if r_secim=="1" else "Telebe" if r_secim=="2" else "Pensiyaci"
            print(f"Rejim dəyişdirildi: {rejim}")

    elif secim == "0":
        print("Sistemdən çıxılır. Xoş istirahətlər!")
        break
    else:
        print("Yanlış seçim!")
