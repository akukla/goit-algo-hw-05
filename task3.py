import timeit


def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

# Алгоритм Боєра-Мура
def boyer_moore(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

# Алгоритм Кнута-Морріса-Пратта
def knuth_morris_pratt(text, pattern):
    m = len(pattern)
    n = len(text)

    # Створюємо префіксну таблицю
    prefix_table = [0] * m
    j = 0

    # Обчислюємо префіксну таблицю
    for i in range(1, m):
        while j > 0 and pattern[j] != pattern[i]:
            j = prefix_table[j-1]
        if pattern[j] == pattern[i]:
            j += 1
        prefix_table[i] = j

    # Пошук шаблону в тексті
    j = 0
    for i in range(n):
        while j > 0 and pattern[j] != text[i]:
            j = prefix_table[j-1]
        if pattern[j] == text[i]:
            j += 1
        if j == m:  # Шаблон знайдено
            return i - m + 1
    return -1

# Алгоритм Рабіна-Карпа
def rabin_karp(text, pattern):
    m = len(pattern)
    n = len(text)
    pattern_hash = 0
    text_hash = 0
    p = 31  # просте число
    d = 256  # кількість символів в вхідному алфавіті
    h = pow(p, m-1) % d

    # Обчислюємо хеш для шаблону та першого вікна тексту
    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % d
        text_hash = (d * text_hash + ord(text[i])) % d

    # Переміщуємо вікно тексту
    for i in range(n - m + 1):
        if pattern_hash == text_hash:  # якщо хеші співпадають, перевіряємо символи
            for j in range(m):
                if text[i+j] != pattern[j]:
                    break
            else:  # Шаблон знайдено
                return i

        # Обчислюємо хеш для наступного вікна тексту
        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i+m])) % d

            # Ми можемо отримати від'ємний значення text_hash, але ми повинні його перетворити на позитивне
            if text_hash < 0:
                text_hash += d
    return -1

# Відкриття текстових файлів
with open('article1.txt', 'r') as file:
    text1 = file.read()

with open('article2.txt', 'r') as file:
    text2 = file.read()

def search(pattern, text, description=None):
    if description is not None:
        print(f'\n{description}: {pattern}')
    # Вимірювання часу виконання алгоритмів
    start = timeit.default_timer()
    boyer_moore(text1, 'pattern')
    end = timeit.default_timer()
    print('Boyer-Moore time: ', end - start)

    start = timeit.default_timer()
    knuth_morris_pratt(text1, 'pattern')
    end = timeit.default_timer()
    print('Knuth-Morris-Pratt time: ', end - start)

    start = timeit.default_timer()
    rabin_karp(text1, 'pattern')
    end = timeit.default_timer()
    print('Rabin-Karp time: ', end - start)

search("можна дробити так само на підзадачі", text1, "Text1, існуючий патерн")
search("іваіва мівакуц сіамо на піваіві", text1, "Text1, не існуючий патерн")
search("було побудовано графік, наведений на рисунку 2", text2, "Text2, існуючий патерн")
search("іваіва мівакуц сіамо на піваіві", text2, "Text2, не існуючий патерн")