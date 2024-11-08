import streamlit as st
import time

# Чтение файла text.txt
def load_text():
    with open("text.txt", "r", encoding="utf-8") as file:
        return file.read()

# Алгоритм Кнута-Морриса-Пратта (KMP)
def kmp_search(text, pattern):
    positions = []
    n, m = len(text), len(pattern)
    lps = [0] * m
    j = 0

    # Создаем массив LPS
    def compute_lps():
        length = 0
        i = 1
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

    compute_lps()
    i = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return positions

# Алгоритм Бойера-Мура-Хорспула
def bmh_search(text, pattern):
    positions = []
    n, m = len(text), len(pattern)
    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j == -1:
            positions.append(i)
            i += m
        else:
            i += skip.get(text[i + m - 1], m)
    return positions

# Основной код приложения
st.title("Поиск подстроки в тексте")
st.write("Введите подстроку для поиска в файле `text.txt`:")

# Загрузка текста из файла
text = load_text()

# Ввод подстроки
pattern = st.text_input("Подстрока для поиска:")

# Выбор алгоритма поиска
algorithm = st.selectbox("Выберите алгоритм:", ["Кнута-Морриса-Пратта", "Бойера-Мура-Хорспула"])

# Выполнение поиска
if st.button("Найти"):
    start_time = time.time()
    if algorithm == "Кнута-Морриса-Пратта":
        positions = kmp_search(text, pattern)
    else:
        positions = bmh_search(text, pattern)
    end_time = time.time()

    # Вывод результатов
    st.write(f"Найдено вхождений: {len(positions)}")
    st.write("Позиции вхождений:", positions)
    st.write(f"Время выполнения: {end_time - start_time:.6f} секунд")
