''' Ecommerce Analytics Dashboard '''
import calendar
import streamlit as st
import pandas as pd
import visualization

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


st.dataframe(order_item_refunds)

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
    st.header('Customer Lifecycle & Repeat Behaviour')


