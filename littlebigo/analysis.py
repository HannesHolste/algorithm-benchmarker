import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def df_from_benchmarks(benchmarks_db, extract_input_size):
    df = pd.DataFrame(
        columns=['id',
                 'group_id',
                 'input_size',
                 'cpu_kernel_time_secs',
                 'cpu_user_time_secs',
                 'resident_set_memory_kb',
                 'wall_time_secs'])

    # Populate dataframe with timing information from database
    i = 0
    for benchmark in benchmarks_db.all():
        if benchmark['timing_result'] is not None:
            row = ([benchmark['id'],
                    benchmark['group_id'],
                    extract_input_size(benchmark['command_with_param']),
                    benchmark['timing_result']['cpu_kernel_time_secs'],
                    benchmark['timing_result']['cpu_user_time_secs'],
                    benchmark['timing_result']['resident_set_memory_kb'],
                    benchmark['timing_result']['wall_time_secs']])
            df.loc[i] = row
            i += 1

    # Unit conversions and new columns
    df['resident_set_memory_kb'] = df['resident_set_memory_kb'].astype(int)
    df['input_size'] = df['input_size'].astype(int)

    # Introduce new columns
    df['cpu_time_total_secs'] = df['cpu_user_time_secs'] + df[
        'cpu_kernel_time_secs']
    df['resident_set_memory_mb'] = (df['resident_set_memory_kb'] /
                                    1000).astype(float)
    return df


def df_from_benchmarks_aggregated(benchmarks_db, extract_input_size):
    df = df_from_benchmarks(benchmarks_db, extract_input_size)

    cols_with_errorbars = ['cpu_kernel_time_secs',
                           'cpu_user_time_secs',
                           'resident_set_memory_kb',
                           'wall_time_secs',
                           'cpu_time_total_secs',
                           'resident_set_memory_mb']

    # Calculate info for error bars for each col in cols_with_errorbars
    df_final = pd.DataFrame()
    for col in cols_with_errorbars:
        # calculate mean and std
        df_errors = (df.groupby(['input_size'], as_index=False)[col]
                     .agg({'{}_mean'.format(col): np.mean,
                           '{}_std'.format(col): np.std})
                     .sort_values(by=['{}_mean'.format(col)]))

        # ensure that 'input_size' column is not duplicated
        cols_to_use = df_errors.columns.difference(df_final.columns)
        df_final = pd.concat([df_final, df_errors[cols_to_use]], axis=1)
    return df_final


def generate_plot(df, y_name, y_std_name=None):
    x = df['input_size']
    y = df[y_name]
    plt.scatter(x, y)
    plt.ylim(0)
    if y_std_name is not None:
        plt.errorbar(x, y, yerr=(df[y_std_name]))
    return plt
