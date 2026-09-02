import sys
import re
import tkinter as tk
import math
from tkinter import scrolledtext, filedialog, messagebox, simpledialog

# Tarjima dvijogimiz
UZ_TO_PY = {
    "yoz": "print",
    "agar ": "if ",
    "yo'qsa:": "else:",
    "toki ": "while ",
    "funksiya ": "def ",
    "qaytar ": "return ",
    "kirit": "kirit",
    "va": "and",
    "yoki": "or",
    "urin:": "try:",
    "xatoda:": "except:",
    "nihoyat:": "finally:",
    "sinf": "class"
}

# Tungi rejimi bayrog'i
is_dark_mode = False
current_file_path = None


def translate_error(error_message):
    """Python xatolik xabarlarini to'liq o'zbek tiliga o'giruvchi funksiya"""
    err_str = str(error_message)

    # Eng ko'p uchraydigan aniq (obvious) xatoliklar lug'ati
    ERROR_TRANSLATIONS = {
        # --- NameError (Topilmagan o'zgaruvchilar) ---
        "name '": "Xatolik: '",
        "' is not defined": "' degan buyruq, o'zgaruvchi yoki sinf topilmadi (e'lon qilinmagan)",

        # --- ZeroDivisionError (Matematik xatolar) ---
        "division by zero": "Sonni nolga bo'lib bo'lmaydi!",

        # --- TypeError (Ma'lumot turlari chalkashligi) ---
        "can only concatenate str (not \"int\") to str": "Matnga faqat matnni qo'shish mumkin (sonni emas). 'matn()' funksiyasidan foydalaning",
        "can only concatenate str (not \"float\") to str": "Matnga faqat matnni qo'shish mumkin (o'nlik sonni emas). 'matn()' funksiyasidan foydalaning",
        "unsupported operand type(s) for": "Ushbu ma'lumot turlari o'rtasida matematik amalni bajarib bo'lmaydi:",
        "not all arguments converted during string formatting": "Matnni formatlashda yoki qoldiq olish (%) amalida xatolik bor",

        # --- ValueError (Noto'g'ri qiymatlar) ---
        "invalid literal for int() with base 10": "Ushbu kiritilgan matnni butun songa (butson) o'tkazib bo'lmaydi. Faqat raqam kiriting:",
        "math domain error": "Matematik xatolik (masalan, manfiy sonni ildizdan chiqarishga urindingiz)!",

        # --- SyntaxError (Sintaksis va imlo xatolari) ---
        "invalid syntax": "Sintaksis xato (buyruq noto'g'ri yozilgan yoki qator oxirida ikki nuqta ':' esdan chiqqan)",
        "unmatched ')'": "Yopilmagan qavs xatoligi! Ochilgan qavslar sonini tekshiring: ')'",
        "unmatched '('": "Ochilmagan qavs xatoligi! Qavslar juftligini tekshiring: '('",
        "was never closed": "matni yoki qavsi oxirigacha yopilmay qolib ketgan",
        "unterminated string literal": "Qo'shtirnoq yopilmay qolgan! Matn boshlangan qo'shtirnoqni oxirida yopishni unutmang",

        # --- IndentationError (Bo'shliq va surilish xatolari) ---
        "expected an indented block": "Bo'shliq (indentation) tashlanishi kerak edi. 'agar', 'toki', 'funksiya' yoki 'sinf' ichidagi qatorni 4 ta bo'shliq o'ngga suring",
        "unexpected indent": "Kutilmagan bo'shliq! Qator boshidagi ortiqcha yoki adashib qo'yilgan bo'shliqlarni o'chiring",
        "unindent does not match any outer indentation level": "Blokdan chiqishda bo'shliq mos kelmadi. Qator boshidagi surilish darajasini tekshiring",

        # --- IndexError (Ro'yxat indeks xatolari) ---
        "list index out of range": "Ro'yxat indeksi chegaradan chiqib ketdi! Mavjud bo'lmagan elementga murojaat qilyapsiz",

        # --- AttributeError (Obyekt xususiyat xatolari) ---
        "object has no attribute": "obyektida bunday xususiyat yoki funksiya mavjud emas"
    }

    # Xatolik xabarini o'zbekcha talqinlar bilan almashtirib chiqamiz
    for eng_err, uz_err in ERROR_TRANSLATIONS.items():
        if eng_err in err_str:
            err_str = err_str.replace(eng_err, uz_err)

    return err_str


def custom_kirit(savol_matni="Ma'lumot kiriting:"):
    """Ma'lumotlarni kiritish oynasi kirit() buyrug'i uchun"""
    # Tkinter dialog oynasini chaqirish
    javob = simpledialog.askstring("IlmiTil - Kiritish maydoni", savol_matni)
    # Agar foydalanuvchi bekor qilsa, kod buzilmasligi uchun bo'sh string qaytaramiz
    return javob if javob is not None else ""


def execute_uz_code(uz_code_text, output_widget):
    """Oynadagi kodni olib, uni o'giradigan va bajaradigan funksiya"""
    output_widget.delete("1.0", tk.END)

    class CustomOutput:
        def write(self, text):
            output_widget.insert(tk.END, text)

        def flush(self):
            pass

    sys.stdout = CustomOutput()

    try:
        # Lug'atni tozalaymiz
        CLEAN_UZ_TO_PY = {k.strip(): v.strip() for k, v in UZ_TO_PY.items()}

        uz_lines = uz_code_text.splitlines()
        py_code = []

        for line in uz_lines:
            translated_line = line

            # 1. "o'zg " so'zini olib tashlaymiz
            if "o'zg " in translated_line:
                translated_line = translated_line.replace("o'zg ", "")

            # Bu qoida faqat ikkitalik qo'shtirnoqlarni ajratadi
            strings_found = re.findall(r'"[^"\\]*(?:\\[\s\S][^"\\]*)*"', translated_line)

            for i, s in enumerate(strings_found):
                translated_line = translated_line.replace(s, f"__STR_{i}__")

            # Bemalol o'zbekcha so'zlarni Python so'zlariga almashtirsak bo'ladi.
            # Endi \b ishlatish shart emas, chunki qo'shtirnoqlar xavfsiz joyda.
            for uz_word, py_word in CLEAN_UZ_TO_PY.items():
                # Agar lug'atdagi so'z satr ichida bo'lsa (masalan "yo'qsa:")
                if uz_word in translated_line:
                    # Uni to'g'ridan-to'g'ri almashtiramiz
                    translated_line = translated_line.replace(uz_word, py_word)

            # 4. Tarjima tugagach, berkitib qo'yilgan qo'shtirnoqli matnlarni o'z joyiga qaytaramiz
            for i, s in enumerate(strings_found):
                translated_line = translated_line.replace(f"__STR_{i}__", s)

            py_code.append(translated_line)

        final_python_script = "\n".join(py_code)

        global_env = {
            "print": sys.stdout.write,
            "kirit": custom_kirit,
            "butson": int,
            "matn": str,
            "ildiz": math.sqrt,
            "daraja": math.pow,
        }
        exec(final_python_script, global_env)

    except Exception as e:
        uz_error = translate_error(e)
        output_widget.insert(tk.END, f"\nXatolik yuz berdi:\n{uz_error}")
    finally:
        sys.stdout = sys.__stdout__


def clear_console(output_widget):
    output_widget.delete("1.0", tk.END)

# AUTO INDENTATION(OTSTUP) FUNKSIYASI
def auto_indent(event, code_editor):
    """ikki nuqta bor qatordan keyin avtomatik 4 ta bo'shliq (:)"""
    # kursor joylashgan qatorning indeksini olish
    current_index = code_editor.index(tk.INSERT)
    line_number = int(current_index.split('.')[0])

    # Enter bosishdan oldin joriy qatorning matnini qabul qilamiz
    current_line_text = code_editor.get(f"{line_number}.0", f"{line_number}.end")

    # Joriy qatorning boshida bo'shliqlarni sanab chiqamiz
    leading_spaces = len(current_line_text) - len(current_line_text.lstrip(' '))
    indentation = " " * leading_spaces

    # Agar qator ikki nuqta bilan tugasa, Enter bosilgach otstup qo'shiladi
    if current_line_text.strip().endswith(':'):
        indentation += "    "

    # Kerakli otstupni joylashtirish
    code_editor.insert(tk.INSERT, "\n" + indentation)

    # Matn yangilangani uchun sintaksis yoritish
    highlight_syntax(None, code_editor)

    return "break"

def update_line_numbers(event, editor, number_bar):
    """Kod maydonidagi qatorlar soniga qarab chap paneldagi raqamlarni yangilaydi"""
    # Kod muharriridagi jami qatorlar sonini aniqlaymiz
    end_index = editor.index('end-1c')
    num_lines = int(end_index.split('.')[0])

    # Raqamlar yoziladigan panelni tahrirlash uchun ochamiz
    number_bar.config(state=tk.NORMAL)
    number_bar.delete('1.0', tk.END)

    # Raqamlarni ketma-ket yozib chiqamiz
    line_numbers_string = "\n".join(str(i) for i in range(1, num_lines + 1))
    number_bar.insert('1.0', line_numbers_string)

    # Panelni yana yopamiz
    number_bar.config(state=tk.DISABLED)

    # Skrollarni sinxronlashtiramiz
    number_bar.yview_moveto(editor.yview()[0])


# SINTAKSISNI RANG-BARANG YORITISH FUNKSIYASI
def highlight_syntax(event, code_editor):
    for tag in ["keyword", "storage", "function", "string", "number", "comment", "self"]:
        code_editor.tag_remove(tag, "1.0", tk.END)

    if is_dark_mode:
        code_editor.tag_config("keyword", foreground="#ff79c6", font=("Consolas", 12, "bold"))
        code_editor.tag_config("storage", foreground="#50fa7b", font=("Consolas", 12, "bold"))
        code_editor.tag_config("function", foreground="#8be9fd")
        code_editor.tag_config("string", foreground="#f1fa8c")
        code_editor.tag_config("number", foreground="#bd93f9")
        code_editor.tag_config("comment", foreground="#6272a4", font=("Consolas", 12, "italic"))
        code_editor.tag_config("self", foreground="#ffb86c", font=("Consolas", 12))
    else:
        code_editor.tag_config("keyword", foreground="#d73a49", font=("Consolas", 12, "bold"))
        code_editor.tag_config("storage", foreground="#005cc5", font=("Consolas", 12, "bold"))
        code_editor.tag_config("function", foreground="#6f42c1")
        code_editor.tag_config("string", foreground="#032f62")
        code_editor.tag_config("number", foreground="#e36209")
        code_editor.tag_config("comment", foreground="#6a737d", font=("Consolas", 12, "italic"))
        code_editor.tag_config("self", foreground="#e36209", font=("Consolas", 12))

    content = code_editor.get("1.0", tk.END)

    # 1. Avval faqat qo'shtirnoqlar va izohlarni bo'yaymiz (bular mustaqil qoidalar)
    base_rules = [
        ("string", r'"[^"\\]*(?:\\.[^"\\]*)*"'),
        ("comment", r"#.*")
    ]
    for tag_name, pattern in base_rules:
        for match in re.finditer(pattern, content):
            code_editor.tag_add(tag_name, f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

    # 2. Endi kalit so'zlar, funksiyalar va sonlarni bo'yaymiz.
    # DIQQAT: Biz pattern boshiga va oxiriga qo'shtirnoq ichida bo'lmaslik qoidasini qo'shdik!
    advanced_rules = [
        ("keyword", r"\b(agar|yo'qsa|toki|funksiya|qaytar|va|yoki|sinf|urin|xatoda|nihoyat)\b"),
        ("storage", r"\bo'zg\b"),
        ("function", r"\b(yoz|kirit|ildiz|daraja|butson|matn)\b"),
        ("number", r"\b\d+\b"),
        ("self", r"\bself\b")
    ]

    for tag_name, pattern in advanced_rules:
        for match in re.finditer(pattern, content):
            start_idx = match.start()
            end_idx = match.end()

            # Tekshiruv: Agar ushbu topilgan so'z ALLAQACHON "string" yoki "comment" tegi ichida bo'lsa, uni bo'yamaymiz
            # Tkinter'ning tag_names funksiyasi o'sha harfda qanday teglar borligini aytadi
            current_tags = code_editor.tag_names(f"1.0 + {start_idx} chars")
            if "string" in current_tags or "comment" in current_tags:
                continue

            code_editor.tag_add(tag_name, f"1.0 + {start_idx} chars", f"1.0 + {end_idx} chars")

    # Xavfsizlik uchun qatlamlarni ko'tarib qo'yamiz
    code_editor.tag_raise("string")
    code_editor.tag_raise("comment")

def load_template(template_name, code_editor):
    """Oynadan tanlangan variantni kod yozish maydoniga chiqarib beradi"""
    templates = {
        "salom": (
            "# 1. Oddiy ma'lumot saqlash\n"
            "o'zg x = 5\n"
            "yoz(x)\n\n"
            "# Agar matn chiqarmoqchi bo'lsangiz, x =  dan keyin qo'shtirnoqlar qo'yib, ichiga so'zni qo'shing."
        ),
        "muloqot": (
            "# 2. Interaktiv muloqot va shartlar\n"
            "o'zg yosh = kirit(\"Yoshingizni kiriting: \")\n"
            "o'zg yosh_soni = butson(yosh) # butun son degani\n\n"
            "agar yosh_soni >= 30:\n"
            "    yoz(\"Siz katta avlod vakilisiz. Hurmatdamiz!\")\n"
            "yo'qsa:\n"
            "    yoz(\"Siz yosh avlod vakilisiz. Hurmatdamiz!\")\n"
        ),
        "matematika": (
            "# 3. Murakkab matematika moduli\n"
            "# daraja(asos, ko'rsatkich) va ildiz(son)\n"
            "o'zg kvadrat = daraja(5, 2) # 5 ning kvadrati\n"
            "o'zg ildiz_son = ildiz(81)  # 81 ning ildizi\n\n"
            "yoz(\"5 ning kvadrati: \")\n"
            "yoz(kvadrat)\n"
            "yoz('\\n')\n"
            "yoz(\"81 ning kvadrat ildizi: \")\n"
            "yoz(ildiz_son)\n"
        ),
        "oop_and_try_exc": (
            "# 3. Sinf (Class) va Obyektlar bilan ishlash\n"
            "sinf Shaxs:\n"
            "    funksiya __init__(self, ism, yosh):\n"
            "        self.ism = ism\n"
            "        self.yosh = yosh\n\n"
            "    funksiya tanish(self):\n"
            "        qaytar \"Salom, mening ismim \" + self.ism + \". Yoshim \" + matn(self.yosh) + \"da.\"\n\n"
            "# Merosxo'rlik (Inheritance) mantiqi\n"
            "sinf Dasturchi(Shaxs):\n"
            "    funksiya __init__(self, ism, yosh, til):\n"
            "        Shaxs.__init__(self, ism, yosh)\n"
            "        self.til = til\n\n"
            "    funksiya malumot(self):\n"
            "        qaytar self.tanish() + \" Men \" + self.til + \" tilida kod yozaman.\"\n\n"
            "# Obyekt yaratish va xatoliklarni tekshirish\n"
            "urin:\n"
            "    o'zg odam = Dasturchi(\"Ali\", 20, \"IlmiTil\")\n"
            "    yoz(odam.malumot())\n"
            "xatoda:\n"
            "    yoz(\"Sinf bilan ishlashda xatolik yuz berdi!\")\n"
        ),

    }

    if template_name in templates:
        code_editor.delete("1.0", tk.END)
        code_editor.insert("1.0", templates[template_name])
        highlight_syntax(None, code_editor)

def save_file_as(code_editor, window):
    """Faylni har doim yangi nom va manzil so'rab saqlaydigan funksiya (Save As)"""
    global current_file_path

    file_path = filedialog.asksaveasfilename(
        defaultextension=".ilmt",
        filetypes=[("IlmiTil fayllari", "*.ilmt"), ("Barcha fayllar", "*.*")]
    )

    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(code_editor.get("1.0", tk.END).strip())

            # Global manzilni yangilaymiz va oyna sarlavhasiga fayl nomini chiqaramiz
            current_file_path = file_path
            file_name = file_path.split('/')[-1]
            window.title(f"IlmiTil Dasturlash Muhiti v1.2 - {file_name}")

            messagebox.showinfo("Muvaffaqiyat", "Fayl muvaffaqiyatli saqlandi!")
        except Exception as e:
            messagebox.showerror("Xatolik", f"Faylni saqlashda xatolik yuz berdi:\n{e}")


def save_file(code_editor, window):
    """Joriy fayl ustiga tezkor saqlash funksiyasi (Save)"""
    global current_file_path

    # Agar fayl avval saqlangan bo'lsa, to'g'ridan-to'g'ri ustiga yozadi
    if current_file_path:
        try:
            with open(current_file_path, "w", encoding="utf-8") as file:
                file.write(code_editor.get("1.0", tk.END).strip())
            messagebox.showinfo("Yaxshi", "O'zgarishlar saqlandi!")
        except Exception as e:
            messagebox.showerror("Xatolik", f"Faylni saqlashda xatolik yuz berdi:\n{e}")
    else:
        # Agar fayl mutlaqo yangi bo'lsa, Save As funksiyasini chaqirib yuboradi
        save_file_as(code_editor, window)


def open_file(code_editor, window, line_number_bar):
    """.ilmt faylini ochib kod muharririga yuklaydi"""
    global current_file_path

    file_path = filedialog.askopenfilename(
        filetypes=[("IlmiTil fayllari", "*.ilmt"), ("Barcha fayllar", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                code_content = file.read()
            code_editor.delete("1.0", tk.END)
            code_editor.insert("1.0", code_content)

            current_file_path = file_path
            file_name = file_path.split('/')[-1]
            window.title(f"IlmiTil Dasturlash Muhiti v1.2 - {file_name}")  # Sarlavha yangilanadi
            # Yuklangan fayl uchun sintaksisni yangilaymiz
            window.after(100, lambda: (
                highlight_syntax(None, code_editor),
                update_line_numbers(None, code_editor, line_number_bar)
            ))
        except Exception as e:
            messagebox.showerror("Xatolik", f"Faylni ochishda xatolik yuz berdi:\n{e}")

# EKRAN REJIMI FUNKSIYASI
def toggle_theme(window, help_panel, help_title, help_desc, main_area, code_label, code_editor, run_button,
                 output_label, theme_button, file_menu, examples_menu, menu_bar, button_frame, editor_frame,
                 line_number_bar):
    global is_dark_mode
    is_dark_mode = not is_dark_mode

    if is_dark_mode:
        window.configure(bg="#1e1e1e")
        help_panel.configure(bg="#2d2d2d", bd=1, relief=tk.SOLID)
        help_title.configure(bg="#2d2d2d", fg="#8ab4f8")
        help_desc.configure(bg="#2d2d2d", fg="#e8eaed")
        main_area.configure(bg="#1e1e1e")
        code_label.configure(bg="#1e1e1e", fg="#e8eaed")
        code_editor.configure(bg="#2d2d2d", fg="#ffffff", insertbackground="white")
        editor_frame.config(bg="#1e1e1e", bd=1, relief=tk.FLAT)
        line_number_bar.config(bg="#1e1e1e", fg="#858585", selectbackground="#44475a")
        output_label.configure(bg="#1e1e1e", fg="#e8eaed")
        theme_button.configure(text="☀️ Kunduzgi rejim", bg="#3c4043", fg="#ffffff")
        file_menu.configure(bg="#2d2d2d", fg="#ffffff", activebackground="#3c4043", activeforeground="#ffffff")
        examples_menu.configure(bg="#2d2d2d", fg="#ffffff")
        button_frame.configure(bg="#1e1e1e")
    else:
        window.configure(bg="#f0f2f5")
        help_panel.configure(bg="#ffffff", bd=1, relief=tk.SOLID)
        help_title.configure(bg="#ffffff", fg="#1a73e8")
        help_desc.configure(bg="#ffffff", fg="#3c4043")
        main_area.configure(bg="#f0f2f5")
        code_label.configure(bg="#f0f2f5", fg="#3c4043")
        code_editor.configure(bg="#ffffff", fg="#202124", insertbackground="black")
        editor_frame.config(bg="#f0f0f0", bd=1, relief=tk.SOLID)
        line_number_bar.config(bg="#f0f0f0", fg="#a0a0a0", selectbackground="#ececec")
        output_label.configure(bg="#f0f2f5", fg="#3c4043")
        theme_button.configure(text="🌙 Tungi rejim", bg="#ffffff", fg="#3c4043")
        file_menu.configure(bg="#ffffff", fg="#3c4043", activebackground="#e8eaed", activeforeground="#000000")
        examples_menu.configure(bg="#ffffff", fg="#000000")
        button_frame.configure(bg="#f0f2f5")

    highlight_syntax(None, code_editor)

# ASOSIY MUHARRIR OYNASINI SOZLASH FUNKSIYASI
def create_gui():
    window = tk.Tk()
    window.title("IlmiTil Dasturlash Muhiti v1.3")
    window.geometry("950x650")
    window.configure(bg="#f0f2f5")

    menu_bar = tk.Menu(window)
    file_menu = tk.Menu(menu_bar, tearoff=0)

    # Menyu punktlariga fayl saqlash tizimini bog'laymiz
    file_menu.add_command(label="Kodni ochish...", command=lambda: open_file(code_editor, window, line_number_bar))
    file_menu.add_command(label="Kodni saqlash (.ilmt)...", command=lambda: save_file(code_editor, window))
    file_menu.add_command(label="Yangi nom bilan saqlash...", command=lambda: save_file_as(code_editor, window))
    file_menu.add_separator()
    file_menu.add_command(label="Chiqish", command=window.quit)

    menu_bar.add_cascade(label="Fayl", menu=file_menu)

    examples_menu = tk.Menu(menu_bar, tearoff=0)
    examples_menu.add_command(label="1. Oddiy kod (O'zgaruvchiga Saqlash)", command=lambda: load_template("salom", code_editor))
    examples_menu.add_command(label="2. Muloqot kodi (Kiritish & Shartlar)", command=lambda: load_template("muloqot", code_editor))
    examples_menu.add_command(label="3. Matematika kodi (Daraja & Ildiz)", command=lambda: load_template("matematika", code_editor))
    examples_menu.add_command(label="4. OOP tamoyili kodi (Sinf qoliplari)", command=lambda: load_template("oop_and_try_exc", code_editor))
    menu_bar.add_cascade(label="Namunalar", menu=examples_menu)

    window.config(menu=menu_bar)

    help_panel = tk.Frame(window, bg="#ffffff", width=260, bd=1, relief=tk.SOLID)
    help_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    help_panel.pack_propagate(False)

    help_title = tk.Label(help_panel, text="IlmiTil Qo'llanmasi", font=("Arial", 14, "bold"), bg="#ffffff", fg="#1a73e8")
    help_title.pack(pady=10)

    help_text = (
        "Buyruqlarni to'g'ri yozish tartibi:\n\n"
        "• o'zg x = 5\n(O'zgaruvchi yaratish)\nMa'lumotlarni saqlovchi belgi\n\n"
        "• yoz(\"Matn\")\n(Ekran(Konsol)ga chiqarish)\n\n"
        "• agar x > 3:\n    yoz(\"Katta\")\n  yo'qsa:\n    yoz(\"Kichik\")\n(Shartli)\n\n"
        "• i = 1\n   toki i < 5:\n    yoz(i)\n     i+=1\n(toki shart yaroqli = ishlaydi)\n\n"
        "• funksiya hisobla(a, b):\n    qaytar a + b\n natija = hisobla(5, 3)\n yoz(natija)\n(Doimiy Funksiya e'lon qilish)\n\n"
        "• # Izoh yozish (Ta'sir qilmaydi)\n"
        "• daraja(5,2) -> 25.0\n(Sonni darajaga ko'tarish)\n"
        "• ildiz(16) -> 4.0\n(Kvadrat ildiz chiqarish)"
    )
    help_desc = tk.Label(help_panel, text=help_text, font=("Arial", 11), bg="#ffffff", fg="#3c4043", justify=tk.LEFT, anchor="nw")
    help_desc.pack(fill=tk.BOTH, expand=True, padx=10)

    theme_button = tk.Button(
        help_panel, text="🌙 Tungi rejim", font=("Arial", 10, "bold"), bg="#ffffff", fg="#3c4043", bd=1, relief=tk.SOLID,
        pady=5
    )
    theme_button.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    main_area = tk.Frame(window, bg="#f0f2f5")
    main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 1. Muharrir sarlavhasi
    code_label = tk.Label(main_area, text="Kod yozish maydoni", font=("Arial", 12, "bold"), bg="#f0f2f5", fg="#3c4043")
    code_label.pack(anchor="w", pady=(0, 5))

    editor_frame = tk.Frame(main_area, bd=1, relief=tk.SOLID)
    editor_frame.pack(fill=tk.BOTH, expand=False, pady=5)

    bar_bg = "#1e1e1e" if is_dark_mode else "#f0f0f0"
    bar_fg = "#858585" if is_dark_mode else "#a0a0a0"

    line_number_bar = tk.Text(
        editor_frame,
        width=4, # Endi 4 ta belgi sig'adigan darajada (9999 qatorgacha yetadi)
        height=18,
        padx=5,
        takefocus=0,
        border=0,
        background=bar_bg,
        foreground=bar_fg,
        font=("Consolas", 12),
        state=tk.DISABLED,
        wrap=tk.NONE
    )
    line_number_bar.pack(side=tk.LEFT, fill=tk.Y)

    # code_editor = scrolledtext.ScrolledText(font=("Consolas", 12), height=15, bg="#ffffff", fg="#202124", bd=0)
    # code_editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    code_editor = scrolledtext.ScrolledText(editor_frame, font=("Consolas", 12), height=18, bg="#ffffff", fg="#202124",
                                            bd=0, wrap=tk.NONE)
    code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    starter_code = "# Interaktiv dastur\no'zg ism = kirit('Ismingizni kiriting:')\nyoz('Assalomu aleykum, ' + ism + '! Virtual miyam sizni qabul qildi.')"
    code_editor.insert(tk.END, starter_code)

    # Eventlarning bog'lanishi
    code_editor.bind("<Return>", lambda event: auto_indent(event, code_editor))
    code_editor.bind("<KeyRelease>", lambda event: (
        highlight_syntax(event, code_editor),
        update_line_numbers(event, code_editor, line_number_bar)
    ))
    # code_editor siljiganda chap panelni ham birga majburiy aylantirish qoidasi
    code_editor.vbar.config(command=lambda *args: (
        code_editor.yview(*args),
        line_number_bar.yview_moveto(code_editor.yview()[0])
    ))

    # Sichqoncha va kursor harakatlanganda raqamlarni to'g'rilab turish
    code_editor.bind("<MouseWheel>", lambda event: update_line_numbers(event, code_editor, line_number_bar))
    code_editor.bind("<Button-1>", lambda event: update_line_numbers(event, code_editor, line_number_bar))
    # raqamlanish darhol ko'rinsin
    window.after(100, lambda: update_line_numbers(None, code_editor, line_number_bar))

    # 3. Boshqaruv tugmalar konteyneri
    button_frame = tk.Frame(main_area, bg="#f0f2f5")
    button_frame.pack(pady=10)

    run_button = tk.Button(
        button_frame,
        text="▶ Ishga tushirish",
        font=("Arial", 12, "bold"),
        bg="#1a73e8",
        fg="#ffffff",
        activebackground="#1557b0",
        activeforeground="#ffffff",
        bd=0,
        padx=20,
        pady=10,
        command=lambda: execute_uz_code(code_editor.get("1.0", tk.END), output_box)
    )
    run_button.pack(side=tk.LEFT, padx=10)

    clear_button = tk.Button(
        button_frame,
        text="🧹 Konsolni tozalash",
        font=("Arial", 11, "bold"),
        bg="#ffffff",
        fg="#3c4043",
        activebackground="#e8eaed",
        activeforeground="#3c4043",
        bd=1,
        relief=tk.SOLID,
        padx=15,
        pady=8,
        command=lambda: clear_console(output_box)
    )
    clear_button.pack(side=tk.LEFT, padx=5)

    theme_button.configure(command=lambda: toggle_theme(
        window, help_panel, help_title, help_desc, main_area, code_label, code_editor, run_button,
        output_label, theme_button, file_menu, examples_menu, menu_bar, button_frame, editor_frame, line_number_bar
    ))

    output_label = tk.Label(main_area, text="Natija (Konsol):", font=("Arial", 12, "bold"), bg="#f0f2f5", fg="#3c4043")
    output_label.pack(anchor="w", pady=5)

    output_box = scrolledtext.ScrolledText(main_area, font=("Consolas", 12), height=8, bg="#202124", fg="#00ff00", bd=0)
    output_box.pack(fill=tk.X, pady=5)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
