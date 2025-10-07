a=input('первое число:')
b=input('второе число:')
if ',' in a or ','in b:
    a=a.replace(',','.')
    b=b.replace(',','.')
print(f'sum = {float(a)+float(b)}; avg = {(float(a)+float(b))/2}')