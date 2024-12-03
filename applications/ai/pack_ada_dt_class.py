import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def train_and_predict_nanoenzyme_type(nanoenzyme_name):
    df = pd.read_csv('data/data20231010_filled_knn.csv')
    df = df.rename(columns={df.columns[0]: "纳米酶名称"})

    X = df['纳米酶名称']
    y = df['Mimic enzyme activity']

    # 转特征向量
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 基础决策树分类器
    base_estimator = DecisionTreeClassifier(max_depth=70,
                                            min_samples_split=2,
                                            min_samples_leaf=1,
                                            max_features=10,
                                            criterion='gini',
                                            splitter='best',
                                            random_state=824)

    # 构建AdaBoostClassifier
    adaboost_clf = AdaBoostClassifier(base_estimator,
                                      n_estimators=19,
                                      learning_rate=0.01)

    adaboost_clf.fit(X_train, y_train)

    def predict_nanoenzyme_type(name):
        name_vector = vectorizer.transform([name])
        prediction = adaboost_clf.predict(name_vector)

        # mapping
        type_mapping = {
            0: "Peroxidase",
            1: "Oxidase",
            2: "Catalase",
            3: "SOD"
        }

        return type_mapping[prediction[0]]

    # 预测纳米酶类型
    predicted_type = predict_nanoenzyme_type(nanoenzyme_name)
    return predicted_type
