import sys
import re
import matplotlib.pyplot as plt
import pandas as pd

def main(input_file,output_file,duration_by_astronaut_output_file,graph_file):
    print("--START--")
    # Read the data from JSON file
    eva_data = read_json_to_dataframe(input_file)

    # Calculate and add crew size to data
    eva_data = add_crew_size_column(eva_data) # added this line

    # Convert and export data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    # Calculate summary table for total EVA per astronaut
    duration_by_astronaut_df = summary_duration_by_astronaut(eva_data)
    # Save summary duration data by each astronaut to CSV file
    write_dataframe_to_csv(duration_by_astronaut_df, duration_by_astronaut_output_file)

    # Sort dataframe by date ready to be plotted (date values are on x-axis)
    eva_data.sort_values('date', inplace=True)

    # Calculate cumulative time spent in space over years
    eva_data_new = add_duration_hours(eva_data)
    eva_data_new['cumulative_time'] = eva_data_new['duration_hours'].cumsum()

    # Plot
    plot_cumulative_duration_vs_date(eva_data_new['date'],eva_data_new['cumulative_time'],graph_file)

    print("--END--")

def summary_duration_by_astronaut(df):
    """
    Summarise the duration data by each astronaut and saves resulting table to a CSV file

    Args: 
        df (pd.DataFrame): Input dataframe to be summarised

    
    Returns:
        sum_by_astro (pd.DataFrame): Data frame with a row for each astronaut and a summarised column 
    """
    print(f'Calculating summary of total EVA time by astronaut')
    subset = df.loc[:,['crew', 'duration']] # subset to work with only relevant columns
    subset = add_duration_hours(subset) # need duration_hours for easier calcs
    subset = subset.drop('duration', axis=1) # dropping the extra 'duration' column as it contains string values not suitable for calulations
    subset = subset.groupby('crew').sum() 
    return subset

def calculate_crew_size(crew):
    """
    Calculate the size of the crew for a single crew entry

    Args:
        crew (str): The text entry in the crew column containing a list of crew member names

    Returns:
        (int): The crew size
    """
    if crew.split() == []:
        return None
    else:
        return len(re.split(r';', crew))-1

def add_crew_size_column(df):
    """
    Add crew_size column to the dataset containing the value of the crew size

    Args:
        df (pd.DataFrame): The input data frame.

    Returns:
        df_copy (pd.DataFrame): A copy of the dataframe df with the new crew_size variable added
    """
    print('Adding crew size variable (crew_size) to dataset')
    df_copy = df.copy()
    df_copy["crew_size"] = df_copy["crew"].apply(
        calculate_crew_size
    )
    return df_copy

def read_json_to_dataframe(input_file):
    """
    Read a .json file into a pandas dataframe
    Args:
        input_file (str): input file name, expects .json file extension
    Returns:
        eva_df (pandas dataframe): data converted to pandas dataframe
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
    duration_hours = int(hours) + int(minutes)/60
    return duration_hours

def plot_cumulative_duration_vs_date(x,y,output_file):
    """
    Plots the cumulative spacewalk time vs year
    Args:
        x: (numpy array) date
        y: (numpy array) cumulative spacewalk time
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
    duration_by_astronaut_output_file = 'results/duration_by_astronaut.csv'

    main(input_file,output_file,duration_by_astronaut_output_file,graph_file)
