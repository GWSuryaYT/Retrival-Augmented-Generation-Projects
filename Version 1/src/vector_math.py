class vector_mathy:
    def cosine_similarity(self, vec1: list[float], vec2: list[float]):
        A = vec1
        B = vec2

        #part1:

        #solving the top part:
        summation_total = 0
        for Ai,Bi in zip(A,B):

            #now we have the Ai and Bi th dimention values:
            multiplication_result = Ai * Bi

            #now lets add this in summation_total
            summation_total += multiplication_result
            #now the values will continue to loop multiplication and get added to the total 
        
        #part2:

        #the denominator have 2 parts aswell:

        summation_of_squared_A = 0
        for ai in A:
            summation_of_squared_A = summation_of_squared_A + (ai**2)

        #now just sqr root left:
        sqr_root_of_summation_a_square = summation_of_squared_A ** 0.5

        #part3:
        summation_of_squared_B = 0
        for bi in B:
            summation_of_squared_B = summation_of_squared_B + (bi**2)
        
        #now just sqr root left:
        sqr_root_of_summation_b_square = summation_of_squared_B ** 0.5


        #now we have all the maths just now devide them togather:

        similarity = summation_total / (sqr_root_of_summation_a_square * sqr_root_of_summation_b_square)

        return similarity
