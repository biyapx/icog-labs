!(import! &self main)
(gene ENSG00000175793)
(gene_type (gene ENSG00000175793) protein_coding)
(chr (gene ENSG00000175793) chr1)
(start (gene ENSG00000175793) 26863149)
(end (gene ENSG00000175793) 26864456)
(gene_name (gene ENSG00000175793) SFN)
(synonyms (gene ENSG00000175793) (YWHAS SFN stratifin 14-3-3_protein_sigma epithelial_cell_marker_protein_1 HGNC:10773))

(= (write_summary_wrapper $space $file)
    (let*
        (
            ($atom (get-atoms $space))
            ($av (getAv $atom))
        )
        (write_summary (($atom $av)) $file)
    )
)
!(write_summary_wrapper &self get_txt_file_name )