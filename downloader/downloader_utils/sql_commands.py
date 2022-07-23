# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

sql_update_command = """INSERT INTO app_offer (id, price, items_in_stock, product_id)
VALUES(%s, %s, %s, %s) 
ON CONFLICT (id) 
DO 
   UPDATE SET price = %s, items_in_stock = %s;"""

sql_get_products_command = """SELECT id FROM app_product"""
