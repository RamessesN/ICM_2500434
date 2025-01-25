import pandas as pd

# 读取两张 Excel 表
df_attacks = pd.read_excel('./result/excel/country_attack_statistics_by_year.xlsx', index_col=0)  # 网络攻击数量表
df_population = pd.read_excel('./result/excel/filtered_population_data.xlsx', index_col=0)  # 人口数量表

# 将人口数量表的列名转换为整数类型
df_population.columns = df_population.columns.astype(int)

# 对齐索引（国家名称）和列（年份）
df_population = df_population.reindex(index=df_attacks.index, columns=df_attacks.columns)

# 确保数据为数值类型
df_attacks = df_attacks.apply(pd.to_numeric, errors='coerce')
df_population = df_population.apply(pd.to_numeric, errors='coerce')

# 处理人口为 0 的情况（替换为 1，避免除零错误）
df_population = df_population.replace(0, 1)

# 计算每百万人的网络犯罪率
df_crime_rate = (df_attacks * 10**8) / df_population

# 将结果保存到新的 Excel 文件
df_crime_rate.to_excel('./result/excel/network_crime_rate_per_million.xlsx', sheet_name='Crime Rate')