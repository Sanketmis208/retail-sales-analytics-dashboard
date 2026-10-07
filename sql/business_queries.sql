-- name: monthly_revenue
select
    month,
    round(sum(net_sales), 2) as revenue,
    round(sum(profit), 2) as profit
from fact_sales
where is_cancelled = 0
group by month
order by month;

-- name: customer_retention
select
    round(avg(retained_customer) * 100, 2) as retention_rate,
    count(distinct customer_id) as active_customers,
    round(sum(case when retained_customer = 1 then 1 else 0 end) * 1.0 / count(*), 4) as repeat_order_share
from fact_sales
where is_cancelled = 0;

-- name: regional_sales
select
    region,
    round(sum(net_sales), 2) as revenue,
    round(sum(profit) / nullif(sum(net_sales), 0) * 100, 2) as profit_margin
from fact_sales
where is_cancelled = 0
group by region
order by revenue desc;

-- name: segment_performance
select
    c.segment,
    count(distinct c.customer_id) as customers,
    round(avg(f.net_sales), 2) as avg_order_value,
    round(sum(f.net_sales), 2) as revenue
from fact_sales f
join dim_customers c on c.customer_id = f.customer_id
where f.is_cancelled = 0
group by c.segment
order by revenue desc;

-- name: inventory_risk
select
    sum(case when inventory_status = 'Reorder' then 1 else 0 end) as products_below_reorder,
    sum(case when inventory_status = 'Overstock' then 1 else 0 end) as overstocked_products,
    round(avg(days_of_cover), 1) as avg_days_of_cover
from fact_inventory;

-- name: pricing_opportunities
select
    p.category,
    round(avg(f.discount_pct) * 100, 2) as avg_discount_pct,
    round(avg(f.profit / nullif(f.net_sales, 0)) * 100, 2) as avg_margin_pct,
    round(sum(f.net_sales), 2) as revenue
from fact_sales f
join dim_products p on p.product_id = f.product_id
where f.is_cancelled = 0
group by p.category
having avg(f.discount_pct) >= 0.08
order by avg_margin_pct asc, revenue desc;
