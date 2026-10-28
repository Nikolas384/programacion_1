import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import csv
from google.colab import files

class StoreItem:
    def __init__(self, itemName, itemCategory, itemPrice, itemStock):
        self.itemName = itemName
        self.itemCategory = itemCategory
        self.itemPrice = itemPrice
        self.itemStock = itemStock
        self.itemsSold = 0

class InventorySystem:
    def __init__(self):
        self.dictItems = {}
  
    def addNewItem(self, newItem):
        self.dictItems[newItem.itemName] = newItem
  
    def deleteItem(self, targetName):
        if targetName in self.dictItems:
            del self.dictItems[targetName]
            return True
        return False
    
    def processSale(self, targetName, amountToSell):
        if targetName in self.dictItems:
            currentItem = self.dictItems[targetName]
            if currentItem.itemStock >= amountToSell:
                currentItem.itemStock -= amountToSell
                currentItem.itemsSold += amountToSell
                return True
        return False

class InventoryInterface:
    def __init__(self):
        self.inventoryMgr = InventorySystem()
        
        # --- UI Elements (Widgets en Colab) ---
        self.lblTitle = widgets.HTML("<h2 style='color: #0056b3;'>📱 Sistema de Inventario - Accesorios</h2>")
        
        self.inputItemName = widgets.Text(description="Nombre:")
        self.inputItemCategory = widgets.Text(description="Categoría:")
        self.inputItemPrice = widgets.FloatText(description="Precio:")
        self.inputItemStock = widgets.IntText(description="Stock:")
        
        self.btnAddItem = widgets.Button(description="Agregar Producto", button_style='success', icon='plus')
        self.btnRemoveItem = widgets.Button(description="Eliminar Producto", button_style='danger', icon='trash')
        self.btnRegisterSale = widgets.Button(description="Registrar Venta", button_style='info', icon='shopping-cart')
        self.btnExportReport = widgets.Button(description="Descargar Reporte", button_style='warning', icon='download')
        
        # Dropdown para reemplazar la selección de la tabla de Tkinter
        self.dropdownSelect = widgets.Dropdown(description="Seleccionar:")
        
        self.outputDisplay = widgets.Output()
        self.tableDisplay = widgets.Output()
        
        # --- Conexión de Eventos ---
        self.btnAddItem.on_click(self.eventAddItem)
        self.btnRemoveItem.on_click(self.eventRemoveItem)
        self.btnRegisterSale.on_click(self.eventRegisterSale)
        self.btnExportReport.on_click(self.eventExportCSV)
        
        # --- Ensamblaje de la Interfaz ---
        formBox = widgets.VBox([self.inputItemName, self.inputItemCategory, self.inputItemPrice, self.inputItemStock])
        actionBox = widgets.HBox([self.btnAddItem, self.dropdownSelect, self.btnRegisterSale, self.btnRemoveItem])
        
        display(self.lblTitle, formBox, actionBox, self.btnExportReport, self.outputDisplay, self.tableDisplay)
        self.refreshDataTable()

    def refreshDataTable(self):
        # Actualizar opciones del menú desplegable dinámicamente
        self.dropdownSelect.options = list(self.inventoryMgr.dictItems.keys())
        
        with self.tableDisplay:
            clear_output(wait=True)
            htmlContent = """
            <table style="width:100%; border-collapse: collapse; text-align: left; font-family: sans-serif;">
                <tr style="background-color: #0056b3; color: white;">
                    <th style="padding: 8px; border: 1px solid #ddd;">Nombre</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Categoría</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Precio</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Stock</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Vendidos</th>
                </tr>
            """
            
            # TRANSFORMACIÓN: Cambio de ciclo 'for' a 'while'
            listItems = list(self.inventoryMgr.dictItems.values())
            indexCounter = 0
            
            while indexCounter < len(listItems):
                curr = listItems[indexCounter]
                htmlContent += f"""
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">{curr.itemName}</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{curr.itemCategory}</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">${curr.itemPrice:.2f}</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{curr.itemStock}</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{curr.itemsSold}</td>
                </tr>
                """
                indexCounter += 1
                
            htmlContent += "</table>"
            display(HTML(htmlContent))

    def eventAddItem(self, buttonContext):
        with self.outputDisplay:
            clear_output(wait=True)
            try:
                newName = self.inputItemName.value.strip()
                if not newName:
                    print("❌ Error: El nombre no puede estar vacío.")
                    return
                
                newItemData = StoreItem(
                    itemName = newName,
                    itemCategory = self.inputItemCategory.value,
                    itemPrice = float(self.inputItemPrice.value),
                    itemStock = int(self.inputItemStock.value)
                )
                
                self.inventoryMgr.addNewItem(newItemData)
                self.refreshDataTable()
                print("✅ Producto agregado correctamente.")
                
                self.inputItemName.value = ""
                self.inputItemCategory.value = ""
                self.inputItemPrice.value = 0.0
                self.inputItemStock.value = 0
            except ValueError:
                print("❌ Error: Ingrese valores numéricos válidos en Precio y Stock.")

    def eventRemoveItem(self, buttonContext):
        with self.outputDisplay:
            clear_output(wait=True)
            targetName = self.dropdownSelect.value
            if targetName:
                self.inventoryMgr.deleteItem(targetName)
                self.refreshDataTable()
                print(f"✅ Producto '{targetName}' eliminado.")
            else:
                print("⚠️ Seleccione un producto primero.")

    def eventRegisterSale(self, buttonContext):
        with self.outputDisplay:
            clear_output(wait=True)
            targetName = self.dropdownSelect.value
            if targetName:
                successSale = self.inventoryMgr.processSale(targetName, 1)
                if successSale:
                    self.refreshDataTable()
                    print(f"🛒 Venta registrada para '{targetName}'.")
                else:
                    print(f"❌ Error: No hay stock suficiente de '{targetName}'.")
            else:
                print("⚠️ Seleccione un producto primero.")

    def eventExportCSV(self, buttonContext):
        with self.outputDisplay:
            clear_output(wait=True)
            fileName = "reporteInventario.csv"
            with open(fileName, mode="w", newline="", encoding="utf-8") as csvFile:
                csvWriter = csv.writer(csvFile)
                csvWriter.writerow(["Nombre", "Categoría", "Precio", "Stock", "Vendidos"])
                
                for keyName in self.inventoryMgr.dictItems:
                    prod = self.inventoryMgr.dictItems[keyName]
                    csvWriter.writerow([prod.itemName, prod.itemCategory, prod.itemPrice, prod.itemStock, prod.itemsSold])
            
            files.download(fileName)
            print("📄 Reporte generado y descargando...")

# Iniciar la aplicación
appInventory = InventoryInterface()