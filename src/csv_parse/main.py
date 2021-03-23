import csv


def csv_parse(path: str, fields: [], quantity):
    with open(path, 'r') as csv_data:
        csv_reader = csv.DictReader(csv_data)
        entities = []
        for row in csv_reader:
            entities.append(row)
            if len(entities) >= quantity:
                break

        filtered_entities = []
        for entity in entities:
            item = {}
            for field in fields:
                item[field] = entity[field]
            filtered_entities.append(item)

        return filtered_entities
