import sys
import matplotlib.pyplot as plt
import pandas as pd

def main(input_file,output_file,graph_file):
    print("--START--")
    # Read the data from JSON file
    eva_data = read_json_to_dataframe(input_file)

    # Convert and export data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    # Sort dataframe by date ready to be plotted (date values are on x-axis)
    eva_data.sort_values('date', inplace=True)

    # Calculate cumulative time spent in space over years
    eva_data_new = add_duration_hours(eva_data)
    eva_data_new['cumulative_time'] = eva_data_new['duration_hours'].cumsum()

    # Plot
    plot_cumulative_duration_vs_date(eva_data_new['date'],eva_data_new['cumulative_time'],graph_file)

    print("--END--")

def read_json_to_dataframe(input_file):
    """
    Read a .json file into a pandas dataframe
    Args:
        input_file: (str) input file name, expects .json file extension
    Returns:
        eva_df: pandas dataframe
    """
    print(f'Reading JSON file {input_file}')
    # Read the data from a JSON file into a Pandas dataframe
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
    eva_df['eva'] = eva_df['eva'].astype(float)
    # Clean the data by removing any rows where duration is missing
    eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)
    return eva_df

def write_dataframe_to_csv(df, output_file):
    """
    Converts a pandas dataframe to a .csv file
    Args:
        df: (pandas dataframe) input dataframe to be converted
        output_file: (str) output file name - should be a .csv
    Returns
        N/A
    """
    print(f'Saving to CSV file {output_file}')
    # Save dataframe to CSV file for later analysis
    df.to_csv(output_file, index=False, encoding='utf-8')

def add_duration_hours(df):
    """
    Add duration in hours variable to the dataset
    Args:
        df: (pandas dataframe) input dataframe
    Returns:
        df_copy: (pandas dataframe) copy of input with new
        duration_hours column
    """
    df_copy = df.copy()
    df_copy['duration_hours'] = df_copy['duration'].apply(text_to_duration)
    return df_copy

def text_to_duration(duration):
    """
    Convert text format duration HH:MM to duration in hours
    Args:
        duration: (str) Input text-format HH:MM duration
    Returns:
        duration_hours: (float) Duration in hours
    """
    hours,minutes = duration.split(':')
    duration_hours = int(hours) + int(minutes)/6 # intentional error
    return duration_hours

def plot_cumulative_duration_vs_date(x,y,output_file):
    """
    Plots the cumulative spacewalk time vs year
    Args:
        x: (pandas dataframe column) date
        y: (pandas dataframe column) cumulative spacewalk time
        output_file: (str) file name for pyplot output image
    Returns:
        N/A
    """
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('Year')
    ax.set_ylabel('Total time spent in space to date (hours)')

    print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
    ax.plot(x,y,'ko-')

    plt.tight_layout()
    plt.savefig(output_file,bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        # use default file names
        input_file = './data/eva_data.json'
        output_file = './results/eva_data.csv'
        print('Using default input and output filenames')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print('Using input and output filenames from command line')
    graph_file = './figs/cumulative_eva_graph.png'

    main(input_file,output_file,graph_file)
