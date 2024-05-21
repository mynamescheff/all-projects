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