# alignment

## Levenshtein-distance based methods

* `leven` (*leven* in the paper): Standard Levenshtein distance (implemented with the Python `edlib` module)
* `leven_corpus_pmi` (*leven-pmi: Weighted Levenshtein distance with PMI costs obtained from the entire corpus (custom implementation in `levenshtein_align.py`)

For both methods, the `add_adjacent_identicals.py` script is applied to increase alignment coverage.

## Stochastic memoryless transducer methods

* `m2m_max11_delXY` (*unigram*): Single-character transducer allowing deletions and insertions (equivalent to Levenshtein distance with EM-learned weights).
* `m2m_max22_delXY_eqmap` (*bigram*): Extension allowing bigrams on either source or target side or both.

All experiments are based on the [m2m-aligner](https://github.com/letter-to-phoneme/m2m-aligner) toolkit by Jiampojamarn et al.

For the unigram transducer, the `add_adjacent_identicals.py` script is applied to increase alignment coverage.

## SMT word alignment methods

* `giza`: [GIZA++](https://github.com/moses-smt/giza-pp) with default parameters (except `mkcls` with 10 classes)
* `fastalign`: [fast_align](https://github.com/clab/fast_align) with default parameters
* `eflomal`: [eflomal](https://github.com/robertostling/eflomal) with default parameters
* `eflomal_corpus_priors` (*eflomal-priors*): eflomal with priors estimated on the entire corpus

## Symmetrization

All methods are run in both directions and are then symmetrized with `atools` (from `fast_align`) with the following methods: *union, intersect, grow-diag-final, grow-diag-final-and*. Only the last one is reported in the paper.

Note: There are (at least) three implementations of alignment symmetrization: `atools`, `symal` (from Moses) and `gdfa.py` (from [NLTK](https://github.com/nltk/nltk/blob/develop/nltk/translate/gdfa.py)). They all yield different results, in particular `gdfa.py` seems to have various problems/bugs. We use `atools`.

