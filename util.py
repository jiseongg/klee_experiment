import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def solver_data_parser(filepath):
    # valid, success, elapsed, type
    success = []
    validityResults = []
    initialValuesResults = []
    valueResults = []
    truthResults = []
    elapsed_times = []
    query_types = []

    try:
        f = open(filepath, 'r')
        for line in f.readlines():
            if "OK" in line:
                success.append(1)
            elif "FAIL" in line:
                success.append(0)
                validityResults.append(None)
                initialValuesResults.append(None)
                valueResults.append(None)
                truthResults.append(None)
                
            if "Validity: " in line:
                validityResults.append(int(line[14:-1]))
                initialValuesResults.append(None)
                valueResults.append(None)
                truthResults.append(None)
                
            if "Solvable: false" in line:
                initialValuesResults.append(0)
                validityResults.append(None)
                valueResults.append(None)
                truthResults.append(None)
            elif "Solvable: true" in line:
                initialValuesResults.append(1)
                validityResults.append(None)
                valueResults.append(None)
                truthResults.append(None)
                
            if "Is Valid: false" in line:
                truthResults.append(0)
                validityResults.append(None)
                initialValuesResults.append(None)
                valueResults.append(None)
            elif "Is Valid: true" in line:
                truthResults.append(1)
                validityResults.append(None)
                initialValuesResults.append(None)
                valueResults.append(None)

            if "Result: " in line:
                valueResults.append(int(line[12:-1]))
                validityResults.append(None)
                initialValuesResults.append(None)
                truthResults.append(None)

            if "Elapsed:" in line:
                elapsed_times.append(float(line[-14:-2]))
            
            if "Type: Value" in line:
                query_types.append("Value")
            elif "Type: InitialValues" in line:
                query_types.append("InitialValues")
            elif "Type: Truth" in line:
                query_types.append("Truth")
            elif "Type: Validity" in line:
                query_types.append("Validity")
                
        f.close()

    except FileNotFoundError:
        print('No such file or directory: %s' % filepath)
        return None


    return (success, validityResults, initialValuesResults, valueResults,
            truthResults, elapsed_times, query_types)

def summarize_data(df):
    print('total queries: ', df.shape[0])
    print('failed queries: ', df[df['success'] == 0].shape[0])
    print('succeeded queries: ', df[df['success'] == 1].shape[0])
    print('Type: Validity ', df[df['query_types'] == 'Validity'].shape[0])
    print('|-- Validity: -1 ', df[df['validityResults'] == -1].shape[0])
    print('|-- Validity: 0 ', df[df['validityResults'] == 0].shape[0])
    print('|-- Validity: 1 ', df[df['validityResults'] == 1].shape[0])
    print('==========================')
    print('Type: InitialValues ', df[df['query_types'] == 'InitialValues'].shape[0])
    print('|-- Solvable: false ', df[df['initialValuesResults'] == 0].shape[0])
    print('|-- Solvable: true ', df[df['initialValuesResults'] == 1].shape[0])
    print('==========================')
    print('Type: Truth: ', df[df['query_types'] == 'Truth'].shape[0])
    print('|-- Is Valid - false', df[df['truthResults'] == 0].shape[0])
    print('|-- Is Valid - true', df[df['truthResults'] == 1].shape[0])
    print('==========================')
    print('Type: Value: ', df[df['query_types'] == 'Value'].shape[0])
    
    fig, axes = plt.subplots(4, 3, figsize=(15, 25))
    fig.delaxes(axes[3, 2])

    df.hist(column='elapsed_times', bins=30, ax=axes[0, 0])
    axes[0, 0].set_title('total queries(mean: %.4fs, sum : %.4fs)' %
                         (df['elapsed_times'].mean(), df['elapsed_times'].sum()))
    axes[0, 0].set_xlabel('elapsed times')
    axes[0, 0].set_ylabel('count')

    df[df['success'] == 0].hist(column='elapsed_times', bins=30, ax=axes[0, 1])
    axes[0, 1].set_title('Failed queries (mean: %.4fs, sum: %.4fs)' %
                         (df[df['success'] == 0]['elapsed_times'].mean(),
                          df[df['success'] == 0]['elapsed_times'].sum()))
    axes[0, 1].set_xlabel('elapsed times')
    axes[0, 1].set_ylabel('count')

    df[df['success'] == 1].hist(column='elapsed_times', bins=30, ax=axes[0, 2])
    axes[0, 2].set_title('Succeeded queries (mean: %.4fs, sum: %.4fs)' %
                         (df[df['success'] == 1]['elapsed_times'].mean(),
                          df[df['success'] == 1]['elapsed_times'].sum()))
    axes[0, 2].set_xlabel('elapsed times')
    axes[0, 2].set_ylabel('count')

    df[df['validityResults'] == -1].hist(column='elapsed_times', bins=30, ax=axes[1, 0])
    axes[1, 0].set_title('Validity: -1 (mean: %.4fs, sum: %.4fs)' %
                         (df[df['validityResults'] == -1]['elapsed_times'].mean(),
                          df[df['validityResults'] == -1]['elapsed_times'].sum()))
    axes[1, 0].set_xlabel('elapsed times')
    axes[1, 0].set_ylabel('count')

    df[df['validityResults'] == 0].hist(column='elapsed_times', bins=30, ax=axes[1, 1])
    axes[1, 1].set_title('Validity: 0 (mean: %.4fs, sum: %.4fs)' %
                         (df[df['validityResults'] == 0]['elapsed_times'].mean(),
                          df[df['validityResults'] == 0]['elapsed_times'].sum()))
    axes[1, 1].set_xlabel('elapsed times')
    axes[1, 1].set_ylabel('count')

    df[df['validityResults'] == 1].hist(column='elapsed_times', bins=30, ax=axes[1, 2])
    axes[1, 2].set_title('Validity: 1 (mean: %.4fs, sum: %.4fs)' %
                         (df[df['validityResults'] == 1]['elapsed_times'].mean(),
                          df[df['validityResults'] == 1]['elapsed_times'].sum()))
    axes[1, 2].set_xlabel('elapsed times')
    axes[1, 2].set_ylabel('count')

    df[df['initialValuesResults'] == 0].hist(column='elapsed_times', bins=30, ax=axes[2, 0])
    axes[2, 0].set_title('Solvable: false (mean: %.4fs, sum: %.4fs)' %
                         (df[df['initialValuesResults'] == 0]['elapsed_times'].mean(),
                          df[df['initialValuesResults'] == 0]['elapsed_times'].sum()))
    axes[2, 0].set_xlabel('elapsed times')
    axes[2, 0].set_ylabel('count')

    df[df['initialValuesResults'] == 1].hist(column='elapsed_times', bins=30, ax=axes[2, 1])
    axes[2, 1].set_title('Solvable: true (mean: %.4fs, sum: %.4fs)' %
                         (df[df['initialValuesResults'] == 1]['elapsed_times'].mean(),
                          df[df['initialValuesResults'] == 1]['elapsed_times'].sum()))
    axes[2, 1].set_xlabel('elapsed times')
    axes[2, 1].set_ylabel('count')
    
    df[df['query_types'] == 'Value'].hist(column='elapsed_times', bins=30, ax=axes[2, 2])
    axes[2, 2].set_title('Type: Value (mean: %.4fs, sum: %.4fs)' %
                         (df[df['query_types'] == 'Value']['elapsed_times'].mean(),
                          df[df['query_types'] == 'Value']['elapsed_times'].sum()))
    axes[2, 2].set_xlabel('elapsed times')
    axes[2, 2].set_ylabel('count')

    df[df['truthResults'] == 0].hist(column='elapsed_times', bins=30, ax=axes[3, 0])
    axes[3, 0].set_title('Is Valid: false (mean: %.4fs, sum: %.4fs)' %
                         (df[df['truthResults'] == 0]['elapsed_times'].mean(),
                          df[df['truthResults'] == 0]['elapsed_times'].sum()))
    axes[3, 0].set_xlabel('elapsed times')
    axes[3, 0].set_ylabel('count')

    df[df['truthResults'] == 1].hist(column='elapsed_times', bins=30, ax=axes[3, 1])
    axes[3, 1].set_title('Is Valid: true (mean: %.4fs, sum: %.4fs)' %
                         (df[df['truthResults'] == 1]['elapsed_times'].mean(),
                          df[df['truthResults'] == 1]['elapsed_times'].sum()))
    axes[3, 1].set_xlabel('elapsed times')
    axes[3, 1].set_ylabel('count')