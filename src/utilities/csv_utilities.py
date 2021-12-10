"""Service for reading from and writing to the items datafile"""
import re

def read_csv(fpath):
    """Reads from the datafile.

    Returns:
        A tuple of (item type: string, item fields: list)
    """
    with open(fpath, "r", encoding="latin1") as file:
        next(file)
        return [(
            item.split(";")[0], item.split(";")[1], re.findall("\'(.+?)\'", item)
            ) for item in file]

def write_csv(fpath, item_id, item_type, item_fields):
    """Writes to the datafile.

    Writes in two columns:
        item type: string, item fields: list
    """
    with open(fpath, "a") as file:
        file.write(f"{item_id};{item_type};{item_fields}\n")

def clear_csv(fpath):
    """Utility for clearing a csv file completely."""
    f = open(fpath, "w")
    f.write("type;fields\n")
    f.truncate()
    f.close()

def delete_csv(fpath, title):
    with open(fpath, "r") as f:
        lines = f.readlines()

    clear_csv(fpath)

    with open(fpath, "w") as f:
        for line in lines:
            if title not in line:
                f.write(line)
        f.truncate()
