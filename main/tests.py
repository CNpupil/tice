import json

data = [
    [100, 5040, 5140, 3400, 3450],
    [95, 4920, 5020, 3350, 3400],
    [90, 4800, 4900, 3300, 3350],
    [85, 4550, 4650, 3150, 3200],
    [80, 4300, 4400, 3000, 3050],
    [78, 4180, 4280, 2900, 2950],
    [76, 4060, 4160, 2800, 2850],
    [74, 3940, 4040, 2700, 2750],
    [72, 3820, 3920, 2600, 2650],
    [70, 3700, 3800, 2500, 2550],
    [68, 3580, 3680, 2400, 2450],
    [66, 3460, 3560, 2300, 2350],
    [64, 3340, 3440, 2200, 2250],
    [62, 3220, 3320, 2100, 2150],
    [60, 3100, 3200, 2000, 2050],
    [50, 2940, 3030, 1960, 2010],
    [40, 2780, 2860, 1920, 1970],
    [30, 2620, 2690, 1880, 1930],
    [20, 2460, 2520, 1840, 1890],
    [10, 2300, 2350, 1800, 1850]
]

data = [
    [100, 6.7, 6.6, 7.5, 7.4],
    [95, 6.8, 6.7, 7.6, 7.5],
    [90, 6.9, 6.8, 7.7, 7.6],
    [85, 7.0, 6.9, 8.0, 7.9],
    [80, 7.1, 7.0, 8.3, 8.2],
    [78, 7.3, 7.2, 8.5, 8.4],
    [76, 7.5, 7.4, 8.7, 8.6],
    [74, 7.7, 7.6, 8.9, 8.8],
    [72, 7.9, 7.8, 9.1, 9.0],
    [70, 8.1, 8.0, 9.3, 9.2],
    [68, 8.3, 8.2, 9.5, 9.4],
    [66, 8.5, 8.4, 9.7, 9.6],
    [64, 8.7, 8.6, 9.9, 9.8],
    [62, 8.9, 8.8, 10.1, 10.0],
    [60, 9.1, 9.0, 10.3, 10.2],
    [50, 9.3, 9.2, 10.5, 10.4],
    [40, 9.5, 9.4, 10.7, 10.6],
    [30, 9.7, 9.6, 10.9, 10.8],
    [20, 9.9, 9.8, 11.1, 11.0],
    [10, 10.1, 10.0, 11.3, 11.2]
]

data = [
    [100, 24.9, 25.1, 25.8, 26.3],
    [95, 23.1, 23.3, 24, 24.4],
    [90, 21.3, 21.5, 22.2, 22.4],
    [85, 19.5, 19.9, 20.6, 21],
    [80, 17.7, 18.2, 19, 19.5],
    [78, 16.3, 16.8, 17.7, 18.2],
    [76, 14.9, 15.4, 16.4, 16.9],
    [74, 13.5, 14, 15.1, 15.6],
    [72, 12.1, 12.6, 13.8, 14.3],
    [70, 10.7, 11.2, 12.5, 13],
    [68, 9.3, 9.8, 11.2, 11.7],
    [66, 7.9, 8.4, 9.9, 10.4],
    [64, 6.5, 7, 8.6, 9.1],
    [62, 5.1, 5.6, 7.3, 7.8],
    [60, 3.7, 4.2, 6, 6.5],
    [50, 2.7, 3.2, 5.2, 5.7],
    [40, 1.7, 2.2, 4.4, 4.9],
    [30, 0.7, 1.2, 3.6, 4.1],
    [20, -0.3, 0.2, 2.8, 3.3],
    [10, -1.3, -0.8, 2, 2.5]
]

data = [
    [100, 273, 275, 207, 208],
    [95, 268, 270, 201, 202],
    [90, 263, 265, 195, 196],
    [85, 256, 258, 188, 189],
    [80, 248, 250, 181, 182],
    [78, 244, 246, 178, 179],
    [76, 240, 242, 175, 176],
    [74, 236, 238, 172, 173],
    [72, 232, 234, 169, 170],
    [70, 228, 230, 166, 167],
    [68, 224, 226, 163, 164],
    [66, 220, 222, 160, 161],
    [64, 216, 218, 157, 158],
    [62, 212, 214, 154, 155],
    [60, 208, 210, 151, 152],
    [50, 203, 205, 146, 147],
    [40, 198, 200, 141, 142],
    [30, 193, 195, 136, 137],
    [20, 188, 190, 131, 132],
    [10, 183, 185, 126, 127]
]

data = [
    [100, 19, 20, 56, 57],
    [95, 18, 19, 54, 55],
    [90, 17, 18, 52, 53],
    [85, 16, 17, 49, 50],
    [80, 15, 16, 46, 47],
    [78, 14, 15, 44, 45],
    [76, 14, 15, 42, 43],
    [74, 13, 14, 40, 41],
    [72, 13, 14, 38, 39],
    [70, 12, 13, 36, 37],
    [68, 12, 13, 34, 35],
    [66, 11, 12, 32, 33],
    [64, 11, 12, 30, 31],
    [62, 10, 11, 28, 29],
    [60, 10, 11, 26, 27],
    [50, 9, 10, 24, 25],
    [40, 8, 9, 22, 23],
    [30, 7, 8, 20, 21],
    [20, 6, 7, 18, 19],
    [10, 5, 6, 16, 17]
]

data = [
    [100, 197, 195, 198, 196],
    [95, 202, 200, 204, 202],
    [90, 207, 205, 210, 208],
    [85, 214, 212, 217, 215],
    [80, 222, 220, 224, 222],
    [78, 227, 225, 229, 227],
    [76, 232, 230, 234, 232],
    [74, 237, 235, 239, 237],
    [72, 242, 240, 244, 242],
    [70, 247, 245, 249, 247],
    [68, 252, 250, 254, 252],
    [66, 257, 255, 259, 257],
    [64, 262, 260, 264, 262],
    [62, 267, 265, 269, 267],
    [60, 272, 270, 274, 272],
    [50, 292, 290, 284, 282],
    [40, 312, 310, 294, 292],
    [30, 332, 330, 304, 302],
    [20, 352, 350, 314, 312],
    [10, 372, 370, 324, 322]
]

data = [
	[60, 28, 28],
	[80, 24, 24],
	[100, 17.9, 17.2],
	[80, 0, 0],
]

male_data = [{"value": row[1], "score": row[0]} for row in data]
female_data = [{"value": row[2], "score": row[0]} for row in data]
result = {"male": male_data, "female": female_data}
json_str = json.dumps(result)

with open('standard.txt', 'a') as f:
    f.write('\nlow\n')
    f.write(json_str)


# male_data = [{"value": row[2], "score": row[0]} for row in data]
# female_data = [{"value": row[4], "score": row[0]} for row in data]
# result = {"male": male_data, "female": female_data}
# json_str = json.dumps(result)

# with open('standard.txt', 'a') as f:
#     f.write('\nhigh\n')
#     f.write(json_str)
#     f.write('\n')