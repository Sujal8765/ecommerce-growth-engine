''' Graph Module '''
import plotly.graph_objects as go
import plotly.express as px


def plot_refund_distribution(prod_info):
    fig = px.pie(prod_info,
                 names='product_id',
                 values='refund_amount_usd',
                 title='Refund Distribution by Product')
    return fig
