import pandas as pd
from arch.unitroot import ADF
import statsmodels.api as sm
from scipy import stats
from scipy.stats import norm
import numpy as np
from scipy import stats


class TestStatistics:
    """
    A collection of unit root tests for time series analysis from arch package.

    This class provides static methods to conduct various unit root tests on
    provided dataframes or series. 
    """
    @staticmethod
    def tau_tau(df, critical_value=-3.45):
        """
        Model (c): constant and deterministic trend
        H0) \gamma = 0
    
        The ττ statistic: Constant + Time Trend  
        alpha          0.01  0.025  0.05  0.10
        Sample_Size_T
        25            -4.38  -3.95 -3.60 -3.24
        50            -4.15  -3.80 -3.50 -3.18
        100           -4.05  -3.73 -3.45 -3.15
        250           -3.99  -3.69 -3.43 -3.13
        500           -3.97  -3.67 -3.42 -3.13
        ∞             -3.96  -3.67 -3.41 -3.12

        Parameters:
        - df: pd.DataFrame
            The input DataFrame containing the time series data.

        - critical_value: float, optional
            The critical value for hypothesis testing (default: -3.45).

        Returns:
        - rh0: pd.DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: pd.DataFrame
            The columns that do not reject the null hypothesis.
        """
    
        if isinstance(df, pd.Series):
            df = df.to_frame()

        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()
        rho_list = []  # List of columns that reject the null hypothesis
        no_rho_list = [] # List of columns that not reject the null hypothesis

        for col in df.columns:
            adf_c = ADF(df[col], trend='ct', method='aic')
            reg_res_c = adf_c.regression
            tau_tau_val = reg_res_c.tvalues[0]
            reject_c = tau_tau_val < critical_value
            if reject_c:
                rh0[col] = df[col]
                rho_list.append(col)
            else:
                no_rh0[col] = df[col]
                no_rho_list.append(col)

        return {'rh0': rh0, 'no_rh0': no_rh0, 'rho_list': rho_list, 'no_rho_list': no_rho_list }
    
    @staticmethod
    def phi_2(df, critical_value=6.50, r=3, alpha=0.05, cols_norho=None):
        """
        Use phi_2 to test the null hypothesis that the data is generated by model (a)
        against the alternative that model (c) is the 'true' model.
        H0) a_0 = \gamma = a_2 = 0
    
        Dicky Fuller (1981) critical values for Φ_2 are:
                Empirical Distribution of Φ_2  
        alpha          0.01  0.025  0.05  0.10
        Sample_Size_T
        25             4.67   5.68  6.75  8.21
        50             4.31   5.13  5.94  7.02
        100            4.16   4.88  5.59  6.50
        250            4.07   4.75  5.40  6.22
        500            4.05   4.71  5.35  6.15
        ∞              4.03   4.68  5.31  6.09
    
        Parameters:
        - df: pd.DataFrame
            The input DataFrame containing the time series data.
        - critical_value: float, optional
           The critical value for hypothesis testing (default: 5.59).
        - r: int, optional
            The number of restrictions in the null hypothesis (default: 3).
        - alpha: float, optional
           The significance level (default: 0.05).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()
        rho_list = []
        no_rho_list = []
        
    
        if cols_norho is None:
            df_sliced = df
        else:
            df_sliced =  df[cols_norho]

        T = len(df_sliced)

        for col in df_sliced:
        # model c: unrestricted
            adf_c = ADF(df_sliced[col], trend='ct')
            reg_res_c = adf_c.regression
            SSR_u = reg_res_c.resid.dot(reg_res_c.resid)
            k = len(reg_res_c.params)

            # model a: restricted
            adf_a = ADF(df_sliced[col], trend='n')
            reg_res_a = adf_a.regression
            SSR_r = reg_res_a.resid.dot(reg_res_a.resid)
            phi_2_val = ((SSR_r - SSR_u) / r) / (SSR_u / (T - k))

            reject_H0 = phi_2_val > critical_value
            if reject_H0:
               rh0[col] = df_sliced[col]
               rho_list.append(col)
            else:
               no_rh0[col] = df_sliced[col]
               no_rho_list.append(col)

            return {'rh0': rh0, 'no_rh0': no_rh0, 'rho_list': rho_list, 'no_rho_list': no_rho_list }

    @staticmethod
    def phi_3(df, critical_value=7.44, r=2, alpha=0.05, cols_norho=None):
        """
        Use phi_3 to test the null hypothesis that the data is generated by model (b)
        against the alternative that model (c) is the 'true' model.
        H0) \gamma = a_2 = 0
        
        Dicky Fuller (1981) critical values for Φ_3 are:
            Empirical Distribution of Φ_3 
        alpha          0.01  0.025  0.05   0.10
        Sample_Size_T
        25             5.91   7.24  8.65  10.61
        50             5.61   6.73  7.81   9.31
        100            5.47   6.49  7.44   8.73
        250            5.39   6.34  7.25   8.43
        500            5.36   6.30  7.20   8.34
        ∞              5.34   6.25  7.16   8.27

        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: 7.44).
        - r: int, optional
            The number of restrictions in the null hypothesis (default: 2).
        - alpha: float, optional
            The significance level (default: 0.05).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        T=len(df)
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()
        rh0_list=[]
        no_rh0_list=[]
        
        if cols_norho is None:
            df_sliced =df
        else:
            df_sliced = df[cols_norho]

        for col in cols_norho:
            # model c: unrestricted
            adf_c = ADF(df_sliced[col], trend='ct')
            reg_res_c = adf_c.regression
            SSR_u = reg_res_c.resid.dot(reg_res_c.resid)
            k = len(reg_res_c.params)

            # model b: restricted
            adf_b = ADF(df_sliced[col], trend='c')
            reg_res_b = adf_b.regression
            SSR_r = reg_res_b.resid.dot(reg_res_b.resid)
            phi_3 = ((SSR_r - SSR_u) / r) / (SSR_u / (T - k))

            reject_H0 = phi_3 > critical_value
            if reject_H0:
                rh0[col] = df_sliced[col]
                rh0_list.append(col)
            else:
                no_rh0[col] = df_sliced[col]
                no_rh0_list.append(col)

        return {'rh0': rh0, 'no_rh0': no_rh0, 'rho_list': rh0_list, 'no_rho_list': no_rh0_list }
    
    @staticmethod
    def tau_mu(df, critical_value=-2.90, return_values=None):
        """
        Model (b): constant but no time trend (a2 = 0)
        H0) \gamma = 0
        The τµ statistic: Constant but No Time Trend (a2 = 0)  
        alpha          0.01  0.025  0.05  0.10
        Sample_Size_T
        25            -3.75  -3.33 -2.99 -2.62
        50            -3.59  -3.22 -2.93 -2.60
        100           -3.50  -3.17 -2.90 -2.59
        250           -3.45  -3.14 -2.88 -2.58
        500           -3.44  -3.13 -2.87 -2.57
        ∞             -3.42  -3.12 -2.86 -2.57

        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: -2.90).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()
        rh0_list=[]
        no_rh0_list=[]
        tau_mu_values = {}

        for col in df.columns:
            adf_b = ADF(df[col], trend='c')
            reg_res_b = adf_b.regression
            tau_mu = reg_res_b.tvalues[0]
            tau_mu_values[col] = tau_mu
            reject_c = tau_mu < critical_value
            if reject_c:
                rh0[col] = df[col]
                rh0_list.append(col)
            else:
                no_rh0[col] = df[col]
                no_rh0_list.append(col)
            rho_count = len(rh0_list)  # Number of columns that reject the null hypothesis
            no_rho_count = len(no_rh0_list)  # Number of columns that do not reject the null hypothesis
            
        # Default to return all if return_values is not specified
        if return_values is None:
            return_values = ['rh0', 'no_rh0', 'tau_mu', 'rho_count', 'no_rho_count', 'rh0_list', 'no_rh0_list']

        output = []
        if 'rh0' in return_values:
            output.append(rh0)
        if 'no_rh0' in return_values:
            output.append(no_rh0)
        if 'tau_mu' in return_values:
            output.append(tau_mu_values)
        if 'rho_count' in return_values:
            output.append(rho_count)
        if 'no_rho_count' in return_values:
            output.append(no_rho_count)
        if 'rh0_list' in return_values:
            output.append(rh0_list)
        if 'no_rh0_list' in return_values:
            output.append(no_rh0_list)
        # If only one value is to be returned, return it directly instead of as a tuple
        if len(output) == 1:
            return output[0]

        return tuple(output) # Return a tuple of all requested values  
        
    @staticmethod
    def phi_1(df, critical_value=5.57, r=2, alpha=0.05, cols_norho=None, return_values=None):
        """
        Use phi_1 to test the null hypothesis that the data is generated by model (a)
        against the alternative that model (b) is the 'true' model.
        H0) \gamma = a_0 = 0

        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: 5.57).
        - r: int, optional
            The number of restrictions in the null hypothesis (default: 2).
        - alpha: float, optional
            The significance level (default: 0.05).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()
        rh0_list=[]
        no_rh0_list=[]
        phi_1_values = {}
        
        T=len(df)
        if cols_norho is None:
            df_sliced = df
        else:
            df_sliced =  df[cols_norho]

        for col in df_sliced:
            # model b: unrestricted
            adf_b = ADF(df_sliced[col], trend='c')
            reg_res_b = adf_b.regression
            SSR_u = reg_res_b.resid.dot(reg_res_b.resid)
            k = len(reg_res_b.params)

            # model a: restricted
            adf_a = ADF(df_sliced[col], trend='n')
            reg_res_a = adf_a.regression
            SSR_r = reg_res_a.resid.dot(reg_res_a.resid)
            phi_1 = ((SSR_r - SSR_u) / r) / (SSR_u / (T - k))
            phi_1_values[col] = phi_1

            reject_H0 = phi_1 > critical_value
            if reject_H0:
                rh0[col] = df_sliced[col]
                rh0_list.append(col)
            else:
                no_rh0[col] = df_sliced[col]
                no_rh0_list.append(col)
            rho_count = len(rh0_list)
            no_rho_count = len(no_rh0_list)
        # Default to return all if return_values is not specified
        if return_values is None:
            return_values = ['rh0', 'no_rh0', 'phi_1', 'rho_count', 'no_rho_count', 'rh0_list', 'no_rh0_list']

        output = []
        if 'rh0' in return_values:
            output.append(rh0)
        if 'no_rh0' in return_values:
            output.append(no_rh0)
        if 'phi_1' in return_values:
            output.append(phi_1_values)
        if 'rho_count' in return_values:
            output.append(rho_count)
        if 'no_rho_count' in return_values:
            output.append(no_rho_count)
        if 'rh0_list' in return_values:
            output.append(rh0_list)
        if 'no_rh0_list' in return_values:
            output.append(no_rh0_list)
        # If only one value is to be returned, return it directly instead of as a tuple
        if len(output) == 1:
            return output[0]

        return tuple(output)
    
    @staticmethod
    def a_0_t(df, cols_rho=None, alpha=0.05, return_values=None):
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()
        rh0_list = []
        no_rh0_list = []
        
        if cols_rho is None:
            df_sliced = df.copy()
        else:
            df_sliced = df[cols_rho].copy()

        for col in df_sliced.columns:
            # Compute the differenced series for the column
            df_sliced['delta_y'] = df_sliced[col].diff().dropna()

            # Perform ADF test
            adf_test = ADF(df_sliced['delta_y'].dropna(),trend='c' )

            print(f"Results for column {col}:")
            print('ADF Statistic:', adf_test.stat)
            print('p-value:', adf_test.pvalue)
            print('Used lag:', adf_test.lags)
            
            

            # Check if a0 = 0 using the t-distribution
            if adf_test.pvalue <= alpha:
                rh0[col] = df_sliced[col]
                rh0_list.append(col)
            else:
                no_rh0[col] = df_sliced[col]
                no_rh0_list.append(col)
        return {'rho_list': rh0_list, 'no_rho_list': no_rh0_list} 


    @staticmethod
    def tau(df, critical_value=-1.95, cols_no_rho=None, alpha=0.05):
        """
        Model (a): Constant Only (a1 = 0, a2 = 0)
        H0) \gamma = 0

        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: -1.95).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()
        rh0_list=[]
        no_rh0_list=[]
        
        if cols_no_rho is None:
            df_sliced = df.copy()
        else:
            df_sliced = df[cols_no_rho].copy()

        for col in df_sliced.columns:
            adf = ADF(df_sliced[col], trend='n')
            reg_res = adf.regression
            tau = reg_res.tvalues[0]
            reject_c = tau < critical_value
            if reject_c:
                rh0[col] = df[col]
                rh0_list.append(col)
            else:
                no_rh0[col] = df[col]
                no_rh0_list.append(col)

        return {'rh0': rh0,'no_rh0': no_rh0,'rho_list': rh0_list, 'no_rho_list': no_rh0_list}      
    