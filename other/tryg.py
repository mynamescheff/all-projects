import math
import sympy as sp

# Definicja symboli
sqrt_6 = sp.sqrt(6)
sqrt_2 = sp.sqrt(2)

# Uproszczenie składowych rzeczywistej i urojonej
real_part = (sqrt_6 + sqrt_2) / 4
imaginary_part = (sqrt_6 - sqrt_2) / 4

# Obliczenie wartości
real_val = real_part.evalf()
imag_val = imaginary_part.evalf()

print(real_val, imag_val)

# Ponowne obliczenie modułu i argumentu bez zaokrągleń
modulus_symbolic = sp.sqrt((real_part**2 + imaginary_part**2).simplify())
argument_symbolic = sp.atan2(imaginary_part, real_part)

# Ewaluacja symbolicznych wyników
modulus_symbolic_val = modulus_symbolic.evalf()
argument_symbolic_val = argument_symbolic.evalf()

print(modulus_symbolic, argument_symbolic, modulus_symbolic_val, argument_symbolic_val)

# Obliczanie końcowego argumentu z dokładnością symboliczną
final_argument_symbolic = 301250 * argument_symbolic

# Normalizacja argumentu do zakresu od 0 do 2π
final_argument_symbolic_normalized = final_argument_symbolic % (2 * sp.pi)

# Obliczenie postaci trygonometrycznej i algebraicznej z dokładnością symboliczną
cos_final_symbolic = sp.cos(final_argument_symbolic_normalized)
sin_final_symbolic = sp.sin(final_argument_symbolic_normalized)

# Wyniki
final_complex_form_symbolic = cos_final_symbolic.evalf() + sp.I * sin_final_symbolic.evalf()
print(cos_final_symbolic.evalf(), sin_final_symbolic.evalf(), final_complex_form_symbolic)
