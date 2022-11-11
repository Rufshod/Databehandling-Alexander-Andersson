# a function to get the between two columns
def percentage_func(df, column: str, lst, column2 = "NA",):
    """Function to get precentages out of a Dataframe and save it to a list.
    column2 can be used when you need percentages between two columns."""
    if column2 == "NA":
        col_sum = df[column].sum()
        for i in range(len(df[column])):
            lst.append(round(df[column][i] / col_sum*100))
    else:
        col_sum2 = df[column2].sum()
        for i in range(len(df[column])):
            lst.append(round(df[column][i] / col_sum2 *100))