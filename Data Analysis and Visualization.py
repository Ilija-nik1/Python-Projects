import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_data(filename):
    try:
        data = pd.read_csv(filename)
        return data
    except FileNotFoundError:
        print("Error: File not found.")
        return None

def calculate_mean(data, column_name):
    if column_name not in data.columns:
        print("Error: Column not found in the data.")
        return None
    mean_value = data[column_name].mean()
    return mean_value

def plot_histogram(data, column_name):
    sns.histplot(data[column_name], kde=True)
    plt.title(f'Distribution of {column_name}')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.show()

def generate_summary_statistics(data):
    summary = data.describe()
    return summary

def plot_boxplot(data, column_name):
    sns.boxplot(data[column_name])
    plt.title(f'Boxplot of {column_name}')
    plt.xlabel('Values')
    plt.show()

def plot_scatter(data, x_column, y_column):
    sns.scatterplot(data=data, x=x_column, y=y_column)
    plt.title(f'Scatter plot: {x_column} vs {y_column}')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.show()

def calculate_correlation(data, column1, column2):
    if column1 not in data.columns or column2 not in data.columns:
        print("Error: One or both columns not found in the data.")
        return None
    correlation = data[column1].corr(data[column2])
    return correlation

# Read the data from a CSV file
data = read_data('data.csv')

# Perform data analysis and visualization
# Example: Calculate the mean, plot a histogram, generate summary statistics, plot a boxplot, plot a scatter plot, and calculate correlation

if data is not None:
    # Select the column to analyze
    column_name = 'column_name'

    # Calculate the mean
    mean_value = calculate_mean(data, column_name)
    if mean_value is not None:
        print(f"Mean: {mean_value}")

    # Plot a histogram
    plot_histogram(data, column_name)

    # Generate summary statistics
    summary_stats = generate_summary_statistics(data)
    print(summary_stats)

    # Plot a boxplot
    plot_boxplot(data, column_name)

    # Plot a scatter plot
    x_column = 'x_column'
    y_column = 'y_column'
    plot_scatter(data, x_column, y_column)

    # Calculate correlation
    correlation = calculate_correlation(data, x_column, y_column)
    if correlation is not None:
        print(f"Correlation between {x_column} and {y_column}: {correlation}")