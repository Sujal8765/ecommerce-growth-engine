import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 1. Traffic vs Orders
def traffic_vs_orders(monthly_summary):
    fig = px.line(
        monthly_summary,
        x="month",
        y=["sessions", "orders"],
        title="Traffic vs Orders Over Time"
    )
    fig.update_layout(height=180, margin=dict(t=40, b=10))
    return fig


def dist_time(data):
    fig = px.histogram(
    data,
    x="days_between",
    nbins=40,
    title="Distribution of Time to Second Purchase"
    )

    return fig

def order_val_dist(data):
    fig = px.violin(
    data,
    x="user_type",
    y="price_usd",
    box=False,         
    # points="all",     
    title="Order Value Distribution: New vs Repeat Customers"
    )

    fig.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Order Value (USD)",
        # title_x=0.5
    )
    return fig

def plot_trend(trend):
        fig = px.line(
        trend,
        x='month',
        y=['revenue', 'orders_count', 'refund_amount'],
        title='Revenue, Orders, and Refund Trends Over Time',
        markers=True
    )

        return fig

def plot_refund_distribution(prod_info):
    fig = px.pie(prod_info,
                 names='product_id',
                 values='refund_amount_usd',
                 title='Refund Distribution by Product')
    return fig
