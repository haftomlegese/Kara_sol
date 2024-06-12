with raw_data as (
    select * from public.telegram_data  -- Adjust the table name as necessary
),

cleaned_data as (
    select
        message_id,
        date,
        sender_id,
        message,
        media_path,
        case
            when media_path is not null then 'Contains Media'
            else 'No Media'
        end as media_status
    from raw_data
    where message is not null
)

select * from cleaned_data