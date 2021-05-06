from typing import List

import numpy as np


class LSH:
    def shingles(self, text: str, ngram: int):
        return set(text[head:head + ngram] for head in range(0, len(text) - ngram))

    def jaccard_ngram(self, set_a, set_b):
        intersection = set_a & set_b
        union = set_a | set_b
        return len(intersection) / len(union)

    def jaccard_signature(self, a: List[int], b: List[int]):
        # jaccard signature with minhash
        union = len(a)
        intersection = 0
        for i in range(len(a)):
            if a[i] == b[i]:
                intersection = intersection + 1
        # jaccard ngram
        # union = 0
        # intersection = 0
        # for i in range(len(a)):
        #     if a[i] == 1 or b[i] == 1:
        #         union = union + 1
        #     if a[i] == b[i] == 1:
        #         intersection = intersection + 1
        return intersection / union

    def init_matrix(self, list_docs: List[str]):
        list_set = []
        set_all = set()
        for doc in list_docs:
            doc_set = self.shingles(text=doc, ngram=4)
            set_all = set_all.union(doc_set)
            list_set.append(doc_set)
        matrix = np.zeros((len(set_all), len(list_docs)), dtype=int)

        t = 0
        for i in list_set:
            k = 0
            for j in set_all:
                if j in i:
                    matrix[k][t] = 1
                k = k + 1
            t = t + 1
        return matrix

    def init_pi_array(self, n: int):
        return np.random.choice(range(n), size=n, replace=False)

    def min_hashing(self, matrix, n_permutation: int):
        print('Min_hashing.')
        rs = []
        for i in range(n_permutation):
            print('n_permutation: ', i)
            arr = []
            pi_array = self.init_pi_array(len(matrix))
            for j in range(len(matrix[0])):
                col = matrix[:, j]
                mul = pi_array * col
                mul = np.extract(mul > 0, mul)
                arr.append(np.amin(mul))
            rs.append(arr)
        return np.array(rs)

    def get_index_of_doc(self, doc: str, list_docs: List[str]):
        for i in range(len(list_docs)):
            if doc == list_docs[i]:
                return i
        return 0


if __name__ == '__main__':
    lsh = LSH()
    s1 = 'Who was the first king of Poland'
    s2 = 'Who was the first ruler of Poland'
    s3 = 'Who was the last pharaoh of Egypt'
    s4 = 'Who was the last pharaoh of Germany'
    docs = [s1, s2, s3, s4]
    matrix = lsh.init_matrix(docs)
    min_hashing = lsh.min_hashing(matrix, 50)
    print(matrix)
    print('\nmin_hashing:')
    print(min_hashing)
    list_a = min_hashing[:, 0]
    list_b = min_hashing[:, 1]
    list_c = min_hashing[:, 2]
    list_d = min_hashing[:, 3]
    print('a vs b: ', lsh.jaccard_signature(list_a, list_b))
    print('a vs c: ', lsh.jaccard_signature(list_a, list_c))
    print('a vs d: ', lsh.jaccard_signature(list_a, list_d))
    print('b vs c: ', lsh.jaccard_signature(list_b, list_c))
    print('b vs d: ', lsh.jaccard_signature(list_b, list_d))
    print('c vs d: ', lsh.jaccard_signature(list_c, list_d))
    print('index = ', lsh.get_index_of_doc(s4, docs))
