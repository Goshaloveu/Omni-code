import pandas as pd


def get_test(path: str, test: str) -> str:
    df = pd.read_excel(path, header=None)

    data = df.iloc[int(test)-1]

    res = f"""Вход - {data.iloc[0]}
Выход - {data.iloc[1]}"""
    
    return res
