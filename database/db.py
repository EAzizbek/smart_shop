import asyncpg
from config import config

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )


    # ---------- USERS ----------
    async def add_user(self, telegram_id, full_name, phone=None):
        query = """
        INSERT INTO users (telegram_id, full_name, phone)
        VALUES ($1, $2, $3)
        ON CONFLICT (telegram_id) DO NOTHING
        """
        await self.pool.execute(query, telegram_id, full_name, phone)
    
    async def user_exists(self, telegram_id):
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id=$1)"
        return await self.pool.fetchval(query, telegram_id)
    
    async def get_users(self):
        query = "SELECT telegram_id, full_name, role FROM users ORDER BY id"
        return await self.pool.fetch(query)


    async def get_user_by_telegram_id(self, telegram_id):
        query = "SELECT * FROM users WHERE telegram_id=$1"
        return await self.pool.fetchrow(query, telegram_id)
    
    async def get_user_id_by_telegram_id(self, telegram_id):
        query = "SELECT id FROM users WHERE telegram_id=$1"
        return await self.pool.fetchval(query, telegram_id)

    async def get_user_role(self, telegram_id):
        query = "SELECT role FROM users WHERE telegram_id=$1"
        return await self.pool.fetchval(query, telegram_id)

    async def set_user_role(self, telegram_id, role):
        query = "UPDATE users SET role=$1 WHERE telegram_id=$2"
        await self.pool.execute(query, role, telegram_id)

    # ---------- PRODUCTS ----------
    async def add_product(self, name, price, description):
        query = """
        INSERT INTO products (name, price, description)
        VALUES ($1, $2, $3)
        """
        await self.pool.execute(query, name, price, description)

    async def get_products(self):
        query = "SELECT * FROM products WHERE is_active=TRUE"
        return await self.pool.fetch(query)
    
    async def get_product(self, product_id):
        query = "SELECT name,price,description FROM products WHERE id=$1"
        return await self.pool.fetchrow(query, product_id)
    
    async def update_product(self, product_id, name, price, description):
        query = """
        UPDATE products
        SET name = $1,
        price = $2,
        description = $3
        WHERE id = $4
        """
        await self.pool.execute(query, name, price, description, product_id)


    async def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id=$1"
        await self.pool.execute(query, product_id)

    # ---------- ORDERS ----------
    async def create_order(self, user_id):
        query = "INSERT INTO orders (user_id) VALUES ($1) RETURNING id"
        return await self.pool.fetchval(query, user_id)

    async def add_order_item(self, order_id, product_id, quantity):
        query = """
        INSERT INTO order_items (order_id, product_id, quantity)
        VALUES ($1, $2, $3)
        """
        await self.pool.execute(query, order_id, product_id, quantity)
    
    async def get_or_create_cart(self, user_id):
        # Avval cart bormi tekshiramiz
        query = """
        SELECT id FROM orders
        WHERE user_id=$1 AND status='cart'
        """
        cart_id = await self.pool.fetchval(query, user_id)

        if cart_id:
            return cart_id

        # Yo‘q bo‘lsa yangi cart ochamiz
        query = """
        INSERT INTO orders (user_id, status)
        VALUES ($1, 'cart')
        RETURNING id
        """
        return await self.pool.fetchval(query, user_id)
    
    async def add_to_cart(self, user_id, product_id, quantity=1):
        cart_id = await self.get_or_create_cart(user_id)

        query = """
        INSERT INTO order_items (order_id, product_id, quantity)
        VALUES ($1, $2, $3)
        ON CONFLICT (order_id, product_id)
        DO UPDATE SET quantity = order_items.quantity + EXCLUDED.quantity
        """
        await self.pool.execute(query, cart_id, product_id, quantity)

    async def get_cart_items(self, user_id):
        query = """
        SELECT 
            p.name,
            p.price,
            oi.quantity,
            (p.price * oi.quantity) AS total
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        JOIN products p ON p.id = oi.product_id
        WHERE o.user_id=$1 AND o.status='cart'
        """
        return await self.pool.fetch(query, user_id)
