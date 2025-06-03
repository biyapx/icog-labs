!(import! &self main)
!(import! &nodes nodes.metta)

; Define the function to write to CSV
(= (write_csv_wrapper $space $file)
    (let*
        (
            ($atom (get-atoms $space))     ; Retrieve atoms from the space
            ($av (getAv $atom))            ; Get associated values from the atom
        )
        (write_to_csv ($atom $av) $file)  ; Call the write_to_csv function
    )
)

; Define the function to summarize the CSV
(= (summarize_csv_wrapper $space $file)
    (let*
        (
            ($summary (summarize_csv $file))  ; Call the summarize_csv function
        )
        $summary  ; Return the summary result
    )
)

; Execute the write and summarize functions
!(write_csv_wrapper $space "nodes.metta")
!(summarize_csv_wrapper $space "nodes.metta")