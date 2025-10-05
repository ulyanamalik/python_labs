# Лабораторная работа №1
## Задание №1
```
name=input('имя:')
a=int(input('возраст:'))
print(f'Привет, {name}!Через год тебе будет {a+1}')
```
<img width="611" height="159" alt="Снимок экрана 2025-09-21 171347" src="https://github.com/user-attachments/assets/3c3fd911-4d82-4b00-bc60-c74cd1c5e14b" />

## Задание №2

```
a = input("Введите первое число: ")
b = input("Введите второе число: ")

if ',' in a or ',' in b:
    a = a.replace(",", ".")
    b = b.replace(",", ".")

sum_result = float(a) + float(b)
avg_result = sum_result / 2

print(f'sum = {sum_result:.2f}; avg = {avg_result:.2f}')
```
<img width="412" height="103" alt="Снимок экрана 2025-09-30 094019" src="https://github.com/user-attachments/assets/0230a13a-b08b-4589-8e92-223388ea885c" />

## Задание №3

```
price=int(input())
discount=int(input())
vat=int(input())
base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount
print(f'База после скидки:{base}0₽')
print(f'НДС:{vat_amount}0₽')
print(f'Итого к оплате:{total}0₽')
```
<img width="555" height="108" alt="Снимок экрана 2025-09-21 180212" src="https://github.com/user-attachments/assets/2b63650a-b66d-473c-bcc9-75fb72bfcbce" />

## Задание №4

```
m=int(input('минуты:'))
print(f'{(m//60):02d}:{(m%60):02d}')
```

<img width="281" height="77" alt="Снимок экрана 2025-09-30 092312" src="https://github.com/user-attachments/assets/44397001-a891-49a7-a137-2a2fcd43a462" />

## Задание №5
```
fio = input("ФИО:")
fio_clean= ' '.join(fio.split())
k = len(fio_clean)
FIO=fio.split()
print(f"Инициалы: {FIO[0][:1]}{FIO[1][:1]}{FIO[2][:1]}")
print(f"Длина: {k}")

```
<img width="692" height="151" alt="Снимок экрана 2025-09-21 182019" src="https://github.com/user-attachments/assets/148fda98-7454-414c-957b-ae00a91a1645" />





