import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_poisson_deviance
from scipy.stats import mstats
import warnings

# 忽略警告
warnings.filterwarnings("ignore")


# === 数据预处理 ===
def preprocess_data(crime_data, bill_data):
    """统一国家名称并处理数据格式"""
    # 犯罪数据处理
    crime_df = (
        pd.DataFrame(crime_data)
        .set_index("Country Name")
        .T
        .rename(columns={
            "United Kingdom": "UK",
            "United Status": "US",  # 统一为US
            "Costa Rica": "Costa Rica"
        })
        .apply(pd.to_numeric)
    )

    # 法案数据处理（修复国家名称映射）
    bill_df = (
        pd.DataFrame(bill_data)
        .set_index("Country Name")
        .T
        .rename(columns={
            "US": "US",
            "UK": "UK",
            "Canada": "Canada",
            "Japan": "Japan",
            "Costa Rica": "Costa Rica"
        })
        .clip(lower=0)  # 处理负值
        .astype(int)
    )

    return crime_df, bill_df


# === 滞后特征生成 ===
def create_lag_features(df, max_lag=3):
    """创建滞后特征并过滤无效数据"""
    if len(df) < max_lag + 1:  # 确保有足够数据
        return pd.DataFrame()
    df_lagged = df.copy()
    for lag in range(1, max_lag + 1):
        df_lagged[f'Bill_lag{lag}'] = df_lagged['Bill'].shift(lag)
    return df_lagged.dropna()


# === 可视化函数 ===
def plot_results(country, combined, model, features):
    """生成分析图表"""
    fig, ax = plt.subplots(figsize=(12, 7), dpi=1200)

    # 主趋势线
    years = combined['Year'].astype(str)
    ax.plot(years, combined['Crime'],
            marker='o', markersize=8, linewidth=2.5,
            color='#2c7bb6', label='Actual Crime',
            zorder=3)

    # 预测趋势线（添加平滑处理）
    y_pred = np.maximum(model.predict(combined[features]), 1e-6)  # 避免零值
    ax.plot(years, y_pred,
            linestyle='--', linewidth=2,
            color='#d7191c',
            label=f'Poisson Fit (Deviance={mean_poisson_deviance(combined["Crime"], y_pred):.1f})',
            zorder=2)

    # 图表标注
    ax.set_title(f'{country}: Cybercrime Analysis\n'
                 f'Optimal Lag: {len(features)} years',
                 fontsize=14, pad=20)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Cases', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.legend()

    # 保存结果
    plt.tight_layout()
    plt.savefig(f'./result/image/{country}_Analysis.pdf',
                dpi=1200, bbox_inches='tight')
    plt.close()

crime_data = {
    "Country Name": ["United Kingdom", "United Status", "Canada", "Japan", "Costa Rica"],
    "2000": [0, 0, 0, 0, 1],
    "2001": [0, 5, 0, 0, 0],
    "2002": [0, 4, 0, 0, 0],
    "2003": [0, 10, 1, 0, 1],
    "2004": [2, 11, 0, 0, 1],
    "2005": [0, 17, 0, 0, 3],
    "2006": [0, 18, 1, 0, 0],
    "2007": [4, 37, 2, 0, 0],
    "2008": [11, 58, 0, 0, 4],
    "2009": [10, 74, 1, 0, 2],
    "2010": [6, 562, 1, 0, 10],
    "2011": [38, 456, 4, 0, 12],
    "2012": [68, 943, 10, 0, 39],
    "2013": [91, 1298, 12, 1, 63],
    "2014": [73, 706, 4, 0, 39],
    "2015": [72, 680, 5, 1, 47],
    "2016": [76, 566, 6, 0, 64],
    "2017": [61, 435, 4, 0, 33],
    "2018": [23, 229, 0, 0, 13],
    "2019": [17, 216, 6, 0, 18],
    "2020": [21, 186, 4, 0, 16],
    "2021": [8, 102, 3, 0, 8],
    "2022": [4, 83, 2, 1, 3],
    "2023": [6, 805, 3, 0, 2]
}

bill_data = {
    "Country Name": ["US", "Japan", "China", "Costa Rica", "Namibia", "UK", "Canada"],
    "2000": [1, 1, 1, 0, 0, 1, 1],
    "2001": [1, 0, 0, 0, 0, 0, 1],
    "2002": [1, 0, 0, 0, 0, 0, 0],
    "2003": [0, 1, 0, 0, 0, 0, 0],
    "2004": [0, 0, 0, 0, 0, 0, 0],
    "2005": [0, 0, 0, 0, 0, 0, 0],
    "2006": [0, 1, 0, 0, 0, 0, 0],
    "2007": [0, 0, 0, 0, 0, 0, 0],
    "2008": [0, 0, 0, 0, 0, 0, 0],
    "2009": [0, 0, 0, 0, 0, 0, 1],
    "2010": [0, 0, 0, 0, 0, 0, 1],
    "2011": [0, 0, 0, 1, 0, 1, 0],
    "2012": [0, 0, 0, 1, 0, 0, 0],
    "2013": [1, 1, 0, 0, 0, 0, 0],
    "2014": [1, 1, 0, 0, 0, 0, 1],
    "2015": [1, 1, 0, 0, 0, 0, 1],
    "2016": [1, 0, 0, 0, 0, 1, 0],
    "2017": [0, 0, 1, 1, 0, 0, 1],
    "2018": [1, 1, 0, 0, 1, 1, 1],
    "2019": [1, 1, 1, 0, 1, 0, 0],
    "2020": [1, 0, 0, 0, 0, 0, 1],
    "2021": [1, 1, 1, 0, 0, 1, 1],
    "2022": [1, 0, 0, 0, 0, 1, 1],
    "2023": [1, 0, 0, 1, 1, 0, 1]
}

# === 主程序 ===
if __name__ == "__main__":
    # 创建输出目录
    os.makedirs('./result/image/policy_time', exist_ok=True)

    # 加载数据
    crime_df, bill_df = preprocess_data(crime_data, bill_data)

    # 分析各国数据
    countries = ["UK", "US", "Canada", "Japan", "Costa Rica"]

    for country in countries:
        try:
            # 合并数据集
            combined = pd.DataFrame({
                'Year': crime_df[country].index.astype(int),
                'Crime': crime_df[country].values,
                'Bill': bill_df[country].reindex(crime_df.index).fillna(0).values
            }).dropna()

            # 跳过无效数据（数据量不足或全零）
            if len(combined) < 5 or combined['Crime'].sum() == 0:
                print(f"跳过 {country}（数据不足）")
                continue

            # 异常值处理（Winsorize上下5%）
            combined['Crime'] = mstats.winsorize(
                combined['Crime'],
                limits=[0.05, 0.05]
            )

            # 生成滞后特征（固定3年滞后）
            combined = create_lag_features(combined, 3)
            if combined.empty:
                print(f"跳过 {country}（滞后特征不足）")
                continue
            features = ['Bill_lag1', 'Bill_lag2', 'Bill_lag3']

            # 准备训练数据（添加平滑）
            X = combined[features]
            y = combined['Crime'] + 1e-6  # 防止零值

            # 训练模型
            model = PoissonRegressor(
                alpha=1.0,
                max_iter=1000,
                tol=1e-6
            ).fit(X, y)

            # 生成可视化
            plot_results(country, combined, model, features)
            print(f"成功生成 {country} 分析报告")

        except Exception as e:
            print(f"处理 {country} 时出错: {str(e)}")
            plt.close()