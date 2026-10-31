from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

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

model_clas = make_pipeline( StandardScaler(), LogisticRegression(max_iter=1000))
model_clas.fit(X_train, y_train)
pred_clas = model_clas.predict(X_test)
acc_clas = accuracy_score(y_test, pred_clas)

print("Tree Accuracy:", acc_tree)
print("Logistic Accuracy:", acc_clas)
