# https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/submissions/1424344105

import math


def solution(n, edges, distance_threshold):
    matrix = [[math.inf] * n for _ in range(n)]

    for i, j, w in edges:
        matrix[i][j] = w
        matrix[j][i] = w

    for i in range(n):
        matrix[i][i] = 0

    for k in range(n):
        for i in range(n):
            for j in range(n):
                matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])
                # matrix[j][i] = matrix[i][j]

    ans, res = 0, n
    for i in range(n):
        matrix[i][i] = math.inf

        t = 0
        for vertex in matrix[i]:
            t += (vertex <= distance_threshold)

        if t <= res:
            res = t
            ans = i

    # print(*matrix, sep='\n')
    return ans


if __name__ == "__main__":
    qwe = 4
    arr = [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]]
    print(solution(qwe, arr, 4))

