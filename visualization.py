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
def plot_repeat_purchase_rate(result):
    fig = px.bar(
        result,
        x='product_name',
        y='repeat_purchase_rate_%',
        title="Actual Repeat Purchase Rate per Product",
        labels={
            'product_name': 'Product Name',
            'repeat_purchase_rate_%': 'Repeat Purchase Rate (%)'
        }
    )

    fig.update_layout(
        xaxis_tickangle=40,
        template='plotly_white'
    )

    return fig


def create_user_pie_chart(user_counts):
    # user_counts should be a Series: index = labels, values = counts
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
        title="New vs Repeat Users"
    )

    return fig

import plotly.express as px

def plot_total_units_sold(product_sales):
    fig = px.bar(
        product_sales,
        x=product_sales["product_id"].astype(str),
        y="total_units_sold",
        title="Total Units Sold per Product",
        labels={
            "x": "Product ID",
            "total_units_sold": "Total Units Sold"
        }
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
def plot_order_gap_distribution(Order_gap):
    fig = px.histogram(
        Order_gap,
        x=Order_gap,
        nbins=20,
        title="Distribution of Days Between First and Second Order"
    )

    return fig

def plot_order_value_distribution(orders_with_type):
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
    fig = px.pie(
        values=user_counts.values,
        names=user_counts.index,
        title="New vs Repeat Users"
    )

    return fig
def plot_repeat_purchase_rate(result):
    fig = px.bar(
        result,
        x="product_name",
        y="repeat_purchase_rate_%",
        title="Actual Repeat Purchase Rate per Product"
    )

    fig.update_layout(
        xaxis_title="Product Name",
        yaxis_title="Repeat Purchase Rate (%)"
    )

    return fig
def plot_refund_heatmap(heat):
    fig = px.imshow(
        heat,
        text_auto=True,
        color_continuous_scale='Blues',
        title='Refund % per Product per Month'
    )

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Product'
    )

    return fig