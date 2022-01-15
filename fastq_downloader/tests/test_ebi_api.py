from fastq_downloader.helper.accession_to_links import srr2link_md5


def test_srr4051017():
    """
    I found SRR4051017 is a special case before
    It is a paired end library but containes single end reads in sra/ena database
    Which results both types of download links
    I want to see how ebi api return after my filter
    """
    zipped = srr2link_md5("SRR4051017")
    fq_list = [link for link, md5 in zipped]
    assert len(fq_list) == 2
