"""Will handle output of data to CSV and handle input of old data to CSV. Will also verify that incoming data is new."""
import csv
# output function

# input function if user says they have an input file
# read csv into dicts, modify if nc to meet the proper format
# if user says they have an input file, bypass doing the stock names/sites
# sends the date of last run & stocks/sites to search_scraper so new date range is ran
# will call verify_new_data
def write_data(data):
    keys = data[0].keys()
    with open("results.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def read_data():
    """Reads a CSV file back in."""
    csv_file = input("\nEnter your CSV filename of previous articles: ")

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        inputted_csv_dist = list(reader)

# verify_new_data()
# which makes sure there are no duplicate article links
