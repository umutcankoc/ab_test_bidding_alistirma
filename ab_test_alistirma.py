import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

##### VERİYİ ÇAĞIRMA ######


### Adım 1: ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutalım.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayalım.

df_control = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")
df_control.head(5)

df_test = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")
df_test.head(5)

### Adım 2: Kontrol ve test grubu verilerini analiz edelim.

df_control.describe().T

df_test.describe().T

### Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştirelim.

df = pd.concat([df_control, df_test], join='inner')

####### Görev 2: A/B Testinin Hipotezinin Tanımlanması ######

# Adım 1: Hipotezi tanımlayalım.

# H0 : M1 = M2
# H1 : M1!= M2

# H0: Average ile bidding yöntemi arasında bir fark yoktur.

# Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz edelim.

df_control["Purchase"].mean()
df_test["Purchase"].mean()

####### Görev 3: Hipotez Testinin Gerçekleştirilmesi #######

# Normallik Analizi

"""
Normallik Varsayımı :
H0: Normal dağılım varsayımı sağlanmaktadır. 
H1: Normal dağılım varsayımı sağlanmamaktadır.
p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ? 
Elde edilen p-value değerlerini yorumlayınız.

"""

#Normallik Varsayımı (H0: Normal dağılım varsayımı sağlanmaktadır.)

test_stat, pvalue = shapiro(df_test.Purchase)
print(f'Test stat= {test_stat}, pvalue {pvalue}')
print(pvalue < 0.05)

test_stat, pvalue = shapiro(df_control.Purchase)
print(f'Test stat= {test_stat}, pvalue {pvalue}')
print(pvalue < 0.05)

#Test stat= 0.9589453935623169, pvalue 0.15413342416286469

#Test stat= 0.9772694110870361, pvalue 0.5891125202178955

# p-value değerleri > 0.05 bu sebeple H0 Reddedilemez.

#Varyans Homojenliği

test_stat, pvalue = levene(df_test.Purchase,
                          df_control.Purchase)

print(f'Test stat= {test_stat}, pvalue {pvalue}')
print(pvalue < 0.05)

#Test stat= 2.6392694728747363, pvalue 0.108285882718748

# p-value > 0.05, HO Reddedilemez.

###################################
# AB TESTİ
###################################

# Varsayımların ikisi de sağlandığı için Bağımsız İki Örneklem T Testi uygulayacağız.

test_stat, pvalue = ttest_ind(df_test.Purchase, df_control.Purchase)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.9416, p-value = 0.3493

# p-value > 0.05 olduğu için H0 Reddedilemez.

"""
Yapılan testler sonucunda H0 hipotezleri Normallik ve Varyans testlerinde reddedilememiştir. 
Bu sebeple, Bağımsız İki Örneklem T Testi kullanılmıştır. Bu testin sonucuda p-value = 0.3493 gelmiştir.
Bu durumda H0 reddedilemez.
Average bidding ile Maximum bidding arasında purchase ortalamaları arasında anlamlı bir fark yoktur.
"""