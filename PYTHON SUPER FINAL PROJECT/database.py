import sqlite3

class Database:
    def __init__(self, db_name='app.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product_table (
                Category VARCHAR(255),
                Product VARCHAR(255), 
                Price REAL, 
                Quantity INT,
                Total INT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sales_table (
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Product VARCHAR(255), 
                Price FLOAT,
                Quantity INT,
                Total FLOAT
            )
        ''')
        self.connection.commit()


    def add_product(self, category, product, price, quantity, total):
        self.cursor.execute(f'INSERT INTO Product_table (Category, Product, Price, Quantity, Total) VALUES (?, ?, ?, ?, ?)', (category, product, price, quantity, total))
        self.connection.commit()

    def add_sale_history(self, product, price, quantity, total):
        self.cursor.execute(f'INSERT INTO Sales_table (Product, Price, Quantity, Total) VALUES (?, ?, ?, ?)', (product, price, quantity, total))
        self.connection.commit()

#For fetching data from the database
    def get_all_products(self):
        self.cursor.execute("SELECT Category, Product, Price, Quantity, Total FROM Product_table")
        return self.cursor.fetchall()
    
    def get_all_sales(self):
        """Fetches all records from the Sales_table, ordered by most recent date."""
        # Select all five columns: date, Product, Price, Quantity, Total
        self.cursor.execute("SELECT date, Product, Price, Quantity, Total FROM Sales_table ORDER BY date DESC")
        return self.cursor.fetchall()

    def update_product_details(self, old_product_name, category, new_product_name, price, quantity, total):
        self.cursor.execute("""
            UPDATE Product_table
            SET Category = ?, Product = ?, Price = ?, Quantity = ?, Total = ?
            WHERE Product = ?
        """, (category, new_product_name, price, quantity, total, old_product_name))
        self.connection.commit()

    def update_product_stock(self, product_name, new_quantity):
        # Update the Quantity and recalculate Total (assuming Total = Price * Quantity)
        self.cursor.execute("""
            UPDATE Product_table
            SET Quantity = ?, Total = Price * ?
            WHERE Product = ?
        """, (new_quantity, new_quantity, product_name))
        self.connection.commit()

#Method for deleting out-of-stock products
    def delete_product(self, product_name):
        self.cursor.execute("DELETE FROM Product_table WHERE Product = ?", (product_name,))
        self.connection.commit()

    def delete_sale(self, date, product_name, quantity):
        # We use date, product, and quantity as a composite key for deletion
        self.cursor.execute("""
            DELETE FROM Sales_table 
            WHERE date = ? AND Product = ? AND Quantity = ?
        """, (date, product_name, quantity))
        self.connection.commit()

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

    def clear_sales_history(self):
        self.cursor.execute("DELETE FROM Sales_table")
        self.connection.commit()