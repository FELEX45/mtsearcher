class Searcher:
    def __init__(self, index):
        self.index = index

    def search(self, term):
        try:
            results = self.index.get(term, [])
            return results
        except Exception as e:
            print(f"Ошибка при поиске термина '{term}': {e}")
            return []
