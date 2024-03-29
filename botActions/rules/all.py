benchmarkRules = [
    [{"lower": "blender"}],
    [{"lower": "pubg"}],
    [{"lower": "pugetbench"}, {"lower": "photoshop"}],
    [{"lower": "photoshop"}],
    [{"lower": "common"}, {"lower": "performance"}, {"lower": "tasks"}],
    [{"lower": "max"}, {"lower": "cpu"}, {"lower": "performance"}],
    [{"lower": "single"}, {"lower": "core"}],
    [{"lower": "single"}, {"IS_PUNCT": True}, {"lower": "core"}],
    [{"lower": "3dmark"}],
    [{"lower": "multi"}],
    [{"lower": "cpu"}, {"lower": "performance"}],
    [{"lower": "gfxbench"}],
    [{"lower": "battery"}, {"lower": "remaining"}],
    [{"lower": "opencl"}, {"lower": "score"}],
    [{"lower": "power"}, {"lower": "consumption"}],
    [
        {"lower": "cinebench"},
        {"lower": "r2o"},
        {"lower": "cpu"},
        {"lower": "multi"},
        {"IS_PUNCT": True},
        {"lower": "thread"},
    ],
    [
        {"lower": "battery"},
        {"lower": "life"},
        {"lower": "4"},
        {"lower": "k"},
        {"lower": "video"},
        {"lower": "test"},
    ],
    [{"lower": "gpu"}, {"lower": "opencl"}],
    [
        {"lower": "3840x2160"},
        {"lower": "4"},
        {"lower": "k"},
        {"lower": "aztec"},
        {"lower": "ruins"},
        {"lower": "high"},
        {"lower": "tier"},
        {"lower": "offscreen"},
    ],
    [{"lower": "power"}, {"lower": "draw"}],
    [
        {"lower": "2560x1440"},
        {"lower": "time"},
        {"lower": "spy"},
        {"lower": "graphics"},
    ],
    [
        {"lower": "wild"},
        {"lower": "life"},
        {"lower": "extreme"},
        {"lower": "unlimited"},
    ],
    [{"lower": "sustained"}, {"lower": "performance"}],
    [{"lower": "performance"}, {"lower": "per"}, {"lower": "watt"}],
    [{"lower": "cpu"}, {"lower": "temperature"}],
    [
        {"lower": "2560x1440"},
        {"lower": "aztec"},
        {"lower": "ruins"},
        {"lower": "high"},
        {"lower": "tier"},
        {"lower": "offscreen"},
    ],
    [
        {"lower": "1920x1080"},
        {"lower": "aztec"},
        {"lower": "ruins"},
        {"lower": "normal"},
        {"lower": "tier"},
        {"lower": "offscreen"},
    ],
    [{"lower": "gimp"}, {"lower": "photo"}],
    [{"lower": "handbrake"}, {"lower": "0.9.9"}, {"lower": "encode"}],
    [{"lower": "heat"}, {"lower": "you"}, {"lower": "feel"}],
    [
        {"lower": "gta"},
        {"lower": "v"},
        {"IS_PUNCT": True},
        {"lower": "1920x1080"},
        {"lower": "highest"},
        {"lower": "settings"},
        {"lower": "possible"},
        {"lower": "aa:4xmsaa"},
        {"lower": "+"},
        {"lower": "fx"},
        {"lower": "af:16x"},
    ],
    [{"lower": "geekbench"}, {"lower": "6"}],
    [{"lower": "timespy"}, {"lower": "graphics"}, {"lower": "score"}],
    [
        {"lower": "the"},
        {"lower": "witcher"},
        {"lower": "3"},
        {"IS_PUNCT": True},
        {"lower": "1920x1080"},
        {"lower": "ultra"},
        {"lower": "graphics"},
        {"IS_PUNCT": True},
        {"lower": "postprocessing"},
        {"IS_PUNCT": True},
        {"lower": "hbao+"},
        {"IS_PUNCT": True},
    ],
    [{"lower": "fan"}, {"lower": "noise"}],
    [{"lower": "pcmark"}, {"lower": "10"}],
    [{"lower": "3dmark"}, {"lower": "time"}, {"lower": "spy"}],
    [{"lower": "adobe"}, {"lower": "lightroom"}],
    [{"lower": "adobe"}, {"lower": "premiere"}, {"lower": "pro"}],
    [{"lower": "microsoft"}, {"lower": "word"}],
    [{"lower": "counter"}, {"lower": "strike"}, {"lower": "2"}],
    [{"lower": "microsoft"}, {"lower": "excel"}],
    [{"lower": "microsoft"}, {"lower": "powerpoint"}],
    [{"lower": "mozilla"}, {"lower": "firefox"}, {"lower": "compile"}],
    [
        {"lower": "spider"},
        {"lower": "man"},
        {"IS_PUNCT": True},
        {"lower": "miles"},
        {"lower": "morales"},
    ],
    [{"lower": "cinebench"}, {"lower": "r23"}],
    [{"lower": "cinebench"}, {"lower": "r24"}],
    [
        {"lower": "cinebench"},
        {"lower": "r23"},
        {"IS_PUNCT": True},
        {"lower": "single"},
        {"lower": "core"},
    ],
    [
        {"lower": "cinebench"},
        {"lower": "r23"},
        {"IS_PUNCT": True},
        {"lower": "multi"},
        {"lower": "core"},
    ],
    [{"lower": "cinebench"}, {"lower": "2024"}],
    [{"lower": "geekbench"}, {"lower": "5.5"}],
    [{"lower": "geekbench"}, {"lower": "6.2"}],
    [
        {"lower": "1920x1080"},
        {"lower": "fire"},
        {"lower": "strike"},
        {"lower": "graphics"},
    ],
    [
        {"lower": "geekbench"},
        {"TEXT": {"REGEX": "\d+\.?\d*"}},
        {"IS_PUNCT": True},
        {"lower": "single"},
        {"IS_PUNCT": True},
        {"lower": "core"},
    ],
    [
        {"lower": "power"},
        {"lower": "consumption"},
        {"IS_PUNCT": True},
        {"lower": "cinebench"},
        {"lower": "r23"},
        {"lower": "single"},
        {"lower": "power"},
        {"lower": "efficiency"},
    ],
    [
        {"lower": "power"},
        {"lower": "consumption"},
        {"IS_PUNCT": True},
        {"lower": "cinebench"},
        {"lower": "r23"},
        {"lower": "single"},
    ],
    [{"lower": "davinci"}, {"lower": "resolve"}, {"lower": "18"}],
    [{"lower": "handbrake"}, {"lower": "video"}, {"lower": "conversion"}],
    [
        {"lower": "battery"},
        {"lower": "test"},
        {"lower": "chrome"},
        {"lower": "refresh"},
    ],
    [{"lower": "battery"}, {"lower": "test"}],
    [
        {"lower": "shadow"},
        {"lower": "of"},
        {"lower": "the"},
        {"lower": "tomb"},
        {"lower": "raider"},
    ],
    [
        {"lower": "chrome"},
        {"lower": "refresh"},
        {"lower": "for"},
        {"lower": "15"},
        {"lower": "sec"},
        {"IS_PUNCT": True},
        {"lower": "screen"},
        {"lower": "set"},
        {"lower": "to"},
        {"lower": "150"},
        {"lower": "nits"},
    ],
    [
        {"lower": "2"},
        {"lower": "gb"},
        {"lower": "4k.mp4"},
        {"lower": "converted"},
        {"lower": "to"},
        {"lower": "1o80p"},
        {"lower": "mkv"},
        {"IS_PUNCT": True},
        {"lower": "cpu"},
        {"lower": "only"},
        {"IS_PUNCT": True},
    ],
    [
        {"lower": "10"},
        {"lower": "min"},
        {"lower": "clog"},
        {"lower": "to"},
        {"lower": "4kh.265"},
        {"lower": "export"},
    ],
]

cpuRules = [
    [{"lower": "78405"}],
    [{"lower": "7730u"}],
    [{"lower": "7840S"}],
    [{"lower": "680ou"}],
    [{"lower": "7840u"}],
    [{"lower": "7730u"}, {"IS_PUNCT": True}],
    [{"lower": "7840hs"}],
    [{"lower": "155h"}],
    [{"lower": "m3"}],
    [{"lower": "ryzen"}, {"lower": "7"}, {"lower": "7840s"}],
    [
        {"lower": "intel"},
        {"lower": "core"},
        {"lower": "i7"},
        {"IS_PUNCT": True},
        {"lower": "1360p|"},
    ],
    [{"TEXT": {"REGEX": "^[iI1]7$"}}, {"IS_PUNCT": True}, {"lower": "1360p"}],
    [{"lower": "i7"}, {"IS_PUNCT": True}, {"TEXT": {"REGEX": "13700[Hh][Jj]?"}}],
    [{"lower": "i7"}, {"IS_PUNCT": True}, {"lower": "1365u"}],
    [{"lower": "i7"}, {"IS_PUNCT": True}, {"lower": "1365u."}],
    # [{"TEXT":{"REGEX":"[1i]7"}}, {'IS_PUNCT': True}, {"TEXT":{"REGEX":"\d+[a-z]"}}],
    [{"lower": "ryzen"}, {"lower": "7"}, {"lower": "6800u"}],
    [{"lower": "ryzen"}, {"lower": "7"}, {"lower": "7840u"}],
    [{"lower": "ryzen"}, {"lower": "7"}, {"lower": "7730u"}],
    [{"lower": "r7"}, {"IS_PUNCT": True}, {"lower": "7840hs"}],
    [{"lower": "r7"}, {"IS_PUNCT": True}, {"lower": "7840h5"}],
    [
        {"lower": "intel"},
        {"lower": "core"},
        {"lower": "i5"},
        {"IS_PUNCT": True},
        {"lower": "13500h"},
        {"IS_PUNCT": True},
    ],
    [
        {"lower": "r7"},
        {"IS_PUNCT": True},
        {"lower": "7840h5,rx"},
        {"lower": "780"},
        {"lower": "m"},
    ],
    [
        {"lower": "r7"},
        {"lower": "7840u"},
        {"IS_PUNCT": True},
        {"lower": "rx"},
        {"lower": "780"},
        {"lower": "m"},
    ],
    [
        {"lower": "intel"},
        {"lower": "core"},
        {"lower": "i7"},
        {"IS_PUNCT": True},
        {"TEXT": {"FUZZY2": "1370p"}},
    ],
    [
        {"lower": "apple"},
        {"lower": "m3"},
        {"lower": "pro"},
        {"IS_DIGIT": True},
        {"IS_PUNCT": True},
        {"lower": "core"},
    ],
    [
        {"lower": "intel", "OP": "?"},
        {"lower": "core"},
        {"lower": "ultra"},
        {"lower": "7"},
        {"TEXT": {"REGEX": "1[s5S][sS5]h"}},
    ],
    [
        {"lower": "core"},
        {"lower": "ultra"},
        {"lower": "7"},
        {"TEXT": {"REGEX": "1[s5S][sS5]H"}},
    ],
    [
        {"lower": "r7"},
        {"IS_PUNCT": True},
        {"lower": "7840hs.rx"},
        {"lower": "780"},
        {"lower": "m"},
    ],
    [{"lower": "amd"}, {"lower": "ryzen"}, {"lower": "7"}, {"lower": "7840s"}],
    [
        {"lower": "amd", "OP": "?"},
        {"lower": "ryzen"},
        {"lower": "7"},
        {"TEXT": {"REGEX": "1[s5S][sS5]H"}},
    ],
    [
        {"lower": "amd", "OP": "?"},
        {"lower": "ryzen"},
        {"lower": "9"},
        {"lower": "pro"},
        {"TEXT": {"REGEX": "\d+[Hh]?[Ss]"}},
    ],
    [
        {"lower": "qualcomm"},
        {"lower": "snapdragon"},
        {"lower": "x"},
        {"lower": "elite"},
    ],
    [{"lower": "amd"}, {"lower": "ryzen"}, {"lower": "7736u"}],
    [{"lower": "680OU"}],
    [{"TEXT": {"REGEX": "^\d+[Ww]h?$"}}],
]

gpuRules = [
    [{"lower": "intel"}, {"lower": "arc"}],
    [{"lower": "intel"}, {"lower": "iris"}, {"lower": "xe"}],
    [{"lower": "rtx"}, {"lower": "4060"}],
    [{"lower": "rtx"}, {"lower": "3050"}, {"lower": "ti"}],
    [{"lower": "rtx"}, {"lower": "4050"}],
    [{"lower": "amd"}, {"lower": "radeon"}, {"lower": "780mj"}],
    [{"lower": "amd"}, {"lower": "radeon"}],
]

productRules = [
    [{"lower": "macbook"}, {"lower": "pro"}, {"lower": "14"}],
    [
        {"lower": "apple"},
        {"lower": "macbook"},
        {"lower": "pro"},
        {"lower": "16"},
        {"lower": "2023"},
        {"lower": "m3"},
        {"TEXT": {"REGEX": "[Pro|Max]"}},
    ],
    [{"lower": "schenker"}, {"lower": "vision"}, {"lower": "14"}, {"lower": "2023"}],
    [
        {"lower": "sd"},
        {"lower": "x"},
        {"lower": "elite"},
        {"lower": "reference"},
        {"TEXT": {"REGEX": "\d+[Ww]"}},
    ],
    [
        {"lower": "microsoft"},
        {"lower": "surface"},
        {"lower": "laptop"},
        {"lower": "studio"},
        {"lower": "2"},
        {"lower": "rtx"},
        {"lower": "4060"},
    ],
    [{"lower": "lenovo"}, {"lower": "yoga"}, {"lower": "slim"}],
    [{"lower": "lenovo"}, {"lower": "slim"}, {"lower": "7i"}],
    [
        {"lower": "lenovo"},
        {"lower": "yoga"},
        {"lower": "9"},
        {"lower": "14irp"},
        {"lower": "g8"},
    ],
    [{"lower": "lenovo"}, {"lower": "yoga"}, {"lower": "slim"}, {"lower": "7"}],
    [{"lower": "lenovo"}, {"lower": "thinkpad"}, {"lower": "x1"}, {"lower": "carbon"}],
    [
        {"lower": "asus"},
        {"lower": "zenbook"},
        {"lower": "14"},
        {"lower": "oled"},
        {"lower": "um3402"},
    ],
    [
        {"lower": "asus"},
        {"lower": "zenbook"},
        {"lower": "14"},
        {"lower": "ux3405ma", "OP": "?"},
    ],
    [{"lower": "asus"}, {"lower": "zenbook"}, {"lower": "13"}, {"lower": "$"}],
    [
        {"lower": "asus"},
        {"lower": "zenbook"},
        {"lower": "14x"},
        {"lower": "oled"},
        {"lower": "q410va"},
    ],
    [{"lower": "zenbook"}, {"lower": "14"}],
    [{"lower": "pavilion"}],
    [
        {"lower": "samsung"},
        {"lower": "galaxy"},
        {"lower": "book3"},
        {"lower": "pro"},
        {"lower": "360"},
    ],
    [{"lower": "zenbool"}, {"lower": "14"}],
    [{"lower": "zenbook"}, {"lower": "14x"}],
    [{"lower": "zenbook"}, {"lower": "13"}, {"lower": "$"}, {"lower": "oled"}],
    [{"lower": "hp"}, {"lower": "dragonfly"}, {"lower": "pro"}],
    [{"lower": "lenovo"}, {"lower": "slim"}, {"lower": "pro"}, {"lower": "9"}],
    [{"lower": "lenovo"}, {"lower": "slim"}, {"lower": "pro"}],
    [{"lower": "acer"}, {"lower": "swift"}],
    [{"lower": "acer"}, {"lower": "swift"}, {"lower": "go"}, {"lower": "14"}],
    [{"lower": "acer"}, {"lower": "swift"}, {"lower": "edge"}, {"lower": "16"}],
    [
        {"lower": "acer"},
        {"lower": "swift"},
        {"lower": "go"},
        {"lower": "14"},
        {"lower": "sfg14"},
        {"IS_PUNCT": True},
        {"lower": "72"},
    ],
    [
        {"lower": "lenovo"},
        {"lower": "yoga"},
        {"lower": "slim"},
        {"lower": "7"},
        {"lower": "14apu"},
        {"lower": "g8"},
    ],
    [{"lower": "lenovo"}, {"lower": "thinkpad"}, {"lower": "x1"}, {"lower": "carbon"}],
    [{"lower": "lenovo"}, {"lower": "thinkpad"}, {"lower": "xI"}, {"lower": "carbon"}],
    [{"lower": "lenovo"}, {"lower": "yoga"}, {"lower": "9i"}],
    [
        {"lower": "hp"},
        {"lower": "elitebook"},
        {"lower": "845"},
        {"lower": "g10"},
        {"lower": "5z4x0es"},
    ],
    [
        {"lower": "hp"},
        {"lower": "elitebook"},
        {"lower": "845"},
        {"lower": "g10"},
        {"lower": "818n0ea"},
    ],
    [
        {"lower": "framework"},
        {"lower": "laptop"},
        {"lower": "13.5"},
        {"lower": "13th"},
        {"lower": "gen"},
        {"lower": "intel"},
    ],
    [
        {"lower": "prestige"},
        {"lower": "16"},
        {"lower": "studio"},
        {"lower": "al", "OP": "?"},
        {"lower": "evo", "OP": "?"},
    ],
    [{"lower": "inspiron"}, {"lower": "16"}, {"lower": "plus"}],
    [{"lower": "pavilion"}, {"lower": "plus"}, {"lower": "14"}],
    [{"lower": "legion"}, {"lower": "slim"}],
    [{"lower": "mocbook"}, {"lower": "pro"}, {"lower": "14"}],
    [{"TEXT": {"REGEX": "m[ao]cboo[lk]"}}, {"lower": "pro"}, {"lower": "16"}],
    [{"lower": "mocbook"}, {"lower": "pro"}, {"lower": "16"}],
    [{"lower": "framework"}, {"lower": "13"}],
    [{"lower": "xps"}, {"lower": "15"}],
    [{"lower": "slim"}, {"lower": "pro"}, {"lower": "9i"}, {"lower": "16"}],
    [{"lower": "slim"}, {"lower": "7"}],
]

scoreRules = [
    [{"TEXT": {"REGEX": "\d{1,4}"}}, {"lower": "mins"}],
    [{"TEXT": {"REGEX": "\d{1,4}"}}, {"lower": "fps"}],
    [{"TEXT": {"REGEX": "\d{1,4}"}}, {"IS_SPACE": True}, {"lower": "points"}],
    [
        {"TEXT": '"'},
        {"TEXT": {"REGEX": "^\d+[,\.:\*]?\d+?$"}},
        {"TEXT": '"'},
    ],  # Get times of the format 4:30 or 12:02
    # [{"lower": '\"'}, {"TEXT": {"REGEX": "^\d+[,\.:\*]?\d+?$"}},{"lower": '\"'}],
    [{"TEXT": '"'}, {"SHAPE": "d"}, {"IS_PUNCT": True}, {"SHAPE": "dd"}, {"TEXT": '"'}],
    [{"TEXT": '"'}, {"SHAPE": "dd"}, {"TEXT": "%"}, {"TEXT": '"'}],
]
