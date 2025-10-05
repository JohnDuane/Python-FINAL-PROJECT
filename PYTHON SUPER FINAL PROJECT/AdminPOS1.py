import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

from database import Database 


class menu:

    def __init__(self):
        super().__init__()

        self.window = QWidget()
        self.window.setGeometry(0, 0, 1366, 768)
        self.window.setStyleSheet("background-color: #242222")
        
        # --- State Variables ---
        self.selected_table = None # 'Product' or 'Sales'
        self.selected_product_data = None # Data of selected Product row
        self.selected_sale_data = None    # Data of selected Sale row
        # -----------------------

        read = QPushButton("EXIT", self.window)
        read.setFont(QFont("Ethnocentric", 15))
        read.setGeometry(400, 670, 300, 50)
        read.setStyleSheet("border-radius: 10px; background-color: lightgray; color: #2742DE")
        read.clicked.connect(self.window.close)


        panel = QFrame(self.window)
        panel.setStyleSheet("background-color: #D4D8FB")
        panel.setGeometry(15, 15, 1025, 630)

        midpanel = QFrame(panel)
        midpanel.setGeometry(497, 0, 30, 630)
        midpanel.setStyleSheet("background-color: #242222")

        

        category = QLabel(panel)
        category.setText("CATEGORY:")
        category.setGeometry(15, 480, 150, 30)
        category.setFont(QFont("Ethnocentric", 14))
        
        choices = QComboBox(panel)
        choices.addItem("CPU")
        choices.setFont(QFont("Ethnocentric"))
        choices.addItem("RAM")
        choices.addItem("CASE")
        choices.addItem("PSU")
        choices.addItem("STORAGE")
        choices.setGeometry(175, 480, 150, 30)
        choices.setStyleSheet("background-color: #F2F2F2")
        self.choices = choices 

        product = QLabel(panel)
        product.setText("PRODUCT:")
        product.setGeometry(25, 515, 150, 30)
        product.setFont(QFont("Ethnocentric", 14))
        
        prodField = QLineEdit(panel)
        prosize = QFont()
        prosize.setPointSize(12)
        prodField.setFont(prosize)
        prodField.setGeometry(175, 515, 200, 30)
        prodField.setStyleSheet("background-color: #F2F2F2")
        self.prodField = prodField 

        quantity = QLabel(panel)
        quantity.setText("QUANTITY:")
        quantity.setGeometry(17, 550, 150, 30)
        quantity.setFont(QFont("Ethnocentric", 14))
        
        quanField = QLineEdit(panel)
        quansize = QFont()
        quansize.setPointSize(12)
        quanField.setFont(quansize)
        quanField.setGeometry(175, 550, 50, 30)
        quanField.setStyleSheet("background-color: #F2F2F2")
        self.quanField = quanField 

        price = QLabel(panel)
        price.setText("PRICE:")
        price.setGeometry(73, 585, 150, 30)
        price.setFont(QFont("Ethnocentric", 14))
        
        priceField = QLineEdit(panel)
        pricesize = QFont()
        pricesize.setPointSize(12)
        priceField.setFont(pricesize)
        priceField.setGeometry(175, 585, 50, 30)
        priceField.setStyleSheet("background-color: #F2F2F2")
        self.priceField = priceField 

        self.totalSales = 0

        clear_history = QPushButton("CLEAR HISTORY", panel)
        clear_history.setFont(QFont("Ethnocentric", 12))
        clear_history.setGeometry(550, 570, 200, 40)
        clear_history.setStyleSheet("border-radius: 10px; background-color: #4E4C4C; color: #2742DE")
        def clearSalesHistory():
            reply = QMessageBox.question(
               self.window, 
               "Confirm Clear History", 
               "Are you sure you want to delete all sales records?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
               try:
                  self.database.clear_sales_history()
                  self.loadSalesHistory()
                  QMessageBox.information(self.window, "Success", "All sales history has been cleared.")
               except Exception as e:
                  QMessageBox.critical(self.window, "Error", f"Failed to clear sales history: {e}")

        clear_history.clicked.connect(clearSalesHistory)


        table = QTableView(panel)
        model = QStandardItemModel(0, 5)
        model.setHorizontalHeaderLabels(['Category', 'Products', 'Price', 'Quantity', 'Total'])
        table.setGeometry(9, 70, 478, 400)
        
        font = QFont()
        font.setPointSize(15)
        table.setFont(font)
        table.verticalHeader().setDefaultSectionSize(30)
        table.horizontalHeader().setDefaultSectionSize(95)
        table.setStyleSheet("background-color: #363636; border: 1px solid gray; color: white;")
        table.horizontalHeader().setStyleSheet(""" QHeaderView::section {
        background-color: #363636;
        color: white;
        font-size: 14px;
        font-weight: bold;
        border: 1px solid gray;
        padding: 5px;
    }""")
        table.setModel(model)
        self.table = table
        self.model = model


        table2 = QTableView(panel)
        model2 = QStandardItemModel(0, 5) 
        model2.setHorizontalHeaderLabels(['Date', 'Product', 'Price', 'Quantity', 'Total'])
        table2.setGeometry(537, 70, 478, 400)
        
        font2 = QFont()
        font2.setPointSize(12)
        table2.setFont(font2)
        table2.verticalHeader().setDefaultSectionSize(30)
        table2.horizontalHeader().setDefaultSectionSize(95)
        table2.setStyleSheet("background-color: #363636; border: 1px solid gray; color: white")
        table2.horizontalHeader().setStyleSheet(""" QHeaderView::section {
        background-color: #363636;
        color: white;
        font-size: 14px;
        font-weight: bold;
        border: 1px solid gray;
        padding: 5px;
    }""")
        table2.setModel(model2)
        self.table2 = table2
        self.model2 = model2


#NAVIGATION BAR
        navbar = QFrame(self.window)
        navbar.setStyleSheet("background-color: #D4D8FB")
        navbar.setGeometry(1057, 15, 295, 715)

#==================================DATABASE CONNECTION=========================================

        self.database = Database()

        def loadProducts():
           self.model.removeRows(0, self.model.rowCount())
           products = self.database.get_all_products()
           for row_data in products:
              row_items = [
                QStandardItem(str(row_data[0])),
                QStandardItem(str(row_data[1])),
                QStandardItem(f"{row_data[2]:.2f}"),
                QStandardItem(str(row_data[3])),
                QStandardItem(f"{row_data[4]:.2f}")
              ]
              self.model.appendRow(row_items)
        self.loadProducts = loadProducts 


        def loadSalesHistory():
            self.model2.removeRows(0, self.model2.rowCount())
            sales = self.database.get_all_sales()
            total_sales_today = 0
            
            for row_data in sales:
                date = str(row_data[0])
                product = str(row_data[1])
                price = float(row_data[2])
                quantity = int(row_data[3])
                total = float(row_data[4])
                
                row_items = [
                    QStandardItem(date),
                    QStandardItem(product),
                    QStandardItem(f"{price:.2f}"),
                    QStandardItem(str(quantity)),
                    QStandardItem(f"{total:.2f}")
                ]
                self.model2.appendRow(row_items)
                
                total_sales_today += total
            
            self.totalSales = total_sales_today
        self.loadSalesHistory = loadSalesHistory 


        loadProducts()
        loadSalesHistory()

        def insertData():
            category = self.choices.currentText()
            product = self.prodField.text()
            try:
                quantity = int(self.quanField.text())
                price = float(self.priceField.text())
            except ValueError:
                QMessageBox.warning(self.window, "Input Error", "Quantity must be an integer and Price must be a number.")
                return

            total = quantity * price

            self.database.add_product(category, product, price, quantity, total)
            self.loadProducts()
            
            self.prodField.clear()
            self.quanField.clear()
            self.priceField.clear()


#=============================================================================

        create = QPushButton("ADD PRODUCT", navbar)
        create.setFont(QFont("Ethnocentric", 12))
        create.setGeometry(40, 40, 230, 40)
        create.setStyleSheet("border-radius: 10px; background-color: #4E4C4C; color: #2742DE")
        create.clicked.connect(insertData)

        update_btn = QPushButton("UPDATE", navbar)
        update_btn.setFont(QFont("Ethnocentric", 12))
        update_btn.setGeometry(40, 100, 230, 40)
        update_btn.setStyleSheet("border-radius: 10px; background-color: #4E4C4C; color: #2742DE")
        update_btn.clicked.connect(self.updateData) 

        delete_btn = QPushButton("REMOVE", navbar)
        delete_btn.setFont(QFont("Ethnocentric", 12))
        delete_btn.setGeometry(40, 160, 230, 40)
        delete_btn.setStyleSheet("border-radius: 10px; background-color: #4E4C4C; color: #2742DE")
        delete_btn.clicked.connect(self.deleteData) 


        photo = QLabel(navbar)
        pixmap = QPixmap("D:/Python Final Project/Images/admin_photo.png")
        size = pixmap.scaled(225, 365, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        photo.setPixmap(size)
        photo.setGeometry(50, 335, 200, 400)


#HEADER
        h1 = QLabel(panel)
        h1.setText("STOCK")
        h1.setGeometry(205, 15, 100, 50)
        h1.setFont(QFont("Ethnocentric", 15))

        h2 = QLabel(panel)
        h2.setText("HISTORY")
        h2.setGeometry(719, 15, 150, 50)
        h2.setFont(QFont("Ethnocentric", 15))

        # --- Connect Table Clicks to Handlers ---
        self.table.clicked.connect(self.product_row_clicked)
        self.table2.clicked.connect(self.sales_row_clicked)


    # --- Methods for Selection and CRUD Operations ---

    def product_row_clicked(self, index):
        """Called when a row in the Product (Stock) table is clicked."""
        
        # --- CRITICAL FIX: Ensure the row is selected in the selection model ---
        self.table2.clearSelection() 
        self.table.selectionModel().select(
            index.siblingAtRow(index.row()), QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        )
        
        self.selected_sale_data = None 
        self.selected_table = 'Product'
        
        row = index.row()
        
        row_data = []
        for col in range(self.model.columnCount()):
            item = self.model.item(row, col)
            row_data.append(item.text() if item else '')
            
        self.selected_product_data = row_data
        
        # Populate fields with current data for product updates
        self.choices.setCurrentText(row_data[0]) 
        self.prodField.setText(row_data[1]) 
        self.priceField.setText(row_data[2].replace(' PHP', '').strip()) 
        self.quanField.setText(row_data[3]) 
        
        
    def sales_row_clicked(self, index):
        """Called when a row in the Sales (History) table is clicked."""
        
        # --- CRITICAL FIX: Ensure the row is selected in the selection model ---
        self.table.clearSelection() 
        self.table2.selectionModel().select(
            index.siblingAtRow(index.row()), QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        )

        self.selected_product_data = None
        self.selected_table = 'Sales'
        
        row = index.row()
        
        row_data = []
        for col in range(self.model2.columnCount()):
            item = self.model2.item(row, col)
            row_data.append(item.text() if item else '')
            
        self.selected_sale_data = row_data
        
        # Clear product input fields 
        self.choices.setCurrentIndex(0) 
        self.prodField.clear()
        self.priceField.clear()
        self.quanField.clear()

    def updateData(self):
        """Updates the selected Product record in the database."""
        
        if self.selected_table != 'Product' or not self.selected_product_data:
            QMessageBox.warning(self.window, "Warning", "Please select a **Product** row and enter new values to update.")
            return

        try:
            old_product_name = self.selected_product_data[1] 
            
            # New values from fields
            category = self.choices.currentText()
            product = self.prodField.text()
            quantity = int(self.quanField.text())
            price = float(self.priceField.text())
            total = quantity * price

            self.database.update_product_details(
                old_product_name, category, product, price, quantity, total
            )
            QMessageBox.information(self.window, "Success", f"Product '{old_product_name}' updated successfully.")
            self.loadProducts() 
            
            # Reset state and fields
            self.selected_table = None
            self.selected_product_data = None
            self.prodField.clear()
            self.priceField.clear()
            self.quanField.clear()
            self.table.clearSelection() 
            
        except ValueError:
            QMessageBox.critical(self.window, "Error", "Invalid data. Quantity must be an integer and Price must be a number.")
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"An error occurred during update: {e}")


    def deleteData(self):
        """Deletes the selected record from either Product or Sales table."""
        
        # This check confirms that a row has been clicked and state variables set.
        if not self.selected_table:
            QMessageBox.warning(self.window, "Warning", "Please **click/select a row** from either table (Stock or History) to delete.")
            return
            
        reply = QMessageBox.question(self.window, 'Confirm Delete',
            "Are you sure you want to permanently delete the selected record?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No:
            return

        try:
            if self.selected_table == 'Product':
                # Ensure we have the necessary data
                if not self.selected_product_data:
                     raise ValueError("Product data not properly loaded for deletion.")
                
                product_name = self.selected_product_data[1]
                self.database.delete_product(product_name)
                QMessageBox.information(self.window, "Success", f"Product '{product_name}' removed from **Stock**.")
                self.loadProducts()

            elif self.selected_table == 'Sales':
                # Ensure we have the necessary data
                if not self.selected_sale_data:
                    raise ValueError("Sale data not properly loaded for deletion.")
                    
                date = self.selected_sale_data[0]
                product_name = self.selected_sale_data[1]
                quantity = int(self.selected_sale_data[3]) 
                self.database.delete_sale(date, product_name, quantity)
                QMessageBox.information(self.window, "Success", f"Sale record for '{product_name}' deleted from **History**.")
                self.loadSalesHistory() 

            # Reset selection state and clear fields
            self.selected_table = None
            self.selected_product_data = None
            self.selected_sale_data = None
            self.prodField.clear()
            self.priceField.clear()
            self.quanField.clear()
            self.table.clearSelection()
            self.table2.clearSelection()

        except ValueError as ve:
             QMessageBox.critical(self.window, "Error", f"Deletion failed: {ve}")
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"An error occurred during deletion: {e}")


    def home(self):
        self.window.showFullScreen()