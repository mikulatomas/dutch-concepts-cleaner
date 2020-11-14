import os
import pandas as pd

if not os.path.exists('clean_csv'):
    os.makedirs('clean_csv')

for subdir, dirs, files in os.walk('dataset'):
    for file in files:
        filepath = os.path.join(subdir, file)
        if '.CSV' in filepath:
            target_dir = subdir.replace('dataset/cvsdata/', '')
            target_dir = os.path.join('clean_csv', target_dir)
            print(f"Cleaning: {filepath}")
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            if 'exemplar feature judgments' in filepath:
                if 'categoryFeatureImportanceRatings' in filepath or 'exemplarFeatureImportanceRatings' in filepath:
                    df = pd.read_csv(filepath, encoding="ISO-8859-1",
                                     header=None, index_col=1)
                    df = df.dropna(how='all', axis=1)
                    df = df.dropna(how='all', axis=0)
                    df = df.drop(0, axis=1)
                    df.columns = range(len(df.columns))
                    df.index.name = ''
                else:
                    df = pd.read_csv(filepath, encoding="ISO-8859-1",
                                     index_col=1, header=1)
                    df = df.dropna(how='all', axis=1)
                    df = df.dropna(how='all', axis=0)
                    df = df.drop(df.columns[0], axis=1)
                    df.rename({'Unnamed: 2': 'freq'}, inplace=True, axis=1)
                    df = df.reset_index().dropna()
                    df.index = df[df.columns[0]]
                    df = df.drop(df.columns[0], axis=1)
                    df.index.name = ''

            elif 'exemplar judgments' in filepath:
                df = pd.read_csv(filepath, encoding="ISO-8859-1", nrows=1)
                df = df.dropna(how='all', axis=1)
                columns = df.columns
                df = pd.read_csv(filepath, encoding="ISO-8859-1",
                                 usecols=columns, index_col=0)
                df = df.dropna(how='all', axis=1)
                df = df.dropna(how='all', axis=0)
                df = df.drop(df.columns[0], axis=1)

            elif 'pairwise similarities' in filepath:
                if 'Birds' in filepath or 'Clothing' in filepath or 'Fish' in filepath or 'Musical' in filepath or 'Vehicles' in filepath:
                    idx_col = 0
                    headr = 1
                elif 'Fruit' in filepath or 'Professions' in filepath or 'Sports' in filepath or 'Vegetables' in filepath:
                    idx_col = 1
                    headr = 0
                else:
                    idx_col = 1
                    headr = 1

                df = pd.read_csv(
                    filepath, encoding="ISO-8859-1", nrows=2, header=None, index_col=idx_col)
                df = df.dropna(how='all', axis=1)

                columns = df.columns

                df = pd.read_csv(filepath, encoding="ISO-8859-1",
                                 usecols=columns, header=headr, index_col=0)
                try:
                    df = df.drop('exemplar DUTCH', axis=0)
                except:
                    pass

                df.index.name = ''

            df.to_csv(os.path.join(target_dir, os.path.basename(filepath)))
