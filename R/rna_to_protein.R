rna_to_protein <- function(rna) {
    l_rna = nchar(rna)

    if (l_rna %% 3 != 0) {
        return("RNA must be divisible by 3")
    }

    s_table <- list(
        list(
            list("Phe", "Phe", "Leu", "Leu"),
            list("Ser", "Ser", "Ser", "Ser"),
            list("Tyr", "Tyr", "Stop", "Stop"),
            list("Cys", "Cys", "Stop", "Trp")
        ),
        list(
            list("Leu", "Leu", "Leu", "Leu"),
            list("Pro", "Pro", "Pro", "Pro"),
            list("His", "His", "Gln", "Gln"),
            list("Arg", "Arg", "Arg", "Arg")
        ),
        list(
            list("Ile", "Ile", "Ile", "Met"),
            list("Thr", "Thr", "Thr", "Thr"),
            list("Asn", "Asn", "Lys", "Lys"),
            list("Ser", "Ser", "Arg", "Arg")
        ),
        list(
            list("Val", "Val", "Val", "Val"),
            list("Ala", "Ala", "Ala", "Ala"),
            list("Asp", "Asp", "Glu", "Glu"),
            list("Gly", "Gly", "Gly", "Gly")
        )
    )

    protein = ""

    n <- 1
    while (n < l_rna) {
        ran <- n:(n + 2)

        indexes <- c(1,1,1)

        for (i in ran) {
            char <- substr(rna, i, i)

            index_for_indexes <- ((i - 1) %% 3) + 1

            switch (char,
                "U" = (indexes[index_for_indexes] <- 1),
                "C" = (indexes[index_for_indexes] <- 2),
                "A" = (indexes[index_for_indexes] <- 3),
                "G" = (indexes[index_for_indexes] <- 4)
            )
        }

        protein <- paste(protein, s_table[[indexes[1]]][[indexes[2]]][[indexes[3]]])

        n <- n + 3
    }

    return(substr(protein, 2,nchar(protein)))
}
