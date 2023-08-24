from itertools import islice

import mwxml

if __name__ == "__main__":
    dump_file = "dump.xml"
    small_dump_file = "small_dump.xml"

    dump = mwxml.Dump.from_file(open(dump_file))

    # Extrahieren Sie die ersten 1000 Seiten aus dem Dump
    small_dump = list(islice(dump, 1000))

    # Speichern Sie den kleinen Dump in einer separaten Datei
    with open(small_dump_file, 'w', encoding='utf-8') as f:
        for page in small_dump:
            f.write(str(page))

    print(f"Small dump saved to {small_dump_file}")
