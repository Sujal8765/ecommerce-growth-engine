''' Graph Module '''
import plotly.graph_objects as go
import plotly.express as px

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

