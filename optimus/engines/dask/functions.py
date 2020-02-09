# This functions must handle one or multiple columns
# Must return None if the data type can not be handle

import dask.array as da
from dask.array import stats
from dask.dataframe.core import DataFrame

from optimus.helpers.converter import val_to_list


def functions(self):
    class Functions:

        @staticmethod
        def min(columns, args):
            def dataframe_min_(df):
                return {"min": df[columns].min()}

            return dataframe_min_

        @staticmethod
        def max(columns, args):
            def dataframe_max_(df):
                return {"max": df[columns].max()}

            return dataframe_max_

        @staticmethod
        def mean(columns, args):
            def dataframe_mean_(df):
                return {"mean": df[columns].mean()}

            return dataframe_mean_

        @staticmethod
        def variance(columns, args):
            def dataframe_var_(df):
                return {"variance": df[columns].var()}

            return dataframe_var_

        @staticmethod
        def sum(columns, args):

            def dataframe_sum_(df):
                return {"sum": df[columns].sum()}

            return dataframe_sum_

        @staticmethod
        def percentile_agg(columns, args):
            values = args[1]

            def _percentile(df):
                return {"percentile": df[columns].quantile(values)}

            return _percentile

        @staticmethod
        def stddev(col_name, args):
            def _stddev(serie):

                return {"stddev": {col: serie[col].std() for col in col_name}}

            return _stddev

        # @staticmethod
        # def stddev(columns, args):
        #     def dataframe_stddev_(df):
        #         return {"stddev": df[columns].std()}
        #
        #     return dataframe_stddev_

        # @staticmethod
        # def mean(col_name, args):
        #     def _mean(serie):
        #         return {"mean": serie[col_name].mean()}
        #
        #     return _mean
        #
        # @staticmethod
        # def sum(col_name, args):
        #     def std_(serie):
        #         return {"sum": serie[col_name].sum()}
        #
        #     return std_
        #
        # @staticmethod
        # def variance(col_name, args):
        #     def var_(serie):
        #         return {"variance": serie[col_name].var()}
        #
        #     return var_

        @staticmethod
        def zeros_agg(col_name, args):
            col_name = val_to_list(col_name)

            def zeros_(df):
                result = {"zeros": {col: (df[col].values == 0).sum() for col in col_name}}
                # result = {"zeros": (df[col_name].values == 0).sum()}
                return result

            return zeros_

        @staticmethod
        def count_na_agg(columns, args):

            def _count_na_agg(df):
                return {"count_na": df[columns].isnull().sum()}

            return _count_na_agg

        # def hist_agg(col_name, df, buckets, min_max=None, dtype=None):
        @staticmethod
        def hist_agg(col_name, args):
            # {'OFFENSE_CODE': {'hist': [{'count': 169.0, 'lower': 111.0, 'upper': 297.0},
            #                            {'count': 20809.0, 'lower': 3645.0, 'upper': 3831.0}]}}

            def hist_agg_(serie):
                df = args[0]
                bins = args[1]
                min_max = args[2]

                result = {}
                for col in col_name:
                    if min_max is None:
                        # print("HIST AGG", df.cols.range(col_name))
                        min_max = df.cols.range(col_name)[col]

                    i, j = (da.histogram(serie[col], bins=bins, range=[min_max["min"], min_max["max"]]))
                    result = {"hist": {col: {"count": list(i), "bins": list(j)}}}
                return result

            return hist_agg_

        @staticmethod
        def kurtosis(columns, args):
            # Maybe we could contribute with this
            # `nan_policy` other than 'propagate' have not been implemented.

            def _kurtosis(serie):
                result = {"kurtosis": {col: float(stats.kurtosis(serie[col])) for col in columns}}
                # result = {"kurtosis": float(stats.kurtosis(serie[col_name], nan_policy="propagate"))}
                return result

            return _kurtosis

        @staticmethod
        def skewness(columns, args):
            def _skewness(serie):
                result = {"skewness": {col: float(stats.skew(serie[col])) for col in columns}}
                # result = {"skewness": float(stats.skew(serie[col_name], nan_policy="propagate"))}
                return result

            return _skewness

        # @staticmethod
        # def count_uniques_agg(columns, args):
        #
        #     def _count_uniques_agg(df):
        #         return {"count_uniques": df[columns].nunique()}
        #
        #     return _count_uniques_agg

        @staticmethod
        def count_uniques_agg(col_name, args):
            estimate = args[0]

            def _count_uniques_agg(df):

                if estimate is True:
                    # result = {"count_uniques": df[col_name].nunique_approx()}
                    ps = {col: df[col].nunique_approx() for col in col_name}
                    # ps = pd.Series({col: df[col].nunique_approx() for col in df.cols.names()})
                else:
                    ps = {col: df[col].nunique() for col in df.cols.names()}
                result = {"count_uniques": ps}

                return result

            return _count_uniques_agg

        @staticmethod
        def range_agg(columns, args):
            def _dataframe_range_agg_(df):
                return {"min": df[columns].min(), "max": df[columns].max()}

            return _dataframe_range_agg_

        @staticmethod
        def mad_agg(col_name, args):
            more = args[0]

            def _mad_agg(serie):
                median_value = serie[col_name].quantile(0.5)
                mad_value = (serie[col_name] - median_value).abs().quantile(0.5)

                _mad = {}
                if more:
                    result = {"mad": mad_value, "median": median_value}
                else:
                    result = {"mad": mad_value}

                return result

            return _mad_agg

    return Functions()


DataFrame.functions = property(functions)