import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

# Получим список файлов в директории с заголовками новостей
directory = '/Users/slavk/PycharmProject/Ultramed_practice_task/titles'
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Прочитаем заголовки новостей из файлов
headlines = []
for file in files:
    with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
        headlines.extend(f.read().splitlines())

# Определим параметры для Grid Search
parameters = {
    'min_df': [1, 3, 5],
    'max_df': [0.7, 0.8, 0.9]
}

# Выполним векторизацию заголовков с помощью Grid Search
vectorizer = TfidfVectorizer(stop_words='russian')
grid_search = GridSearchCV(vectorizer, parameters)
grid_search.fit(headlines)
X = grid_search.best_estimator_.transform(headlines)

# Снизим размерность до 2D для визуализации
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X.toarray())

# Выполним кластеризацию с Agglomerative Clustering
clustering = AgglomerativeClustering(n_clusters=10, linkage='ward')
clusters = clustering.fit_predict(X.toarray())

# Выведем категории заголовков
category_names = {
    0: 'Политика',
    1: 'Экономика',
    2: 'Спорт',
    3: 'Наука',
    4: 'Культура',
    5: 'Медицина',
    6: 'Криминал',
    7: 'Компьютерные игры',
    8: 'Эротика',
    9: 'Автомобили'
}

for i, category in enumerate(clusters):
    print(f'Headline: {headlines[i]} - Category: {category_names[category]}')

# Нарисуем график для визуализации кластеров
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', s=50, alpha=0.5)
plt.title('Кластеризация заголовков новостей')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar()
plt.show()


