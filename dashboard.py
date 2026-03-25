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
   
    
    
    #REFUND AMOUNT PER PRODUCT
    merged = pd.merge(order_items,order_item_refunds,on='order_item_id',how='left')
    sales_per_product = order_items.groupby('product_id')['price_usd'].sum().reset_index()
    sales_per_product.columns = ['product_id', 'sales_revenue']
    refund_per_product = merged.groupby('product_id')['refund_amount_usd'].sum().reset_index()
    products_refund=pd.merge(sales_per_product,refund_per_product,on='product_id')


    tab2_columns = st.columns([0.7, 0.3], gap='large')
    
with tab2_columns[0]:
        
 with tab2_columns[1]:
    st.plotly_chart(vis.plot_refund_distribution(products_refund))
       
 with tab[3]:
    st.header('Customer Lifecycle & Repeat Behaviour')
    