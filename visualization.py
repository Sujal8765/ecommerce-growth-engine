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

# 2. Bubble Chart
def traffic_vs_conversion(channel_summary):
    fig = px.scatter(
        channel_summary,
        x="sessions",
        y="conversion_rate",
        size="revenue",
        color="utm_source",
        title="Traffic vs Conversion Rate"
    )
    fig.update_yaxes(tickformat=".0%")
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
