import os
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Предопределенные ключевые слова для категорий
category_keywords = {
    'политика': ['политика', 'правительство', 'президент', 'партия', 'выборы', 'парламент', 'депутат', 'закон'],
    'спорт': ['спорт', 'футбол', 'хоккей', 'баскетбол', 'олимпиада', 'чемпионат', 'матч', 'игрок', 'команда'],
    'игры': ['игра', 'видеоигра', 'консоль', 'геймплей', 'разработчик', 'платформа', 'жанр', 'релиз', 'игровой'],
    'технологии': ['технология', 'гаджет', 'смартфон', 'компьютер', 'программа', 'приложение', 'разработка', 'инновация'],
    'культура': ['культура', 'искусство', 'музыка', 'фильм', 'книга', 'выставка', 'концерт', 'фестиваль', 'творчество'],
    'бизнес': ['бизнес', 'компания', 'корпорация', 'стартап', 'инвестиции', 'прибыль', 'акции', 'рынок', 'экономика'],
    'наука': ['наука', 'исследование', 'открытие', 'эксперимент', 'теория', 'ученый', 'технология', 'инновация'],
    'здоровье': ['здоровье', 'медицина', 'болезнь', 'лечение', 'фитнес', 'диета', 'упражнения', 'здоровый образ жизни'],
    'путешествия': ['путешествие', 'туризм', 'отпуск', 'отель', 'курорт', 'достопримечательность', 'авиакомпания', 'направление']
}

# Функция для чтения заголовков из текстовых файлов
def read_headlines(directory):
    headlines = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                for line in f:
                    headline = line.strip()
                    headlines.append(headline)
    return headlines

# Функция для кластеризации заголовков
def cluster_headlines(headlines, n_clusters):
    vectorizer = TfidfVectorizer(stop_words=None)
    X = vectorizer.fit_transform(headlines)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)

    clusters = {}
    for i, label in enumerate(kmeans.labels_):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(headlines[i])

    return clusters, vectorizer.get_feature_names_out(), kmeans

# Функция для определения категорий
def get_categories(clusters, feature_names):
    categories = {}
    for label, cluster in clusters.items():
        word_counts = Counter()
        for headline in cluster:
            words = re.findall(r'\w+', headline.lower())
            word_counts.update(words)

        category_scores = {}
        for category, keywords in category_keywords.items():
            score = sum(word_counts[keyword] for keyword in keywords if keyword in feature_names)
            category_scores[category] = score

        category = max(category_scores, key=category_scores.get)
        categories[label] = category

    return categories

# Функция для визуализации кластеризации
def visualize_clustering(kmeans, headlines, vectorizer):
    plt.figure(figsize=(10, 8))
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=100, c='red', label='Centroids')
    plt.scatter(kmeans.transform(vectorizer.transform(headlines))[:, 0], kmeans.transform(vectorizer.transform(headlines))[:, 1], label='Headlines')
    plt.title('Clustering of Headlines')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.show()

# Пример использования
directory = '/Users/slavk/PycharmProject/Ultramed_practice_task/titles'
headlines = read_headlines(directory)
clusters, feature_names, kmeans = cluster_headlines(headlines, n_clusters=200)
categories = get_categories(clusters, feature_names)
vectorizer = TfidfVectorizer(stop_words=None)
vectorizer.fit_transform(headlines)

# Вывод результатов
for label, cluster in clusters.items():
    print(f"Категория {categories[label]}:")
    for headline in cluster:
        print(headline)
    print()

# Визуализация кластеризации
visualize_clustering(kmeans, headlines, vectorizer)
