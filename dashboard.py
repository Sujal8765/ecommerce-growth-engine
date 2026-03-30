''' Ecommerce Analytics Dashboard '''
import calendar
import streamlit as st
import pandas as pd
import visualization as vis

st.set_page_config(page_title="Analytics Dashboard", layout='wide')
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

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

    # =========================
    # KPI SECTION 
    # =========================

    total_sessions = website_sessions['website_session_id'].nunique()

    total_orders = orders['order_id'].nunique()

    conversion_rate = total_orders / total_sessions

    # Bounce Rate (sessions with only 1 pageview)
    page_counts = website_pageviews.groupby('website_session_id').size()
    bounce_sessions = page_counts[page_counts == 1].count()
    bounce_rate = bounce_sessions / total_sessions

    # Avg Revenue per Session
    total_revenue = orders['price_usd'].sum()
    avg_rev_per_session = total_revenue / total_sessions


    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sessions", f"{total_sessions:,}")
    col2.metric("Bounce Rate", f"{bounce_rate:.2%}")
    col3.metric("Conversion Rate", f"{conversion_rate:.2%}")
    col4.metric("Avg Revenue/Session", f"${avg_rev_per_session:.2f}")
   
    # =========================
    # 🔥 DATA PREPARATION FIRST
    # =========================

    # Monthly summary
    website_sessions["created_at"] = pd.to_datetime(website_sessions["created_at"])
    orders["created_at"] = pd.to_datetime(orders["created_at"])

    website_sessions["month"] = website_sessions["created_at"].dt.to_period("M").astype(str)
    orders["month"] = orders["created_at"].dt.to_period("M").astype(str)

    monthly_sessions = website_sessions.groupby("month").size().reset_index(name="sessions")
    monthly_orders = orders.groupby("month").size().reset_index(name="orders")

    monthly_summary = monthly_sessions.merge(monthly_orders, on="month", how="left").fillna(0)

    # Channel summary
    session_level = website_sessions.merge(orders, on="website_session_id", how="left")

    channel_summary = session_level.groupby("utm_source").agg(
        sessions=("website_session_id", "count"),
        orders=("order_id", "count"),
        revenue=("price_usd", "sum")
    ).reset_index()

    channel_summary["conversion_rate"] = channel_summary["orders"] / channel_summary["sessions"]

    # Campaign summary
    campaign_summary = session_level.groupby(["utm_campaign", "utm_source"]).agg(
        sessions=("website_session_id", "count"),
        orders=("order_id", "count")
    ).reset_index()

    # =========================
    # 🎯 NOW CREATE LAYOUT
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            vis.traffic_vs_orders(monthly_summary),
            use_container_width=True
            
        )
    with col2:
        st.plotly_chart(
            vis.traffic_vs_conversion(channel_summary),
            use_container_width=True
            
        )

    col3, col4 = st.columns(2)

    with col3:
        pie_option = st.radio("Distribution:", ["Revenue", "Traffic"], horizontal=True)

        if pie_option == "Revenue":
            fig = vis.pie_chart(channel_summary, "revenue", "Revenue")
        else:
            fig = vis.pie_chart(channel_summary, "sessions", "Traffic")

        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.plotly_chart(
            vis.traffic_performance(campaign_summary),
            use_container_width=True
            
    )



with tab[1]:
    st.header('Conversion Funnel & UX Optimization')

    # =========================
    # KPI SECTION 🔥
    # =========================
    total_pageviews = website_pageviews.shape[0]

    total_sessions = website_sessions['website_session_id'].nunique()
    total_orders = orders['order_id'].nunique()

    conversion_rate = total_orders / total_sessions
    dropoff_rate = 1 - conversion_rate
    retention_rate = conversion_rate

    mobile_sessions = website_sessions[
        website_sessions['device_type'] == 'mobile'
    ]['website_session_id'].nunique()

    desktop_sessions = website_sessions[
        website_sessions['device_type'] == 'desktop'
    ]['website_session_id'].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Page Views", f"{total_pageviews:,}")
    col2.metric("Drop-off Rate", f"{dropoff_rate:.2%}")
    col3.metric("Retention Rate", f"{retention_rate:.2%}")
    col4.metric("Mobile Sessions", f"{mobile_sessions:,}")
    col5.metric("Desktop Sessions", f"{desktop_sessions:,}")

    # =========================
    # FUNNEL DATA (FIXED 🔥)
    # =========================
    pages = [
        '/home',
        '/products',
        '/cart',
        '/shipping',
        '/billing',
        '/thank-you-for-your-order'
    ]

    stage_names = [
        "Home",
        "Product Page",
        "Cart",
        "Shipping",
        "Billing",
        "Order Complete"
    ]

    counts = []

    for page in pages:
        if page == '/billing':   # 🔥 FIX FOR BILLING
            count = website_pageviews[
                website_pageviews['pageview_url'].isin(['/billing', '/billing-2'])
            ]['website_session_id'].nunique()
        else:
            count = website_pageviews[
                website_pageviews['pageview_url'] == page
            ]['website_session_id'].nunique()

        counts.append(count)

    funnel_df = pd.DataFrame({
        "Stage": stage_names,
        "Sessions": counts
    })

    # =========================
    # DROP-OFF
    # =========================
    funnel_df["Previous_Stage"] = funnel_df["Sessions"].shift(1)
    funnel_df["Drop_Off"] = funnel_df["Previous_Stage"] - funnel_df["Sessions"]
    funnel_df["Drop_Off_Rate"] = funnel_df["Drop_Off"] / funnel_df["Previous_Stage"]

    # =========================
    # 2 COLUMN GRAPH LAYOUT 🔥
    # =========================
    st.markdown("###")

    col1, col2 = st.columns([1.2, 1])   # Funnel slightly bigger

    with col1:
        st.plotly_chart(
            vis.plot_funnel(funnel_df),
            use_container_width=True
        )

    with col2:
        landing, product, cart, shipping, billing, order_complete = counts

        labels = [
            "Landing","Product","Cart","Shipping","Billing","Order Complete",
            "Drop After Landing","Drop After Product","Drop After Cart",
            "Drop After Shipping","Drop After Billing"
        ]

        source = [0,1,2,3,4, 0,1,2,3,4]
        target = [1,2,3,4,5, 6,7,8,9,10]

        values = [
            min(landing, product),
            cart,
            shipping,
            billing,
            order_complete,
            landing - min(landing, product),
            product - cart,
            cart - shipping,
            shipping - billing,
            billing - order_complete
        ]

        fig = vis.plot_sankey(labels, source, target, values)

        fig.update_layout(height=400)  # match funnel height

        st.plotly_chart(fig, use_container_width=True)


    


with tab[2]:
    st.header('Product Performance & Refund Analysis')
    a,b,c,d=st.columns(4)
    #KPI 
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
   
    #TOTAL UNITS SOLD
    product_sales =order_items.groupby("product_id").size().reset_index(name="total_units_sold").sort_values("total_units_sold", ascending=False)
    
    
    #HEATMAP
    df = order_items[['order_item_id', 'order_id', 'product_id']]

    df = df.merge(
    orders[['order_id', 'created_at']],
    on='order_id',
    how='left'
    )
    df = df.merge(
    products[['product_id', 'product_name']],
    on='product_id',
    how='left'
    )
    refunds = order_item_refunds[['order_item_id', 'created_at']]

    refunds = refunds.merge(
    order_items[['order_item_id', 'product_id']],
    on='order_item_id',
    how='left'
    )

    refunds = refunds.merge(
    products[['product_id', 'product_name']],
    on='product_id',
    how='left'
    )
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['month'] = df['created_at'].dt.to_period('M').astype(str)
    refunds['created_at'] = pd.to_datetime(df['created_at'])
    refunds['month'] = refunds['created_at'].dt.to_period('M').astype(str)
    total_pm = df.groupby(['product_name', 'month']).size().reset_index(name='total_orders')
    refund_pm = refunds.groupby(['product_name', 'month']).size().reset_index(name='refund_orders')
    rate = total_pm.merge(refund_pm, on=['product_name', 'month'], how='left')
    rate['refund_orders'] = rate['refund_orders'].fillna(0) 
    rate['refund_pct'] = (rate['refund_orders'] / rate['total_orders']) * 100
    rate['refund_pct'] = rate['refund_pct'].round(1)    
    heat = rate.pivot(index='product_name',columns='month',values='refund_pct').fillna(0)
    # TREND
    orders['created_at'] = pd.to_datetime(orders['created_at'], errors='coerce')
    order_item_refunds['created_at'] = pd.to_datetime(order_item_refunds['created_at'], errors='coerce')
    order_item_refunds['month'] = order_item_refunds['created_at'].dt.to_period('M').astype(str)
    revenue_trend = orders.groupby('month')['price_usd'].sum().reset_index(name='revenue')

    orders_trend = orders.groupby('month').size().reset_index(name='orders_count')

    refund_trend = order_item_refunds.groupby('month')['refund_amount_usd'].sum().reset_index(name='refund_amount')

    trend = revenue_trend.merge(orders_trend, on='month', how='left').merge(refund_trend, on='month', how='left').fillna(0)
    tab2_columns = st.columns([0.7, 0.3], gap='large')
    
    with tab2_columns[0]:
        st.plotly_chart(vis.plot_trend(trend))
        
    with tab2_columns[1]:
        st.plotly_chart(vis.plot_total_units_sold(product_sales))
    
    
    #HEATMAP
    df = order_items[['order_item_id', 'order_id', 'product_id']]

    df = df.merge(
    orders[['order_id', 'created_at']],
    on='order_id',
    how='left'
    )
    df = df.merge(
    products[['product_id', 'product_name']],
    on='product_id',
    how='left'
    )
    refunds = order_item_refunds[['order_item_id', 'created_at']]

    refunds = refunds.merge(
    order_items[['order_item_id', 'product_id']],
    on='order_item_id',
    how='left'
    )

    refunds = refunds.merge(
    products[['product_id', 'product_name']],
    on='product_id',
    how='left'
    )
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['month'] = df['created_at'].dt.to_period('M').astype(str)
    refunds['created_at'] = pd.to_datetime(df['created_at'])
    refunds['month'] = refunds['created_at'].dt.to_period('M').astype(str)
    total_pm = df.groupby(['product_name', 'month']).size().reset_index(name='total_orders')
    refund_pm = refunds.groupby(['product_name', 'month']).size().reset_index(name='refund_orders')
    rate = total_pm.merge(refund_pm, on=['product_name', 'month'], how='left')
    rate['refund_orders'] = rate['refund_orders'].fillna(0) 
    rate['refund_pct'] = (rate['refund_orders'] / rate['total_orders']) * 100
    rate['refund_pct'] = rate['refund_pct'].round(1)    
    heat = rate.pivot(index='product_name',columns='month',values='refund_pct').fillna(0)

    
        
    #REFUND AMOUNT PER PRODUCT
    merged = pd.merge(order_items,order_item_refunds,on='order_item_id',how='left')
    sales_per_product = order_items.groupby('product_id')['price_usd'].sum().reset_index()
    sales_per_product.columns = ['product_id', 'sales_revenue']
    refund_per_product = merged.groupby('product_id')['refund_amount_usd'].sum().reset_index()
    products_refund=pd.merge(sales_per_product,refund_per_product,on='product_id')

    tab2_columns = st.columns([0.7, 0.3], gap='large')
    with tab2_columns[0]:
        st.plotly_chart(vis.plot_refund_heatmap(heat))
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

    # Data prep
    df = order_items.merge(
        orders[["order_id", "user_id"]], on="order_id", how="left"
    ).merge(
        products[["product_id", "product_name"]], on="product_id", how="left"
    )
    user_product = df.groupby(["product_name", "user_id"]).size().reset_index(name="times_bought")
    total_customers = user_product.groupby("product_name")["user_id"].nunique().reset_index(name="total_customers")
    repeat_df = user_product[user_product["times_bought"] > 1]
    repeat_customers = repeat_df.groupby("product_name")["user_id"].nunique().reset_index()
    repeat_customers.columns = ["product_name", "repeat_customers"]
    result = total_customers.merge(repeat_customers, on="product_name", how="left").fillna(0)
    result["repeat_purchase_rate_%"] = (result["repeat_customers"] / result["total_customers"]) * 100

    user_orders = orders.groupby("user_id")["order_id"].count().reset_index()
    user_orders.columns = ["user_id", "total_orders"]
    user_orders["user_type"] = "New User"
    user_orders.loc[user_orders["total_orders"] > 1, "user_type"] = "Repeat User"
    user_counts = user_orders["user_type"].value_counts()

    tab3_columns = st.columns([0.6,0.4],gap='large')
    with tab3_columns[0]:
        st.plotly_chart(vis.dist_time(repurchase_data))
        st.plotly_chart(vis.order_val_dist(orders_with_type))

    # Layout: only inside columns, no standalone charts above
    with tab3_columns[1]:
        st.plotly_chart(vis.plot_repeat_purchase_rate(result), use_container_width=True, key="repeat_purchase_rate")
        st.plotly_chart(vis.create_user_pie_chart(user_counts), use_container_width=True, key="user_pie_chart")
