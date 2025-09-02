# knowledge_store.py
# Этот скрипт управляет базой знаний, работающей на Weaviate.
# Для его работы требуется установить клиент Weaviate:
# pip install weaviate-client

import weaviate
import json

class KnowledgeBase:
    """ Класс для взаимодействия с базой знаний Weaviate. """

    def __init__(self, weaviate_url="http://localhost:8080"):
        """ Инициализирует клиент и подключается к Weaviate. """
        try:
            self.client = weaviate.Client(weaviate_url)
            print("Успешное подключение к Weaviate!")
        except Exception as e:
            print(f"Ошибка подключения к Weaviate: {e}")
            self.client = None

    def ensure_schema_exists(self):
        """
        Проверяет, существует ли схема 'Knowledge', и создает ее при необходимости.
        Схема определяет, как будут храниться данные.
        """
        if not self.client:
            return

        class_obj = {
            "class": "Knowledge",
            "description": "A piece of knowledge about music, Ableton, or AI interaction.",
            "vectorizer": "text2vec-transformers",
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The main content of the knowledge.",
                },
                {
                    "name": "category",
                    "dataType": ["string"],
                    "description": "The category of the knowledge (e.g., 'Ableton', 'Music Theory', 'AI').",
                },
                {
                    "name": "source",
                    "dataType": ["string"],
                    "description": "Where the knowledge came from (e.g., a file name, a URL, or 'user').",
                }
            ]
        }

        # Проверяем, существует ли уже класс
        schema = self.client.schema.get()
        if not any(c['class'] == 'Knowledge' for c in schema['classes']):
            print("Схема 'Knowledge' не найдена. Создаю...")
            self.client.schema.create_class(class_obj)
            print("Схема успешно создана.")
        else:
            print("Схема 'Knowledge' уже существует.")

    def add_knowledge(self, content, category, source):
        """
        Добавляет новый фрагмент знаний в базу данных.
        Weaviate автоматически векторизует 'content' для семантического поиска.
        """
        if not self.client:
            return None

        knowledge_object = {
            "content": content,
            "category": category,
            "source": source
        }

        try:
            uuid = self.client.data_object.create(
                data_object=knowledge_object,
                class_name="Knowledge"
            )
            print(f"Знание успешно добавлено с UUID: {uuid}")
            return uuid
        except Exception as e:
            print(f"Ошибка при добавлении знания: {e}")
            return None

    def search_knowledge(self, query, limit=3):
        """
        Выполняет семантический поиск по базе знаний.
        Находит наиболее релевантные фрагменты, даже если они не содержат точных ключевых слов.
        """
        if not self.client:
            return []

        try:
            response = (
                self.client.query
                .get("Knowledge", ["content", "category", "source"])
                .with_near_text({"concepts": [query]})
                .with_limit(limit)
                .do()
            )
            return response['data']['Get']['Knowledge']
        except Exception as e:
            print(f"Ошибка при поиске: {e}")
            return []

# --- Пример использования ---
if __name__ == '__main__':
    # 1. Инициализация базы знаний
    kb = KnowledgeBase()

    if kb.client:
        # 2. Убедимся, что схема существует
        kb.ensure_schema_exists()

        # 3. Добавим пример знания (если его еще нет)
        # Это можно сделать, проверив, есть ли уже знания по этой теме
        search_result = kb.search_knowledge("Amen Break pattern")
        if not search_result:
            print("\nДобавляю информацию о паттерне Amen Break...")
            kb.add_knowledge(
                content="The Amen Break is a famous drum loop from the song 'Amen, Brother' by The Winstons. It is one of the most sampled breaks in music history, particularly in hip hop and drum and bass. The pattern is characterized by a syncopated kick and snare rhythm.",
                category="Music Production",
                source="User request"
            )

        # 4. Пример поиска
        print("\n--- Пример поиска ---")
        query = "how to make a syncopated drum beat"
        print(f"Ищу знания по запросу: '{query}'")
        results = kb.search_knowledge(query)

        if results:
            print("\nНайдено результатов:")
            for i, result in enumerate(results, 1):
                print(f"  {i}. Категория: {result['category']}")
                print(f"     Источник: {result['source']}")
                print(f"     Содержание: {result['content']}")
        else:
            print("Ничего не найдено.")
