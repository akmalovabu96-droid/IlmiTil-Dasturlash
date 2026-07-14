# IlmiTil
### IlmiTil Dasturlash Muhiti v1.0 🇺🇿
### Kompyuter bilan o'z tilingizda gaplashing!

**IlmiTil** — bu murakkab inglizcha terminlarsiz, mutlaqo sodda va ona tilimizda raqamli dasturlash mantiqini o'rganish uchun yaratilgan muhitdir. 

Dasturlash — bu sehrgarlik emas. Bu shunchaki kompyuterga hayotiy, mantiqiy topshiriqlarni navbat bilan tushuntirishdir. Agar siz hayotda to'g'ri qarorlar qabul qila olsangiz va rejalar tuza olsangiz, demak, dastlab **IlmiTil** orqali, keyinchalik dunyo miqyosdagi Python kabi dasturlash tillar orqali qiziqarli kod-vazifalar ham yoza olasiz!

---

## 🛠️ IlmiTil Qoidalari (Hayotiy misollar bilan)

Keling, dasturlash muhitidagi eng asosiy tushunchalarini kundalik hayotimizga bog'lab o'tamiz:

### 1. O'zgaruvchi (`o'zg`) | Variable
*   **Hayotiy o'xshatish:** Tasavvur qiling, shakar solib qo'yiladigan maxsus quti bor. Qutining ustiga "shakar_idishi" deb yozib qo'ygansiz. Ichiga 5 kilo shakar soldingiz. Endi xonadoshingizga "shakar qayerda?" desangiz, u shakar idishini ko'rsatadi.
*   **IlmiTil qoidasi:** Kompyuter RAM (vaqtinchalik) xotirasida ma'lumot saqlash uchun idish (quti) ajratamiz va unga nom beramiz:

    ```text
    o'zg shakar_idishi = 5
    ```

### 2. Ekranga chiqarish (`yoz`) | print
*   **Hayotiy o'xshatish:** Bu xuddi qo'lingizga qog'oz va ruchka olib, biror gapni baland ovozda o'qib, doskaga yozib qo'yishdek gap. Kompyuter sizga o'zi o'ylayotgan narsani ko'rsatishi uchun shu buyruq kerak.
*   **IlmiTil qoidasi:**

    ```text
    yoz("Assalomu alaykum!")
    Konsoldagi natija: Assalomu alaykum!
    ```

### 3. Interaktiv Muloqot (`kirit`) *Yangi v1.1* | input
*   **Hayotiy o'xshatish:** Sizdan savol so'rashdi, siz javob berdingiz. Eslab qoldingiz.
*   **IlmiTil qoidasi:** Dastur ishlayotgan vaqtda ekranda chiroyli oyna ochiladi, foydalanuvchidan matn so'raydi va uni xotiraga saqlaydi:

    ```text
    o'zg ism = kirit("Ismingizni kiriting: ")

    Ishga tushirish tugmasini bosdingiz -> Oyna chiqadi -> OK
    Konsoldagi natija: Siz oynaga kiritgan narsa chiqadi
    ```

### 3. Shartlar (`agar` va `yo'qsa`) | if/else
*   **Hayotiy o'xshatish:** Ko'chaga chiqishdan oldin derazaga qaraysiz. **Agar** yomg'ir yog'ayotgan bo'lsa — soyabon olasiz. **Yo'qsa (aks holda)** — soyabonsiz ketasiz. Hayotimiz mana shunday tanlovlardan iborat. Kompyuter ham xuddi shunday qaror qabul qiladi.
*   **IlmiTil qoidasi:**

    ```text
    o'zg ob_havo = "yomg'ir"

    agar ob_havo == "yomg'ir":
        yoz("Soyabon oling!")
    yo'qsa:
        yoz("Batafsilroq izlaning, darrov chiqmang.")

    Konsoldagi natija: Soyabon oling! # Chunki o'zgaruvchiga "yomg'ir" degan qiymat saqlangan.
    ```

### 4. Takrorlanish Tsikl (`toki`) | while
*   **Hayotiy o'xshatish:** Choynakka suv to'ldiryapsiz. To choynak to'lmaguncha quyishda davom etasiz. Yoki mashinaga benzin quyayotganda, bak to'lguniga qadar pistolet ishlab turadi.
*   **IlmiTil qoidasi:** Ma'lum bir shart bajarilmagunicha kodni qayta-qayta aylantirish(ishlatish):

    ```text
    o'zg suv_miqdori = 1

    toki suv_miqdori <= 3:
        yoz("Choynakka suv quyilmoqda...")
        suv_miqdori = suv_miqdori + 1

    Konsoldagi natija: Choynakka suv quyilmoqda...Choynakka suv quyilmoqda...Choynakka suv quyilmoqda... # bu yerda to'xtaydi
    ```

### 6. Kengaytirilgan Matematika moduli *Yangi v1.1* | math
*   **Hayotiy o'xshatish:** Kundalik hayotda yer maydoningiz kvadratini hisoblash yoki murakkab matematik ildizlarni topish kerak bo'ladi.
*   **IlmiTil qoidasi:** Endi til ichida o'zbekcha matematik buyruqlar bor:
    *   `daraja(asos, ko'rsatkich)` — sonni darajaga ko'tarish (Masalan: `daraja(5, 2)` -> 25.0)
    *   `ildiz(son)` — sondan kvadrat ildiz chiqarish (Masalan: `ildiz(81)` -> 9.0)

### 5. Vazifalar yoki Funksiyalar (`funksiya` va `qaytar`) | def/return
*   **Hayotiy o'xshatish:** Bu xuddi oshxonadagi taom retseptiga o'xshaydi. Masalan, "Palov tayyorlash" degan umumiy rejangiz bor. Bu reja ichiga sabzi to'g'rash, go'sht qovurish, guruch solish kiradi. Siz har safar mehmonga palov qilganda noldan tushuntirmaysiz, shunchaki "Palov damlaymiz" deysiz (tayyor vazifani chaqirasiz) va oxirida stolga tayyor lagan (natija) **qaytadi**.
*   **IlmiTil qoidasi:** Murakkab ishni bir marta blok sifatida yozib, keyin faqat nomini e'lon qilib ishlatish:

    ```text
    funksiya yoshni_tekshir(yil):
        o'zg hisob = 2026 - yil
        qaytar hisob

    o'zg otamning_yoshi = yoshni_tekshir(1970)
    yoz(otamning_yoshi)

    Konsoldagi natija: 56
    ```

### 6. Izohlar (`#`) | Comments
*   **Hayotiy o'xshatish:** Kitob o'qiyotganda chetiga o'zingiz uchun qalam bilan belgi yoki eslatma yozib qo'yishingizga o'xshaydi. Bu eslatma kitob matniga ta'sir qilmaydi, faqat o'zingizga tushunarli bo'lishi uchun xizmat qiladi.
*   **IlmiTil qoidasi:** Kompyuter bu qatorni o'qimaydi va e'tiborsiz qoldiradi:

    ```text
    # Bu qator shunchaki eslatma, kompyuter buni bajarmaydi
    ```

---

## 🎨 IlmiTil Dasturining Qulayliklari
Dasturni ochganingizda sizga yordam beruvchi ajoyib imkoniyatlar yaratilgan:
*   **Fayllar tizimi (Yangi v1.1):** Tepadagi **"Fayl"** menyusi orqali kodlaringizni `.ilmt` kengaytmasidagi fayl sifatida kompyuterga saqlashingiz va oldin yozilgan kodlarni qayta ochishingiz mumkin.
*   **Tayyor Namunalar (Yangi v1.1):** Tepadagi **"Namunalar"** menyusi orqali bitta klik bilan tayyor kod andozalarini (O'zgaruvchiga ma'lumot saqlash, Muloqot yoki Matematika namunalarini) ekranga yuklab, darhol "Ishga tushirish" tugmasini bosish orqali sinab ko'rishingiz mumkin.
*   **Konsolni Tozalash (Yangi v1.1):** Eski dastur natijalari aralashib ketmasligi uchun supurgi tugmasi orqali konsol ekranini bir marta tozalab tashlashingiz mumkin.
*   **IlmiTil Qo'llanmasi (Chap tomonda):** Qoidalar har doim ko'z oldingizda turadi, adashib ketmaysiz.
*   **Avtomatik Otstup (Joy tashlash):** `agar`, `toki` yoki `funksiya` yozib, `Enter` tugmasini bossangiz, dastur o'zi avtomat ravishda ichkariga 4 ta joy tashlab beradi. Masofani qo'lda sanab o'tirmaysiz!
*   **Tungi Rejim (Dark Mode):** Kechasi ko'zingiz charchamasligi uchun pastdagi tugma orqali ekranni qorong'u rejimiga o'tkazishingiz mumkin.

---
**Yaratuvchi:** Akbarxon Akmalov 💻 
*   **Ilhom olingan:** Python dasturlash tilidan
*   **Savollar bo'yicha:** akmalovabu96@gmail.com

*   Virtual Ilm yo'lidagi ilk qadamingiz qutlug' bo'lsin!

