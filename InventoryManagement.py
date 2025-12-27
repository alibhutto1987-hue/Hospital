import streamlit as st

# ---------------- Product Class ----------------
class Product:
    def __init__(self, product_id, name, quantity):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity

    def add_stock(self, amount):
        if amount > 0:
            self.quantity += amount
            return True
        return False

    def sell_stock(self, amount):
        if amount > self.quantity:
            return False
        self.quantity -= amount
        return True

    def is_low_stock(self):
        return self.quantity < 5

# ---------------- Session State ----------------
if "products" not in st.session_state:
    st.session_state.products = {}

# ---------------- Dashboard ----------------
st.set_page_config(page_title="Inventory Dashboard", layout="centered")
st.title("🛒 Inventory Management System")

menu = st.sidebar.selectbox(
    "Dashboard Menu",
    ["Add Product", "Add Stock", "Sell Stock", "View Inventory"]
)

# ---------------- Add Product ----------------
if menu == "Add Product":
    st.subheader("➕ Add New Product")
    with st.form("add_form"):
        product_id = st.text_input("Product ID", key="add_id")
        name = st.text_input("Product Name", key="add_name")
        quantity = st.number_input("Initial Quantity", min_value=0, key="add_qty")
        submitted = st.form_submit_button("Add Product")
        if submitted:
            if product_id in st.session_state.products:
                st.error("❌ Product ID already exists!")
            elif product_id == "" or name == "":
                st.warning("⚠️ Fill all fields")
            else:
                st.session_state.products[product_id] = Product(product_id, name, quantity)
                st.success(f"✅ Product '{name}' added successfully!")

# ---------------- Add Stock ----------------
elif menu == "Add Stock":
    st.subheader("📦 Add Stock (Shipment Arrival)")
    with st.form("add_stock_form"):
        product_id = st.text_input("Product ID", key="stock_id")
        amount = st.number_input("Quantity to Add", min_value=1, key="stock_qty")
        submitted = st.form_submit_button("Add Stock")
        if submitted:
            product = st.session_state.products.get(product_id)
            if not product:
                st.error("❌ Product not found")
            else:
                product.add_stock(amount)
                st.success(f"✅ Added {amount} units to '{product.name}'. New quantity: {product.quantity}")

# ---------------- Sell Stock ----------------
elif menu == "Sell Stock":
    st.subheader("💰 Sell Product")
    with st.form("sell_stock_form"):
        product_id = st.text_input("Product ID", key="sell_id")
        amount = st.number_input("Quantity to Sell", min_value=1, key="sell_qty")
        submitted = st.form_submit_button("Sell Stock")
        if submitted:
            product = st.session_state.products.get(product_id)
            if not product:
                st.error("❌ Product not found")
            elif not product.sell_stock(amount):
                st.error(f"❌ Not enough stock! Available: {product.quantity}")
            else:
                st.success(f"✅ Sold {amount} units of '{product.name}'. Remaining: {product.quantity}")
                if product.is_low_stock():
                    st.warning(f"⚠️ LOW STOCK ALERT for '{product.name}'! Re-stock immediately.")

# ---------------- View Inventory ----------------
elif menu == "View Inventory":
    st.subheader("📋 Inventory Status")
    if not st.session_state.products:
        st.warning("⚠️ No products in inventory.")
    else:
        for product in st.session_state.products.values():
            low_stock = "⚠️ Low Stock" if product.is_low_stock() else ""
            st.markdown("---")
            st.write(f"**ID:** {product.product_id} | **Name:** {product.name} | **Quantity:** {product.quantity} {low_stock}")
