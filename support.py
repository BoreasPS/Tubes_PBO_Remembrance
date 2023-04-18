from csv import reader

def import_csv_layout(path):
    with open(path) as level_map:
        list_layout = []
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            list_layout.append(list(row))
    return list_layout

