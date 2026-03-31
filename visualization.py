""" 
Visulization Functions Declaration for entire dashboard.
"""
import plotly.express as px
import plotly.graph_objects as go

def traffic_vs_orders(monthly_summary):
    ''' Traffic vs Orders Over Time '''
    fig = px.line(
        monthly_summary,
        x="month",
        y=["sessions", "orders"],
        title="Traffic vs Orders Over Time"
    )

    fig.update_layout(
        height=300,
        # margin=dict(t=40, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=dict(
                text="Traffic Activity",
                side="left"
            ),
        )
    )

    return fig

def traffic_vs_conversion(channel_summary):
    ''' Traffic vs Conversion Rate '''
    fig = px.scatter(
        channel_summary,
        x="sessions",
        y="conversion_rate",
        size="revenue",
        color="utm_source",
        title="Traffic vs Conversion Rate"
    )

    fig.update_yaxes(tickformat=".0%")

    fig.update_layout(
        height=300,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=dict(
                text="Channel Source",
                side="left"
            ),
        )
    )

    return fig

def pie_chart(channel_summary, value, title):
    ''' Revenue / Traffic Pie Chart '''
    fig = px.pie(
        channel_summary,
        names="utm_source",
        values=value,
        hole=0.4,
        title=title
    )

    fig.update_layout(
        height=300,
        # margin=dict(t=40, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="left",
            x=0.5,
            title=dict(
                text="Channel Source",
                side="left"
            ),
        )
    )

    return fig

def traffic_performance(campaign_summary):
    ''' Campaign Performance by Traffic '''
    fig = px.bar(
        campaign_summary,
        y="utm_campaign",
        x="sessions",
        color="utm_source",
        orientation="h",
        title="Campaign Performance by Traffic"
    )

    fig.update_layout(
        height=300,
        # margin=dict(t=40, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=dict(
                text="Channel Source",
                side="left"
            ),
        )
    )

    return fig

def plot_funnel(funnel_df):
    ''' Ecommerce Conversion Funnel '''
    fig = px.funnel(
        funnel_df,
        x="Sessions",
        y="Stage",
        title="Ecommerce Conversion Funnel"
    )

    fig.update_traces(
        textposition="inside",
        marker=dict(color="#52C7C7")
    )

    fig.update_layout(
        height=500
        )

    return fig

def plot_sankey(data):
    ''' Customer Journey Diagram '''
    landing, product, cart, shipping, billing, order_complete = data

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

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            label=labels
        ),
        link=dict(
            source=source,
            target=target,
            value=values
        )
    )])

    fig.update_layout(
        title_text="Customer Journey Diagram",
        font_size=12,
        height=500
    )

    return fig

def dist_time(data):
    ''' Distribution of Time to Second Purchase '''
    fig = px.histogram(
    data,
    x="days_between",
    nbins=40,
    title="Distribution of Time to Second Purchase"
    )

    fig.update_layout(
        height = 250
    )

    return fig

def order_val_dist(data):
    ''' Order Value Distribution: New vs Repeat Customers '''
    fig = px.violin(
    data,
    x="user_type",
    y="price_usd",
    box=False,
    title="Order Value Distribution: New vs Repeat Customers"
    )

    fig.update_layout(
        height=350,
        xaxis_title="Customer Type",
        yaxis_title="Order Value (USD)",
    )

    return fig

def plot_trend(trend):
    ''' Revenue, Orders, and Refund Trends Over Time '''
    fig = px.line(
        trend,
        x='month',
        y=['revenue', 'orders_count', 'refund_amount'],
        title='Revenue, Orders, and Refund Trends Over Time',
        markers=True
    )

    fig.update_layout(
        height=300,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=dict(
                text="Performance Metric",
                side="left"
            ),
        )
    )

    return fig

def plot_refund_distribution(prod_info):
    ''' Refund Distribution by Product '''
    fig = px.pie(prod_info,
                 names='product_name',
                 values='refund_amount_usd',
                 title='Refund Distribution by Product')

    fig.update_layout(
        height=300,
        # margin=dict(t=40, b=10),
    )

    return fig

def plot_repeat_purchase_rate(result):
    ''' Actual Repeat Purchase Rate per Product '''
    fig = px.bar(
        result,
        y='product_name',
        x='repeat_purchase_rate_%',
        title="Actual Repeat Purchase Rate per Product",
        labels={
            'product_name': 'Product Name',
            'repeat_purchase_rate_%': 'Repeat Purchase Rate (%)'
        }
    )

    fig.update_layout(
        xaxis_tickangle=40,
        template='plotly_white',
        height = 300
    )

    return fig

def create_user_pie_chart(user_counts):
    ''' New vs Repeat Users '''
    fig = go.Figure(
        data=[
            go.Pie(
                labels=user_counts.index,
                values=user_counts.values,
                textinfo='percent+label'
            )
        ]
    )

    fig.update_layout(
        height = 300,
        title="New vs Repeat Users"
    )

    return fig

def plot_total_units_sold(product_sales):
    ''' Total Units Sold per Product '''
    fig = px.bar(
        product_sales,
        y=product_sales["product_name"].astype(str),
        x="total_units_sold",
        title="Total Units Sold per Product",
        labels={
            "x": "Product",
            "total_units_sold": "Total Units Sold"
        }
    )

    fig.update_layout(
        height=300,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=dict(
                text="Channel Source",
                side="left"
            ),
        )
    )

    return fig


def plot_order_gap_distribution(order_gap):
    ''' Distribution of Days Between First and Second Order '''
    fig = px.histogram(
        order_gap,
        x=order_gap,
        nbins=20,
        title="Distribution of Days Between First and Second Order"
    )

    return fig

def plot_order_value_distribution(orders_with_type):
    ''' Order Value Distribution: New vs Repeat Customers '''
    fig = px.violin(
        orders_with_type,
        x="user_type",
        y="price_usd",
        box=True,
        points=False,
        title="Order Value Distribution: New vs Repeat Customers"
    )

    fig.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Order Value (USD)"
    )

    return fig

def plot_user_distribution(user_counts):
    ''' New vs Repeat Users '''
    fig = px.pie(
        values=user_counts.values,
        names=user_counts.index,
        title="New vs Repeat Users"
    )

    return fig

def plot_refund_heatmap(heat):
    ''' Refund Percentage per Product per Month '''
    fig = px.imshow(
        heat,
        text_auto=True,
        color_continuous_scale='Blues',
        title='Refund % per Product per Month'
    )

    fig.update_layout(
        height=300,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=dict(
                text="Performance Metric",
                side="left"
            ),
        ),
        xaxis_title='Month',
        yaxis_title='Product'
    )

    return fig
