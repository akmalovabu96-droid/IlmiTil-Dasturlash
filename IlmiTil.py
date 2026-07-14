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
    "kirit": "kirit"
}

# Tungi rejimi bayrog'i
is_dark_mode = False
current_file_path = None

def custom_kirit(savol_matni="Ma'lumot kiriting:"):
    """Ma'lumotlarni kiritish oynasi kirit() buyrug'i uchun"""
    # Tkinter dialog oynasini chaqirish
    javob = simpledialog.askstring("IlmiTil - Kiritish maydoni", savol_matni)
    # Agar foydalanuvchi bekor qilsa, kod buzilmasligi uchun bo'sh string qaytaramiz
    return javob if javob is not None else ""

def execute_uz_code(uz_code_text, output_widget):
    """Oynadagi kodni olib, uni o'giradigan va bajaradigan funksiya"""
    output_widget.delete("1.0", tk.END)
    # Python’ning standart chiqishini (print) o'zgartiramiz, shunda u konsolga emas, balki bizning kod yozish oynamizga yozadi.
    class CustomOutput:
        def write(self, text):
            output_widget.insert(tk.END, text)

        def flush(self):
            pass

    sys.stdout = CustomOutput()

    try:
        uz_lines = uz_code_text.splitlines()
        py_code = []

        for line in uz_lines:
            translated_line = line
            if "o'zg " in translated_line:
                translated_line = translated_line.replace("o'zg ", "")
            for uz_word, py_word in UZ_TO_PY.items():
                if uz_word in translated_line:
                    translated_line = translated_line.replace(uz_word, py_word)
            py_code.append(translated_line)

        final_python_script = "\n".join(py_code)
        global_env = {
            "print": sys.stdout.write,
            "kirit": custom_kirit,  # kirit buyrug'ini oynaga bog'laymiz
            "butson": int,
            "matn": str,
            "ildiz": math.sqrt,
            "daraja": math.pow,
        }
        exec(final_python_script, global_env)

    except Exception as e:
        output_widget.insert(tk.END, f"\nXatolik yuz berdi:\n{e}")
    finally:
        sys.stdout = sys.__stdout__

def clear_console(output_widget):
    output_widget.delete("1.0", tk.END)

# AUTO INDENTATION(OTSTUP) FUNKSIYASI
def auto_indent(event, code_editor, line_label):
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


# SINTAKSISNI RANG-BARANG YORITISH FUNKSIYASI
def highlight_syntax(event, code_editor):
    for tag in ["keyword", "storage", "function", "string", "number", "comment"]:
        code_editor.tag_remove(tag, "1.0", tk.END)

    if is_dark_mode:
        code_editor.tag_config("keyword", foreground="#ff79c6", font=("Consolas", 12, "bold"))
        code_editor.tag_config("storage", foreground="#50fa7b", font=("Consolas", 12, "bold"))
        code_editor.tag_config("function", foreground="#8be9fd")
        code_editor.tag_config("string", foreground="#f1fa8c")
        code_editor.tag_config("number", foreground="#bd93f9")
        code_editor.tag_config("comment", foreground="#6272a4", font=("Consolas", 12, "italic"))
    else:
        code_editor.tag_config("keyword", foreground="#d73a49", font=("Consolas", 12, "bold"))
        code_editor.tag_config("storage", foreground="#005cc5", font=("Consolas", 12, "bold"))
        code_editor.tag_config("function", foreground="#6f42c1")
        code_editor.tag_config("string", foreground="#032f62")
        code_editor.tag_config("number", foreground="#e36209")
        code_editor.tag_config("comment", foreground="#6a737d",font=("Consolas", 12, "italic"))  # Спокойный серый курсив для светлой темы

    content = code_editor.get("1.0", tk.END)

    rules = [
        ("keyword", r"\b(agar|yo'qsa|toki|funksiya|qaytar)\b"),
        ("storage", r"\bo'zg\b"),
        ("function", r"\b(yoz|kirit||ildiz|daraja|butson|matn)\b"),
        ("number", r"\b\d+\b"),
        ("string", r'"[^"\\]*(?:\\.[^"\\]*)*"'),
        ("comment", r"#.*")
    ]

    for tag_name, pattern in rules:
        for match in re.finditer(pattern, content):
            start_pos = f"1.0 + {match.start()} chars"
            end_pos = f"1.0 + {match.end()} chars"
            code_editor.tag_add(tag_name, start_pos, end_pos)


def load_template(template_name, code_editor):
    """Oynadan tanlangan variantni kod yozish maydoniga chiqarib beradi"""
    templates = {
        "salom": (
            "# 1. Oddiy ma'lumot saqlash\n"
            "o'zg x = 5\n"
            "yoz(x)\n\n"
            "# Agar matn chiqarmoqchi bo'lsangiz, \"x = \" dan keyin qo'shtirnoqlar qo'yib, ichiga so'zni qo'shing."
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
            "yoz(\"81 ning kvadrat ildizi: \") # 81'dan oldin \\n yozib qo'ying. Bu ushbu qatorni keyingisiga o'tkazadi\n"
            "yoz(ildiz_son)\n"
        )
    }

    if template_name in templates:
        code_editor.delete("1.0", tk.END)
        code_editor.insert("1.0", templates[template_name])
        highlight_syntax(None, code_editor)


def save_file(code_editor):
    """Joriy kodni .ilmt fayliga saqlash uchun messagebox chaqiriladi"""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".ilmt",
        filetypes=[("IlmiTil fayllari", "*.ilmt"), ("Barcha fayllar", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(code_editor.get("1.0", tk.END).strip())
            messagebox.showinfo("Yaxshi", "Kod muvaffaqiyatli saqlandi! 🎉")
        except Exception as e:
            messagebox.showerror("Xatolik", f"Faylni saqlashda xatolik yuz berdi:\n{e}")


def open_file(code_editor):
    """.ilmt faylini ochib kod muharririga yuklaydi"""
    file_path = filedialog.askopenfilename(
        filetypes=[("IlmiTil fayllari", "*.ilmt"), ("Barcha fayllar", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                code_content = file.read()
            code_editor.delete("1.0", tk.END)
            code_editor.insert("1.0", code_content)

            # Yuklangan fayl uchun sintaksisni yangilaymiz
            highlight_syntax(None, code_editor)
        except Exception as e:
            messagebox.showerror("Xatolik", f"Faylni ochishda xatolik yuz berdi:\n{e}")

def save_file_as(code_editor, window):
    global current_file_path
    file_path = filedialog.asksaveasfilename(
        defaultextension=".ilmt",
        filetypes=[("IlmiTil fayllari", "*.ilmt"), ("Barcha fayllar", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(code_editor.get("1.0", tk.END).strip())
            current_file_path = file_path
            window.title(f"IlmiTil Dasturlash Muhiti v1.0 - {file_path.split('/')[-1]}")
            messagebox.showinfo("Muvaffaqiyat", "Fayl muvaffaqiyatli yaratildi va saqlandi!")
        except Exception as e:
            messagebox.showerror("Xatolik", f"Faylni saqlashda xatolik yuz berdi:\n{e}")

# EKRAN REJIMI FUNKSIYASI
def toggle_theme(window, help_panel, help_title, help_desc, main_area, code_label, code_editor, run_button,
                 output_label, theme_button, file_menu, examples_menu, menu_bar, button_frame):
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
        output_label.configure(bg="#f0f2f5", fg="#3c4043")
        theme_button.configure(text="🌙 Tungi rejim", bg="#ffffff", fg="#3c4043")
        file_menu.configure(bg="#ffffff", fg="#3c4043", activebackground="#e8eaed", activeforeground="#000000")
        examples_menu.configure(bg="#ffffff", fg="#000000")
        button_frame.configure(bg="#f0f2f5")

    highlight_syntax(None, code_editor)

# ASOSIY MUHARRIR OYNASINI SOZLASH FUNKSIYASI
def create_gui():
    window = tk.Tk()
    window.title("IlmiTil Dasturlash Muhiti v1.1")
    window.geometry("950x650")
    window.configure(bg="#f0f2f5")

    menu_bar = tk.Menu(window)
    file_menu = tk.Menu(menu_bar, tearoff=0)

    # Menyu punktlariga fayl saqlash tizimini bog'laymiz
    file_menu.add_command(label="Kodni ochish...", command=lambda: open_file(code_editor))
    file_menu.add_command(label="Kodni saqlash (.ilmt)...", command=lambda: save_file(code_editor))
    file_menu.add_command(label="Yangi nom bilan saqlash...", command=lambda: save_file_as(code_editor, window))
    file_menu.add_separator()
    file_menu.add_command(label="Chiqish", command=window.quit)

    menu_bar.add_cascade(label="Fayl", menu=file_menu)

    examples_menu = tk.Menu(menu_bar, tearoff=0)
    examples_menu.add_command(label="1. Oddiy kod (O'zgaruvchiga Saqlash)", command=lambda: load_template("salom", code_editor))
    examples_menu.add_command(label="2. Muloqot kodi (Kiritish & Shartlar)", command=lambda: load_template("muloqot", code_editor))
    examples_menu.add_command(label="3. Matematika kodi (Daraja & Ildiz)", command=lambda: load_template("matematika", code_editor))
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

    # 1. Заголовок редактора
    code_label = tk.Label(main_area, text="Kod yozish maydoni", font=("Arial", 12, "bold"), bg="#f0f2f5", fg="#3c4043")
    code_label.pack(anchor="w", pady=(0, 5))

    # code_editor = scrolledtext.ScrolledText(font=("Consolas", 12), height=15, bg="#ffffff", fg="#202124", bd=0)
    # code_editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    code_editor = scrolledtext.ScrolledText(main_area, font=("Consolas", 12), height=15, bg="#ffffff", fg="#202124",
                                            bd=1, relief=tk.SOLID)
    code_editor.pack(fill=tk.BOTH, expand=True, pady=5)

    starter_code = "# Interaktiv dastur\no'zg ism = kirit('Ismingizni kiriting:')\nyoz('Assalomu aleykum, ' + ism + '! Virtual miyam sizni qabul qildi.')"
    code_editor.insert(tk.END, starter_code)

    # Привязки событий
    code_editor.bind("<Return>", lambda event: auto_indent(event, code_editor))
    code_editor.bind("<KeyRelease>", lambda event: [highlight_syntax(event, code_editor)])
    highlight_syntax(None, code_editor)
    # 3. Контейнер для кнопок управления (кладем внутрь top_layout_frame, чтобы он не улетал вниз)
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
        output_label, theme_button, file_menu, examples_menu, menu_bar, button_frame
    ))

    output_label = tk.Label(main_area, text="Natija (Konsol):", font=("Arial", 12, "bold"), bg="#f0f2f5", fg="#3c4043")
    output_label.pack(anchor="w", pady=5)

    output_box = scrolledtext.ScrolledText(main_area, font=("Consolas", 12), height=8, bg="#202124", fg="#00ff00", bd=0)
    output_box.pack(fill=tk.X, pady=5)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
