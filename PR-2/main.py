import numpy as np

# Исходные данные

# Создаём структурированный массив для документов
document_dtype = np.dtype([
    ('type', 'U20'),
    ('number', 'U20'),
    ('name', 'U50')
])

documents = np.array([
    ('passport', '2207 876234', 'Василий Гупкин'),
    ('invoice', '11-2', 'Геннадий Покемонов'),
    ('insurance', '10006', 'Аристарх Павлов')
], dtype=document_dtype)

# Создаём словарь полок, где каждая полка содержит массив номеров документов
directories = {
    '1': np.array(['2207 876234', '11-2']),
    '2': np.array(['10006']),
    '3': np.array([], dtype='U20')
}


def get_owner_by_number(number):
    """Возвращает владельца документа по его номеру."""
    matches = documents[documents['number'] == number]
    if matches.size > 0:
        return matches['name'][0]
    return None


def get_shelf_by_number(number):
    """Возвращает номер полки, на которой хранится документ."""
    for shelf, docs in directories.items():
        if number in docs:
            return shelf
    return None


def list_all_documents():
    """Выводит информацию по всем документам."""
    for doc in documents:
        shelf = get_shelf_by_number(doc['number'])
        print(f"№: {doc['number']}, тип: {doc['type']}, владелец: {
              doc['name']}, полка хранения: {shelf}")


def add_shelf(shelf_number):
    """Добавляет новую полку, если её ещё нет."""
    if shelf_number in directories:
        print(f"Такая полка уже существует. Текущий перечень полок: {
              ', '.join(sorted(directories.keys()))}.")
    else:
        directories[shelf_number] = np.array([], dtype='U20')
        print(f"Полка добавлена. Текущий перечень полок: {
              ', '.join(sorted(directories.keys()))}.")


def delete_shelf(shelf_number):
    """Удаляет полку, если она пуста."""
    if shelf_number not in directories:
        print(f"Такой полки не существует. Текущий перечень полок: {
              ', '.join(sorted(directories.keys()))}.")
    elif directories[shelf_number].size > 0:
        print(f"На полке есть документы, удалите их перед удалением полки. Текущий перечень полок: {
              ', '.join(sorted(directories.keys()))}.")
    else:
        del directories[shelf_number]
        print(f"Полка удалена. Текущий перечень полок: {
              ', '.join(sorted(directories.keys()))}.")


def add_document(doc_number, doc_type, doc_owner, shelf_number):
    """Добавляет новый документ в базу и на указанную полку."""
    global documents
    if shelf_number not in directories:
        print("Такой полки не существует. Добавьте полку командой ads.")
        return
    # Проверка на уникальность номера документа
    if np.any(documents['number'] == doc_number):
        print("Документ с таким номером уже существует.")
        return
    # Создание нового документа
    new_doc = np.array([(doc_type, doc_number, doc_owner)],
                       dtype=document_dtype)
    documents = np.concatenate((documents, new_doc))
    # Добавление номера документа на полку
    directories[shelf_number] = np.append(
        directories[shelf_number], doc_number)
    print("Документ добавлен. Текущий список документов:")
    list_all_documents()


def delete_document(doc_number):
    """Удаляет документ из базы и с полки."""
    global documents
    index = np.where(documents['number'] == doc_number)[0]
    if index.size == 0:
        print("Документ не найден в базе.")
    else:
        # Удаление документа из массива
        documents = np.delete(documents, index)
        # Удаление номера документа с полки
        shelf = get_shelf_by_number(doc_number)
        if shelf:
            directories[shelf] = directories[shelf][directories[shelf] != doc_number]
        print("Документ удален.")
    print("Текущий список документов:")
    list_all_documents()


def move_document(doc_number, target_shelf):
    """Перемещает документ на другую полку."""
    global directories
    current_shelf = get_shelf_by_number(doc_number)
    if current_shelf is None:
        print("Документ не найден в базе.")
        return
    if target_shelf not in directories:
        print(f"Такой полки не существует. Текущий перечень полок: {
              ', '.join(sorted(directories.keys()))}.")
        return
    # Удаление документа с текущей полки
    directories[current_shelf] = directories[current_shelf][directories[current_shelf] != doc_number]
    # Добавление документа на целевую полку
    directories[target_shelf] = np.append(
        directories[target_shelf], doc_number)
    print("Документ перемещен.")
    print("Текущий список документов:")
    list_all_documents()


def main():
    """Основной цикл программы."""
    while True:
        command = input("Введите команду: ").strip().lower()
        if command == 'q':
            print("Программа завершена.")
            break
        elif command == 'p':
            number = input("Введите номер документа: ").strip()
            owner = get_owner_by_number(number)
            if owner:
                print(f"Владелец документа: {owner}")
            else:
                print("Документ не найден в базе.")
        elif command == 's':
            number = input("Введите номер документа: ").strip()
            shelf = get_shelf_by_number(number)
            if shelf:
                print(f"Документ хранится на полке: {shelf}")
            else:
                print("Документ не найден в базе.")
        elif command == 'l':
            print("Результат:")
            list_all_documents()
        elif command == 'ads':
            shelf_number = input("Введите номер полки: ").strip()
            add_shelf(shelf_number)
        elif command == 'ds':
            shelf_number = input("Введите номер полки: ").strip()
            delete_shelf(shelf_number)
        # Задание 2
        elif command == 'ad':
            doc_number = input("Введите номер документа: ").strip()
            doc_type = input("Введите тип документа: ").strip()
            doc_owner = input("Введите владельца документа: ").strip()
            shelf_number = input("Введите полку для хранения: ").strip()
            add_document(doc_number, doc_type, doc_owner, shelf_number)
        elif command == 'd':
            doc_number = input("Введите номер документа: ").strip()
            delete_document(doc_number)
        elif command == 'm':
            doc_number = input("Введите номер документа: ").strip()
            target_shelf = input("Введите номер полки: ").strip()
            move_document(doc_number, target_shelf)
        else:
            print("Неизвестная команда. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
