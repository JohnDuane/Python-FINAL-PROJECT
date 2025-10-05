import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # FOR PUTTING THE LOGO
from PyQt5.QtCore import Qt  # FOR SMOOTHING AND SIZING THE LOGO
from AdminPOS1 import menu
from database import Database  # FOR DATABASE CONNECTION

app = QApplication(sys.argv)
window = QWidget()
window.setGeometry(0, 0, 1366, 768)
window.setStyleSheet("background-color: #242222")

#Styles
inactive_style = """
    border-radius: 10px;
    background-color: #424242;
    color: white;
"""
active_style = """
    border-radius: 10px;
    background-color: #5269FF;
    color: white;
"""

#Sidebar
sidenav = QFrame(window)
sidenav.setGeometry(0, 0, 250, 768)
sidenav.setStyleSheet("background-color: #424242;")

logo = QLabel(sidenav)
pixmap = QPixmap("D:/Python Final Project/Images/logoo.png")
size = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
logo.setPixmap(size)
logo.setGeometry(20, 30, 260, 200)

justin = QLabel(sidenav)
pixmap2 = QPixmap('D:/Python Final Project/Images/nabunturan.png')
size2 = pixmap2.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
justin.setPixmap(size2)
justin.setGeometry(10, 520, 150, 300)

redGuy = QLabel(sidenav)
pixmap3 = QPixmap('D:/Python Final Project/Images/RedGuy.png')
size3 = pixmap3.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
redGuy.setPixmap(size3)
redGuy.setGeometry(120, 520, 150, 300)

title = QLabel("JUSTIN STORE", sidenav)
font = QFont("Ethnocentric", 15)
title.setFont(font)
title.setStyleSheet("color: #2643DE")
title.setGeometry(20, 220, 200, 30)

butfont = QFont("Ethnocentric", 14)

#Buttons
mainMenu = QPushButton("MAIN MENU", sidenav)
mainMenu.setFont(butfont)
mainMenu.setGeometry(20, 330, 200, 50)
mainMenu.setStyleSheet(active_style)

myCart = QPushButton("MY CART", sidenav)
myCart.setFont(butfont)
myCart.setGeometry(20, 400, 200, 50)
myCart.setStyleSheet(inactive_style)

about = QPushButton("ABOUT", sidenav)
about.setFont(butfont)
about.setGeometry(20, 470, 200, 50)
about.setStyleSheet(inactive_style)

# --- Button switching function ---
def set_active(button):
    mainMenu.setStyleSheet(inactive_style)
    myCart.setStyleSheet(inactive_style)
    about.setStyleSheet(inactive_style)
    button.setStyleSheet(active_style)

# --- Connect buttons ---
def show_main_menu():
    set_active(mainMenu)

    # Hide Cart view widgets
    for attr in ['cart_table', 'total_pay_label', 'total_items_label', 'buy_btn', 'cart_header']:
        if hasattr(window, attr):
            getattr(window, attr).hide()

    # Show Main Menu widgets
    for w in [parts, table, exit_btn, next_btn]:
        w.show()

    if not hasattr(window, 'main_header'):
        main_header = QLabel("PARTS", window)
        main_header.setFont(QFont("Ethnocentric", 22))
        main_header.setStyleSheet("color: white")
        main_header.setGeometry(280, 20, 300, 30)
        window.main_header = main_header
    window.main_header.show()
    
    # Reload products to reflect any purchases
    loadProducts()

mainMenu.clicked.connect(show_main_menu)

# --- "PARTS" label ---
parts = QLabel("PARTS", window)
fonts = QFont("Ethnocentric", 22)
parts.setFont(fonts)
parts.setStyleSheet("color: white")
parts.setGeometry(280, 20, 200, 30)

# --- Table ---
table = QTableView(window)
model = QStandardItemModel(7, 5)
model.setHorizontalHeaderLabels(['Category', 'Product', 'Price', 'Stock', ' '])
table.setGeometry(280, 70, 1064, 520)
table.verticalHeader().setVisible(False)
# Set the whole table size
font = QFont()
font.setPointSize(15)  # adjust the text inside the table
table.setFont(font)
table.verticalHeader().setDefaultSectionSize(30)   # row height
table.horizontalHeader().setDefaultSectionSize(212) # col width

table.setStyleSheet("background-color: #363636; border: 1px solid gray; color: white;")
table.horizontalHeader().setStyleSheet(""" QHeaderView::section {
        background-color: #363636;   /* background */
        color: white;             /* text color */
        font-size: 14px;
        font-weight: bold;
        border: 1px solid gray;   /* border around headers */
        padding: 5px;
    }""")
table.setModel(model)

database = Database()

# --- Cart Data ---
# cart_items entries: [category(str), name(str), price(float), qty(int)]
cart_items = []

def add_to_cart(product):
    """
    product is expected as (category, name, price, stock)
    This function:
      - adds/increments item in cart_items
      - decrements stock in the table model (UI only, DB update happens on BUY)
      - disables Add button when stock reaches 0
    """
    if not product:
        return
    category, name, price, stock = product

    # 1. ensure price is float
    try:
        # Tries to handle a price like "100.00 PHP" if it sneaks in
        price = float(price) 
    except Exception:
        price = float(str(price).replace(' PHP', '').replace(',', '').strip())

    # 2. add or increment in cart_items
    for item in cart_items:
        if item[1] == str(name):
            item[3] += 1
            break
    else:
        cart_items.append([str(category), str(name), price, 1])

    # 3. decrease stock in product table (the UI model)
    for row in range(model.rowCount()):
        prod_item = model.item(row, 1)
        if prod_item and prod_item.text() == str(name):
            stock_item = model.item(row, 3)
            if stock_item:
                try:
                    current_stock = int(stock_item.text())
                except Exception:
                    current_stock = 0
                
                # Check if stock can be decremented
                if current_stock > 0:
                    new_stock = current_stock - 1
                    model.setItem(row, 3, QStandardItem(str(new_stock)))

                    # disable Add button if now zero
                    btn = table.indexWidget(model.index(row, 4))
                    if btn and new_stock == 0:
                        btn.setEnabled(False)
            break

def loadProducts():
    model.removeRows(0, model.rowCount())  # clear existing rows
    products = database.get_all_products() or []

    for row, row_data in enumerate(products):
        # Database structure: (Category, Product, Price, Quantity, Total)
        try:
            category = row_data[0]
            product_name = row_data[1]
            price = float(row_data[2])
            stock = int(row_data[3])
        except Exception:
            # Fallback if DB returns unexpected data
            continue

        row_items = [
            QStandardItem(str(category)),
            QStandardItem(str(product_name)),
            QStandardItem(f"{price:.2f}"),
            QStandardItem(str(stock))
        ]
        model.appendRow(row_items)

        btn = QPushButton("Add to Cart")
        btn.setFont(QFont("Ethnocentric", 10))
        btn.setStyleSheet("background-color: #424242; color: white;")

        # capture product values as a tuple literal to avoid late-binding
        product_tuple = (category, product_name, price, stock)
        
        # Connect the button to add_to_cart
        btn.clicked.connect(lambda checked, p=product_tuple: add_to_cart(p))

        # Disable button if out of stock from the start
        if stock <= 0:
            btn.setEnabled(False)

        table.setIndexWidget(model.index(row, 4), btn)

# --- NEW FUNCTION: Database Transaction Logic ---
def process_purchase():
    """
    1. Records sales to Sales_table.
    2. Updates stock in Product_table using the current UI model stock.
    3. Deletes product from Product_table if stock hits zero.
    """
    global cart_items

    for item in cart_items:
        # item = [category, name, price(float), qty(int)]
        category, product_name, price, purchased_qty = item
        total_price = price * purchased_qty

        # 1. Record Sale History
        database.add_sale_history(product_name, price, purchased_qty, total_price)

        # 2. Get current stock from the *main product model* (which reflects the remaining stock)
        new_stock_in_db = 0
        product_found = False
        
        for row in range(model.rowCount()):
            prod_item = model.item(row, 1)
            # Find the product by name
            if prod_item and prod_item.text() == product_name:
                stock_item = model.item(row, 3)
                if stock_item:
                    try:
                        # This stock has already been reduced by `add_to_cart`
                        new_stock_in_db = int(stock_item.text())
                        product_found = True
                    except Exception:
                        pass
                break
        
        # 3. Update or Delete Product in the actual database
        if product_found:
            if new_stock_in_db > 0:
                # Update stock in DB to the remaining quantity
                database.update_product_stock(product_name, new_stock_in_db)
            elif new_stock_in_db <= 0:
                # Delete product if stock reached or went below zero
                database.delete_product(product_name)

# --- End of NEW FUNCTION ---

parts = QLabel("total items:", window)
fonts = QFont("Ethnocentric", 15)
parts.setFont(fonts)
parts.setStyleSheet("color: white")
parts.setGeometry(290, 594, 200, 30)

# --- Exit and Next buttons at bottom ---
exit_font = QFont("Ethnocentric", 12)
exit_btn = QPushButton("EXIT", window)
exit_btn.setFont(exit_font)
exit_btn.setGeometry(280, 710, 100, 40)
exit_btn.setStyleSheet(inactive_style)
exit_btn.clicked.connect(app.quit)


# --- show_my_cart (single definitive implementation) ---
def show_my_cart():
    set_active(myCart)

    # Hide main content widgets except sidebar
    for w in window.children():
        if w not in [sidenav, mainMenu, myCart, about, logo, justin, redGuy, title]:
            try:
                w.hide()
            except Exception:
                pass

    # Cart Table
    cart_table = QTableView(window)
    cart_model = QStandardItemModel(0, 5)
    cart_model.setHorizontalHeaderLabels(['Category', 'Product', 'Price', 'Qty', 'Remove'])
    cart_table.setGeometry(280, 70, 1064, 400)
    cart_table.verticalHeader().setVisible(False)
    cart_table.setFont(QFont('Arial', 13))
    cart_table.verticalHeader().setDefaultSectionSize(30)
    cart_table.horizontalHeader().setDefaultSectionSize(212)
    cart_table.setStyleSheet("background-color: #363636; border: 1px solid gray; color: white;")
    cart_table.horizontalHeader().setStyleSheet(""" QHeaderView::section {
            background-color: #363636;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: 1px solid gray;
            padding: 5px;
        }""")

    # Fill cart model from cart_items
    for row, item in enumerate(cart_items):
        # item = [category, name, price(float), qty(int)]
        cart_model.setItem(row, 0, QStandardItem(str(item[0])))
        cart_model.setItem(row, 1, QStandardItem(str(item[1])))
        cart_model.setItem(row, 2, QStandardItem(f"{item[2]:.2f} PHP"))
        cart_model.setItem(row, 3, QStandardItem(str(item[3])))
        # Leave 'Remove' column empty for now
    cart_table.setModel(cart_model)
    cart_table.show()

    # Header text for cart
    if not hasattr(window, 'cart_header'):
        cart_header = QLabel("YOUR CART", window)
        cart_header.setFont(QFont("Ethnocentric", 22))
        cart_header.setStyleSheet("color: white")
        cart_header.setGeometry(280, 20, 300, 30)
        window.cart_header = cart_header
    window.cart_header.show()

    # Totals
    total_payment = sum([item[2] * item[3] for item in cart_items]) if cart_items else 0.0
    total_items = sum([item[3] for item in cart_items]) if cart_items else 0

    total_pay_label = QLabel(f"TOTAL PAYMENT: {total_payment:.2f} PHP", window)
    total_pay_label.setFont(QFont("Ethnocentric", 13))
    total_pay_label.setStyleSheet("color: white")
    total_pay_label.setGeometry(290, 480, 400, 30)
    total_pay_label.show()

    total_items_label = QLabel(f"TOTAL ITEMS: {total_items}", window)
    total_items_label.setFont(QFont("Ethnocentric", 13))
    total_items_label.setStyleSheet("color: white")
    total_items_label.setGeometry(290, 510, 400, 30)
    total_items_label.show()

    # BUY Button
    buy_btn = QPushButton("BUY", window)
    buy_btn.setFont(QFont("Ethnocentric", 16))
    buy_btn.setGeometry(1200, 500, 120, 50)
    buy_btn.setStyleSheet("background-color: #4a4a4a; color: white; border-radius: 10px;")
    buy_btn.show()

    # Wrapper to execute purchase logic then show popup
    def trigger_purchase_and_popup():
        if cart_items:
            # 1. Process the database changes (update stock, record sale, delete out-of-stock)
            process_purchase()
            # 2. Show the confirmation
            show_thank_you_popup()
        else:
            # Simple error dialog if cart is empty
            QMessageBox.warning(window, "Cart Empty", "Your cart is empty. Please add items before buying.")


    def show_thank_you_popup():
        popup = QDialog(window)
        popup.setWindowFlags(Qt.FramelessWindowHint)
        popup.setStyleSheet("background-color: #232323;")
        popup.setFixedSize(500, 400)

        # Center the popup
        qr = popup.frameGeometry()
        cp = window.frameGeometry().center()
        qr.moveCenter(cp)
        popup.move(qr.topLeft())

        # Image
        img_label = QLabel(popup)
        pix = QPixmap('D:/Python Final Project/Images/nabunturan.png')
        pix = pix.scaled(180, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img_label.setPixmap(pix)
        img_label.setGeometry(180, 20, 180, 220)

        # Thank you text
        thank_label = QLabel("THANK YOU FOR SHOPPING\nWITH US", popup)
        thank_label.setFont(QFont("Ethnocentric", 15))
        thank_label.setStyleSheet("color: #2643DE;")
        thank_label.setAlignment(Qt.AlignCenter)
        thank_label.setGeometry(50, 240, 400, 60)

        # Buttons
        back_btn = QPushButton("BACK TO MENU", popup)
        back_btn.setFont(QFont("Ethnocentric", 9))
        back_btn.setGeometry(80, 320, 150, 40)
        back_btn.setStyleSheet("background-color: #bdbdbd; color: #2643DE; border-radius: 10px;")

        exit_btn2 = QPushButton("EXIT", popup)
        exit_btn2.setFont(QFont("Ethnocentric", 12))
        exit_btn2.setGeometry(270, 320, 150, 40)
        exit_btn2.setStyleSheet("background-color: #bdbdbd; color: #2643DE; border-radius: 10px;")

        def back_to_menu():
            popup.accept()
            # Clear cart and refresh everything for a new transaction
            cart_items.clear()
            show_main_menu() # Calls loadProducts() internally

        def exit_app():
            app.quit()

        back_btn.clicked.connect(back_to_menu)
        exit_btn2.clicked.connect(exit_app)

        popup.exec_()

    buy_btn.clicked.connect(trigger_purchase_and_popup)

    # Store references to avoid garbage collection
    window.cart_table = cart_table
    window.cart_model = cart_model
    window.total_pay_label = total_pay_label
    window.total_items_label = total_items_label
    window.buy_btn = buy_btn

# connect myCart after defining it
myCart.clicked.connect(show_my_cart)
about.clicked.connect(lambda: set_active(about))

next_btn = QPushButton("NEXT", window)
next_btn.setFont(QFont("Ethnocentric", 12))
next_btn.setGeometry(1230, 710, 100, 40)
next_btn.setStyleSheet(inactive_style)
next_btn.clicked.connect(show_my_cart)

# Show main menu by default
show_main_menu()

# --- Show window ---
window.showFullScreen()
sys.exit(app.exec_())