import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from database import Database


class MainMenu:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setGeometry(0, 0, 1366, 768)
        self.window.setStyleSheet("background-color: #242222")

        # Styles
        self.inactive_style = """
            border-radius: 10px;
            background-color: #424242;
            color: white;
        """
        self.active_style = """
            border-radius: 10px;
            background-color: #5269FF;
            color: white;
        """

        self.database = Database()
        self.cart_items = []

        self.setup_ui()
        self.show_main_menu()
        self.window.showFullScreen()
        sys.exit(self.app.exec_())

    def setup_ui(self):
        # Sidebar
        self.sidenav = QFrame(self.window)
        self.sidenav.setGeometry(0, 0, 250, 768)
        self.sidenav.setStyleSheet("background-color: #424242;")

        logo = QLabel(self.sidenav)
        pixmap = QPixmap("D:/Python Final Project/Images/logoo.png")
        size = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(size)
        logo.setGeometry(20, 30, 260, 200)

        justin = QLabel(self.sidenav)
        pixmap2 = QPixmap('D:/Python Final Project/Images/nabunturan.png')
        size2 = pixmap2.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        justin.setPixmap(size2)
        justin.setGeometry(10, 520, 150, 300)

        redGuy = QLabel(self.sidenav)
        pixmap3 = QPixmap('D:/Python Final Project/Images/RedGuy.png')
        size3 = pixmap3.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        redGuy.setPixmap(size3)
        redGuy.setGeometry(120, 520, 150, 300)

        title = QLabel("JUSTIN STORE", self.sidenav)
        font = QFont("Ethnocentric", 15)
        title.setFont(font)
        title.setStyleSheet("color: #2643DE")
        title.setGeometry(20, 220, 200, 30)

        butfont = QFont("Ethnocentric", 14)

        self.mainMenu_btn = QPushButton("MAIN MENU", self.sidenav)
        self.mainMenu_btn.setFont(butfont)
        self.mainMenu_btn.setGeometry(20, 330, 200, 50)
        self.mainMenu_btn.setStyleSheet(self.active_style)
        self.mainMenu_btn.clicked.connect(self.show_main_menu)

        self.myCart_btn = QPushButton("MY CART", self.sidenav)
        self.myCart_btn.setFont(butfont)
        self.myCart_btn.setGeometry(20, 400, 200, 50)
        self.myCart_btn.setStyleSheet(self.inactive_style)
        self.myCart_btn.clicked.connect(self.show_my_cart)

        self.about_btn = QPushButton("ABOUT", self.sidenav)
        self.about_btn.setFont(butfont)
        self.about_btn.setGeometry(20, 470, 200, 50)
        self.about_btn.setStyleSheet(self.inactive_style)
        self.about_btn.clicked.connect(lambda: self.set_active(self.about_btn))

        self.parts = QLabel("PARTS", self.window)
        fonts = QFont("Ethnocentric", 22)
        self.parts.setFont(fonts)
        self.parts.setStyleSheet("color: white")
        self.parts.setGeometry(280, 20, 200, 30)

        self.table = QTableView(self.window)
        self.model = QStandardItemModel(7, 5)
        self.model.setHorizontalHeaderLabels(['Category', 'Product', 'Price', 'Stock', ' '])
        self.table.setGeometry(280, 70, 1064, 520)
        self.table.verticalHeader().setVisible(False)
        font = QFont()
        font.setPointSize(15)
        self.table.setFont(font)
        self.table.verticalHeader().setDefaultSectionSize(30)
        self.table.horizontalHeader().setDefaultSectionSize(212)
        self.table.setStyleSheet("background-color: #363636; border: 1px solid gray; color: white;")
        self.table.horizontalHeader().setStyleSheet(""" QHeaderView::section {
            background-color: #363636;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: 1px solid gray;
            padding: 5px;
        }""")
        self.table.setModel(self.model)

        exit_font = QFont("Ethnocentric", 12)
        self.exit_btn = QPushButton("EXIT", self.window)
        self.exit_btn.setFont(exit_font)
        self.exit_btn.setGeometry(280, 710, 100, 40)
        self.exit_btn.setStyleSheet(self.inactive_style)
        self.exit_btn.clicked.connect(self.app.quit)

        self.next_btn = QPushButton("NEXT", self.window)
        self.next_btn.setFont(QFont("Ethnocentric", 12))
        self.next_btn.setGeometry(1230, 710, 100, 40)
        self.next_btn.setStyleSheet(self.inactive_style)
        self.next_btn.clicked.connect(self.show_my_cart)

    def set_active(self, button):
        self.mainMenu_btn.setStyleSheet(self.inactive_style)
        self.myCart_btn.setStyleSheet(self.inactive_style)
        self.about_btn.setStyleSheet(self.inactive_style)
        button.setStyleSheet(self.active_style)

    def loadProducts(self):
        self.model.removeRows(0, self.model.rowCount())
        products = self.database.get_all_products() or []

        for row, row_data in enumerate(products):
            try:
                category = row_data[0]
                product_name = row_data[1]
                price = float(row_data[2])
                stock = int(row_data[3])
            except Exception:
                continue

            row_items = [
                QStandardItem(str(category)),
                QStandardItem(str(product_name)),
                QStandardItem(f"{price:.2f}"),
                QStandardItem(str(stock))
            ]
            self.model.appendRow(row_items)

            btn = QPushButton("Add to Cart")
            btn.setFont(QFont("Ethnocentric", 10))
            btn.setStyleSheet("background-color: #424242; color: white;")

            product_tuple = (category, product_name, price, stock)
            btn.clicked.connect(lambda checked, p=product_tuple: self.add_to_cart(p))
            if stock <= 0:
                btn.setEnabled(False)

            self.table.setIndexWidget(self.model.index(row, 4), btn)

    def add_to_cart(self, product):
        if not product:
            return
        category, name, price, stock = product

        try:
            price = float(price)
        except Exception:
            price = float(str(price).replace(' PHP', '').replace(',', '').strip())

        for item in self.cart_items:
            if item[1] == str(name):
                item[3] += 1
                break
        else:
            self.cart_items.append([str(category), str(name), price, 1])

        for row in range(self.model.rowCount()):
            prod_item = self.model.item(row, 1)
            if prod_item and prod_item.text() == str(name):
                stock_item = self.model.item(row, 3)
                if stock_item:
                    try:
                        current_stock = int(stock_item.text())
                    except Exception:
                        current_stock = 0
                    if current_stock > 0:
                        new_stock = current_stock - 1
                        self.model.setItem(row, 3, QStandardItem(str(new_stock)))
                        btn = self.table.indexWidget(self.model.index(row, 4))
                        if btn and new_stock == 0:
                            btn.setEnabled(False)
                break

    def process_purchase(self):
        for item in self.cart_items:
            category, product_name, price, purchased_qty = item
            total_price = price * purchased_qty
            self.database.add_sale_history(product_name, price, purchased_qty, total_price)

            new_stock_in_db = 0
            product_found = False

            for row in range(self.model.rowCount()):
                prod_item = self.model.item(row, 1)
                if prod_item and prod_item.text() == product_name:
                    stock_item = self.model.item(row, 3)
                    if stock_item:
                        try:
                            new_stock_in_db = int(stock_item.text())
                            product_found = True
                        except Exception:
                            pass
                    break

            if product_found:
                if new_stock_in_db > 0:
                    self.database.update_product_stock(product_name, new_stock_in_db)
                elif new_stock_in_db <= 0:
                    self.database.delete_product(product_name)

    def show_main_menu(self):
        self.set_active(self.mainMenu_btn)
        for attr in ['cart_table', 'cart_model', 'total_pay_label', 'total_items_label', 'buy_btn']:
            if hasattr(self, attr):
                widget = getattr(self, attr)
                if isinstance(widget, QWidget):
                    widget.hide()
        self.parts.show()
        self.table.show()
        self.exit_btn.show()
        self.next_btn.show()
        self.loadProducts()

    def show_my_cart(self):
        self.set_active(self.myCart_btn)
        for w in self.window.children():
            if w not in [self.sidenav, self.mainMenu_btn, self.myCart_btn, self.about_btn]:
                try:
                    w.hide()
                except Exception:
                    pass
        self.cart_table = QTableView(self.window)
        self.cart_model = QStandardItemModel(0, 5)
        self.cart_model.setHorizontalHeaderLabels(['Category', 'Product', 'Price', 'Qty', 'Remove'])
        self.cart_table.setGeometry(280, 70, 1064, 400)
        self.cart_table.verticalHeader().setVisible(False)
        self.cart_table.setFont(QFont('Arial', 13))
        self.cart_table.verticalHeader().setDefaultSectionSize(30)
        self.cart_table.horizontalHeader().setDefaultSectionSize(212)
        self.cart_table.setStyleSheet("background-color: #363636; border: 1px solid gray; color: white;")
        self.cart_table.horizontalHeader().setStyleSheet(""" QHeaderView::section {
            background-color: #363636;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: 1px solid gray;
            padding: 5px;
        }""")
        for row, item in enumerate(self.cart_items):
            self.cart_model.setItem(row, 0, QStandardItem(str(item[0])))
            self.cart_model.setItem(row, 1, QStandardItem(str(item[1])))
            self.cart_model.setItem(row, 2, QStandardItem(f"{item[2]:.2f} PHP"))
            self.cart_model.setItem(row, 3, QStandardItem(str(item[3])))
        self.cart_table.setModel(self.cart_model)
        self.cart_table.show()
        total_payment = sum([item[2] * item[3] for item in self.cart_items]) if self.cart_items else 0.0
        total_items = sum([item[3] for item in self.cart_items]) if self.cart_items else 0
        self.total_pay_label = QLabel(f"TOTAL PAYMENT: {total_payment:.2f} PHP", self.window)
        self.total_pay_label.setFont(QFont("Ethnocentric", 13))
        self.total_pay_label.setStyleSheet("color: white")
        self.total_pay_label.setGeometry(290, 480, 400, 30)
        self.total_pay_label.show()
        self.total_items_label = QLabel(f"TOTAL ITEMS: {total_items}", self.window)
        self.total_items_label.setFont(QFont("Ethnocentric", 13))
        self.total_items_label.setStyleSheet("color: white")
        self.total_items_label.setGeometry(290, 510, 400, 30)
        self.total_items_label.show()
        self.buy_btn = QPushButton("BUY", self.window)
        self.buy_btn.setFont(QFont("Ethnocentric", 16))
        self.buy_btn.setGeometry(1200, 500, 120, 50)
        self.buy_btn.setStyleSheet("background-color: #4a4a4a; color: white; border-radius: 10px;")
        self.buy_btn.show()
        def trigger_purchase_and_popup():
            if self.cart_items:
                self.process_purchase()
                self.show_thank_you_popup()
            else:
                QMessageBox.warning(self.window, "Cart Empty", f"<font color='white'>Your cart is empty. Please add items before buying.")
        self.buy_btn.clicked.connect(trigger_purchase_and_popup)

    def show_thank_you_popup(self):
        popup = QDialog(self.window)
        popup.setWindowFlags(Qt.FramelessWindowHint)
        popup.setStyleSheet("background-color: #232323;")
        popup.setFixedSize(500, 400)

        qr = popup.frameGeometry()
        cp = self.window.frameGeometry().center()
        qr.moveCenter(cp)
        popup.move(qr.topLeft())

        img_label = QLabel(popup)
        pix = QPixmap('D:/Python Final Project/Images/nabunturan.png')
        pix = pix.scaled(180, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img_label.setPixmap(pix)
        img_label.setGeometry(180, 20, 180, 220)

        thank_label = QLabel("THANK YOU FOR SHOPPING\nWITH US", popup)
        thank_label.setFont(QFont("Ethnocentric", 15))
        thank_label.setStyleSheet("color: #2643DE;")
        thank_label.setAlignment(Qt.AlignCenter)
        thank_label.setGeometry(50, 240, 400, 60)

        back_btn = QPushButton("BACK TO MENU", popup)
        back_btn.setFont(QFont("Ethnocentric", 9))
        back_btn.setGeometry(80, 320, 150, 40)
        back_btn.setStyleSheet("background-color: #bdbdbd; color: #2643DE; border-radius: 10px;")
        back_btn.clicked.connect(lambda: (popup.accept(), self.cart_items.clear(), self.show_main_menu()))

        exit_btn2 = QPushButton("EXIT", popup)
        exit_btn2.setFont(QFont("Ethnocentric", 12))
        exit_btn2.setGeometry(270, 320, 150, 40)
        exit_btn2.setStyleSheet("background-color: #bdbdbd; color: #2643DE; border-radius: 10px;")
        exit_btn2.clicked.connect(self.app.quit)
        popup.exec_()


if __name__ == "__main__":
    MainMenu()
