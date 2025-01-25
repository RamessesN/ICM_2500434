import os
import json
import pandas as pd
from collections import defaultdict
from pycountry import countries

# ================== 配置部分 ==================
INPUT_DIR = "./data/json/"  # 存放JSON文件的文件夹路径
OUTPUT_EXCEL = "./result/excel/country_attack_statistics_by_year.xlsx"  # 输出文件路径
YEAR_RANGE = (2000, 2023)  # 强制包含的年份范围

# 指定有效国家列表
VALID_COUNTRIES = [
    'Albania', 'United Arab Emirates', 'Argentina', 'Armenia', 'Antigua and Barbuda', 'Australia', 'Austria', 'Azerbaijan',
    'Belgium', 'Bangladesh', 'Bulgaria', 'Bahrain', 'Bahamas', 'Bosnia and Herzegovina', 'Belarus', 'Belize',
    'Brazil', 'Brunei Darussalam', 'Botswana', 'Canada', 'Switzerland', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Cyprus',
    'Germany', 'Denmark', 'Algeria', 'Ecuador', 'Spain', 'Estonia', 'Ethiopia', 'Finland', 'France', 'Gabon', 'United Kingdom',
    'Georgia', 'Ghana', 'Greece', 'Guatemala', 'Guam', 'Honduras', 'Croatia', 'Haiti', 'Hungary', 'Indonesia', 'Isle of Man',
    'India', 'Ireland', 'Iraq', 'Iceland', 'Israel', 'Italy', 'Jamaica', 'Jordan', 'Japan', 'Kazakhstan', 'Kenya', 'Cambodia',
    'Kuwait', 'Lebanon', 'Sri Lanka', 'Lithuania', 'Luxembourg', 'Latvia', 'Morocco', 'Monaco', 'Mexico', 'North Macedonia',
    'Mali', 'Malta', 'Montenegro', 'Mozambique', 'Mauritania', 'Malaysia', 'Namibia', 'Nigeria', 'Netherlands', 'Norway', 'Nepal',
    'New Zealand', 'Oman', 'Pakistan', 'Panama', 'Peru', 'Philippines', 'Poland', 'Puerto Rico', 'Portugal', 'Paraguay', 'Qatar',
    'Romania', 'Rwanda', 'Saudi Arabia', 'Sudan', 'Singapore', 'Serbia', 'Slovakia', 'Slovenia', 'Sweden', 'Thailand', 'Tajikistan',
    'Turkmenistan', 'Timor-Leste', 'Trinidad and Tobago', 'Tunisia', 'Uganda', 'Ukraine', 'Uruguay',
    'United States', 'Uzbekistan', 'Yemen', 'South Africa', 'Zambia', 'Zimbabwe'
]

# ================== 核心处理函数 ==================
def process_directory(input_dir):
    """处理整个文件夹的JSON文件"""
    attack_data = defaultdict(lambda: defaultdict(int))
    countries_seen = set()
    years_seen = set()

    # 遍历文件夹及子文件夹
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if not filename.lower().endswith('.json'):
                continue

            file_path = os.path.join(root, filename)
            process_single_file(file_path, attack_data, countries_seen, years_seen)

    # 生成完整数据矩阵
    return build_dataframe(attack_data, countries_seen, years_seen)

def process_single_file(file_path, attack_data, countries_seen, years_seen):
    """处理单个JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 提取国家代码
            country_code = data.get('victim', {}).get('country', [''])[0] or 'Unknown'
            if len(country_code) != 2:  # 验证是否为ISO 2字母代码
                country_code = 'Unknown'

            # 转换国家名称
            try:
                country_name = countries.get(alpha_2=country_code).name
            except:
                country_name = country_code

            # 提取年份
            year = data.get('timeline', {}).get('incident', {}).get('year', 0)
            if not isinstance(year, int) or year < YEAR_RANGE[0]:
                year = 0

            # 更新统计
            if country_name != 'Unknown' and year != 0:
                attack_data[country_name][year] += 1
                countries_seen.add(country_name)
                years_seen.add(year)

    except Exception as e:
        print(f"处理文件失败 {os.path.basename(file_path)}: {str(e)}")

def build_dataframe(attack_data, countries_seen, years_seen):
    """构建最终数据矩阵"""
    # 生成完整年份列
    min_year = min(years_seen) if years_seen else YEAR_RANGE[0]
    max_year = max(years_seen) if years_seen else YEAR_RANGE[1]
    existing_years = sorted(years_seen.union(set(range(*YEAR_RANGE))))

    # 创建DataFrame
    df = pd.DataFrame(
        index=sorted(countries_seen),
        columns=existing_years,
        dtype=int
    ).fillna(0)

    # 填充数据
    for country, years in attack_data.items():
        for year, count in years.items():
            df.at[country, year] = count

    # 确保包含配置的完整年份范围
    full_columns = list(range(*YEAR_RANGE)) + [YEAR_RANGE[1]]
    df = df.reindex(columns=full_columns, fill_value=0)

    # 筛选有效国家
    df = df.reindex(VALID_COUNTRIES)

    # 排序处理
    df = df.sort_index(axis=0).sort_index(axis=1)
    df.index.name = 'Country Name'

    return df

# ================== 执行入口 ==================
if __name__ == "__main__":
    # 检查输入路径
    if not os.path.exists(INPUT_DIR):
        raise FileNotFoundError(f"输入文件夹不存在: {INPUT_DIR}")

    # 处理数据
    print(f"开始处理文件夹: {INPUT_DIR}")
    result_df = process_directory(INPUT_DIR)

    # 导出Excel
    result_df.to_excel(OUTPUT_EXCEL, sheet_name='Attack Statistics')
    print(f"处理完成，共统计 {len(result_df) - 1} 个国家/地区")
    print(f"结果已保存至: {os.path.abspath(OUTPUT_EXCEL)}")