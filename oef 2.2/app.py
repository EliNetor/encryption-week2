import tenseal as ts

context = ts.context(
    ts.SCHEME_TYPE.CKKS, 
    poly_modulus_degree=8192,  
    coeff_mod_bit_sizes=[60, 40, 40, 60]  
)

context.global_scale = 2**40
context.generate_galois_keys()

number1 = 75
number2 = 326

encrypted_number1 = ts.ckks_vector(context, [number1])
encrypted_number2 = ts.ckks_vector(context, [number2])

encrypted_sum = encrypted_number1 + encrypted_number2

result = encrypted_sum.decrypt()

print(f"De som is {round(result[0])}")
