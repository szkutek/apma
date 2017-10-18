import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv("train.csv")

    # # AD. 3
    df3 = pd.DataFrame(data, columns=['Sex', 'PassengerId'])
    df3 = df3.groupby('Sex').count()
    # df3.plot(kind='pie', subplots=True)
    df3.plot(kind='pie', y='PassengerId', title='male/female proportion of passengers')

    # # AD. 4 scatter plot with fare and age; color by gender
    df4 = pd.DataFrame(data, columns=['Fare', 'Age', 'Sex'])
    colors = {'female': 'red', 'male': 'blue'}
    _, ax = plt.subplots()
    for key, group in df4.groupby('Sex'):
        group.plot.scatter(x='Age', y='Fare', label=key, color=colors[key], ax=ax,
                           title='scatter plot with fare and age')

    # ks = data[data.Sex == 'male']
    # ks2 = data[data.Sex == 'female']
    # 
    # ax2 = ks.plot.scatter(y='Fare', x='Age', color='DarkBlue', label='male')
    # ks2.plot.scatter(y='Fare', x='Age', color='Magenta', label='female', ax=ax2)

    # # AD. 5
    df5 = data['Survived'].sum()

    # # AD. 6 histogram with Fare
    data.plot(kind='hist', y='Fare')

    # # AD. 7 male/female proportion of survivors
    df7 = pd.DataFrame(data, columns=['Survived', 'Sex', 'PassengerId'])
    df7 = df7[df7.Survived == 1].groupby('Sex').count()
    df7.plot(kind='pie', y='PassengerId', title='Proportion of survivors')

    # scatter plot with fare and age; color by gender; for survivors
    df8 = pd.DataFrame(data, columns=['Fare', 'Age', 'Sex', 'Survived'])
    colors = {'female': 'red', 'male': 'blue'}
    _, ax2 = plt.subplots()
    for key, group in df8[df8.Survived == 1].groupby('Sex'):
        group.plot.scatter(x='Age', y='Fare', label=key, color=colors[key], ax=ax2,
                           title='scatter plot with fare and age for survivors')

    print(df5)
    plt.show()
