with source as (
    select * from read_csv_auto('../data/raw_sales.csv')
),

cleaned as (
    select
        cast(customer_id as varchar) as customer_id,
        cast(store_location as varchar) as store_id,
        amount,
        try_cast(transaction_date as timestamp) as sale_date
    from source
    where amount is not null and amount > 0
)

select * from cleaned