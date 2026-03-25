''' Ecommerce Analytics Dashboard '''
import calendar
import streamlit as st
import pandas as pd
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


    
    
