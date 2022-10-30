import matplotlib.pyplot as plt
import seaborn as sns


def nan_bar_plot(dataframe):
    missingrows = dataframe.isnull().sum()
    sf = missingrows.loc[lambda x : x > 0]
    sns.barplot(x= sf.index, y=sf.values, palette="Spectral")