def initialise_EduPredict(user_test):

  from sklearn.model_selection import train_test_split
  from sklearn.tree import DecisionTreeClassifier
  from sklearn.linear_model import LogisticRegression
  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import StandardScaler
  from sklearn.metrics import accuracy_score, classification_report, f1_score

  X_train, X_test, y_train, y_test = train_test_split(
      X,
      y,
      test_size=0.3,
      random_state=42,
      stratify=y
  )


  model_tree = DecisionTreeClassifier(max_depth=3, random_state=42)
  model_tree.fit(X_train, y_train)
  pred_tree = model_tree.predict(X_test)
  acc_tree = accuracy_score(y_test, pred_tree)

  model_logistic = make_pipeline( StandardScaler(), LogisticRegression(max_iter=1000))
  model_logistic.fit(X_train, y_train)
  pred_logistic = model_logistic.predict(X_test)
  acc_logistic = accuracy_score(y_test, pred_logistic)


  comparison = pd.DataFrame({
      "Model": ["Decision Tree", "Logistic Regression"],
      "Accuracy": [acc_tree, acc_logistic],
      "Macro F1": [
          f1_score(y_test, pred_tree, average="macro"),
          f1_score(y_test, pred_logistic, average="macro")
      ]
  })

  if comparison["Macro F1"][0] > comparison["Macro F1"][1]:
    prediction = model_tree.predict(user_test)
  else:
    prediction = model_logistic.predict(user_test)


  if prediction == 0:
    return "The model predicts a low performance category."
  else:
    return "The model predicts a high performance category."


while True:
  user_study = float(input("Enter estimated study hours in one day: "))
  if user_study > 24 or user_study < 0:
    print("Incorrect input.")
    continue
  else:
    break

while True:
  user_atd = float(input("Enter estimated percentage of school attendance: "))
  if user_atd > 100 or user_atd < 0:
    print("Incorrect input.")
    continue
  else:
    break

while True:
  user_scr = float(input("Enter estimated previous average score in percentage: "))
  if user_scr > 100 or user_scr < 0:
    print("Incorrect input.")
    continue
  else:
    break
  
while True:
  user_asg = float(input("Enter estimated percentage of assignment done: "))
  if user_asg > 100 or user_asg < 0:
    print("Incorrect input.")
    continue
  else:
    break

while True:
  user_sleep = float(input("Enter estimated sleep hours: "))
  if user_sleep > 24 or user_sleep < 0:
    print("Incorrect input.")
    continue
  else:
    break

user_test = pd.DataFrame([{
    "study_hours": user_study,
    "attendance": user_atd,
    "previous_scores": user_scr,
    "assignment": user_asg,
    "sleep_hours": user_sleep
}])

initialise_EduPredict(user_test)

