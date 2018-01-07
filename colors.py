# colors
def get_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# from light to dark greyscale
wb1 = "#dbe0e7"
wb2 = "#a3acbe"
wb3 = "#67708b"
wb4 = "#4e5371"
wb5 = "#393a56"
wb6 = "#26243a"
wb7 = "#141020"

# from bright green to dark blue
# gets dark in the middle
gb1 = "#7bcf5c"
gb2 = "#509b4b"
gb3 = "#2e6a42"
gb4 = "#1a453b"
gb5 = "#0f2738"
gb6 = "#0d2f6d"
gb7 = "#0f4da3"
gb8 = "#0e82ce"
gb9 = "#13b2f2"
gb10 = "#41f3fc"

# from beige to yellow
# gets darik in the middle
by1 = "#f0d2af"
by2 = "#e5ae78"
by3 = "#c58158"
by4 = "#945542"
by5 = "#623530"
by6 = "#46211f"
by7 = "#97432a"
by8 = "#e57028"
by9 = "#f7ac37"
by10 = "#fbdf6b"

# from pink to purple.
# gets redissh in the middle
pp1 = "#fe979b"
pp2 = "#ed5259"
pp3 = "#c42c36"
pp4 = "#781f2c"
pp5 = "#351428"
pp6 = "#4d2352"
pp7 = "#7f3b86"
pp8 = "#b45eb3"
pp9 = "#e38dd6"
