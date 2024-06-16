import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from indexer import Indexer
from search import Searcher

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Многопоточная обработка файлов: Индексирование и Поиск")
        self.geometry("600x400")

        self.directory = ""
        self.indexer = None
        self.searcher = None

        self.create_widgets()

    def create_widgets(self):
        self.dir_label = ttk.Label(self, text="Выберите директорию для индексирования:")
        self.dir_label.pack(pady=10)

        self.dir_button = ttk.Button(self, text="Выбрать директорию", command=self.choose_directory)
        self.dir_button.pack(pady=10)

        self.index_button = ttk.Button(self, text="Создать индекс", command=self.create_index)
        self.index_button.pack(pady=10)
        self.index_button["state"] = "disabled"

        self.search_label = ttk.Label(self, text="Введите термин для поиска:")
        self.search_label.pack(pady=10)

        self.search_entry = ttk.Entry(self)
        self.search_entry.pack(pady=10)

        self.search_button = ttk.Button(self, text="Поиск", command=self.search)
        self.search_button.pack(pady=10)
        self.search_button["state"] = "disabled"

        self.results_text = tk.Text(self, wrap="word", height=10, width=50)
        self.results_text.pack(pady=10)

    def choose_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.index_button["state"] = "normal"
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Выбрана директория: {self.directory}\n")

    def create_index(self):
        if not self.directory:
            messagebox.showerror("Ошибка", "Не выбрана директория для индексирования.")
            return

        self.indexer = Indexer(self.directory)
        try:
            self.indexer.create_index()
            self.searcher = Searcher(self.indexer.get_index())
            self.search_button["state"] = "normal"
            self.results_text.insert(tk.END, "Индексирование завершено.\n")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании индекса: {e}")

    def search(self):
        term = self.search_entry.get()
        if not term:
            messagebox.showerror("Ошибка", "Введите термин для поиска.")
            return

        if self.searcher:
            results = self.searcher.search(term)
            self.results_text.delete(1.0, tk.END)
            if results:
                for result in results:
                    self.results_text.insert(tk.END, f"Найдено в {result[0]} на строке {result[1]}\n")
            else:
                self.results_text.insert(tk.END, "Результатов не найдено.\n")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
