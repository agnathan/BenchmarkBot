import re

regexes = {
    "Intel155h": {
        "hint_regexes": [re.compile(r"1[S5][S5]H", re.IGNORECASE)],
        "standard_entities": [
            "Intel Core i7-13705H",
            "Intel Core i7-1370P",
            "Intel Core i7-13700H",
            "Intel Core Ultra 7 155H",
        ],
    },
    "Macbook": {
        "hint_regexes": [
            # re.compile(r'[Mm]acBook\sPro\s\d{2}', re.IGNORECASE),
            re.compile(r"m[ao]cboo[lk]", re.IGNORECASE),
        ],
        "standard_entities": [
            "Apple M3 Max 40-Core GPU",
            "Apple M3 Pro 18-Core GPU",
            "Apple M3 Pro 14-Core GPU",
            "Apple MacBook Pro 14 2023 M3 Pro",
            "Apple MacBook Pro 16 2023 M3 Pro",
            "Apple MacBook Pro 16 2023 M3 Max",
            "Apple MacBook Pro 14 2023 M3",
            "Macbook Pro 14",
            "Macbook Pro 16",
        ],
    },
    "AppleM": {
        "hint_regexes": [re.compile(r"m[23]", re.IGNORECASE)],
        "standard_entities": [
            "Apple M2",
            "Apple M3",
            "Apple M3 Max 40-Core GPU",
            "Apple M3 Pro 11-Core",
            "Apple M3 Pro 12-Core",
            "Apple M3 Max 16-Core",
        ],
    },
    "Intel13700H": {
        "hint_regexes": [
            re.compile(r"[i1]7-13700HJ?", re.IGNORECASE),
        ],
        "standard_entities": [
            "Intel Core i7-13700H",
        ],
    },
    "Intel": {
        "hint_regexes": [
            re.compile(r"i[357]"),
            re.compile(r"I7-1365U", re.IGNORECASE),
            re.compile(r"[i1]7-1360P", re.IGNORECASE),
            re.compile(r"[i1]7-13700P", re.IGNORECASE),
        ],
        "standard_entities": [
            "Intel Core i5-13500H",
            "Intel Core i7-13705H",
            "Intel Core i7-1370P",
            "Intel Core i7-1360P",
            "Intel Core i7-1365U",
            "Intel Core Ultra 7 155H",
        ],
    },
    "Intel13700H": {
        "hint_regexes": [
            re.compile(r"[i1]7-13700HJ?", re.IGNORECASE),
        ],
        "standard_entities": [
            "Intel Core i7-13700H",
        ],
    },
    "IntelArc": {
        "hint_regexes": [
            re.compile(r"Intel\sArc", re.IGNORECASE),
        ],
        "standard_entities": [
            "Intel Arc",
        ],
    },
    "AMD78405": {
        "hint_regexes": [re.compile(r"7840[S5Uh]s?", re.IGNORECASE)],
        "standard_entities": [
            "AMD Ryzen 7 7840S",
            "AMD Ryzen 7 7840HS",
            "AMD Ryzen 7 7840U",
        ],
    },
    "AMD7730U": {
        "hint_regexes": [re.compile(r"7730u", re.IGNORECASE)],
        "standard_entities": [
            "AMD Ryzen 7 7730U",
        ],
    },
    "AMD6800U": {
        "hint_regexes": [re.compile(r"680Ou", re.IGNORECASE)],
        "standard_entities": [
            "AMD Ryzen 7 6800U",
        ],
    },
    "AMD": {
        "hint_regexes": [
            re.compile(r"AMD", re.IGNORECASE),
            re.compile(r"Ryzen", re.IGNORECASE),
            re.compile(r"r7-7840H[sS5]", re.IGNORECASE),
        ],
        "standard_entities": [
            "AMD Radeon",
            "AMD Ryzen 7 7840HS",
            "AMD Ryzen 7 6800U",
            "AMD Ryzen 7 7840S",
            "AMD Ryzen 7 7840U",
            "AMD Ryzen 7 7730U",
            "AMD Radeon 780MJ",
            "AMD Ryzen 9 PRO 7940HS",
        ],
    },
    "Benchmarks": {
        "hint_regexes": [
            re.compile(r"DaVinci", re.IGNORECASE),
            re.compile(r"Battery", re.IGNORECASE),
            re.compile(r"Procyon", re.IGNORECASE),
            re.compile(r"Cinebench\sr2[34]", re.IGNORECASE),
        ],
        "standard_entities": [
            "DaVinci Resolve 18",
            "UL Procyon AI (Integer)",
            "Battery Test",
            "Cinebench R23",
            "Cinebench R24",
        ],
    },
    "Lenovo": {
        "hint_regexes": [re.compile(r"Legion\sslim", re.IGNORECASE)],
        "standard_entities": ["Lenovo Legion Slim 5", "Lenovo Legion Slim 7"],
    },
    "ASUS": {
        "hint_regexes": [
            re.compile(r"Zenboo[kl]", re.IGNORECASE),
            re.compile(r"ASUS", re.IGNORECASE),
        ],
        "standard_entities": [
            "ASUS Zenbook 14",
            "ASUS Zenbook 13 S OLED",
            "Asus ZenBook 14 UX3405MA",
            "Asus Zenbook 14 OLED UM3402",
            "ASUS Zenbook 14X",
        ],
    },
    "Products": {
        "hint_regexes": [
            re.compile(r"Lenovo", re.IGNORECASE),
            re.compile(r"slim\s[7Z]", re.IGNORECASE),
            re.compile(r"pavilion", re.IGNORECASE),
            re.compile(r"Acer", re.IGNORECASE),
        ],
        "standard_entities": [
            "Pavilion Plus 14",
            "Lenovo Slim Pro 9",
            "Lenovo Yoga 9 14IRP G8",
            "Lenovo Thinkpad X1 Carbon",
            "Acer Swift Edge 16",
            "Acer Swift Go 14",
            "Acer Swift Go 14 SFG14-72",
            "Lenovo Yoga 9i",
            "Lenovo Yoga Slim 7",
            "Lenovo Slim 7i",
        ],
    },
}
