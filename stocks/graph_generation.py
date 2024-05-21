#!/usr/bin/env python3

"""
graph_generation.py
---------

Parses the pdf file and extracts the table from the mentioned page based on search criteria

Functions:
- graph_generation: Brief description of what the function does.

"""

import matplotlib.pyplot as plt
import seaborn as sns

def graph_generation(df):
    """
    Brief description of the function's purpose.

    Parameters:
    param1 (type): Description of the first parameter.
    param2 (type): Description of the second parameter.

    Returns:
    type: Description of the return value.
    """
    # Bar plot using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(df['Category'], df['Value'], color='skyblue')
    plt.title('Values by Category')
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

    # Bar plot using Seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Category', y='Value', data=df, palette='viridis')
    plt.title('Values by Category')
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.show()

    # Pie chart using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.pie(df['Value'], labels=df['Category'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis', len(df)))
    plt.title('Value Distribution by Category')
    plt.show()
