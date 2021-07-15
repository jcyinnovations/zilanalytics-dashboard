import plotly.express as px
import streamlit as st

discrete_palette = ['#29ccc4', '#299197', '#036f7d', 
                    '#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600',
                    '#00876c', '#6aaa96', '#aecdc2', '#f1f1f1', '#f0b8b8', '#e67f83', '#d43d51']

zil_palette = dict(bg="#242828", p1="#29ccc4", p2="#299197", p3="#036f7d")

tick_font   = dict(family="Roboto", size=10, color="white")

legend_font = dict(family="Roboto", size=10, color="white")

def default_barchart_layout(fig, x_title, y_title, legend_title):
    fig.update_layout(barmode='stack',
                    xaxis_tickangle=-45, 
                    yaxis=dict(title=y_title,tickfont=tick_font,gridcolor="gray"),
                    xaxis=dict(title=x_title, dtick=3,tickfont=tick_font),
                    legend_title_text=legend_title,
                    plot_bgcolor =zil_palette['bg'],
                    paper_bgcolor=zil_palette['bg'],
                    legend=dict(
                        yanchor="top",
                        xanchor="left",
                        orientation="h",
                        bgcolor=zil_palette['bg'], 
                        font=legend_font)
                    )
    return fig

def plotly_plot(chart_type: str, df, x, y, title, color=None, text=None):
    """ return plotly plots """

    if chart_type == "Bar":
        color_map = None
        disp_color = None
        if color:
            uniques = df[color].unique()
            color_map = {uniques[idx%len(discrete_palette)]:discrete_palette[idx%len(discrete_palette)] for idx in range(len(uniques))}
            disp_color = color

        #with st.echo():
        fig = px.bar(
            data_frame=df,
            color=disp_color,
            color_discrete_map=color_map,
            color_discrete_sequence =list(zil_palette.values())[1:],
            x=x,
            y=y,
            title=title
        )
        # by default shows stacked bar chart (sum) with individual hover values
        fig = default_barchart_layout(fig, x, y, color)

    elif chart_type == "Scatter":
        with st.echo():
            fig = px.scatter(
                data_frame=df,
                x=x,
                y=y,
                color=color,
                title=title,
            )
    elif chart_type == "Histogram":
        with st.echo():
            fig = px.histogram(
                data_frame=df,
                x=x,
                title=title,
            )

    elif chart_type == "Boxplot":
        with st.echo():
            fig = px.box(data_frame=df, x=x, y=y)
    elif chart_type == "Line":
        with st.echo():
            fig = px.line(
                data_frame=df,
                x=df.index,
                y=y,
                title=title,
            )
    elif chart_type == "3D Scatter":
        with st.echo():
            fig = px.scatter_3d(
                data_frame=df,
                x=x,
                y=y,
                z="body_mass_g",
                color=color,
                title=title,
            )

    return fig
