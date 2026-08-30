with sales as (
    select * from {{ ref('stg_sales') }}
)

select
    store_id,
    count(customer_id) as total_transactions,
    sum(amount) as total_revenue
from sales
group by store_id