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

result = []

for row in data:
    low = {
        "male": {"score": row[0], "value": row[1]},
        "female": {"score": row[0], "value": row[3]}
    }
    high = {
        "male": {"score": row[0], "value": row[2]},
        "female": {"score": row[0], "value": row[4]}
    }
    result.append({"low": low, "high": high})

json_data = json.dumps(result, indent=4)

with open('standard.txt', 'w') as f:
    f.write(json_data)

# print(json_data)
