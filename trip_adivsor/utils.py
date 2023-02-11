import csv


def open_csv(path, fieldnames, mode='w', delimiter=','):
    csv_file = open(path, mode=mode, newline='', encoding='utf-8')
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=delimiter)
    return writer
