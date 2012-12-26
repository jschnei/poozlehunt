import collections

# global-use maps

solid_list = ["Ocean", "Mountain", "Rock"]

# basic tiles / area info

tile_map = { }
tile_map["noodle"] = [[["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Dirt"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Grass"],["Dirt"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Grass"],["Grass"],["Dirt"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Grass"],["Grass"],["Grass"],["Dirt"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"]],[["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"]],[["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Grass"],["Grass"],["Grass"]],[["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Grass"]],[["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"]],[["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"]]]
tile_map["noodle"][5][9] += ["p1"]

tile_map["noodle2"] = [[["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"]],[["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"]],[["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"]],[["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"]],[["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"]],[["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"]],[["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"]],[["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"]],[["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"],["Ocean"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","City"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Mountain"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Rock"],["Grass"],["Grass"],["Grass"],["Grass","Rock"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain","Mountain","Mountain","Mountain","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain","Mountain"]],[["Grass","Mountain","Mountain","Mountain","Mountain","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain","Mountain","Mountain","Mountain","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain"]],[["Grass","Mountain","Mountain","Mountain","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain"]],[["Grass","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain"]],[["Grass","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"]],[["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain"],["Grass","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain","Mountain"]]]
tile_map["noodle2"][11][11] += ["w1"]

area_map = {}
area_map["noodle"] = "Noodle Village"
area_map["noodle2"] = "Noodle Peninsula"

# enemy encounters/types

enemy_map = { }
enemy_map["noodle2"] = [[0.7, "wolf"], [0.3, "tiger"]]

prob_map = { }
prob_map["noodle2"] = [0.4, 0.1, 0]

prob_encounter = { "noodle2" : 1.0 }

# enemy information

unit_stats = { }
unit_stats['wolf'] = {'lvl':1, 'atk':11, 'pdef':6, 'mag':1, 'mdef':6, 'spd':3.8, 'mspd':1., 'maxhp':22, 'maxmp':0}
unit_stats['tiger'] = {'lvl':1, 'atk':13, 'pdef':6, 'mag':1, 'mdef':7, 'spd':3.6, 'mspd':1., 'maxhp':26, 'maxmp':0}

# loot information

defeat_stats = { }
defeat_stats['wolf'] = {'xp':9, 'gold':2, 'spoils': [[0.25, 'small']] }
defeat_stats['tiger'] = {'xp':10, 'gold':2, 'spoils': [[0.25, 'small']] }

spoil_groups = { }
spoil_groups['small'] = [[0.5,'h_potion_s'], [0.5,'m_potion_s']]

# item information

item_info = { }
item_info['h_potion_s'] = {'name': 'Small Healing Potion', 'desc': 'Restores 15 health.', 'use_ooc': True, 'buffs': {'heal': 15} }
item_info['m_potion_s'] = {'name': 'Small Mana Potion', 'desc': 'Restores 10 mana.', 'use_ooc': True, 'buffs': {'mheal': 10} }

# person information

person_map = { }
person_map["p1"] = ["misc_man1", "Charlem", "talk"]

talk_choice_map = collections.defaultdict(dict)
talk_choice_map["p1"]["village"] = 'say: "What can you tell me about the village?"'
talk_choice_map["p1"]["area"] = 'say: "What can you tell me about the area?"'

talk_dialog_map = collections.defaultdict(dict)
talk_dialog_map["p1"][""] = "Hello, $NAME!  How are you?"
talk_dialog_map["p1"]["village"] = "Noodle Village has been a small farming village for over a century.  Many of us grow fruits and take them to market in Lynbrook, a city to the south."
talk_dialog_map["p1"]["area"] = "Well, for starters, we're in Noodle Village!  It's on the northern tip of the continent!  Also, it's surrounded by mountains on all sides, and a tunnel to the south is the only way to get in or out."

# tags for specialized use

tag_map = collections.defaultdict(str)
tag_map["noodle"] = [["town", "noodle2", 11, 11]]

# warps

warp_map = { }
warp_map["w1"] = ["noodle", 5, 5]
