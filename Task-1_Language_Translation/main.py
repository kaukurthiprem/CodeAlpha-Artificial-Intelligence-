import tkinter as tk
from tkinter import ttk
import requests

# Language map: you can expand this
LANGUAGES = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Chinese": "zh"
}

# Create GUI window
root = tk.Tk()
root.title("🌐 Language Translator - Python 3.13 Compatible")
root.geometry("500x400")
root.config(bg="#f0f0f0")

tk.Label(root, text="Enter Text:", bg="#f0f0f0").pack()
input_text = tk.Text(root, height=6, width=50)
input_text.pack(pady=5)

src_lang = ttk.Combobox(root, values=list(LANGUAGES.keys()), width=20)
src_lang.set("English")
src_lang.pack(pady=5)

dest_lang = ttk.Combobox(root, values=list(LANGUAGES.keys()), width=20)
dest_lang.set("French")
dest_lang.pack(pady=5)

tk.Label(root, text="Translated Text:", bg="#f0f0f0").pack()
output_box = tk.Text(root, height=6, width=50, fg="blue")
output_box.pack(pady=5)

def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    from_lang = LANGUAGES.get(src_lang.get(), "en")
    to_lang = LANGUAGES.get(dest_lang.get(), "fr")
    
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={from_lang}|{to_lang}"
    try:
        response = requests.get(url)
        translated_text = response.json()['responseData']['translatedText']
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, translated_text)
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Error: {e}")

tk.Button(root, text="Translate", command=translate_text, bg="#4CAF50", fg="white").pack(pady=10)

root.mainloop()
