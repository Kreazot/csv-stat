import pandas as pd
from pandas import DataFrame as DF

from .consts import REQUIRED_COLUMNS
from .exceptions import NotValidException


def check_column(csv_file) -> None:
    """Проверка наличия необходимых столбцов в csv."""
    df_cols = pd.read_csv(csv_file, nrows=0, sep=';')
    df_cols_list = df_cols.columns.tolist()
    for column in REQUIRED_COLUMNS:
        if column not in df_cols_list:
            raise NotValidException(
                f'В наборе данных отсутствует колонка: {column}')


def amount_of_profit(df: DF) -> float:
    """Подсчет общего профита."""
    return df['Profit'].sum().round(2)


def best_top(df: DF, size: int) -> None:
    """
    Выводит в STDOUT топ лучших продуктов.
    (продажи, количества продаж, профита)
    """
    best_sales = products_stats(df, column='Sales', asc=False, size=size)
    best_quantity = products_stats(df, column='Quantity', asc=False, size=size)
    best_profit = products_stats(df, column='Profit', asc=False, size=size)

    print(f'\nЛучшие по продажам:\n{best_sales}')
    print(f'\nЛучшие по количеству продаж:\n{best_quantity}')
    print(f'\nЛучшие по профиту:\n{best_profit}')


def worst_top(df: DF, size: int) -> None:
    """
    Выводит в STDOUT топ худших продуктов.
    (продажи, количества продаж, профита)
    """
    worst_sales = products_stats(df, column='Sales', asc=True, size=size)
    worst_quantity = products_stats(df, column='Quantity', asc=True, size=size)
    worst_profit = products_stats(df, column='Profit', asc=True, size=size)

    print(f'\nХудшие по продажам:\n{worst_sales}')
    print(f'\nХудшие по количеству продаж:\n{worst_quantity}')
    print(f'\nХудшие по профиту:\n{worst_profit}')


def delivery_period_stats(df: DF) -> None:
    """
    Выводит в STDOUT средний срок доставки и стандартное отклонение от него.
    """
    df['Delevery Period'] = df['Ship Date'] - df['Order Date']

    # среднее время доставки и стандартное отклонение
    avg_delivery_period = df['Delevery Period'].mean()
    std_delivery_period = df['Delevery Period'].std()

    print(f'\nCредний срок доставки товара клиенту:\n{avg_delivery_period}')
    print(
        f'\nCтандартное отклонение от среднего срока доставки:'
        f'\n{std_delivery_period}'
    )


def save_result_stats_to_csv(df: DF, file_name: str) ->None:
    """
    Сохранение продажи, количество продаж и профит по каждому продукту в csv.
    """
    print(f'\nСохраняем данные по продажам, количеству продаж'
          f' и профит по каждому продукту в файл {file_name}')

    df.groupby('Product Name')['Sales', 'Quantity', 'Profit'].sum()\
        .to_csv(file_name, sep=';')


def products_stats(df: DF, column: str, asc: bool, size: int) -> DF:
    """
    Группировка продуктов и сортировка по дополнительной колонке.
    :param df: исходный DataFrame
    :param column: серия по которой необходимо сортировать
    :param asc: параметр сортировки
    :param size: количество выводимых продуктов
    :return: DataFrame
    """
    return df.groupby('Product Name')[column].\
        sum().sort_values(ascending=asc).head(size)
