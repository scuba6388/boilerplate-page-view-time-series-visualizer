import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
filter = df.quantile([0.025, 0.975])

# Filter the DataFrame for values in the top 2.5%
df = df[df['value'] > filter.iloc[0]['value']]
df = df[df['value'] <= filter.iloc[1]['value']]

def draw_line_plot():
    # Draw line plot
    df1 = df.copy()
    ax1 = df1.plot(
        use_index=True, 
        kind='line', 
        title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
        xlabel='Date',
        ylabel='Page Views',
        color='red',
        figsize=(32,10))
    
    ax1.autoscale(enable=True)

    # Get figure
    fig1 = ax1.get_figure()

    # Save image and return fig (don't change this part)
    fig1.savefig('line_plot.png')
    return fig1

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['Year'] = [d.year for d in df_bar['date']]
    df_bar['MonthNum'] = [d.month for d in df_bar['date']]
    df_bar['Month'] = [d.strftime('%B') for d in df_bar['date']]
    df_bar = pd.pivot_table(df_bar, index=['Year'], columns=['Month', 'MonthNum'], values=['value'], aggfunc='mean')
    df_bar = df_bar.sort_values('MonthNum', axis=1)
    df_bar = df_bar.droplevel(level=[0, 'MonthNum'], axis=1)

    # Draw bar plot
    ax2 = df_bar.plot(
        kind='bar', 
        title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
        xlabel='Years',
        ylabel='Average Page Views',
        figsize=(12, 10))

    # Get figure
    fig2 = ax2.get_figure()

    # Save image and return fig (don't change this part)
    fig2.savefig('bar_plot.png')
    return fig2

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]
    df_box['MonthNum'] = [d.month for d in df_box['date']]

    # Draw box plots (using Seaborn)
    fig3, ax3 = plt.subplots(nrows=1, ncols=2, figsize=(28, 10))
    
    sns.boxplot(ax=ax3[0], data=df_box, x='Year', y='value', hue='Year', legend=False, orient='v')
    ax3[0].set_title('Year-wise Box Plot (Trend)')
    ax3[0].set_xlabel('Year')
    ax3[0].set_ylabel('Page Views')

    df_box.sort_values('MonthNum', inplace=True)
    sns.boxplot(ax=ax3[1], data=df_box, x='Month', y='value', hue='Month', legend=False, orient='v')
    ax3[1].set_title('Month-wise Box Plot (Seasonality)')
    ax3[1].set_xlabel('Month')
    ax3[1].set_ylabel('Page Views')

    fig3.show()

    # Save image and return fig (don't change this part)
    fig3.savefig('box_plot.png')
    return fig3
