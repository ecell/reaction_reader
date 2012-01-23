'''

'''

from func import *

with molecule_types:
    L(r, d) # Ligand w/ receptor binding and dimerization sites.
    R(l, tf(Y, pY)) # Receptor with ligand and TF binding sites.
    TF(r, d(Y, pY), dna, im) # Transcription factor (monomer) with recepter...
    DNA(p1, p2) # DNA molecule with two promoter sites.
    mRNA1() # mRNA transcript for Protein 1.
    mRNA2() # mRNA transcript for Protein 2.
    P1(im, dna) # Protein 1 with importin and DNA binding domains.
    P2() # Protein 2.
    Im(fg, cargo) # nuclear importin molecule with hydrophobic domain (fg) ...
    NP(fg) # nuclear pore complex w/ hydrophobic FG repeat domain.
    Sink() # a place for deleted molecules.


with molecule_inits:
    L(r, d, loc(EC)) [1000]
    R(l, tf(Y), loc(PM)) [200]
    TF(r, d(Y), dna, im, loc(CP)) [200]
    DNA(p1, p2, loc(NU)) [2]
    Im(fg, cargo, loc(CP)) [40]
    NP(fg, loc(NM)) [4]

    # Arbitrarily asssign compartment CP to the abstract molecule "Sink".
    Sink(loc(CP)) [0]
       

with reaction_rules:
    # receptor-ligand binding.
    L(r) + R(l) <_> L(r[1]).R(l[1]) | (0.1, 1.0)

    # ligand dimerization
    L(d) + L(d) <_> L(d[1]).L(d[1]) | (0.1, 1.0)

    # Rule3: receptor-dimer internalization.
    R(loc(PM)).R(loc(PM)) > R(loc(EM)).R(loc(EM)) | 1.0

    # receptor, ligand recycling.
    R(loc(EM)) > R(loc(PM)) | 0.1
    L(loc(EN)) > L(loc(EC)) | 0.1

    # receptor transphosphorylation.
    R().R(tf(Y)) > R().R(tf(pY)) | 1.0

    # receptor dephossphorylation.
    R(tf(pY)) > R(tf(Y)) | 0.1

    # receptor-TF binding. favor binding if TF(dim~Y), unbinding if (TF(dim~pY).
    R(tf(pY)) + TF(d(Y), r) <_> R(tf(pY)[1]).TF(d(Y), r[1]) | (0.1, 0.1)
    R(tf(pY)) + TF(d(pY), r) <_> R(tf(pY)[1]).TF(d(pY), r[1]) | (0.1, 10.0)

    # transcription factor trans-phosphorylation.
    TF().R().R().TF(d(Y)) > TF().R().R().TF(d(pY)) | 1.0

    # transcription factor dephosphorylation (CP only).
    TF(d(pY), loc(CP)) > TF(d(Y), loc(CP)) | 1.0

    # transcription factor dimerization.
    TF(r, d(pY), dna) + TF(r, d(pY), dna) <_> TF(r, d(pY)[1], dna).TF(r, d(pY)[1], dna) | (0.1, 1.0)

    # TF dimer binds promoter 1.
    # TF(dna, im).TF(dna, im) + DNA(p1) <_> TF(dna[1], im).TF(dna[2], im).DNA(p1[1][2]) | (0.1, 1.0)
    # ng.1 : [1][2]

    # transcription.
    # DNA(p1[+]) > DNA(p1[+]) + mRNA1(loc(NU)) | 1.0
    # DNA(p2[+]) > DNA(p2[+]) + mRNA1(loc(NU)) | 1.0
    # ng.2 : [+]

    # mRNA transport to cytoplams.
    mRNA1(loc(NU)) > mRNA1(loc(CP)) | 1.0
    mRNA2(loc(NU)) > mRNA2(loc(CP)) | 1.0

    # mRNA tanslatio to protain.
    mRNA1(loc(CP)) > mRNA1(loc(CP)) + P1(im, dna, loc(CP)) | 1.0
    mRNA2(loc(CP)) > mRNA2(loc(CP)) + P2(loc(CP)) | 1.0

    # mRNA degradation.
    mRNA1() > Sink(loc(CP)) | 1.0
    mRNA2() > Sink(loc(CP)) | 1.0

    # protain degradation.
    P1(loc) > Sink(loc(CP)) | 0.1
    P2(loc) > Sink(loc(CP)) | 0.1

    # importin binds TF dimer (tends to pick up in CP, drop off in NU).
    # TF(im, dna, r).TF(im, dna, r) + Im(cargo, loc(NU)) <_> TF(im[1], dna, r).TF(im[2], dna, r).Im(cargo[1][2], loc(CP) | (0.1, 0.1)
    # TF(im, dna, r).TF(im, dna, r) + Im(cargo, loc(NU)) <_> TF(im[1], dna, r).TF(im[2], dna, r).Im(cargo[1][2], loc(CP) | (0.1, 10.0)
    # ng.1: [1][2]

    # importin binds P1 (tends to pick up in CP, drop off in NU).
    P1(im, dna) + Im(cargo, loc(CP)) <_> P1(im[1], dna).Im(cargo[1], loc(CP)) | (0.1, 0.1)
    P1(im, dna) + Im(cargo, loc(NU)) <_> P1(im[1], dna).Im(cargo[1], loc(NU)) | (0.1, 10.0)

    # importin enters nuclear pore.
    Im(fg) + NP(fg) <_> Im(fg[1]).NP(fg[1]) | (0.1, 1.0)

    # importin traverses nuclear pore (with any cargo).
    Im(fg[1], loc(CP)).NP(fg[1]) <_> Im(fg[1], loc(NU)).NP(fg[1]) | (1.0, 1.0)

    # P1 binds promoter 2.
    P1(im, dna) + DNA(p2) <_> P1(im, dna[1]).DNA(p2[1]) | (0.1, 1.0)
