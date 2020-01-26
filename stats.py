import click
import pandas as pd

from helpers.common import (
    check_column,
    amount_of_profit,
    best_top,
    worst_top,
    delivery_period_stats,
    save_result_stats_to_csv,
)
from helpers.exceptions import NotValidException


@click.command()
@click.option('--csv_data', '-cd', default='example.csv', help='Файл с исходными данными.')
@click.option('--top_size', '-ts', default=10, help='Количество данных в топах.')
@click.option('--save_result', '-sr', default='result.csv', help='Имя файла для сохранения статистики.')
def main(csv_data, top_size, save_result):
    try:
        check_column(csv_data)
        df = pd.read_csv(
            csv_data,
            sep=';',
            decimal=',',
            parse_dates=['Order Date', 'Ship Date'],
            index_col='Row ID'
        )

        all_profit = amount_of_profit(df)
        print(f'Общий профит: {all_profit}')

        best_top(df, size=top_size)
        worst_top(df, size=top_size)
        delivery_period_stats(df)
        save_result_stats_to_csv(df, save_result)

    except (NotValidException, Exception) as e:
        print(f'Ошибка: {e}')


if __name__ == '__main__':
    main()
