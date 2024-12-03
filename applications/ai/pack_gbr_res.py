import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import json
from difflib import get_close_matches
import matplotlib.pyplot as plt
from skopt import BayesSearchCV

def find_similar_formula(chemical_formula, mapping):
    available_formulas = list(mapping.keys())
    matches = get_close_matches(chemical_formula, available_formulas)
    if matches:
        matching_formula = matches[0]
        return matching_formula  # 返回匹配的化学式名称，而不是映射的值
    else:
        return None  # 返回None，表示没有找到匹配项

def predict_property(target_columns, attributes, *new_sample_values):
    new_sample_dict = dict(zip(attributes, new_sample_values))
    new_sample_df = pd.DataFrame(new_sample_dict, index=[0])

    # 读取并处理数据
    dataset = pd.read_csv('data/data20231010_filled_knn.csv', header=0, index_col=0)
    dataset = dataset[attributes + target_columns]

    # 划分数据
    x = dataset.drop(target_columns, axis=1).values
    y = dataset[target_columns].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=7)

    # 数据归一化
    sc = MinMaxScaler(feature_range=(0, 1))
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    # 取对数处理
    y_train_log = np.log10(y_train.ravel())
    y_test_log = np.log10(y_test.ravel())

    # 定义超参数搜索空间
    param_grid = {
        'n_estimators': (1, 200),
        'learning_rate': [0.001, 0.01, 0.1, 0.5],
        'max_depth': (1, 100),
        'min_samples_split': (2, 10),
        'min_samples_leaf': (2, 10),
        'max_features': (1, 100),
        'loss': ['squared_error', 'absolute_error'],
        'criterion': ['friedman_mse', 'squared_error']
    }

    # 贝叶斯优化
    gbr = GradientBoostingRegressor(random_state=7)
    search = BayesSearchCV(gbr, param_grid, n_iter=50, random_state=7, cv=3)
    search.fit(x_train, y_train_log)

    print("最佳参数：", search.best_params_)

    # 预测
    new_sample_scaled = sc.transform(new_sample_df.values)
    y_pred_log = search.predict(new_sample_scaled)
    y_pred_num = np.power(10, y_pred_log)

    # 测试集上预测
    y_test_pred_log = search.predict(x_test)
    y_test_pred = np.power(10, y_test_pred_log)  # 还原回原始尺度

    # 计算R平方
    r2 = r2_score(y_test, y_test_pred)
    mse = mean_squared_error(y_test, y_test_pred)
    mae = mean_absolute_error(y_test, y_test_pred)
    rmse = np.sqrt(mse)

    print(f"R²: {r2:.4f}, MSE: {mse:.4f}, MAE: {mae:.4f}, RMSE: {rmse:.4f}")

    return y_pred_num

def predict_advanced(Chemical_formula, N, P, S, Si, Se, B, F, Cl, Br, I, shape, size, surface_modification, buffer_pH,
                     temperature, substrate1, substrate2, substrate2_concentration):
    attributes = [
        'Chemical_formula',
        'N',
        'P',
        'S',
        'Si',
        'Se',
        'B',
        'F',
        'Cl',
        'Br',
        'I',
        'shape',
        'Size/nm',
        'Surface modification',
        'Buffer pH value',
        'Temperature/℃',
        'Substrate1',
        'Substrate2',
        'Substrate2 concentration(mM)',
    ]

    results = {}

    for target_columns in [["Km/mM"], ["Vmax/μM s-1"], ["Kcat/s-1"]]:
        predicted_values = predict_property(target_columns, attributes,
                                            Chemical_formula, N, P, S, Si, Se, B, F, Cl, Br, I,
                                            shape, size, surface_modification,
                                            buffer_pH, temperature, substrate1,
                                            substrate2, substrate2_concentration)
        results[target_columns[0]] = predicted_values[0]

    return results

if __name__ == '__main__':
    with open('data/string_mappings.json', encoding='utf-8') as f:
        mapping = json.load(f)

    # 修改：访问mapping的第一个元素
    chemical_formula_mapping = mapping[0]

    # 在这里改需要预测的属性（Km/mM、Vmax/μM s-1 或 Kcat/s-1三选一）
    target_columns = ["Km/mM"]

    attributes = [
        'Chemical_formula',
        'N',
        'P',
        'S',
        'Si',
        'Se',
        'B',
        'F',
        'Cl',
        'Br',
        'I',
        'shape',
        'Size/nm',
        'Surface modification',
        'Buffer pH value',
        'Temperature/℃',
        'Substrate1',
        'Substrate2',
        'Substrate2 concentration(mM)',
    ]

    # 映射到数值 否则 字符串相似度匹配（化学式变量为formula）
    formula = "FeCV"
    Chemical_formula = chemical_formula_mapping.get(formula)
    if Chemical_formula is None:
        similar_formula = find_similar_formula(formula, chemical_formula_mapping)
        if similar_formula:
            Chemical_formula = chemical_formula_mapping.get(similar_formula)

    if Chemical_formula is None:
        print(f"没有找到化学式: {formula} 或类似项")
        exit(1)  # 如果没有找到化学式，退出程序

    N = 0
    P = 1
    S = 0
    Si = 0
    Se = 0
    B = 0
    F = 0
    Cl = 0
    Br = 0
    I = 0
    shape = 1
    size = 40
    surface_modification = 0
    buffer_pH = 4.5
    temperature = 25
    substrate1 = 0
    substrate2 = 0
    substrate2_concentration = 10

    print("Predicting...")
    predicted_values = predict_property(target_columns, attributes, Chemical_formula, N, P, S, Si, Se, B, F, Cl, Br, I,
                                        shape, size, surface_modification,
                                        buffer_pH, temperature, substrate1,
                                        substrate2, substrate2_concentration)
    for i in range(len(target_columns)):
        print(f"{target_columns[i]} prediction:", predicted_values[i])
