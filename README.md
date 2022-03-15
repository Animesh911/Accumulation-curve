## Rarefaction-curve

Plot rarefaction curve based on subsampling with repacement

## Usage

```
Usage: rarefy_kaiju.py [-h] [--file FILE] [--sample_frac SAMPLE_FRAC] [--threshold [THRESHOLD]] [--sim [SIM]]

  Options:

    -h, --help                  output usage information
    --file FILE                 TSV file where samples are in column (required)
    --sample_frac SAMPLE_FRAC   comma seperated fraction of sample (default 0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,.85,0.9,0.95,1)
    --threshold [THRESHOLD]     Minimum occurance in a sample to claim a species (default 2)
    --sim [SIM]                 No of times to simulate (default 10)

```
## Example

```
python rarefy_kaiju.py --file test.txt

```


## TSV file with header
```
test.txt: 
column_a	column_b
0	288793
0	0
0	0
0	0
0	0
1696	0
0	0
0	0
0	0
0	0
0	398767
0	0
0	2591109
881	58050
454601	0
1555112	1367477
0	0
218208	0
179	0
443144	0
1930071	0
1917158	0
0	1936003
0	0
0	2575375
0	2601894
0	936155
585455	0
0	1110502
135619	1851148
```
