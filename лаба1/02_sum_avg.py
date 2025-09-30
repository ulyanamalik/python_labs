a = input("Введите первое число: ")
b = input("Введите второе число: ")

if ',' in a or ',' in b:
    a = a.replace(",", ".")
    b = b.replace(",", ".")

sum_result = float(a) + float(b)
avg_result = sum_result / 2

print(f'sum = {sum_result:.2f}; avg = {avg_result:.2f}')
