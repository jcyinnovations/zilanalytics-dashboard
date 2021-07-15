import numpy as np

# Monthly transactions by type
sql_monthly_tx_by_type = """
select block_month, ztype as transaction_type, count(id) as quantity from transactions 
    where success=true 
    group by block_month,ztype 
    order by block_month;
"""

# Monthly block capacity
sql_monthly_block_count="""
SELECT block_month, count(distinct block_number) as quantity FROM transactions 
    GROUP BY block_month 
    ORDER BY block_month;
"""

# All Unique Deployed DApps
sql_dapps_list = "select distinct code from transactions where success=true and ztype=2"

# Unique deployed DApps by month
sql_singleton_contracts = """
select block_month, code, 1 as quantity from transactions 
    where code in (SELECT (contracts.contract)::text FROM contracts GROUP BY contracts.contract HAVING count(contract) = 1) 
    order by block_month;
"""

sql_singleton_contracts = """
select distinct code, block_month, 1 as quantity from transactions 
    where ztype=2 
    order by block_month;
"""


# Monthly Transactions by top DApps
sql_monthly_call_by_dapp = """
select t.block_month, c.contract, count(t.id) as quantity
    from transactions as t join contracts as c on t.to_addr = c.addr
    where success=true and ztype=1 
    group by t.block_month,c.contract 
    order by t.block_month asc, quantity desc
"""

sql_top_dapp_monthly_transactions = """
    SELECT rank_filter.* FROM (
        SELECT transactions.block_month, contracts.contract as contract_name, count(transactions.id) as quantity,
        rank() OVER (
            PARTITION BY transactions.block_month
            ORDER BY count(transactions.id) DESC
        )
        FROM transactions left join contracts on transactions.to_addr = contracts.addr
        WHERE transactions.success = true and ztype = 1
        group by transactions.block_month, contracts.contract
        order by transactions.block_month
    ) rank_filter WHERE RANK < 5
"""


dashboard_queries = [
    {"name": "Monthly Transactions by Type", 
        "query": sql_monthly_tx_by_type, 
        "x": "block_month", 
        "y": "quantity", 
        "color": "transaction_type", 
        "chart": "Bar", 
        "dtype": {'block_month': str, 'transaction_type': str, 'quantity': np.int32}},

    {"name": "Blockchain Block Capacity Growth", 
        "query": sql_monthly_block_count, 
        "x": "block_month", 
        "y": "quantity", 
        "color": None, 
        "chart": "Bar",
        "dtype": {'block_month': str, 'quantity': np.int32}},
    {"name": "Unique Contracts Deployed Monthly", 
        "query": sql_singleton_contracts, 
        "x": "block_month", 
        "y": "quantity", 
        "color": None,
        "text": "code", 
        "chart": "Bar",
        "dtype": {'block_month': str, 'code': str, 'quantity': np.int32}},
    {"name": "Top DApps by Transaction Volume Monthly", 
        "query": sql_top_dapp_monthly_transactions, 
        "x": "block_month", 
        "y": "quantity", 
        "color": "contract_name", 
        "chart": "Bar", 
        "dtype": {'block_month': str, 'contract_name': str, 'quantity': np.int32, 'rank': np.int32}}
]
