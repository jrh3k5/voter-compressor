# voter-compressor

A command-line tool used to compress raw voter data by combining people in the same household.

## Usage

You can run this from the command line like so:

```
python compressor.py input_data.csv output_destination.csv
```

The input file is expected to have the following columns (named in a header row):

* Precinct
* Last Name
* First Name
* New First
* Hs Num
* Pre Direction
* Street Name
* Street Type
* Unit Type
* Unit Num
* City (RA)
* State (RA)
* Zip (RA)

...and a final column of any name that contains the combined address of the record. The other columns can be in any order, but this combined address must be the final column.

It will, to the given destination file, write a CSV file that collapses multiple records for the same household (but with multiple family members and, if applicable, families) into the same row. The ordering of the columns will match the ordering of the columns in the given input file.