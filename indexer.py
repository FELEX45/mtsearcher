import os
import threading
from collections import defaultdict

class Indexer:
    def __init__(self, directory):
        self.directory = directory
        self.index = defaultdict(list)
        self.lock = threading.Lock()

    def index_file(self, filepath):
        try:
            with open(filepath, 'r', errors='ignore') as file:
                for line_num, line in enumerate(file):
                    words = line.strip().split()
                    with self.lock:
                        for word in words:
                            self.index[word].append((filepath, line_num))
        except Exception as e:
            print(f"Ошибка при обработке файла {filepath}: {e}")

    def create_index(self):
        threads = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                filepath = os.path.join(root, file)
                if os.path.isfile(filepath):
                    thread = threading.Thread(target=self.index_file, args=(filepath,))
                    threads.append(thread)
                    thread.start()
                else:
                    print(f"Пропускаем не файл {filepath}")

        for thread in threads:
            thread.join()

    def get_index(self):
        return dict(self.index)
