from typing import List, Union

def load_countries(filename: str, ignore: str):
    unavailable_countries = _load_unavailable_countries(ignore)
    countries = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line_list = line.split(",")
            code = line_list[0]
            country = line_list[1]
            if country not in unavailable_countries:
                countries.append((code, country))
    return countries

def _load_unavailable_countries(filename: str):
    unavailable_countries = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            unavailable_countries.append(line)
    return unavailable_countries

def check_is_valid_indexing(countries: Union[int, List[str]]):
    """ checks if the number of sampels provides sensible indexing """
    if isinstance(countries, int):
        if countries < 0:
            raise ValueError("Number of countries can't be negative")
        elif countries > 250:
            raise ValueError("Doesn't exist so many countries?")
        else:
            return True
    elif isinstance(countries, list):
        if len(countries) > 0:
            return True
        else:
            raise ValueError("No countries provided")
   
