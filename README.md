# Fastq Downloader (WIP)
use this [snakemake script](https://gist.github.com/TTTPOB/1a8a960474a6a784f2da215b03ab3cc9) to get more fluent experience.

This python package let you download fastq files from ena.
It can automatic merge and rename fastq files based on the input file provided.
specify the out dir is not working now

## How to use
auto merge multiple files are not tested now
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
snakemake -s path/to/thisname.sml -j16 --config infotsv=infotsv output_dir=output refresh_acc=True -p
```

## todo
  - [ ] test for paired-end reads run merge
  - [ ] if fail, retry
  - [ ] use dag to run the pipeline
  - [ ] option to resume download when md5 not match
  - [ ] option to manually specify which to redownload
  - [ ] option to continue from last time download
  - [ ] implement second level parallelization
