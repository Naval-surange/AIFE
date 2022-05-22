import pandas as pd
import numpy as np
import streamlit as st


class DataLoader:
    def load_data(method, aws_bucket=None, access_key=None, secret_access=None, session_token=None, file_name=None):

        if file_name.name.endswith("csv"):
            df = pd.read_csv(file_name, header=0, skip_blank_lines=True)
        elif file_name.name.endswith("tsv"):
            df = pd.read_csv(file_name, sep="\t", header=0,
                             skip_blank_lines=True)
        elif file_name.name.endswith("xls") or file_name.name.endswith("xlsx"):
            df = pd.read_excel(file_name, header=0)

        re_index_flag = False
        nan_flag = False

        while(str(df.columns[0]).startswith("Unnamed")):
            df.columns = df.iloc[0]
            df = df.iloc[1:, ].reindex()
            re_index_flag = True

        if(df.isnull().values.any()):
            nan_flag = True

        df.fillna(df.mean(), inplace=True)
        df = df.select_dtypes([np.number])

        if(re_index_flag or nan_flag):
            msg = "Note: Data reindexing has been performed, NAN values are replaced with mean value for the column and non catagorical columns have been dropped."
            st.info(msg)

        return df
