import json
import os
import pandas as pd

# 国家代码到全名的映射字典
COUNTRY_CODES = {
    'AF': 'Afghanistan', 'AX': 'Åland Islands', 'AL': 'Albania', 'DZ': 'Algeria', 'AS': 'American Samoa',
    'AD': 'Andorra', 'AO': 'Angola', 'AI': 'Anguilla', 'AQ': 'Antarctica', 'AG': 'Antigua and Barbuda',
    'AR': 'Argentina', 'AM': 'Armenia', 'AW': 'Aruba', 'AU': 'Australia', 'AT': 'Austria', 'AZ': 'Azerbaijan',
    'BS': 'Bahamas', 'BH': 'Bahrain', 'BD': 'Bangladesh', 'BB': 'Barbados', 'BY': 'Belarus', 'BE': 'Belgium',
    'BZ': 'Belize', 'BJ': 'Benin', 'BM': 'Bermuda', 'BT': 'Bhutan', 'BO': 'Bolivia', 'BA': 'Bosnia and Herzegovina',
    'BW': 'Botswana', 'BV': 'Bouvet Island', 'BR': 'Brazil', 'VG': 'British Virgin Islands', 'IO': 'British Indian Ocean Territory',
    'BN': 'Brunei Darussalam', 'BG': 'Bulgaria', 'BF': 'Burkina Faso', 'BI': 'Burundi', 'KH': 'Cambodia', 'CM': 'Cameroon',
    'CA': 'Canada', 'CV': 'Cape Verde', 'KY': 'Cayman Islands', 'CF': 'Central African Rep.', 'TD': 'Chad', 'CL': 'Chile',
    'CN': 'China', 'HK': 'Hong Kong', 'MO': 'Macao', 'CX': 'Christmas Island', 'CC': 'Cocos Islands', 'CO': 'Colombia',
    'KM': 'Comoros', 'CG': 'Congo', 'CD': 'Dem. Rep. Congo', 'CK': 'Cook Islands', 'CR': 'Costa Rica', 'CI': "Côte d'Ivoire",
    'HR': 'Croatia', 'CU': 'Cuba', 'CY': 'Cyprus', 'CZ': 'Czechia', 'DK': 'Denmark', 'DJ': 'Djibouti', 'DM': 'Dominica',
    'DO': 'Dominican Rep.', 'EC': 'Ecuador', 'EG': 'Egypt', 'SV': 'El Salvador', 'GQ': 'Equatorial Guinea', 'ER': 'Eritrea',
    'EE': 'Estonia', 'ET': 'Ethiopia', 'FK': 'Falkland Is.', 'FO': 'Faroe Islands', 'FJ': 'Fiji', 'FI': 'Finland', 'FR': 'France',
    'GF': 'French Guiana', 'PF': 'French Polynesia', 'TF': 'Fr. S. Antarctic Lands', 'GA': 'Gabon', 'GM': 'Gambia', 'GE': 'Georgia',
    'DE': 'Germany', 'GH': 'Ghana', 'GI': 'Gibraltar', 'GR': 'Greece', 'GL': 'Greenland', 'GD': 'Grenada', 'GP': 'Guadeloupe',
    'GU': 'Guam', 'GT': 'Guatemala', 'GG': 'Guernsey', 'GN': 'Guinea', 'GW': 'Guinea-Bissau', 'GY': 'Guyana', 'HT': 'Haiti',
    'HM': 'Heard Island and McDonald Islands', 'VA': 'Holy See', 'HN': 'Honduras', 'HU': 'Hungary', 'IS': 'Iceland', 'IN': 'India',
    'ID': 'Indonesia', 'IR': 'Iran', 'IQ': 'Iraq', 'IE': 'Ireland', 'IM': 'Isle of Man', 'IL': 'Israel', 'IT': 'Italy', 'JM': 'Jamaica',
    'JP': 'Japan', 'JE': 'Jersey', 'JO': 'Jordan', 'KZ': 'Kazakhstan', 'KE': 'Kenya', 'KI': 'Kiribati', 'KP': 'North Korea',
    'KR': 'South Korea', 'KW': 'Kuwait', 'KG': 'Kyrgyzstan', 'LA': 'Laos', 'LV': 'Latvia', 'LB': 'Lebanon', 'LS': 'Lesotho',
    'LR': 'Liberia', 'LY': 'Libya', 'LI': 'Liechtenstein', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'MK': 'North Macedonia',
    'MG': 'Madagascar', 'MW': 'Malawi', 'MY': 'Malaysia', 'MV': 'Maldives', 'ML': 'Mali', 'MT': 'Malta', 'MH': 'Marshall Islands',
    'MQ': 'Martinique', 'MR': 'Mauritania', 'MU': 'Mauritius', 'YT': 'Mayotte', 'MX': 'Mexico', 'FM': 'Micronesia', 'MD': 'Moldova',
    'MC': 'Monaco', 'MN': 'Mongolia', 'ME': 'Montenegro', 'MS': 'Montserrat', 'MA': 'Morocco', 'MZ': 'Mozambique', 'MM': 'Myanmar',
    'NA': 'Namibia', 'NR': 'Nauru', 'NP': 'Nepal', 'NL': 'Netherlands', 'NC': 'New Caledonia', 'NZ': 'New Zealand', 'NI': 'Nicaragua',
    'NE': 'Niger', 'NG': 'Nigeria', 'NU': 'Niue', 'NF': 'Norfolk Island', 'MP': 'Northern Mariana Islands', 'NO': 'Norway', 'OM': 'Oman',
    'PK': 'Pakistan', 'PW': 'Palau', 'PS': 'Palestine', 'PA': 'Panama', 'PG': 'Papua New Guinea', 'PY': 'Paraguay', 'PE': 'Peru',
    'PH': 'Philippines', 'PN': 'Pitcairn', 'PL': 'Poland', 'PT': 'Portugal', 'PR': 'Puerto Rico', 'QA': 'Qatar', 'RE': 'Réunion',
    'RO': 'Romania', 'RU': 'Russia', 'RW': 'Rwanda', 'BL': 'Saint Barthélemy', 'SH': 'Saint Helena', 'KN': 'Saint Kitts and Nevis',
    'LC': 'Saint Lucia', 'MF': 'Saint Martin', 'PM': 'Saint Pierre and Miquelon', 'VC': 'Saint Vincent and the Grenadines', 'WS': 'Samoa',
    'SM': 'San Marino', 'ST': 'Sao Tome and Principe', 'SA': 'Saudi Arabia', 'SN': 'Senegal', 'RS': 'Serbia', 'SC': 'Seychelles', 'SL': 'Sierra Leone',
    'SG': 'Singapore', 'SK': 'Slovakia', 'SI': 'Slovenia', 'SB': 'Solomon Is.', 'SO': 'Somalia', 'ZA': 'South Africa', 'GS': 'South Georgia and the South Sandwich Islands',
    'SS': 'S. Sudan', 'ES': 'Spain', 'LK': 'Sri Lanka', 'SD': 'Sudan', 'SR': 'Suriname', 'SJ': 'Svalbard and Jan Mayen', 'SZ': 'eSwatini', 'SE': 'Sweden',
    'CH': 'Switzerland', 'SY': 'Syria', 'TW': 'Taiwan', 'TJ': 'Tajikistan', 'TZ': 'Tanzania', 'TH': 'Thailand', 'TL': 'Timor-Leste', 'TG': 'Togo', 'TK': 'Tokelau',
    'TO': 'Tonga', 'TT': 'Trinidad and Tobago', 'TN': 'Tunisia', 'TR': 'Turkey', 'TM': 'Turkmenistan', 'TC': 'Turks and Caicos Islands', 'TV': 'Tuvalu', 'UG': 'Uganda',
    'UA': 'Ukraine', 'AE': 'United Arab Emirates', 'GB': 'United Kingdom', 'US': 'United States of America', 'UM': 'United States Minor Outlying Islands', 'UY': 'Uruguay',
    'UZ': 'Uzbekistan', 'VU': 'Vanuatu', 'VE': 'Venezuela', 'VN': 'Vietnam', 'WF': 'Wallis and Futuna', 'EH': 'Western Sahara', 'YE': 'Yemen', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'
}

def get_full_country_name(code):
    """
    将国家代码转换为全名。如果找不到对应的国家代码，则返回原代码或 'Unknown'。
    """
    if not code:
        return 'Unknown'
    return COUNTRY_CODES.get(code, code)

def extract_successful_countries(json_data):
    """
    从 JSON 数据中提取被攻击国家的代码，如果 'security_incident' 为 'Confirmed'。
    """
    security_incident = json_data.get("security_incident", "")
    if security_incident != "Suspected":
        return []
    country_codes = json_data.get("victim", {}).get("country", [])
    countries = [code for code in country_codes if code]
    return countries

def process_json_files(json_dir):
    """
    遍历指定目录中的所有 JSON 文件，统计每个国家成功的攻击次数。
    """
    successful_countries_count = {}
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(json_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    json_data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {file_path}: {e}")
                continue
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue

            country_codes = extract_successful_countries(json_data)
            for code in country_codes:
                if code != 'Unknown':
                    if code in successful_countries_count:
                        successful_countries_count[code] += 1
                    else:
                        successful_countries_count[code] = 1

    return successful_countries_count

def save_successful_countries(countries_count, output_file):
    """
    将成功攻击的国家及其次数保存到 Excel 文件中。
    """
    if not countries_count:
        print(f"No successful attacks found. {output_file} not created.")
        return
    # 构建包含国家代码、国家全名和成功攻击次数的列表
    data = []
    for code, count in countries_count.items():
        name = get_full_country_name(code)
        data.append({'Country': name, 'Suspected Attacks': count})
    df = pd.DataFrame(data)
    df = df.sort_values('Suspected Attacks', ascending=False)
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Suspected countries saved: {output_file}")

def main():
    """
    主函数，定义 JSON 文件目录和输出 Excel 文件路径，并执行数据处理和保存。
    """
    json_directory = "./data/json"  # 指定包含 JSON 文件的目录
    successful_stats_excel = "./result/excel/suspected_countries.xlsx"  # 输出 Excel 文件路径

    # 确保输出目录存在
    os.makedirs(os.path.dirname(successful_stats_excel), exist_ok=True)

    # 处理 JSON 文件，获取成功攻击的国家及其次数
    suspected_countries_count = process_json_files(json_directory)

    # 保存结果到 Excel 文件
    save_successful_countries(suspected_countries_count, successful_stats_excel)

if __name__ == '__main__':
    main()