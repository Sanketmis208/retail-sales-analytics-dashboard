drop table if exists dim_customers;
drop table if exists dim_products;
drop table if exists fact_inventory;
drop table if exists fact_sales;

create table dim_customers (
    customer_id integer primary key,
    customer_name text,
    region text,
    city text,
    age_group text,
    join_date text,
    segment text,
    preferred_channel text
);

create table dim_products (
    product_id integer primary key,
    product_name text,
    category text,
    unit_cost real,
    base_price real,
    supplier_lead_days integer
);

create table fact_inventory (
    product_id integer,
    stock_on_hand integer,
    reorder_point integer,
    days_of_cover real,
    inventory_status text,
    snapshot_date text
);

create table fact_sales (
    order_id integer primary key,
    order_date text,
    customer_id integer,
    product_id integer,
    region text,
    sales_channel text,
    payment_method text,
    quantity integer,
    gross_sales real,
    discount_pct real,
    net_sales real,
    cost_of_goods real,
    profit real,
    shipment_days integer,
    order_status text,
    month text,
    is_returned integer,
    is_cancelled integer,
    retained_customer integer
);
