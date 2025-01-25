import pandas as pd

# 读取人口数据
df_population = pd.read_excel('./data/population/Global population.xls', index_col=0)

# 指定目标国家列表
target_countries = [
    'United States of America', 'United Kingdom', 'Canada', 'Australia', 'India', 'New Zealand',
    'China', 'Japan', 'Ireland', 'Germany', 'Israel', 'South Korea', 'France', 'Russia', 'Turkey',
    'Netherlands', 'Taiwan', 'South Africa', 'Singapore', 'Spain', 'Belgium', 'Hong Kong', 'Thailand',
    'Switzerland', 'Ukraine', 'Pakistan', 'Brazil', 'United Arab Emirates', 'Philippines', 'Indonesia',
    'Argentina', 'Sweden', 'Mexico', 'Denmark', 'Malaysia', 'Syria', 'Italy', 'Czechia', 'Kenya', 'Iran',
    'Finland', 'Puerto Rico', 'Poland', 'Norway', 'United States Minor Outlying Islands', 'Cook Islands',
    'Kazakhstan', 'Austria', 'Bangladesh', 'Egypt', 'Peru', 'Cyprus', 'Venezuela', 'Armenia', 'Lithuania',
    'Azerbaijan', 'Panama', 'Ecuador', 'Nigeria', 'Romania', 'Chile', 'Vietnam', 'North Korea', 'Belarus',
    'Bulgaria', 'Zimbabwe', 'Saudi Arabia', 'Bahamas', 'Jordan', 'Qatar', 'Ethiopia', 'Slovakia', 'Gabon',
    'Lebanon', 'Jamaica', 'Portugal', 'Oman', 'Palestine', 'Turkmenistan', 'Estonia', 'Colombia', 'Honduras',
    'Latvia', 'Ghana', 'Uzbekistan', 'Malta', 'Hungary', 'Botswana', 'Albania', 'Cambodia', 'Luxembourg',
    'Moldova', 'Bolivia', 'eSwatini', 'Namibia', 'Iceland', 'Costa Rica', 'Serbia', 'Paraguay', 'Belize',
    'Morocco', 'Guatemala', 'Sri Lanka', 'Georgia', 'Nepal', 'Afghanistan', 'Bahrain', 'North Macedonia',
    'Croatia', 'Uganda', 'Timor-Leste', 'Haiti', 'Tajikistan', 'Iraq', 'Yemen', 'Sudan', 'Rwanda', 'Zambia',
    'Virgin Islands', 'Algeria', 'Guam', 'Brunei Darussalam', 'Antigua and Barbuda', 'Uruguay', 'Isle of Man', 'Greece',
    'Congo', 'Mozambique', 'Mali', 'Curaçao', 'Trinidad and Tobago', 'Montenegro', 'Tunisia', 'Slovenia',
    'Bosnia and Herzegovina', 'Mauritania', 'Monaco', 'Kuwait', 'Tanzania'
]

# 指定排序顺序的国家列表
sorted_countries = [
    'Albania', 'Algeria', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
    'Bahamas', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Belize', 'Bosnia and Herzegovina', 'Botswana',
    'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Cambodia', 'Canada', 'Chile', 'China', 'Colombia', 'Costa Rica',
    'Croatia', 'Cyprus', 'Denmark', 'Ecuador', 'Estonia', 'Ethiopia', 'Finland', 'France', 'Gabon', 'Georgia',
    'Germany', 'Ghana', 'Greece', 'Guam', 'Guatemala', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India',
    'Indonesia', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan',
    'Kenya', 'Kuwait', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Malaysia', 'Mali', 'Malta', 'Mauritania',
    'Mexico', 'Monaco', 'Montenegro', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand',
    'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines',
    'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Rwanda', 'Saudi Arabia', 'Serbia', 'Singapore',
    'Slovakia', 'Slovenia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Switzerland', 'Tajikistan',
    'Thailand', 'Timor-Leste', 'Trinidad and Tobago', 'Tunisia', 'Turkmenistan', 'Uganda', 'Ukraine',
    'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Yemen', 'Zambia', 'Zimbabwe'
]

# 筛选目标国家
filtered_df = df_population[df_population.index.isin(target_countries)]

# 将 "United States of America" 改为 "United States"
filtered_df = filtered_df.rename(index={'United States of America': 'United States'})

# 按照指定顺序重新排序
filtered_df = filtered_df.reindex(sorted_countries)

# 导出到Excel
filtered_df.to_excel('./result/excel/filtered_population_data.xlsx')

print("处理完成，结果已保存至 './result/excel/filtered_population_data.xlsx'")