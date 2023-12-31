import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from arch.unitroot import ADF
import pickle
import pandas as pd
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
prepro_file_path = os.path.join(project_root, "data", "prepro", "datos_fred_procesados.csv")
from utils.adf_tests_arch import ModelsADF

df = pd.read_csv(prepro_file_path, sep=",", index_col='index')
HOUSTMW=df['HOUSTMW']
stl_result = STL(HOUSTMW, seasonal=13, period=12).fit()
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))

# Original Time Series
ax1.plot(HOUSTMW)
ax1.set_title('Original Time Series')

# Trend Component
ax2.plot(stl_result.trend)
ax2.set_title('Trend Component')

# Seasonal Component
ax3.plot(stl_result.seasonal)
ax3.set_title('Seasonal Component')

# Residual Component
ax4.plot(stl_result.resid)
ax4.set_title('Residual Component')

plt.tight_layout()
plt.show()

# Plot ACF and PACF for the original time series
plt.figure(figsize=(12, 4))
plt.subplot(121)
plot_acf(HOUSTMW, lags=50, ax=plt.gca())
plt.title('ACF for Original Time Series')

plt.subplot(122)
plot_pacf(HOUSTMW, lags=50, ax=plt.gca())
plt.title('PACF for Original Time Series')

plt.tight_layout()
plt.show()
#
adf_test = ADF(stl_result.resid,trend='ct' )
adf_test_result = adf_test.summary()
print(adf_test_result)
#
dfHOUTSMW = pd.DataFrame({'HOUTSMW': stl_result.resid})
pickle_HOUTSMW_file_path = os.path.join(project_root, "data", "prepro", 'residualsHOUTSMW.pkl')
print(pickle_HOUTSMW_file_path)
dfHOUTSMW.to_pickle(pickle_HOUTSMW_file_path)