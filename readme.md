# MyDiff

Этот проект представляет собой инструмент командной строки для сравнения журналов сборки C/C++ проектов. Инструмент сравнивает два файла построчно, с игнорированием временных меток, путей и версии файлов. Он выводит различия между файлами в удобочитаемом формате, повторяющем стиль вывода утилиты diff, что полезно для анализа изменений между версиями файлов, в процессе сборки.

## Начало работы

Эти инструкции помогут вам настроить и запустить проект. Следуйте приведенным ниже шагам, чтобы начать.

### Требования

Для запуска проекта на вашей локальной машине необходимо установить Python. Также нужно установить все зависимости с помощью pip.


### Установка

Чтобы начать работу с проектом, выполните следующие шаги:

1. Клонируйте репозиторий:
```
git clone https://github.com/*** cd mydiff
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
3. Для запуска скрипта используйте команду:
```
python3 mydiff.py <путь_к_файлу1> <путь_к_файлу2>
```



## Функции:

* Сравнение двух текстовых файлов.
* Игнорирование временных меток, путей и версий файлов.
* Вывод различий между файлами, включая добавленные, удаленные и измененные строки.
* Возможность работы с различными версиями файлов.


## Описание методов

### `diff(file1_path, file2_path)`

**Описание:** Метод сравнивает два файла, выводя различия между ними. Он нормализует файлы, игнорируя временные метки и пути, а затем использует матрицу LCS для выявления различий.

**Параметры:**
* file1_path (str): Путь к первому файлу.
* file2_path (str): Путь ко второму файлу.

**Пример использования:**
```python
diff('path/to/file1.log', 'path/to/file2.log')
```


### `calc_lcs_matr(file1, file2)`

**Описание:** Метод вычисляет матрицу для нахождения наибольшей общей подстроки (LCS) двух списков строк.

**Параметры:**
* file1 (list): Первый список строк (например, строки из первого файла).
* file2 (list): Второй список строк (например, строки из второго файла).

**Возвращает:** Двухмерный список (матрицу), где каждый элемент представляет собой длину наибольшей общей подстроки для соответствующих строк из file1 и file2.

**Пример использования:**
```python
lcs_matrix = calc_lcs_matr(normalized_file1, normalized_file2)
```


### `find_chunks_by_matr(file1, file2, matr)`

**Описание:** Метод находит и выводит фрагменты различий между двумя файлами, используя матрицу LCS для вычисления местоположений различий.

**Параметры:**
* file1 (list): Содержимое первого файла.
* file2 (list): Содержимое второго файла.
* matr (list): Матрица LCS, вычисленная с помощью функции calc_lcs_matr.

**Возвращает:** `True`, если различий между файлами нет (с учетом нормализации). `False`, если различия были найдены.

**Пример использования**:
```python
no_diff = find_chunks_by_matr(file1_content, file2_content, lcs_matrix)
```


### `print_chunk(i, j, d, a, file1, file2)`

**Описание:** Метод выводит фрагмент различий между двумя файлами (добавленные или удаленные строки).

**Параметры:**
* i (int): Индекс начала фрагмента в file1.
* j (int): Индекс начала фрагмента в file2.
* d (int): Количество удаленных строк.
* a (int): Количество добавленных строк.
* file1 (list): Содержимое первого файла.
* file2 (list): Содержимое второго файла.

**Пример использования:**
```python
print_chunk(2, 2, 1, 3, file1_content, file2_content)
```


### `print_in_red(line)`

**Описание:** Метод выводит строку в красном цвете в консоль.

**Параметры:** line (str): Строка для вывода в красном цвете.

**Пример использования**:
```python
print_in_red('This is a red line.')
```


### `print_in_green(line)`

**Описание:** Метод выводит строку в зеленом цвете в консоль.

**Параметры:** line (str): Строка для вывода в зеленом цвете.

**Пример использования:**
```python
print_in_green('This is a green line.')
```


### `parse_arguments()`

**Описание:** Метод для парсинга аргументов командной строки. Он ожидает два обязательных аргумента — пути к файлам, которые нужно сравнить.

**Возвращает:** Кортеж, содержащий два элемента — пути к файлам, которые нужно сравнить.

**Пример использования:**
```python
file1_path, file2_path = parse_arguments()
```


### `read_file(path)`

**Описание:** Метод открывает файл по заданному пути, читает его содержимое и нормализует данные (удаляет временные метки и пути). Возвращает исходное и нормализованное содержимое файла в виде списков строк.

**Параметры:** path (str): Путь к файлу, который нужно открыть.

**Возвращает:** Кортеж из двух элементов:
* Содержимое файла в виде списка строк.
* Нормализованное содержимое файла в виде списка строк.

**Пример использования:**
```python
content, normalized_content = read_file('path/to/log1.txt')
```


### `get_name_ver(path)`

**Описание:** Метод извлекает имя и версию файла из его пути.

**Параметры:** path (str): Путь к файлу, из которого нужно извлечь имя и версию.

**Возвращает:** Кортеж из двух элементов:
* name (str): Имя файла (без версии и расширения).
* version (str): Версия файла (или пустая строка, если версия не указана).

**Пример использования:**
```python
name, version = get_name_ver('path/to/file.1.2.txt')
```


### `normalize(content, name, version)`

**Описание:** Метод нормализует список строк, удаляя временные метки, пути и имя с версией. Этот метод используется для предварительной обработки содержимого файлов.

**Параметры:**
* content (list): Список строк, которые необходимо нормализовать.
* name (str): Имя файла, которое нужно удалить.
* version (str): Версия файла, которую нужно удалить.

**Возвращает:** Нормализованный список строк, где удалены временные метки, пути и имя с версией.

**Пример использования:**
```python
normalized_content = normalize(file_content, 'file', '1.2')
```


### `remove_name_ver(line, name, version)`

**Описание:** Метод удаляет имя файла и его версию из строки текста.

**Параметры:**
* line (str): Строка, из которой нужно удалить имя и версию.
* name (str): Имя файла, которое нужно удалить.
* version (str): Версия файла, которую нужно удалить.

**Возвращает:** Обработанную строку без имени и версии файла.

**Пример использования:**
```python
cleaned_line = remove_name_ver('path/to/file_v1.2.txt', 'file', '1.2')
```



## Создано с использованием

* [Python](https://www.python.org/) - Язык программирования, используемый в проекте.
* [colorama](https://pypi.org/project/colorama/) - Библиотека для цветного вывода в консоль.

## Авторы
* Вороненко Иван - [GitHub](https://github.com/Helsing02)
