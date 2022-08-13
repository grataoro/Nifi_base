import numpy as np
import pandas as pd

class sqlTransform:

    def __init__(self,data) -> None:
        self.data = data

    def records(self):
        df = pd.DataFrame(self.data)

        timestamp = list(df.dtypes[df.dtypes == 'datetime64[ns]'].index)
        for i in timestamp:
            df[i] = df[i].astype(str)

        if type(object) in df.dtypes.to_list():  
            df.replace({'NaT': None}, inplace=True)
            
        df.replace({np.nan: None}, inplace=True)
        return df.to_records(index = False).tolist()