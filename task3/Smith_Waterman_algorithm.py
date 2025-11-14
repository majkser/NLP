def Smith_Waterman_algorithm(first_str, second_str):
    n = len(first_str)
    m = len(second_str)
    matrix = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    
    penalty = -2
    match = 3
    mismatch = -3
    
    #initalization of matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if first_str[i - 1] == second_str[j - 1]:
                score_diagonal = matrix[i - 1][j - 1] + match
            else:
                score_diagonal = matrix[i - 1][j - 1] + mismatch
                
            score_up = matrix[i - 1][j] + penalty
            score_left = matrix[i][j - 1] + penalty
            matrix[i][j] = max(0, score_diagonal, score_up, score_left)

    # find max score in matrix
    max_score = 0
    max_index = (0, 0)
    for i in range(n + 1):
        for j in range(m + 1):
            if matrix[i][j] > max_score:
                max_score = matrix[i][j]
                max_index = (i, j)
    
    # traceback
    first_aligment = ""
    second_aligment = ""
    i, j = max_index
    
    while matrix[i][j] != 0:
        curr_score = matrix[i][j]
        score_diagonal = matrix[i - 1][j - 1]
        score_up = matrix[i - 1][j]
        score_left = matrix[i][j - 1]
        
        if curr_score == score_diagonal + (match if first_str[i - 1] == second_str[j - 1] else mismatch):
            first_aligment += first_str[i - 1]
            second_aligment += second_str[j - 1]
            i -= 1
            j -= 1
        elif curr_score == score_up + penalty:
            first_aligment += first_str[i - 1]
            second_aligment += "-"
            i -= 1
        elif curr_score == score_left + penalty:
            first_aligment += "-"
            second_aligment += second_str[j - 1]
            j -= 1
        
    first_aligment = first_aligment[::-1]
    second_aligment = second_aligment[::-1]
    
    print("First Alignment:\n" + first_aligment + "\n")
    print("Second Alignment:\n" + second_aligment + "\n")
    
    return first_aligment, second_aligment