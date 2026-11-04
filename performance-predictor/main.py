def initialise_EduPredict(user_test):

  from sklearn.model_selection import train_test_split
  from sklearn.linear_model import LogisticRegression
  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import StandardScaler
  from sklearn.metrics import accuracy_score, classification_report

  X_train, X_test, y_train, y_test = train_test_split(
      X,
      y,
      test_size=0.3,
      random_state=42,
      stratify=y
  )

  model = make_pipeline(
      StandardScaler(),
      LogisticRegression(max_iter=1000)
  )

  model.fit(X_train, y_train)

  test_prediction = model.predict(X_test)

  classification_report(
    y_test,
    test_prediction,
    target_names=["Low Performance", "High Performance"],
    zero_division=0
  )

  prediction = model.predict(user_test)
  

  if prediction[0] == 0:
    return "The model predicts a low performance category."
  else:
    return "The model predicts a high performance category."

print(initialise_EduPredict(user_test))
