data = {
  "study_hours":     [2,   0,  3,  5,  6,  4,  6,  7,  8, 9],
  "attendance":      [40, 60, 50, 70, 90, 60, 85, 100, 80, 90],
  "previous_scores": [40, 20, 35, 60, 90, 50, 70,  95, 90, 100],
  "assignment":      [0,  10,  20, 70, 100, 60, 80, 90, 100, 90],
  "sleep_hours":     [5,  3,   5,  6,  7,   5,   7,  6,  6,  5]
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
y = [0, 0, 0, 0, 1, 0, 1, 1, 1, 1]
