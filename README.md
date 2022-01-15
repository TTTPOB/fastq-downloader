# Fastq Downloader (WIP)

This python package let you download fastq files from ena.
It can automatic merge and rename fastq files based on the input file provided.
If you have trouble downloading this repo's release, please go to [fastgit](https://fastgit.org)

## How to use
auto merge multiple files of paired end reads are not tested now, but should be usable
```bash
conda create --name fastq-downloader -c conda-forge -c hcc -c bioconda aspera-cli snakemake httpx lxml click beautifulsoup4 python=3.9
## use what ever you want to download the gist mentioned above to thisname.smk
## download whl file from github release of this project to thisname.whl
conda activate fastq-downloader
pip install fastq-downloader==0.3.1
## make sure to create an infotsv before, you can just copy from the geo website,
## then go to vim, type :set paste to get into paste mode, paste the table into vim,
## save the file as whatever name you want, then exit vim
## the white space will be auto convert to underscore
## refresh_acc need to be False if you don't want to query again the accesion number,
## or due to the recreation of the link file(default set to false), all files are to be downloaded.
fastq-downloader smk --info thisname.tsv --out thisname --refresh_acc False
```

It will automatically try to download the file, check md5, retry if file integrity check failed, and merge the files if the number of files is more than 2, finally rename the files to the description you provided.

prepare the info.tsv like this:
note the file must be tab delimited (tsv file), you can simply achieve this by paste it from the Excel or GEO website. Or from SRA Run Selector downloaded csv file.
```
GSM12345  h3k9me3_rep1
GSM12345  h3k9me3_rep2
```


## todo
  - [ ] test for paired-end reads run merge
  - [ ] publish to bioconda
  - [x] if fail, retry
  - [x] use dag to run the pipeline (sort of, implemented by using snakemake)
  - [x] option to resume download when md5 not match
  - [x] option to continue from last time download
  - [x] implement second level parallelization

## update content
  - 0.3.2:
     - add filter for library layout (some sra entry has content mismatches its library layout)