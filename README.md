# Fastq Downloader (WIP)

This python package let you download fastq files from ena.
It can automatic merge and rename fastq files based on the input file provided.
If you have trouble downloading this repo's release, please go to [fastgit](https://fastgit.xyz) to see if this project can help you.

## Notice for Readme
If you are reading this from pypi, please go to [github](https://github.com/TTTPOB/fastq-downloader) to read the latest readme file, for I won't modify pypi readme unless new version released.

## How to Use

### Installation
```bash
conda create --name fastq-downloader -c conda-forge -c hcc -c bioconda aspera-cli snakemake-minimal httpx lxml click beautifulsoup4 python=3.9
## use what ever you want to download the gist mentioned above to thisname.smk
conda activate fastq-downloader
pip install fastq-downloader==0.4.4
```

### Usage
make sure to create an `info.tsv` before, you can just copy from the [GEO](https://www.ncbi.nlm.nih.gov/gds) website,
then go to vim, type `:set` paste to get into paste mode,
paste the table into vim,
and you can modify the names of samples to suit your need,
the downloaded file will then be renamed too.
Save the file as whatever name you want, then exit vim
the white space will be auto convert to underscore

first, we have to turn info tsv to individual sample accession files
```bash
## step 1
## you can use fastq-downloader breakdown-tsv --help to view the help
fastq-downloader breakdown-tsv \
  -i path/to/info.tsv \
  -o path/to/output/dir
```
All paths can be relative paths.  
Then we can start to download.
```bash
## step 2
fastq-downloader smk \
  -i path/to/info.tsv \
  -o path/to/output/dir \
  -t {number_of_threads_you_want} \
  --download-backend ascp
```

after the download is done, you can use `find` command to get all of the `fastq.gz` files and link them to anoter place. For example I have a bunch of file downloaded to `download` folder, the folder structure should look like this:
```
# this is what inside download folder
. 
└── merged_fastq
    ├── GSM5159835
    │   ├── wt_1_R1.fastq.gz
    │   └── wt_1_R2.fastq.gz
    ├── GSM5159836
    │   ├── wt_2_R1.fastq.gz
    │   └── wt_2_R2.fastq.gz
    └── GSM5159837
        ├── wt_3_R1.fastq.gz
        └── wt_3_R2.fastq.gz
```
Then execute `find -name "*fastq.gz" | xargs -I {} ln -s {} .`  
All `fastq.gz` files will be linked to the root of `download` folder:
```
.
├── merged_fastq
│   ├── GSM5159835
│   │   ├── wt_1_R1.fastq.gz
│   │   └── wt_1_R2.fastq.gz
│   ├── GSM5159836
│   │   ├── wt_2_R1.fastq.gz
│   │   └── wt_2_R2.fastq.gz
│   └── GSM5159837
│       ├── wt_3_R1.fastq.gz
│       └── wt_3_R2.fastq.gz
├── wt_1_R1.fastq.gz -> merged_fastq/GSM5159835/wt_1_R1.fastq.gz
├── wt_1_R2.fastq.gz -> merged_fastq/GSM5159835/wt_1_R2.fastq.gz
├── wt_2_R1.fastq.gz -> merged_fastq/GSM5159836/wt_2_R1.fastq.gz
├── wt_2_R2.fastq.gz -> merged_fastq/GSM5159836/wt_2_R2.fastq.gz
├── wt_3_R1.fastq.gz -> merged_fastq/GSM5159837/wt_3_R1.fastq.gz
└── wt_3_R2.fastq.gz -> merged_fastq/GSM5159837/wt_3_R2.fastq.gz
```
This should add some convinience for your subsequent process.


These command lines should suit your need in most situations,
for those who want more flexiblity and control to the underlying `snakemake` workflow,
you can append your argument to the `-s` option of the `smk` subcommand;
or you can directly use the snakemake file in this repo.

For other advanced use you can always use `--help`, or read the source code.

It will automatically try to download the file, check md5, retry if file integrity check failed, and merge the files if the number of files is more than 2, finally rename the files to the description you provided.

prepare the info.tsv like this:
note the file must be tab delimited (tsv file), you can simply achieve this by paste it from the Excel or GEO website. Or from SRA Run Selector downloaded csv file.
```
GSM12345  h3k9me3_rep1
GSM12345  h3k9me3_rep2
```

## Notice for Commonly Encountered Problems
1. error from `ascp` saying `failed to authenticate`:
  - It can be a network issue according to [this issue on github](https://github.com/wwood/kingfisher-download/issues/9) or a server issue of EBI [this post on biostar](https://www.biostars.org/p/9493414/) 
  - If you have encountered this problem, please try to delete the download target folder and change the `--download-backend` argument to `wget` to use ftp links.

## Todo
- [x] test for paired-end reads run merge
- [ ] publish to bioconda
- [x] if fail, retry
- [x] use dag to run the pipeline (sort of, implemented by using snakemake)
- [x] option to resume download when md5 not match
- [x] option to continue from last time download
- [x] implement second level parallelization

## Known Issues
- Will fail to download the files contains both paired-end reads and single-end reads. (yes it exists).

## Update Content
- 0.4.4:
  - Bump version to trigger pypi readme update
  - Fix version number.  
- 0.4.3:
  - Update readme.
  - Breakdown the download process to two steps and add new download backend and `wget`.
- 0.3.2:
   - Add filter for library layout (some sra entry has content mismatches its library layout)