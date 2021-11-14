# Fastq Downloader (WIP)
use this [snakemake script](https://gist.github.com/TTTPOB/1a8a960474a6a784f2da215b03ab3cc9) to get more fluent experience.

This python package let you download fastq files from ena.
It can automatic merge and rename fastq files based on the input file provided.

## How to use
auto merge multiple files of paired end reads are not tested now, but should be usable
```bash
conda create --name fastq-download -c conda-forge -c hcc -c bioconda aspera-cli snakemake httpx lxml click beautifulsoup4 python=3.9
## use what ever you want to download the gist mentioned above to thisname.smk
## download whl file from github release of this project to thisname.whl
conda activate fastq-download
pip install thisname.whl
## make sure to create an infotsv before, you can just copy from the geo website,
## then go to vim, type :set paste to get into paste mode, paste the table into vim,
## save the file as whatever name you want, then exit vim
## the white space will be auto convert to underscore
## refresh_acc need to be False if you don't want to query again the accesion number,
## or due to the recreation of the link file, all files are to be downloaded.
python3 -m fastq_download --infotsv thisname.tsv --outdir thisname --refresh_acc False
```

## todo
  - [ ] test for paired-end reads run merge
  - [ ] publish to bioconda
  - [x] if fail, retry
  - [x] use dag to run the pipeline (sort of, implemented by using snakemake)
  - [x] option to resume download when md5 not match
  - [x] option to continue from last time download
  - [x] implement second level parallelization
