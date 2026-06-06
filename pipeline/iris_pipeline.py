import kfp
from kfp import dsl

@dsl.component(
    base_image='python:3.9',
    packages_to_install=['scikit-learn', 'pandas', 'joblib']
)
def load_data(output_path: str):
    from sklearn.datasets import load_iris
    import pandas as pd
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

@dsl.component(
    base_image='python:3.9',
    packages_to_install=['scikit-learn', 'pandas', 'joblib']
)
def train_model(data_path: str, model_path: str) -> float:
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    import joblib
    df = pd.read_csv(data_path)
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    acc = float(accuracy_score(y_test, model.predict(X_test)))
    joblib.dump(model, model_path)
    print(f"Accuracy: {acc:.4f}")
    return acc

@dsl.component(
    base_image='python:3.9',
    packages_to_install=['scikit-learn', 'joblib']
)
def evaluate_model(model_path: str, accuracy: float):
    print(f"Model evaluation complete!")
    print(f"Final accuracy: {accuracy:.4f}")
    print(f"Model saved at: {model_path}")

@dsl.pipeline(
    name='iris-classification-pipeline',
    description='Iris classification using RandomForest'
)
def iris_pipeline():
    data_task = load_data(output_path='/tmp/iris_data.csv')
    train_task = train_model(
        data_path='/tmp/iris_data.csv',
        model_path='/tmp/iris_model.pkl')
    train_task.after(data_task)
    eval_task = evaluate_model(
        model_path='/tmp/iris_model.pkl',
        accuracy=train_task.output)
    eval_task.after(train_task)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        iris_pipeline,
        '/home/kaaba/mlops-k8s-project/pipeline/iris_pipeline.yaml')
    print("Pipeline compiled successfully!")
