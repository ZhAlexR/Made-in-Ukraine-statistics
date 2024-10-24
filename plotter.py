import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd

class Plotter:

    @staticmethod
    @st.cache_data
    def prepare_heatmap_data(filtered_products):
        top_40_brands = filtered_products['Бренд'].value_counts().nlargest(40).index
        filtered_top_40_brands = filtered_products[filtered_products['Бренд'].isin(top_40_brands)]
        heatmap_data = filtered_top_40_brands.pivot_table(
            index=filtered_top_40_brands.index.date,
            columns='Бренд',
            aggfunc='size',
            fill_value=0
        )
        heatmap_data.index.name = 'Оновлено'
        heatmap_data_melted = heatmap_data.reset_index().melt(
            id_vars='Оновлено', var_name='Бренд', value_name='Кількість товарів'
        )
        return heatmap_data_melted

    def plot_interactive_heatmap(self, products_df, start_date, end_date):
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        filtered_products = products_df.loc[start_date:end_date]
        heatmap_data_melted = self.prepare_heatmap_data(filtered_products)

        fig = px.density_heatmap(
            heatmap_data_melted, x='Бренд', y='Оновлено', z='Кількість товарів',
            color_continuous_scale='YlGnBu',
            labels={'Оновлено': 'Дата', 'Бренд': 'Бренд', 'Кількість товарів': 'Кількість товарів'}
        )

        fig.update_layout(
            title="Активність брендів за кількістю доданого товару",
            xaxis_tickangle=-90, xaxis_title="Бренд", yaxis_title="Дата"
        )

        st.plotly_chart(fig)

    def plot_manufacturers_combined(self, products_df, start_date, end_date):
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        filtered_products = products_df.loc[start_date:end_date]
        manufacturers_by_date = filtered_products.groupby(filtered_products.index.date)['Юридична назва'].nunique()
        manufacturers_cumulative = manufacturers_by_date.cumsum()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=manufacturers_by_date.index,
            y=manufacturers_by_date.values,
            name='Кількість виробників',
            marker_color='skyblue',
            yaxis='y1'
        ))

        fig.add_trace(go.Scatter(
            x=manufacturers_cumulative.index,
            y=manufacturers_cumulative.values,
            mode='lines+markers',
            name='Кумулятивна кількість',
            line=dict(color='blue', dash='dash'),
            yaxis='y2'
        ))

        fig.update_layout(
            title='Динаміка кількості та кумулятивна зміна виробників',
            xaxis_title='Дата',
            yaxis=dict(title='Кількість виробників', side='left', showgrid=False),
            yaxis2=dict(title='Кумулятивна кількість', side='right', overlaying='y', showgrid=False),
            legend=dict(x=0.01, y=0.99, borderwidth=1)
        )
        st.plotly_chart(fig)

    def plot_brands_combined(self, products_df, start_date, end_date):
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        filtered_products = products_df.loc[start_date:end_date]
        brands_by_date = filtered_products.groupby(filtered_products.index.date)['Бренд'].nunique()
        brands_cumulative = brands_by_date.cumsum()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=brands_by_date.index,
            y=brands_by_date.values,
            name='Кількість доданих брендів',
            marker_color='green',
            yaxis='y1'
        ))

        fig.add_trace(go.Scatter(
            x=brands_cumulative.index,
            y=brands_cumulative.values,
            mode='lines+markers',
            name='Кумулятивна кількість',
            line=dict(color='darkgreen', dash='dash'),
            yaxis='y2'
        ))

        fig.update_layout(
            title='Динаміка кількості та кумулятивна зміна брендів',
            xaxis_title='Дата',
            yaxis=dict(title='Кількість брендів', side='left', showgrid=False),
            yaxis2=dict(title='Кумулятивна кількість', side='right', overlaying='y', showgrid=False),
            legend=dict(x=0.01, y=0.99, borderwidth=1)
        )
        st.plotly_chart(fig)

    def plot_products_combined(self, products_df, start_date, end_date):
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        filtered_products = products_df.loc[start_date:end_date]
        products_by_date = filtered_products.groupby(filtered_products.index.date).size()
        products_cumulative = products_by_date.cumsum()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=products_by_date.index,
            y=products_by_date.values,
            name='Кількість доданих товарів',
            marker_color='red',
            yaxis='y1'
        ))

        fig.add_trace(go.Scatter(
            x=products_cumulative.index,
            y=products_cumulative.values,
            mode='lines+markers',
            name='Кумулятивна кількість',
            line=dict(color='darkred', dash='dash'),
            yaxis='y2'
        ))

        fig.update_layout(
            title='Динаміка кількості та кумулятивна зміна товарів',
            xaxis_title='Дата',
            yaxis=dict(title='Кількість товарів', side='left', showgrid=False),
            yaxis2=dict(title='Кумулятивна кількість', side='right', overlaying='y', showgrid=False),
            legend=dict(x=0.01, y=0.99, borderwidth=1)
        )
        st.plotly_chart(fig)

    def plot_sellers_combined(self, sellers_df, start_date, end_date):
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        filtered_sellers = sellers_df.loc[start_date:end_date]
        sellers_by_date = filtered_sellers.groupby(filtered_sellers.index.date)['Бренд'].nunique()
        sellers_cumulative = sellers_by_date.cumsum()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=sellers_by_date.index,
            y=sellers_by_date.values,
            name='Кількість доданих продавців',
            marker_color='orange',
            yaxis='y1'
        ))

        fig.add_trace(go.Scatter(
            x=sellers_cumulative.index,
            y=sellers_cumulative.values,
            mode='lines+markers',
            name='Кумулятивна кількість',
            line=dict(color='darkorange', dash='dash'),
            yaxis='y2'
        ))

        fig.update_layout(
            title='Динаміка кількості та кумулятивна зміна унікальних продавців',
            xaxis_title='Дата',
            yaxis=dict(title='Кількість продавців', side='left', showgrid=False),
            yaxis2=dict(title='Кумулятивна кількість', side='right', overlaying='y', showgrid=False),
            legend=dict(x=0.01, y=0.99, borderwidth=1)
        )
        st.plotly_chart(fig)

    def plot_pie_chart(self, products_df):
        brand_counts = products_df['Бренд'].value_counts()
        top_brands = brand_counts[:5]
        other_brands_count = brand_counts[5:].sum()

        labels = top_brands.index.tolist() + ['Інші бренди']
        sizes = top_brands.tolist() + [other_brands_count]

        fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3)])
        fig.update_layout(title="Відсоткове співвідношення топ 5 брендів і інших")
        st.plotly_chart(fig)
