import pandas as pd

# 读取犯罪密度数据
df_population = pd.read_excel('./result/excel/country_attack_statistics_by_year.xlsx', index_col=0)

# 指定目标国家列表
target_countries = [
    'Qatar', 'Saudi Arabia', 'United Arab Emirates', 'Indonesia', 'Denmark', 'Finland', 'Italy', 'United Kingdom',
    'United States', 'Singapore', 'Portugal', 'Spain', 'Sweden', 'Ghana', 'Thailand', 'Netherlands', 'Iceland', 'France',
    'Malaysia', 'Luxembourg', 'Jordan', 'Kenya', 'India', 'Rwanda', 'Cyprus', 'Bahrain', 'Japan', 'Morocco', 'Greece',
    'Oman', 'Norway', 'Bangladesh', 'Belgium', 'Serbia', 'Pakistan', 'Slovenia', 'Brazil', 'Australia', 'Estonia',
    'Uruguay', 'Slovakia', 'Kazakhstan', 'Germany', 'Azerbaijan', 'Israel', 'Poland', 'Philippines', 'Canada', 'Malta',
    'Lithuania', 'Zambia', 'Georgia', 'China', 'Romania', 'Switzerland', 'Ireland', 'Uzbekistan', 'Austria', 'Hungary',
    'Croatia', 'Ecuador', 'Sri Lanka', 'Albania', 'South Africa', 'Mexico', 'Ukraine', 'Peru', 'Uganda', 'Latvia',
    'New Zealand', 'Nigeria', 'Tunisia', 'Botswana', 'Ethiopia', 'Monaco', 'Costa Rica', 'Montenegro', 'Paraguay',
    'Bulgaria', 'Brunei Darussalam', 'Chile', 'Nepal', 'Panama', 'Mozambique', 'North Macedonia', 'Colombia', 'Algeria',
    'Belarus', 'Kuwait', 'Jamaica', 'Trinidad and Tobago', 'Armenia', 'Iraq', 'Argentina', 'Sudan', 'Guatemala', 'Gabon',
    'Zimbabwe', 'Mauritania', 'Cambodia', 'Namibia', 'Bahamas', 'Bosnia and Herzegovina', 'Lebanon', 'Belize', 'Mali',
    'Honduras', 'Turkmenistan', 'Tajikistan', 'Haiti', 'Antigua and Barbuda', 'Yemen'
]

# 筛选目标国家
filtered_df = df_population[df_population.index.isin(target_countries)]

# 按照指定顺序重新排序
filtered_df = filtered_df.reindex(target_countries).dropna()

# 导出到Excel
filtered_df.to_excel('./result/excel/filtered_country_crime_by_year.xlsx')

print("处理完成，结果已保存至 './result/excel/filtered_country_crime_by_year.xlsx'")