with reaction_rules:
    # Ligand-receptor binding
    egfr(l,r) + egfr(r) <> egfr(l[1],r).egf(r[1])
