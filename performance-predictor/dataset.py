data = {
  "study_hours":     [2,   0,  3,  5,  6,  4,  6,  7,  8, 9,  3,  2,  2, 3, 1, 2, 1, 2],
  "attendance":      [40, 60, 50, 70, 90, 60, 85, 100, 80, 90, 80, 60, 50, 80, 50, 80, 100, 100],
  "previous_scores": [40, 20, 35, 60, 90, 50, 70,  95, 90, 100, 65, 60, 60, 70, 60, 45, 50, 60],
  "assignment":      [0,  10,  20, 70, 100, 60, 80, 90, 100, 90, 70, 50, 60, 80, 40, 70, 65, 60],
  "sleep_hours":     [5,  3,   5,  6,  7,   5,   7,  6,  6,  5, 5,  4,  10, 7, 9, 6, 7,  5],
  "results":          [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
}

import pandas as pd
df = pd.DataFrame(data)

X = df[[
    "study_hours",
    "attendance",
    "previous_scores",
    "assignment",
    "sleep_hours"
    ]]
y = df[
    "results"
]
