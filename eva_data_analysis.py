import matplotlib.pyplot as plt
import pandas as pd

def read_json_to_dataframe(input_file):
    print(f'Reading JSON file {input_file}')
    # Read the data from a JSON file into a Pandas dataframe
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
    eva_df['eva'] = eva_df['eva'].astype(float)
    # Clean the data by removing any rows where duration is missing
    eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)
    return eva_df


def write_dataframe_to_csv(df, output_file):
    print(f'Saving to CSV file {output_file}')
    # Save dataframe to CSV file for later analysis
    df.to_csv(output_file, index=False, encoding='utf-8')

def plot_cumulative_duration_vs_date(x,y,output_file):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('Year')
    ax.set_ylabel('Total time spent in space to date (hours)')

    print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
    ax.plot(x,y,'ko-')

    plt.tight_layout()
    plt.savefig(output_file,bbox_inches='tight')
    plt.show()




# Main code

print("--START--")

input_file = open('./eva_data.json', 'r', encoding='ascii')
output_file = open('./eva_data.csv', 'w', encoding='utf-8')
graph_file = './cumulative_eva_graph.png'

# Read the data from JSON file
eva_data = read_json_to_dataframe(input_file)

# Convert and export data to CSV file
write_dataframe_to_csv(eva_data, output_file)

# Sort dataframe by date ready to be plotted (date values are on x-axis)
eva_data.sort_values('date', inplace=True)

# Calculate cumulative time spent in space over years
eva_data['duration_hours'] = eva_data['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
eva_data['cumulative_time'] = eva_data['duration_hours'].cumsum()

# Plot
plot_cumulative_duration_vs_date(eva_data['date'],eva_data['cumulative_time'],graph_file)

print("--END--")

