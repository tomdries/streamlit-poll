import gspread

gc = gspread.service_account(filename='client_secret.json')

sh = gc.open("Form-app")

print(sh.sheet1.get('A1'))

# insert row
sh.sheet1.insert_row(['a', 'b', 'c', 'd'], 2)
