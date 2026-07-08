import sys
import re
import tkinter as tk
from tkinter import scrolledtext

# Tarjima dvijogimiz
UZ_TO_PY = {
    "yoz": "print",
    "agar ": "if ",
    "yo'qsa:": "else:",
    "toki ": "while ",
    "funksiya ": "def ",
    "qaytar ": "return ",
}

# Tungi rejimi bayrog'i
is_dark_mode = False


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
        global_env = {"print": sys.stdout.write, "int": int, "str": str}
        exec(final_python_script, global_env)

    except Exception as e:
        output_widget.insert(tk.END, f"\nXatolik yuz berdi:\n{e}")
    finally:
        sys.stdout = sys.__stdout__


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
        ("function", r"\b(yoz)\b"),
        ("number", r"\b\d+\b"),
        ("string", r'"[^"\\]*(?:\\.[^"\\]*)*"'),
        ("comment", r"#.*")
    ]

    for tag_name, pattern in rules:
        for match in re.finditer(pattern, content):
            start_pos = f"1.0 + {match.start()} chars"
            end_pos = f"1.0 + {match.end()} chars"
            code_editor.tag_add(tag_name, start_pos, end_pos)


# EKRAN REJIMI FUNKSIYASI
def toggle_theme(window, help_panel, help_title, help_desc, main_area, code_label, code_editor, run_button,
                 output_label, theme_button):
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

    highlight_syntax(None, code_editor)

# ASOSIY MUHARRIR OYNASINI SOZLASH FUNKSIYASI
def create_gui():
    window = tk.Tk()
    window.title("IlmiTil Dasturlash Muhiti v1.0")
    window.geometry("950x650")
    window.configure(bg="#f0f2f5")

    help_panel = tk.Frame(window, bg="#ffffff", width=260, bd=1, relief=tk.SOLID)
    help_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    help_panel.pack_propagate(False)

    help_title = tk.Label(help_panel, text="IlmiTil Qo'llanmasi", font=("Arial", 14, "bold"), bg="#ffffff",
                          fg="#1a73e8")
    help_title.pack(pady=10)

    help_text = (
        "Har bir buyruqni to'g'ri yozish tartibi:\n\n"
        "• o'zg x = 5\n(O'zgaruvchi yaratish)\nMa'lumotlarni saqlovchi belgi\n\n"
        "• yoz(\"Matn\")\n(Ekran(Konsol)ga chiqarish)\n\n"
        "• agar x > 3:\n    yoz(\"Katta\")\n  yo'qsa:\n    yoz(\"Kichik\")\n(Shartli)\n\n"
        "• i = 1\n   toki i < 5:\n    yoz(i)\n     i+=1\n(toki shart yaroqli = ishlaydi)\n\n"
        "• funksiya hisobla(a, b):\n    qaytar a + b\n natija = hisobla(5, 3)\n yoz(natija)\n(Doimiy Funksiya e'lon qilish)\n\n"
        "• # Izoh yozish (Ta'sir qilmaydi\noddiy zametka uchun)"
    )
    help_desc = tk.Label(help_panel, text=help_text, font=("Arial", 11), bg="#ffffff", fg="#3c4043", justify=tk.LEFT,
                         anchor="nw")
    help_desc.pack(fill=tk.BOTH, expand=True, padx=10)

    theme_button = tk.Button(
        help_panel, text="🌙 Tungi rejim", font=("Arial", 10, "bold"), bg="#ffffff", fg="#3c4043", bd=1, relief=tk.SOLID,
        pady=5
    )
    theme_button.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    main_area = tk.Frame(window, bg="#f0f2f5")
    main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    code_label = tk.Label(main_area, text="Kod yozish maydoni", font=("Arial", 12, "bold"), bg="#f0f2f5", fg="#3c4043")
    code_label.pack(anchor="w", pady=5)

    code_editor = scrolledtext.ScrolledText(main_area, font=("Consolas", 12), height=15, bg="#ffffff", fg="#202124",
                                            bd=1, relief=tk.SOLID)
    code_editor.pack(fill=tk.BOTH, expand=True, pady=5)

    starter_code = "# IlmiTil dasturidagi birinchi satrlaringiz!\n# Quyidagi vazifani yechish uchun Ishga Tushirish tugmasini bosing.\n\no'zg x = 10\n\nagar x > 5:\n    yoz(\"X beshdan katta!\") # Natijani chiqarish\nyo'qsa:\n    yoz(\"X kichik yoki teng!\")"
    code_editor.insert(tk.END, starter_code)

    # Avto-otstup hiylasi: Enter
    code_editor.bind("<Return>", lambda event: auto_indent(event, code_editor))

    # Qayta yoritish uchun harflarni oddiy yozish usulini ham bog'laymiz.
    code_editor.bind("<KeyRelease>", lambda event: highlight_syntax(event, code_editor))
    highlight_syntax(None, code_editor)

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
    run_button.pack()

    theme_button.configure(command=lambda: toggle_theme(
        window, help_panel, help_title, help_desc, main_area, code_label, code_editor, run_button, output_label,
        theme_button
    ))

    output_label = tk.Label(main_area, text="Natija (Konsol):", font=("Arial", 12, "bold"), bg="#f0f2f5", fg="#3c4043")
    output_label.pack(anchor="w", pady=5)

    output_box = scrolledtext.ScrolledText(main_area, font=("Consolas", 12), height=8, bg="#202124", fg="#00ff00", bd=0)
    output_box.pack(fill=tk.X, pady=5)

    window.mainloop()

# Oynani ishga tushirish
if __name__ == "__main__":
    create_gui()
