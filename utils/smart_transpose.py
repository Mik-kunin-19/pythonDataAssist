class IntegrateAndPrepareDf():
    def __init__(self, df):
        self.df=df
    def changeOrientation(self, old_first_col_name, new_first_col_name, trim_sample_names=False, separator="_\d+"):
        """
        Description:
        This function transposes the input table and brings it's column names to become row values in the first column
        Arguments: 
        1. df -- imported table to be transposed
        2. old_first_col_name -- old name on top of the first column (defining metabolite/gene/protein/etc.. names) which has become the column names
        3. new_first_col_name -- new column to be created as first column containing Groups
        4. trim_sample_names -- Boolean whether to trim sample names in newly created
        column to remove separators of replicates needed to determine between columns.
        When in rows they are normally no longer needed
        default: False
        5. separator -- usually replicates have _1,_2,...,_n numbers "_\d+" means  
        """
        self.df=self.df.T.reset_index()
        self.df.columns=self.df.iloc[0,]
        self.df=self.df.iloc[1:,]
        self.df.index.name = None
        self.df.rename(columns={old_first_col_name : new_first_col_name}, inplace=True)
        if trim_sample_names:
            self.df[new_first_col_name]=self.df[new_first_col_name].str.replace(separator, "", regex=True)
            return self.df
        else:
            return self.df
