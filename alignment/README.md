# alignment

## Edit-distance based alignment methods

* `leven`: Standard Levenshtein distance
* `leven_corpus_pmi`: Weighted Levenshtein distance with PMI costs obtained from the entire corpus
* `leven_doc_pmi`: Weighted Levenshtein distance with PMI costs obtained from each document separately
* `leven_swap`: Levenshtein-Damerau distance, i.e. with transposition/swap

Standard Levenshtein distance uses the Python `edlib` module, all other methods are custom implementations in `levenshtein_align.py`.

For all methods, the `add_adjacent_identicals.py` script is applied to increase alignment coverage.

## Stochastic transducer methods

* `m2m_max11_delXY`: Single-character transducer allowing deletions and insertions (i.e. Levenshtein distance with EM-learned weights).
* `m2m_max11_delXY_init`: Same as above, initialized with Levenshtein weights.
* `m2m_max22_delXY`: Extension allowing bigrams on either source or target side, but not both.
* `m2m_max22_delXY_eqmap`: Extension allowing bigrams on either source or target side or both.
* `m2m_max22_eqmap`: Extension allowing bigrams on either source or target side or both, but disallowing insertions and deletions.
* `m2m_max22`: Extension allowing bigrams on either source or target side, but not both. Insertions and deletions are also disallowed.
* `m2m_asym_max21_max12_delXY`: Runs the max22_delXY model twice, once restricting source to unigrams, once restricting target to unigrams. Results are then symmetrized.

All experiments are based on the [m2m-aligner](https://github.com/letter-to-phoneme/m2m-aligner) toolkit by Jiampojamarn et al.

We only use `m2m_max11_delXY` and `m2m_max22_delXY_eqmap` for further evaluation.

## Word alignment methods

* `giza`: [GIZA++](https://github.com/moses-smt/giza-pp) with default parameters (except `mkcls` with 10 classes)
* `mgiza`: [MGIZA](https://github.com/moses-smt/mgiza) with default parameters (except `mkcls` with 10 classes) - yields (almost) the same results as `giza` but isn't significantly faster
* `fastalign`: [fast_align](https://github.com/clab/fast_align) with default parameters
* `eflomal`: [eflomal](https://github.com/robertostling/eflomal) with default parameters
* `eflomal_corpus_priors`: eflomal with priors estimated on the entire corpus
* `eflomal_leven_priors`: eflomal with priors simulating Levenshtein distance (high probability for character identity, low probability for character difference)

All word alignment methods are run in both directions and are then symmetrized with atools (from `fast_align`) using the *grow-diag-final-and* method. 
Other symmetrization methods are not considered here.

**Note:** There are (at least) three implementations of the *grow-diag-final-and* method: `atools`, `symal` (from Moses) and `gdfa.py` (from [NLTK](https://github.com/nltk/nltk/blob/develop/nltk/translate/gdfa.py)). They all yield different results, in particular `gdfa.py` seems to have various problems/bugs. The `symcheck` directory contains a few experiments.
