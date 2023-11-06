# newfangled_untangler
Splits genome files into seperate folders based on common metadata. This is useful as a precursor to the wonderful [Assembly-dereplicator](https://github.com/rrwick/Assembly-Dereplicator) tool to ensure that dereplication of genomes only occurs between outbreak isolates, rather than isolates which were isolated from different countries/times/sources/hosts etc.
Best to run this tool after data collection, assembly and assembly quality control screening, but prior to prior to annotation and other analyses.

## Installation

Create environment for dependencies:
```bash
conda create -y --name newfangled_untangler_dependencies
conda activate newfangled_untangler_dependencies
conda install -y -c anaconda pandas
conda install -y -c bioconda mash
git clone https://github.com/bananabenana/newfangled_untangler
git clone https://github.com/rrwick/Assembly-dereplicator
```

## Quick usage

1) Seperate genomes based on shared metadata
```bash
python newfangled_untangler/newfangled_untangler.py -i genome_metadata.txt -c 3 -d fasta_directory
```

2) Run Assembly-Dereplicator on genomes which share the same metadata profile
```bash
for dir in duplicated_metadata/*; do
Assembly-dereplicator/dereplicator.py --distance 0.0003 $dir derep_metadata_dir/"$dir"
echo "Dereplicated $dir"
done
```

3) Collate dereplicated metadata genomes with unique metadata genomes into a single directory
```bash
# Make final output directory
mkdir genomes_for_study

# Move files to directory
mv unique_metadata/*.fasta genomes_for_study/
mv derep_metadata_dir/duplicated_metadata/*/*.fasta genomes_for_study

# Remove unneeded files and directories
rm -rf duplicated_metadata unique_metadata derep_metadata_dir fastas
```

## Input files required

You will need 3 things:
1) Input metadata file `-i`. This is tab-delimited with a user-choice number of columns. The first column is the ID column (filename of the genome without extension). For example, genome_metadata.txt:

|Filename|Country|Source|Cluster|
|---|---|---|---|
|Genome_1|France|Human|1|
|Genome_2|France|Human|2|
|Genome_3|Netherlands|Equine|3|
|Genome_4|Netherlands|Equine|3|

2) Number of metadata columns you want to use to group isolates by `-c`. Integer.
3) Directory containing corresponding fasta files `-d`. Can be *.fasta, *.fna, *.fa formats.

Now you should be ready to go.


## Author

Ben Vezina

