import pandas as pd

class DataLoader:
    def load_data(method,aws_bucket=None,access_key=None,secret_access=None,session_token=None,file_name=None):

        if file_name.name.endswith("csv"):
            df = pd.read_csv(file_name,header=0)
        elif file_name.name.endswith("tsv"):
            df = pd.read_csv(file_name,sep="\t",header=0)
        elif file_name.name.endswith("xls") or file_name.name.endswith("xlsx"):
            df = pd.read_excel(file_name,header=0)


        return df
