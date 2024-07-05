import numpy as np

# Defining the matrix A
A = np.array([[-4, 5], 
              [-5, 6]])

# Calculating the determinant of matrix A
det_A = np.linalg.det(A)
#rounding the determinant to 2 decimal places
det_A = round(det_A, 2)
# Calculating the inverse of matrix A
inv_A = np.linalg.inv(A)
print("Determinant of A:", det_A)
print("Inverse of A:\n", inv_A)
#calculate inverse of A to the power of 50 step by step, first calculate inverse of A to the power of 5, then to the power of 5*5, then to the power of 5*5*2
inv_A_2 = np.linalg.matrix_power(inv_A, 2)
inv_A_5 = np.linalg.matrix_power(inv_A, 5)
inv_A_25 = np.linalg.matrix_power(inv_A_5, 5)
inv_A_50 = np.linalg.matrix_power(inv_A_25, 2)
print("Inverse of A to the power of 2:\n", inv_A_2)
print("Inverse of A to the power of 5:\n", inv_A_5)
print("Inverse of A to the power of 25:\n", inv_A_25)
print("Inverse of A to the power of 50:\n", inv_A_50)

#calculate inv_A^1*inv_A^2*inv_A^2
inv_A_1 = np.linalg.matrix_power(inv_A, 1)
inv_A_2 = np.linalg.matrix_power(inv_A, 2)
print("Inverse of A to the power of 1:\n", inv_A_1)
print("Inverse of A to the power of 2:\n", inv_A_2)
inv_A_4 = np.matmul(inv_A_2, inv_A_2)
print("Inverse of A to the power of 4:\n", inv_A_4)

B=np.array([[1, 1, 1, 1],
            [1, 1, 1, 2],
            [1, 1, 2, 2],
            [1, 2, 2, 2]])

# Calculating the determinant of matrix B
det_B = np.linalg.det(B)
#calculating the inverse of matrix B
inv_B = np.linalg.inv(B)

print("Determinant of B:", det_B)
print("Inverse of B:\n", inv_B)

#calculate inv_B^1*inv_B^2*inv_B^2
inv_B_1 = np.linalg.matrix_power(inv_B, 1)
inv_B_2 = np.linalg.matrix_power(inv_B, 2)
print("Inverse of B to the power of 1:\n", inv_B_1)
print("Inverse of B to the power of 2:\n", inv_B_2)
inv_B_4 = np.matmul(inv_B_2, inv_B_2)
print("Inverse of B to the power of 4:\n", inv_B_4)

C=np.array([[1, 1, 1, 1],
            [1, 2, 1, 1],
            [2, 2, 2, 1],
            [3, 1, 2, 2]])

#calculate c^2
C_2 = np.linalg.matrix_power(C, 2)
print("C^2:\n", C_2)

#calculate determinant of C
det_C = np.linalg.det(C)
print("Determinant of C:", det_C)

D=np.array([[1, 1, 1, 1],
            [1, 1, 1, 2],
            [1, 1, 2, 2],
            [1, 2, 2, 2]])

#calculate det D

det_D = np.linalg.det(D)
print("Determinant of D:", det_D)