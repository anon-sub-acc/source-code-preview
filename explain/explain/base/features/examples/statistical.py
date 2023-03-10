"""
Example Statistical Features
----------------------------
"""
import math

import zlib

import numpy as np
import scipy as sp
import scipy.special
import scipy.stats

from explain.base.features import CachedCallableFeature, FeatureCollection, FeatureReturnType
from explain.base.features.examples import linguistic
from explain.base.features.examples.utility import JoinedSubdomainsNGrams, JoinedSubdomainsBitArray, \
    JoinedSubdomainsUnicodeBitarray

__all__ = [
    'BitsEntropy',
    'NgramStatisticalFunctions',
    'RandomnessTests',
    'ZlibBitsCompressionRatio'
]


def _alphabet_diversity(ngram):
    return ngram.size / ngram.sum()


def _alphabet_size(ngram):
    return ngram.size


def _arithmetic_mean(ngram):
    return np.mean(ngram)


def _harmonic_mean(ngram):
    return sp.stats.hmean(ngram, axis=None)


def _kurtosis(ngram):
    kurtosis = sp.stats.kurtosis(ngram, axis=None)
    if math.isnan(kurtosis):
        return 0
    return kurtosis


def _lower_quartile(ngram):
    return np.percentile(ngram, q=25)


def _max(ngram):
    return np.max(ngram)


def _median(ngram):
    return np.median(ngram)


def _min(ngram):
    return np.min(ngram)


def _shannon_entropy(ngram):
    return sp.stats.entropy(ngram, base=2, axis=None)


def _skewness(ngram):
    skewness = sp.stats.skew(ngram, axis=None)
    if math.isnan(skewness):
        return 0
    return skewness


def _standard_deviation(ngram):
    return np.std(ngram)


def _upper_quartile(ngram):
    return np.percentile(ngram, q=75)


NGRAM_FUNCTIONS = {
    'alphabet-diversity': (FeatureReturnType.RATIONAL, _alphabet_diversity),
    'alphabet-size':      (FeatureReturnType.INTEGER, _alphabet_size),
    'arithmetic-mean':    (FeatureReturnType.RATIONAL, _arithmetic_mean),
    'harmonic-mean':      (FeatureReturnType.RATIONAL, _harmonic_mean),
    'kurtosis':           (FeatureReturnType.RATIONAL, _kurtosis),
    'lower-quartile':     (FeatureReturnType.RATIONAL, _lower_quartile),
    'max':                (FeatureReturnType.INTEGER, _max),
    'median':             (FeatureReturnType.RATIONAL, _median),
    'min':                (FeatureReturnType.INTEGER, _min),
    'shannon-entropy':    (FeatureReturnType.RATIONAL, _shannon_entropy),
    'skewness':           (FeatureReturnType.RATIONAL, _skewness),
    'standard-deviation': (FeatureReturnType.RATIONAL, _standard_deviation),
    'upper-quartile':     (FeatureReturnType.RATIONAL, _upper_quartile),
}


def _ngram_statistics(sample, stat_func, ngram_feature):
    subdomains_length = linguistic.SubdomainsLength.evaluate(sample)

    if subdomains_length < ngram_feature.n:
        with np.errstate(all='raise'):  # , warnings.catch_warnings():
            # warnings.filterwarnings('ignore')
            try:
                res = stat_func(ngram_feature.evaluate(sample))

                if np.isnan(res) or np.isinf(res):
                    return 0

                return res
            except (FloatingPointError, ValueError, IndexError):
                return 0

    return stat_func(ngram_feature.evaluate(sample))


NgramStatisticalFunctions = FeatureCollection([
    CachedCallableFeature(name=f'{ngram_feature.name[0]}-gram-{stat_name}',
                          return_type=return_type,
                          eval_func=FeatureCollection.generate(_ngram_statistics, **{'stat_func': stat_func,
                                                                                     'ngram_feature': ngram_feature}))
    for ngram_feature in JoinedSubdomainsNGrams.unpack()
    for stat_name, (return_type, stat_func) in NGRAM_FUNCTIONS.items()
])
"""Evaluates various statistical functions on n-grams of the joined subdomains for multiple n.

This is a collection of 39 features with the same base value, that apply different statistical functions on it.
They return rational and integer values.

Notes
-----
They first try to apply their statistical function and return 0 if that fails.
The features' identifiers are according to their applied statistical function and used n-gram:

- {1, 2, 3}-gram-alphabet-diversity: ratio of n-gram sequences and unique n-gram sequences
- {1, 2, 3}-gram-alphabet-size: number of n-gram sequences
- {1, 2, 3}-gram-arithmetic-mean: arithmetic mean of the n-gram sequence counts
- {1, 2, 3}-gram-harmonic-mean: harmonic mean of the n-gram sequence counts
- {1, 2, 3}-gram-kurtosis: kurtosis of the n-gram sequence counts
- {1, 2, 3}-gram-lower-quartile: lower quartile of the n-gram sequence counts
- {1, 2, 3}-gram-max: maximum of the n-gram sequence counts
- {1, 2, 3}-gram-median: median of the n-gram sequence counts
- {1, 2, 3}-gram-min: minimum of the n-gram sequence counts
- {1, 2, 3}-gram-shannon-entropy: Shannon entropy of the n-gram sequence counts
- {1, 2, 3}-gram-skewness: skewness of the n-gram sequence counts
- {1, 2, 3}-gram-standard-deviation: standard deviation of the n-gram sequence counts
- {1, 2, 3}-gram-upper-quartile: upper quartile of the n-gram sequence counts

To prevent runtime errors the features depend on :py:data:`.SubdomainsLength` to detect very short domains.

Examples
--------
>>> sample = 'ieee-security.org'
>>> ngram_stat_features = NgramStatisticalFunctions.unpack(['1-gram-alphabet-diversity', '2-gram-max', 
...                                                         '2-gram-shannon-entropy', '3-gram-kurtosis'])
>>> for ngram_stat_feature in ngram_stat_features:
>>>     print(ngram_stat_feature.name, ngram_stat_feature.evaluate(sample))
1-gram-alphabet-diversity 0.6923076923076923
2-gram-max 2
2-gram-shannon-entropy 3.41829583405449
3-gram-kurtosis -3.0

"""


def _probabilities(rank):
    p_full = np.prod([
        1 - pow(2, k - rank)
        for k in range(rank)
    ])

    p_near_full = 0.5 * np.prod([
        np.square(1 - pow(2, k - rank)) / (1 - pow(2, k - rank + 1))
        for k in range(rank - 1)
    ])

    p_remaining = 1.0 - p_full - p_near_full

    return p_full, p_near_full, p_remaining


BINARY_MATRIX_RANK_TEST_PROBABILITIES = {
    matrix_size: _probabilities(matrix_size)
    for matrix_size in range(2, 33)
}


def _binary_matrix_rank_test(bits):
    highest_dimension = max(int(np.sqrt(bits.size / 38)), 2)

    # We are bound by the number of bits the subdomains consist of
    dimension = min(highest_dimension, 32)
    block_size = dimension * dimension

    splits = list(range(block_size, bits.size, block_size))
    discard = bits.size % block_size

    blocks = np.array_split(bits,
                            splits)
    if discard > 0:
        blocks = blocks[:-1]

    full_rank_matrices = 0         # full rank
    near_full_rank_matrices = 0    # full rank -1
    remaining_matrices = 0         # len(blocks) - full_rank_matrices - near_full_rank_matrices

    for block in blocks:
        matrix = block.reshape((dimension, dimension))
        rank = np.linalg.matrix_rank(matrix)

        if rank == dimension:
            full_rank_matrices += 1
        elif rank == dimension - 1:
            near_full_rank_matrices += 1
        else:
            remaining_matrices += 1

    p_full, p_near_full, p_remaining = BINARY_MATRIX_RANK_TEST_PROBABILITIES[dimension]
    N = len(blocks)

    N_full_expected = float(N * p_full)
    N_near_full_expected = float(N * p_near_full)
    N_remaining_expected = float(N * p_remaining)

    chisq = ((full_rank_matrices - N_full_expected) ** 2) / N_full_expected + \
            ((near_full_rank_matrices - N_near_full_expected) ** 2) / N_near_full_expected + \
            ((remaining_matrices - N_remaining_expected) ** 2) / N_remaining_expected
    p_value = np.exp(-chisq / 2.0)

    return p_value
    # return p_value >= 0.01


def _block_frequency_test(bits):
    block_size = (bits.size // 10) + 1  # block_size > n / 10

    # for block_size == 1 degenerates to monobit test
    if block_size == 1:
        return _monobit_test(bits)

    splits = list(range(block_size, bits.size, block_size))
    discard = bits.size % block_size

    blocks = np.array_split(bits,
                            splits)
    if discard > 0:
        blocks = blocks[:-1]

    pi = np.apply_along_axis(lambda x: x.sum() / block_size, 1, blocks)
    chisq = 4 * block_size * np.sum(np.apply_along_axis(lambda x: (x - 0.5) ** 2,
                                                        0,
                                                        pi))
    p_value = sp.special.gammaincc(len(blocks) / 2,
                                   chisq / 2)

    return p_value
    # return p_value >= 0.01


def _cusum_test_statistic(bits):
    z = bits[0]
    S_i = 0

    for i in range(bits.size):
        S_i += 2 * bits[i] - 1
        z = max(z, abs(S_i))

    return z


def _cusum_test_pvalue(n, z):
    sum_1 = sum(scipy.stats.norm.cdf(((4 * k + 1) * z) / np.sqrt(n)) - scipy.stats.norm.cdf(((4 * k - 1) * z) / np.sqrt(n))
                for k
                in range(int((-n / z + 1) * 0.25), 1 + int((n / z - 1) * 0.25)))
    sum_2 = sum(scipy.stats.norm.cdf(((4 * k + 3) * z) / np.sqrt(n)) - scipy.stats.norm.cdf(((4 * k + 1) * z) / np.sqrt(n))
                for k
                in range(int((-n / z - 3) * 0.25), 1 + int((n / z - 1) * 0.25)))

    return 1 - sum_1 + sum_2


def _double_cusum_test(bits):
    # TODO: Probably more information through splitting test(s)
    n = bits.size

    forward_z = _cusum_test_statistic(bits)
    backward_z = _cusum_test_statistic(bits[::-1])

    forward_pvalue = _cusum_test_pvalue(n, forward_z)
    backward_pvalue = _cusum_test_pvalue(n, backward_z)

    return forward_pvalue + backward_pvalue
    # return forward_pvalue >= 0.01 and backward_pvalue >= 0.01


def _longest_run_of_ones_test(bits):
    n = bits.size

    # TODO: decide what to do with (too) short bit streams
    if n < 128:
        # Try experimental M, N
        K = 2
        M = 4
        V = [1, 2, 3]
        pi = [0.5, 0.3125, 0.1875]
    elif n < 6272:
        K = 3
        M = 8
        V = [1, 2, 3, 4]
        pi = [0.21484375, 0.3671875, 0.23046875, 0.1875]
        # ^ should be the only cases, but you never know ... so additional cases:
    elif n < 750000:
        K = 5
        M = 128
        V = [4, 5, 6, 7, 8, 9]
        pi = [0.1174035788, 0.242955959, 0.249363483, 0.17517706, 0.102701071, 0.112398847]
    else:
        K = 6
        M = 10000
        V = [10, 11, 12, 13, 14, 15, 16]
        pi = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

    splits = list(range(M, bits.size, M))
    discard = bits.size % M

    blocks = np.array_split(bits,
                            splits)
    if discard > 0:
        blocks = blocks[:-1]

    N = len(blocks)
    frequencies = np.zeros(shape=K + 1)

    for block in blocks:
        max_run = linguistic._longest_streak(block, [1])

        if max_run <= V[0]:
            frequencies[0] += 1
        elif max_run > V[-1]:
            frequencies[-1] += 1
        else:
            for i in range(1, K):
                if max_run == V[i]:
                    frequencies[i] += 1

    chisq = sum([((frequencies[i] - N * pi[i]) ** 2) / (N * pi[i])
                 for i in range(K + 1)])
    p_value = sp.special.gammaincc(K / 2,
                                   chisq / 2)

    return p_value
    # return p_value >= 0.01


def _monobit_test(bits):
    s = 0
    for bit in bits:
        if bit:
            s += 1
        else:
            s -= 1

    s_abs = np.abs(s) / np.sqrt(bits.size)
    p_value = sp.special.erfc(s_abs / 1.4142135623730951)
    return p_value
    # return p_value >= 0.01


def _runs_test(bits):
    pi = np.sum(bits) / bits.size
    tau = 2 / np.sqrt(bits.size)

    # not applicable if failed Frequency (Monobit) test -> p_value = 0.00...
    if np.abs(pi - 0.5) >= tau:
        return 0
        # return False

    v = np.sum(np.abs(np.ediff1d(bits))) + 1
    pi_sq = pi * (1 - pi)
    p_value = sp.special.erfc(np.abs(v - 2 * bits.size * pi_sq) / (2 * np.sqrt(2 * bits.size) * pi_sq))
    return p_value
    # return p_value >= 0.01


def _spectral_test(bits):
    n = bits.size

    X = [2 * bit - 1 for bit in bits]
    S = sp.fft.fft(X)

    M = np.abs(S[:n // 2])
    T = np.sqrt(2.995732273553991 * n)  # sqrt(log(1 / 0.05) * n)

    N_0 = 0.95 * n / 2
    N_1 = np.where(M < T)[0].size

    d = (N_1 - N_0) / np.sqrt(n * 0.011875)                    # (n1 - n0) / sqrt(n * (0.95)(0.05) / 4)
    p_value = sp.special.erfc(np.abs(d) / 1.4142135623730951)  # erfc(abs(d) / sqrt(2))

    return p_value
    # return p_value >= 0.01


def _randomness_test(sample, test, bitarray):
    bits = bitarray.evaluate(sample)
    return test(bits)


TEST_MAPPING = {
    'binary-matrix-rank':  _binary_matrix_rank_test,
    'block-frequency':     _block_frequency_test,
    'double-cusum':        _double_cusum_test,
    'longest-run-of-ones': _longest_run_of_ones_test,
    'monobit':             _monobit_test,
    'runs':                _runs_test,
    'spectral':            _spectral_test
}

RandomnessTests = FeatureCollection([
    CachedCallableFeature(name=f'{prefix}-test{suffix}',
                          return_type=FeatureReturnType.INTEGER,
                          eval_func=FeatureCollection.generate(_randomness_test, **{'test': test, 'bitarray': bitarray}))
    for prefix, test in TEST_MAPPING.items()
    for suffix, bitarray in {
        '': JoinedSubdomainsBitArray,
        '-unicode': JoinedSubdomainsUnicodeBitarray
    }.items()
])
"""Evaluates different randomness tests.

This is a collection of 14 features.
They evaluate different test statistics to determine whether a bit sequence behaves similar to a truly random sequence.
For each test and bit sequence there exists one feature in this collection.
For samples passing a test, the features return 1, otherwise 0.

Notes
-----
[1]_ serves as reference for the implementation and selection of the tests.

The identifiers are {binary-matrix-rank, block-frequency, double-cusum, longest-run-of-ones, monobit, runs, spectral}-test.
Features with the test applied to the second bit sequence use equally: {...}-test-unicode.
Note that the double Cusum test is the conjunction of the single Cusum test applied to a bit sequence and its inverse.

All features depend on either :py:data:`.JoinedSubdomainsBitArray` or :py:data:`.JoinedSubdomainsUnicodeBitarray`.

References
----------
.. [1] Lawrence E Bassham III et al. Sp 800-22 rev. 1a. a statistical test suite for random and pseudorandom number generators for cryptographic applications. National Institute of Standards & Technology, 2010.
    
Examples
--------
>>> sample = 'ieee-security.org'
>>> for randomness_test in RandomnessTests.unpack(['block-frequency-test', 'runs-test-unicode']):
>>>     print(randomness_test.name, randomness_test.evaluate(sample))
block-frequency-test True
runs-test-unicode False

"""


def _zlib_bit_compression_ratio(sample):
    bits = JoinedSubdomainsBitArray.evaluate(sample)
    bit_string = ''.join(map(str, bits)).encode()

    compressed_data = zlib.compress(bit_string, 9)

    return len(bit_string) / len(compressed_data)


ZlibBitsCompressionRatio = CachedCallableFeature(name='zlib-bits-compression-ratio',
                                                 return_type=FeatureReturnType.RATIONAL,
                                                 eval_func=_zlib_bit_compression_ratio)
"""Evaluates the data compression ratio the compression library zlib achieves with the UTF-8 encoded 
binary sequence of the joined subdomains.

This feature returns rational values.

Notes
-----
In the implementation we use the highest level of compression that zlib offers (i.e. using the Z_BEST_COMPRESSION flag).

This feature depends on :py:data:`.JoinedSubdomainsBitArray`.

Examples
--------
>>> ZlibBitsCompressionRatio.evaluate('ieee-security.org')
2.4761904761904763

"""


def _bits_entropy(sample):
    bits = JoinedSubdomainsBitArray.evaluate(sample)

    return sp.stats.entropy(bits,
                            base=2)


BitsEntropy = CachedCallableFeature(name='bits-entropy',
                                    return_type=FeatureReturnType.RATIONAL,
                                    eval_func=_bits_entropy)
"""Evaluates the entropy of the UTF-8 encoded binary sequence of the joined subdomains.

This feature returns rational values.

Notes
-----
Logarithm calculations use 2 as base.

This feature depends on :py:data:`.JoinedSubdomainsBitArray`.

Examples
--------
>>> BitsEntropy.evaluate('ieee-security.org')
5.781359713524662

"""
