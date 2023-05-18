import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm

# settings
pd.options.display.max_columns = None

# import
df = pd.read_csv('uchazeci_pbi_export.csv')
df = df.rename(columns={
    'Rok': 'rok',
    'Výběrovost': 'vyb',
    'Absolventi procento': 'absPercent',
    'Cekový počet studií': 'pocStud'})
# print(df.head())

# konverze jednotek
df['rok'] = df['rok'].astype(int)
df['vyb'] = df['vyb'].str.rstrip('%').astype(float) / 100.0
df['absPercent'] = df['absPercent'].str.rstrip('%').astype('float') / 100.0

df = df[df['pocStud'].notnull()]
df['pocStud'] = df['pocStud'].astype(int)

# filter
df = df[(df['rok'] <= 2016) & (df['vyb'] != 1) & (df['pocStud'] >= 25) & (df['absPercent'] != 0)]
dfVer = df[df['forma'] == 'veřejná']

# vyber pro koleraci
print("PCC všechny školy: " + str(df[['vyb', 'absPercent']].corr().iat[1, 0]))
print("PCC soukromé školy: " + str(df[df['forma'] == 'soukromá'][['vyb', 'absPercent']].corr().iat[1, 0]))
print("PCC veřejné školy: " + str(dfVer[['vyb', 'absPercent']].corr().iat[1, 0]))

# OLS
result = sm.ols(formula='absPercent ~ vyb', data=dfVer).fit()
print(result.summary())

# graf
plt.scatter('vyb', 'absPercent', data=dfVer)
plt.plot(dfVer["vyb"], result.params["Intercept"] + result.params["vyb"] * dfVer["vyb"], "-", c="black")
plt.show()