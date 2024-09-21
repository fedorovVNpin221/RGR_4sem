import os
import pandas as pd
from sklearn.decomposition import NMF

# Функция для чтения данных из файлов
def read_data(directory):
    data = []
    stock_names = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path, header=None, names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'])
            data.append(df)
            stock_names.append(os.path.splitext(filename)[0])
    return data, stock_names

# Функция для извлечения признаков с помощью NMF
def extract_features(data, n_components):
    # Объединение данных в один DataFrame
    combined_data = pd.concat(data, ignore_index=True)

    # Создание матрицы данных для NMF
    X = combined_data[['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']].values

    # Применение NMF
    nmf = NMF(n_components=n_components, random_state=42)
    W = nmf.fit_transform(X)
    H = nmf.components_

    # Определение релевантности признаков для каждой акции
    feature_relevance = {}
    for i in range(len(data)):
        start = sum(len(d) for d in data[:i])
        end = start + len(data[i])
        stock_name = os.path.splitext(os.path.basename(data[i].iloc[0]['Date']))[0]
        feature_relevance[stock_name] = W[start:end].sum(axis=0)

    # Определение дней, когда признаки проявлялись наиболее отчетливо
    feature_days = {}
    for i in range(n_components):
        feature_days[i] = sorted([(value, combined_data.iloc[index]['Date']) for index, value in enumerate(H[:, i])], reverse=True)[:3]

    return feature_relevance, feature_days

# Пример использования
directory = '/Users/slavk/PycharmProject/Ultramed_practice_task/stock'
data, stock_names = read_data(directory)
n_components = 5
feature_relevance, feature_days = extract_features(data, n_components)

# Вывод результатов
for i in range(n_components):
    print(f"Признак {i}:")
    sorted_relevance = sorted(feature_relevance.items(), key=lambda x: x[1][i], reverse=True)
    for stock_name, relevance in sorted_relevance:
        print(f"   ({relevance[i]}, '{stock_name}') - {stock_names[list(feature_relevance.keys()).index(stock_name)]}.txt")
    print("   Дни, когда признак проявлялся наиболее отчетливо:")
    for value, date in feature_days[i]:
        print(f"   ({value}, '{date}')")
    print()
