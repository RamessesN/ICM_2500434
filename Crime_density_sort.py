import pandas as pd

# 读取犯罪密度数据
df_population = pd.read_excel('./result/excel/network_crime_rate_per_million.xlsx', index_col=0)

# 指定目标国家列表
target_countries = [
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

# 指定新的排序顺序的国家列表
sorted_countries = [
    'Mauritius', 'Egypt', 'Qatar', 'Saudi Arabia', 'United Arab Emirates', 'Indonesia', 'Republic of Korea', 'Denmark',
    'Finland', 'Italy', 'Türkiye', 'United Kingdom', 'United States', 'Singapore', 'Portugal', 'Viet Nam', 'Spain',
    'Sweden', 'Ghana', 'Tanzania', 'Thailand', 'Netherlands (Kingdom of the)', 'Iceland', 'France', 'Malaysia',
    'Luxembourg', 'Jordan', 'Kenya', 'India', 'Rwanda', 'Cyprus', 'Bahrain', 'Japan', 'Morocco', 'Greece', 'Oman',
    'Norway', 'Bangladesh', 'Belgium', 'Serbia', 'Pakistan', 'Slovenia', 'Brazil', 'Australia', 'Estonia', 'Uruguay',
    'Slovakia', 'Kazakhstan', 'Germany', 'Azerbaijan', 'Israel', 'Poland', 'Philippines', 'Canada', 'Malta', 'Lithuania',
    'Zambia', 'Russian Federation', 'Georgia', 'China', 'Romania', 'Benin', 'Switzerland', 'Ireland', 'Uzbekistan',
    'Austria', 'Togo', 'Hungary', 'Czech Republic', 'Croatia', 'Ecuador', 'Sri Lanka', 'Albania', 'South Africa', 'Mexico',
    'Ukraine', 'Peru', 'Uganda', 'Latvia', 'New Zealand', 'Nigeria', 'Tunisia', 'Malawi', 'Eswatini', "Cote d'lvoire",
    'Botswana', 'Andorra', 'Ethiopia', 'Dominican Republic', 'Manaco', 'Costa Rica', 'Montenegro', 'Paraguay', 'Bulgaria',
    'Myanmar', 'Cuba', 'Brunei Darussalam', 'Burkina Faso', 'Chile', 'Nepal(Republic of)', 'Vanuatu', 'Libya', 'Senegal',
    'Panama', 'Mozambique', 'North Macedonia', 'Colombia', 'Algeria', 'Kyrgyzstan', 'Cameroon', 'Iran(Islamic Republic of)',
    'Moldova', 'Papua New Guinea', 'Gambia', 'Belarus', 'Kuwait', 'Bhutan', 'Jamaica', 'Democratic Republic of the Congo',
    'Sierra Leone', 'Guinea', 'Mongolia', 'Trinidad and Tobago', 'Kiribati', 'Fiji', 'Armenia', 'Iraq', 'Liechtenstein',
    'Cabo Verde', 'Argentina', 'Syrian Arab Republic', 'Seychelles', 'Chad', 'Sudan', 'Guyana', 'Samoa', 'Bolivia', 'Niger',
    'Venezuela', 'Guatemala', 'Gabon', 'Zimbabwe', 'Angola', 'Mauritania', 'Comoros', 'State of Palestine', 'Somalia',
    'Cambodia', 'Namibia', 'Barbados', 'Suriname', 'South Sudan', 'Bahamas', 'Tonga', 'Bosnia and Herzegovina', 'Lao P.D.R.',
    'Lebanon', 'Belize', 'Madagascar', 'Saint Kitts and Nevis', 'Djibouti', 'Lesotho', 'Mali', 'Honduras', 'Congo',
    'Saint Vincent and the Grenadines', 'Saint Lucia', 'San Marino', 'Trukmenistan', 'Equatorial Guinea', 'Tajikistan',
    'Haiti', 'Dominica', 'Nauru', 'Liberia', 'Nicaragua', 'Sao Tome and Principe', 'Tuvalu', 'Grenada', 'Afghanistan',
    'Antigua and Barbuda', 'Solomon Islands', 'Timor-Leste', 'Burundi', 'Maldives', 'Marshall Islands', 'Vatican',
    'Micronesia', 'Yemen', 'Guinea-Bissau', "Democratic People's Republic of Korea", 'Central African Republic', 'Eritrea'
]

# 国家名称映射（将新列表中的名称映射到原列表中的名称）
country_name_mapping = {
    'Republic of Korea': 'South Korea',  # 假设原数据中为 South Korea
    'Türkiye': 'Turkey',  # 假设原数据中为 Turkey
    'Viet Nam': 'Vietnam',  # 假设原数据中为 Vietnam
    'Netherlands (Kingdom of the)': 'Netherlands',  # 假设原数据中为 Netherlands
    'Russian Federation': 'Russia',  # 假设原数据中为 Russia
    'Iran(Islamic Republic of)': 'Iran',  # 假设原数据中为 Iran
    'Nepal(Republic of)': 'Nepal',  # 假设原数据中为 Nepal
    "Cote d'lvoire": "Côte d'Ivoire",  # 假设原数据中为 Côte d'Ivoire
    'Democratic People\'s Republic of Korea': 'North Korea',  # 假设原数据中为 North Korea
    'State of Palestine': 'Palestine',  # 假设原数据中为 Palestine
    'Lao P.D.R.': 'Laos',  # 假设原数据中为 Laos
    'Trukmenistan': 'Turkmenistan',  # 假设原数据中为 Turkmenistan
    'Cabo Verde': 'Cape Verde',  # 假设原数据中为 Cape Verde
    'Syrian Arab Republic': 'Syria',  # 假设原数据中为 Syria
    'Eswatini': 'Swaziland',  # 假设原数据中为 Swaziland
    'Timor-Leste': 'East Timor',  # 假设原数据中为 East Timor
    'Democratic Republic of the Congo': 'Congo (Kinshasa)',  # 假设原数据中为 Congo (Kinshasa)
    'Congo': 'Congo (Brazzaville)',  # 假设原数据中为 Congo (Brazzaville)
    'Myanmar': 'Burma',  # 假设原数据中为 Burma
    'Manaco': 'Monaco',  # 假设原数据中为 Monaco
    'Guinea-Bissau': 'Guinea Bissau',  # 假设原数据中为 Guinea Bissau
    'Central African Republic': 'Central Africa',  # 假设原数据中为 Central Africa
    'Vatican': 'Vatican City',  # 假设原数据中为 Vatican City
    'Micronesia': 'Federated States of Micronesia',  # 假设原数据中为 Federated States of Micronesia
}

# 将新列表中的国家名称映射到原国家名称
sorted_countries = [country_name_mapping.get(country, country) for country in sorted_countries]

# 筛选目标国家
filtered_df = df_population[df_population.index.isin(target_countries)]

# 按照指定顺序重新排序
filtered_df = filtered_df.reindex(sorted_countries).dropna()

# 导出到Excel
filtered_df.to_excel('./result/excel/crime_density_sort.xlsx')

print("处理完成，结果已保存至 './result/excel/crime_density_sort.xlsx'")