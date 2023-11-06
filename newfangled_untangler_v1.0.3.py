import pandas as pd
import os
import shutil
import argparse
import glob

# Function to create directories
def create_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Separate genomes based on metadata.')
parser.add_argument('-i', '--input', required=True, help='Input data file containing metadata columns. Tab delimited. File extensions not required in ID col (col 1)')
parser.add_argument('-c', '--columns', type=int, default=3, help='Number of metadata columns not including ID col (col 1)')
parser.add_argument('-d', '--fasta_directory', required=True, help='Directory containing fasta files to be seperated based on metadata')
args = parser.parse_args()

# Update the input directory argument to accept multiple file extensions
input_files = glob.glob(os.path.join(args.fasta_directory, "*.fna")) + \
              glob.glob(os.path.join(args.fasta_directory, "*.fasta")) + \
              glob.glob(os.path.join(args.fasta_directory, "*.fa"))

# Import data as a DataFrame
df = pd.read_csv(args.input, sep='\t')

# Define variables
metadata_columns = df.columns[1:args.columns + 1].tolist()
identifier_column = df.columns[0]
uniques_all = df.drop_duplicates(subset=metadata_columns, keep=False)
dupes_all = df[df.duplicated(subset=metadata_columns, keep=False)]

# Create 'unique_metadata' directory
create_directory('unique_metadata')

# Copy genomes with unique metadata
for filename in uniques_all[identifier_column]:
    base_filename = f"{filename}.fasta"
    possible_extensions = [".fasta", ".fna"]

    source = None
    for ext in possible_extensions:
        potential_source = os.path.join(args.fasta_directory, f"{filename}{ext}")
        if os.path.exists(potential_source):
            source = potential_source
            break  # Found a valid source, no need to continue checking

    if source:
        destination = os.path.join('unique_metadata', base_filename)
        shutil.copy(source, destination)
    else:
        print(f"Warning: No valid source file found for {base_filename}")

# Create 'duplicated_metadata' directory
create_directory('duplicated_metadata')

# Copy genomes with duplicated metadata to separate directories
for idx, row in dupes_all.iterrows():
    key = '_'.join(str(row[column]) for column in metadata_columns)
    key_dir = os.path.join('duplicated_metadata', key)
    create_directory(key_dir)

    # Construct the source and destination paths
    base_filename = f"{row[identifier_column]}.fasta"
    possible_extensions = [".fasta", ".fna"]

    source = None
    for ext in possible_extensions:
        potential_source = os.path.join(args.fasta_directory, f"{row[identifier_column]}{ext}")
        if os.path.exists(potential_source):
            source = potential_source
            break  # Found a valid source, no need to continue checking

    if source:
        destination = os.path.join(key_dir, base_filename)
        shutil.copy(source, destination)
    else:
        print(f"Warning: No valid source file found for {base_filename}")

# Save unique and duplicated metadata lists
uniques_all.to_csv('uniques_all.tsv', sep='\t', index=False)
dupes_all.to_csv('dupes_all.tsv', sep='\t', index=False)

print(f'Total of {len(uniques_all)} unique metadata combinations found from the initial total of {len(df)} genomes')
print(f'Total of {len(dupes_all)} duplicated metadata combinations found from the initial total of {len(df)} genomes')
