import json
import sqlite3

class DatabaseHelper():
    def createDatabase(self):
        conn = sqlite3.connect('things.db')
        print("Opened database successfully");
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS things
               (_id INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
               category         TEXT    NOT NULL,
               brand            TEXT    NOT NULL,
               name             TEXT    NOT NULL,
               price            INTEGER,
                   image_url        TEXT);''')
        print("Table created successfully");
        conn.commit()
        conn.close()

    def insertData(self):
        conn = sqlite3.connect('things.db')
        print("Opened database successfully")
        cursor = conn.cursor()

        with open("cigarette.json",'r') as file:
            json_str = json.load(file)
            for item in json_str:
                name = item['name']
                prices = item['price']
                img = item['img']

                category = '烟'
                brand = name.split('（')[0].split('(')[0]
                name = name.replace('(','').replace(')','')
                name = name.replace('（','').replace('）','')

                img = 'https://www.cnxiangyan.com' + img

                for price in prices:
                    price = price.replace('￥','').replace('元','')
                    try:
                        price = int(price)
                    except ValueError:
                        price = 0
                    print(category, brand, name, price, img)
                    cursor.execute("INSERT INTO things(category, brand, name, price, image_url) VALUES (?, ?, ?, ?, ?)", [category, brand, name, price, img])
        print("Records created successfully")

        conn.commit()
        conn.close()


if __name__ == '__main__':

    helper = DatabaseHelper()
    helper.createDatabase()
    helper.insertData();

    pass
