from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

# Iris dataset load karein
iris = load_iris()
X, y = iris.data, iris.target

# Model train karein
model = RandomForestClassifier()
model.fit(X, y)

# model.pkl file save karein
joblib.dump(model, 'model.pkl')
print("model.pkl successfully created!")
