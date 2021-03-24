import json
import re

names, years = [], []

#Read the file and for each line extract all text as name up to last (
#and number inside last ( and ) will be the delcared as the year
with open("Films.txt", encoding='UTF8') as f:
    for line in f:
        if(name := re.search(r".*(?=\()",line)) is not None:
            names.append(name.group(0))
        if(year := re.search(r"\d{4}(?=\))",line)) is not None:
            years.append(year.group(0))

movies = [{"name": n, "year": y} for n, y  in zip(names, years)]

out_file = open("test1.json", "w")
json.dump(movies, out_file, indent = 4, sort_keys = False)
out_file.close()
