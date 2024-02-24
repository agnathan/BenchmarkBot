import re

lemmas = {
    "Intel": {
        "hint_regexes": [
            re.compile(r"[Ii]ntel"),
            re.compile(r"[Cc]ore"),
            re.compile(r"i[357]"),
        ],
        "standard_entities": [
            "Intel Core i7-1370P",
            "Intel Core i7-13700H",
            "Intel Core Ultra 7 155H",
        ],
    },
    "AMD": {
        "hint_regexes": [
            re.compile(r"AMD", re.IGNORECASE),
            re.compile(r"Ryzen", re.IGNORECASE),
        ],
        "standard_entities": [
            "AMD Ryzen 7 6800U",
            "AMD Ryzen 7 7840S",
            "AMD Ryzen 7 7840U",
            "AMD Ryzen 9 PRO 7940HS",
        ],
    },
    "Benchmarks": {
        "hint_regexes": [
            re.compile(r"DaVinci", re.IGNORECASE),
            re.compile(r"Battery", re.IGNORECASE),
            re.compile(r"Procyon", re.IGNORECASE),
        ],
        "standard_entities": [
            "DaVinci Resolve 18",
            "UL Procyon AI (Integer)",
            "Battery Test",
        ],
    },
    "Products": {
        "hint_regexes": [
            re.compile(r"Zenbook", re.IGNORECASE),
            re.compile(r"Lenovo", re.IGNORECASE),
            re.compile(r"ASUS", re.IGNORECASE),
            re.compile(r"Acer", re.IGNORECASE),
        ],
        "standard_entities": [
            "ASUS Zenbook 13 S OLED",
            "Lenovo Slim 7i",
            "Lenovo Yoga Slim 7",
            "ASUS Zenbook 14X",
            "ASUS Zenbook 14",
            "Acer Swift Edge 16",
        ],
    },
}
