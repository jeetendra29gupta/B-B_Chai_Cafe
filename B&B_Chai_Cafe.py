menu = {
    "Butter Chicken": 12.50,
    "Palak Paneer": 10.95,
    "Chole Bhature": 9.75,
    "Chicken Biryani": 13.25,
    "Paneer Tikka Masala": 11.50,
    "Aloo Paratha": 8.50,
    "Samosa": 2.75,
    "Tandoori Chicken": 14.00,
    "Masala Dosa": 9.25,
    "Rogan Josh": 12.75,
    "Pani Puri": 4.50,
    "Gulab Jamun": 3.00,
    "Raita": 3.25,
    "Naan": 2.00,
    "Mango Lassi": 4.75
}

print("Welcome to B&B Chai Cafe, Here is our MENU.")
print()
for key, value in menu.items():
    print(f"{key}: {value}")
print("______________________________________________________________________")
flag = True
total_amount = 0
while flag:
    item = input("Enter the item name you want to order: ").title()
    if menu.get(item):
        price = menu.get(item)
        print(f"you have order {item} : price -> {price}")
        total_amount += price
        yes_or_no = input("Do you want to order something else? (YES, NO) ").lower()
        if yes_or_no == "no":
            flag = False
    else:
        print("The Item is not in Menu, Check and retry.")
    print("______________________________________________________________________")
print(f"The total amount is {total_amount}, Have a nice Day.")
