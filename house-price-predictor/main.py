import pandas as pd

data = pd.read_csv("singapore_house.csv")
data = data.drop_duplicates()

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numerical_features = ["floor_area_sqm", "lease_commence_date"]
categorical_features = ["town", "flat_type", "storey_range", "flat_model", "remaining_lease"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

X = data.drop(["resale_price", "month"], axis=1)
y = data["resale_price"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)


# Linear Regression
model_linear = LinearRegression()

model_linear.fit(X_train_processed, y_train)

predictions_linear = model_linear.predict(X_test_processed)

mae_linear = mean_absolute_error(y_test, predictions_linear)
print("MAE Score:", mae_linear)
r2_linear = r2_score(y_test, predictions_linear)
print("R2 Score:", r2_linear)

# Random Forest
model_random = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model_random.fit(X_train_processed, y_train)

predictions_random = model_random.predict(X_test_processed)

mae_random = mean_absolute_error(y_test, predictions_random)
print("MAE Score:", mae_random)
r2_random = r2_score(y_test, predictions_random)
print("R2 Score:", r2_random)

# Boosting
model_boosting = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.01,
    max_depth=10,
    random_state=42
)

model_boosting.fit(X_train_processed, y_train)

predictions_boosting = model_boosting.predict(X_test_processed)

mae_boosting = mean_absolute_error(y_test, predictions_boosting)
print("MAE Score:", mae_boosting)
r2_boosting = r2_score(y_test, predictions_boosting)
print("R2 Score:", r2_boosting)


# User input
town_inp = input("Indicate town name: ").upper()
flat_type_inp = input("Enter flat type: ").upper()
storey_range_inp = input("Indicate storey range (e.g. 01 TO 03): ").upper()
floor_area_sqm_inp = float(input("Enter floor area (to squared metre): "))
flat_model_inp = input("Enter flat model: ")
lease_commence_date_inp = int(input("Enter lease commence date: "))
remaining_lease_inp = input("Enter remaining lease: ")

numerical_features_inp = ["floor_area_sqm_inp", "lease_commence_date_inp"]
categorical_features_inp = ["town_inp", "flat_type_inp", "storey_range_inp", "flat_model_inp", "remaining_lease_inp"]

user_inp = pd.DataFrame({
    "town": [town_inp],
    "flat_type": [flat_type_inp],
    "storey_range": [storey_range_inp],
    "floor_area_sqm": [floor_area_sqm_inp],
    "flat_model": [flat_model_inp],
    "lease_commence_date": [lease_commence_date_inp],
    "remaining_lease": [remaining_lease_inp]
})

def house_price_predict(inp):

  input_transformed = preprocessor.transform(inp)

  predictions_1 = model_linear.predict(input_transformed)
  predictions_2 = model_random.predict(input_transformed)
  predictions_3 = model_boosting.predict(input_transformed)

  print("First prediction:", predictions_1)
  print("Second prediction:", predictions_2)
  print("Third prediction:", predictions_3)

house_price_predict(user_inp)
