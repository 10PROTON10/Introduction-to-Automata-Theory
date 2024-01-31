import xml.etree.ElementTree as ET


def parse_tag(tag):
    parts = tag.split()
    tag_name = parts[0]

    attributes = {}
    for part in parts[1:]:
        if '=' in part:
            attr_name, attr_value = part.split('=')
            attributes[attr_name] = attr_value.strip('"\'')

    return tag_name, attributes


def parse_xml_string(xml_content):
    index = 0
    while index < len(xml_content):
        if xml_content[index] == '<':
            # Начало тега
            end_index = xml_content.find('>', index)
            if end_index != -1:
                tag = xml_content[index + 1:end_index]
                tag_name, attributes = parse_tag(tag)

                if tag.startswith("/"):
                    # Закрывающий тег
                    print(f"открывающий тег: <")
                    print(f"Имя закрывающего тега: {tag_name}")
                    print(f"закрывающий тег: >")
                else:
                    # Открывающий тег
                    print(f"открывающий тег: <")
                    print(f"Имя тега: {tag_name}")

                    # Вывод атрибутов
                    for attr_name, attr_value in attributes.items():
                        print(f"Имя атрибута: {attr_name}")
                        print(f"Значение атрибута: {attr_value}")

                    print(f"закрывающий тег: >")
                index = end_index + 1
            else:
                # Не удалось найти конец тега, выходим из цикла
                break
        elif xml_content[index].isspace():
            # Пропускаем пробелы и символы новой строки
            index += 1
        else:
            # Начало текста
            end_index = xml_content.find('<', index)
            if end_index != -1:
                text_content = xml_content[index:end_index].strip()
                if text_content:
                    print(f"Текст тега: {text_content}")
                index = end_index
            else:
                # Не удалось найти начало следующего тега, выходим из цикла
                break


if __name__ == "__main__":
    xml_file_path = 'Test.xml'

    # Чтение XML-файла
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Преобразование XML в строку
    xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

    # Разделение строки на отдельные строки
    xml_lines = xml_string.splitlines()

    # Создание словаря для хранения строк
    xml_dict = {}
    for i, line in enumerate(xml_lines, start=1):
        xml_dict[i] = line

    # Парсим каждую строку из словаря
    for i in xml_dict:
        print(f"-------- Обработка строки {i} --------")
        parse_xml_string(xml_dict[i])





