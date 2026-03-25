''' Ecommerce Analytics Dashboard '''
import calendar
import streamlit as st
import pandas as pd
import visualization as vis
import visualization as vis

st.set_page_config(page_title="Analytics Dashboard", layout='wide')

@st.cache_data
def load_data(path):
    ''' Load the sales data from a csv file. '''
    order_item_refunds = pd.read_csv(path + 'order_item_refunds.csv') #pylint: disable=redefined-outer-name
    order_items = pd.read_csv(path + 'order_items.csv') #pylint: disable=redefined-outer-name
    orders = pd.read_csv(path + 'orders.csv') #pylint: disable=redefined-outer-name
    products = pd.read_csv(path + 'products.csv') #pylint: disable=redefined-outer-name
    website_pageviews = pd.read_csv(path + 'website_pageviews.csv') #pylint: disable=redefined-outer-name
    website_sessions = pd.read_csv(path + 'website_sessions.csv') #pylint: disable=redefined-outer-name

    return order_item_refunds, order_items, orders, products, website_pageviews, website_sessions

(
    order_item_refunds,
    order_items,
    orders,
    products,
    website_pageviews,
    website_sessions
 ) = load_data('./data/')


# st.dataframe(order_item_refunds)

# Setting Title
st.title("Dashboard")


# Module Wise Analysis

tab = st.tabs([
    "Marketing Channel & Efficiency",
    "Conversion Funnel & UX Optimization",
    "Product Performance & Refund Analysis",
    "Customer Lifecycle & Repeat Behaviour"
])

with tab[0]:
    st.header('Marketing Channel & Effiiency')



with tab[1]:
    st.header('Conversion Funnel & UX Optimization')



with tab[2]:
    st.header('Product Performance & Refund Analysis')
    a,b,c,d=st.columns(4)
    #KPI TOTAL NET REVENUE
    merged = pd.merge(order_items,order_item_refunds,on='order_item_id',how='left')
    sales_per_product = order_items.groupby('product_id')['price_usd'].sum().reset_index()
    sales_per_product.columns = ['product_id', 'sales_revenue']
    refund_per_product = merged.groupby('product_id')['refund_amount_usd'].sum().reset_index()
    prod_info=pd.merge(sales_per_product,refund_per_product,on='product_id')
    
    prod_info['net_revenue'] = prod_info['sales_revenue'] - prod_info['refund_amount_usd']
    total_revenue = prod_info['net_revenue'].sum()
    a.metric( label="Total Net Revenue",value=f'{total_revenue:,.2f}')

    refund_amt=order_item_refunds["refund_amount_usd"].sum()
    b.metric( label="Refund Amount",value=f'{refund_amt:,.2f}')

    average_order_value = orders["price_usd"].mean()
    c.metric( label="Average Order Value",value=f'{average_order_value:,.2f}')

    total_orders=order_items.order_item_id.nunique()
    d.metric( label="Total Orders",value=f'{total_orders:,.2f}')
    
    refund_table=pd.read_csv('data/order_item_refunds.csv')
    orders['created_at'] = pd.to_datetime(orders['created_at'], errors='coerce')
    orders['month'] = orders['created_at'].dt.to_period('M').astype(str)
    refund_table['created_at'] = pd.to_datetime(refund_table['created_at'], errors='coerce')
    refund_table['month'] = refund_table['created_at'].dt.to_period('M').astype(str)
    revenue_trend = orders.groupby('month')['price_usd'].sum().reset_index(name='revenue')

    orders_trend = orders.groupby('month').size().reset_index(name='orders_count')

    refund_trend = refund_table.groupby('month')['refund_amount_usd'].sum().reset_index(name='refund_amount')

    trend = revenue_trend.merge(orders_trend, on='month', how='left').merge(refund_trend, on='month', how='left').fillna(0)

        
    #REFUND AMOUNT PER PRODUCT
    merged = pd.merge(order_items,order_item_refunds,on='order_item_id',how='left')
    sales_per_product = order_items.groupby('product_id')['price_usd'].sum().reset_index()
    sales_per_product.columns = ['product_id', 'sales_revenue']
    refund_per_product = merged.groupby('product_id')['refund_amount_usd'].sum().reset_index()
    products_refund=pd.merge(sales_per_product,refund_per_product,on='product_id')

    tab2_columns = st.columns([0.7, 0.3], gap='large')
    with tab2_columns[0]:
        st.plotly_chart(vis.plot_trend(trend))
    with tab2_columns[1]:
        st.plotly_chart(vis.plot_refund_distribution(products_refund))
    
with tab[3]:
    st.subheader('Customer Lifecycle & Repeat Behaviour')

    a,b,c,d=st.columns(4)
    #KPI NEW USERS
    user_orders = orders.groupby("user_id")["order_id"].count().reset_index()
    user_orders.columns = ["user_id", "total_orders"]
    user_orders["user_type"] = "New_User"
    user_orders.loc[user_orders["total_orders"] > 1, "user_type"] = "Repeat_User"
    new_Cust_counts = user_orders["user_type"].value_counts()
    new_users = new_Cust_counts["New_User"]
    a.metric( label="New Users",value=f"{new_users:,}" )
    #KPI AVERAGE ORDER REPEAT CYCLE
    Order_gap = orders.sort_values(['user_id','created_at'])
    Order_gap['created_at'] = pd.to_datetime(Order_gap['created_at'])
    Order_gap['days_gap'] = Order_gap.groupby('user_id')['created_at'].diff().dt.days
    mean_order_gap = Order_gap['days_gap'].mean()
    b.metric(label="Average Order Gap (Days)", value=f"{mean_order_gap:.2f}")
    #KPI 
    order_counts = orders.groupby('user_id')['order_id'].count()
    repeat_customers = order_counts[order_counts > 1].index
    repeat_orders = orders[orders['user_id'].isin(repeat_customers)]
    repeat_aov = repeat_orders['price_usd'].sum() / repeat_orders['order_id'].count()
    c.metric(label="Repeat Customer AOV", value=f"{repeat_aov:.2f}")
    #KPI
    user_counts =user_orders["user_type"].value_counts()
    repeat_percentage = (user_counts['Repeat_User'] / user_counts.sum()) * 100
    d.metric(label="Repeat Customer %", value=f"{repeat_percentage:.2f}%")

    #distribution of time to second purchase histogram
    orders_per_customer = orders.groupby('user_id')['order_id'].count()
    repeat_customers = orders_per_customer[orders_per_customer > 1].count()
    total_customers = orders['user_id'].nunique()
    new_customers_count= total_customers-repeat_customers
    repeat_purchase_rate = (repeat_customers / total_customers) * 100
    orders['created_at'] = pd.to_datetime(orders['created_at'])
    orders_sorted = orders.sort_values(['user_id','created_at'])
    orders['order_number'] = orders.groupby('user_id').cumcount() + 1
    first_orders = orders[orders['order_number'] == 1]
    second_orders = orders[orders['order_number'] == 2]
    repurchase_data = pd.merge(first_orders, second_orders, on='user_id')
    repurchase_data['created_at_x'] = pd.to_datetime(repurchase_data['created_at_x'])
    repurchase_data['created_at_y'] = pd.to_datetime(repurchase_data['created_at_y'])
    repurchase_data['days_between'] = (
        repurchase_data['created_at_y'] - repurchase_data['created_at_x']
    ).dt.days
    average_days = repurchase_data['days_between'].mean()

    #Repeat customer AOV
    order_counts = orders.groupby('user_id')['order_id'].count()
    repeat_customers = order_counts[order_counts > 1].index
    repeat_orders = orders[orders['user_id'].isin(repeat_customers)]
    repeat_aov = repeat_orders['price_usd'].sum() / repeat_orders['order_id'].count()
    orders_with_type = orders.merge(
        user_orders[['user_id', 'user_type']],
        on='user_id',
        how='left'
    )


    tab3_columns = st.columns([0.6,0.4],gap='large')
    with tab3_columns[0]:
        st.plotly_chart(vis.dist_time(repurchase_data))
        st.plotly_chart(vis.order_val_dist(orders_with_type))




    
   
    

            
    

        