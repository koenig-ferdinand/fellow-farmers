import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64
from io import BytesIO

# Farbpalette basierend auf Syngenta Branding
syngenta_colors = {
    'turquoise': '#00CFCD',
    'green': '#7FCA3F',
    'orange': '#EB8200',
    'pink': '#EC3AAA',
    'dark_green': '#265000',
    'dark_turquoise': '#334E56',
    'background': '#F5F5F5',
    'white': '#FFFFFF'
}

# Erstellen der Daten für den Stress Buster (Daten aus dem PDF extrahiert)
stress_buster_data = {
    'Anwendung': ['Mit Stress Buster', 'Ohne Behandlung'],
    'Kälte': [5, 0],
    'Hitze': [8.2, 0],
    'Trockenheit': [5.1, 0]
}

stress_science_data = {
    'Kategorie': ['Transkriptomik', 'Phenomik', 'Metabolomik'],
    'Beschreibung': [
        'Aktivierung von >100 Genen bei behandelten Pflanzen, vor allem bei abiotischer Stresstoleranz',
        'Verbesserte Biomasse, Gesundheitsindex und Wassergehalt unter Stressbedingungen',
        'Modulation spezifischer Metaboliten-Klassen, verbunden mit der Reaktion auf abiotischen Stress'
    ]
}

# Erstellen der Daten für den Yield Booster (Daten aus dem PDF extrahiert)
yield_booster_data = {
    'Kultur': ['Weizen', 'Reis', 'Sojabohne', 'Mais'],
    'Ertragssteigerung (t/ha)': [0.30, 0.66, 0.27, 0.64],
    'ROI': [3, 14, 9, 7]
}

yield_science_data = {
    'Kategorie': ['Transkriptomik', 'Phenomik'],
    'Beschreibung': [
        'NGS-Experiment: Aktivierung von Genen für Zuckertransport, Zellteilung und Fettsäurebiosynthese',
        'Verbesserte Biovolumen, Pflanzenkompaktheit und Grünindex in Mais und Sojabohnen'
    ]
}

# ROI-Vergleich für verschiedene Kulturen mit/ohne Produkt
def plot_roi_comparison(product_data, product_name):
    fig = make_subplots(
        rows=1, cols=2, specs=[[{'type': 'bar'}, {'type': 'domain'}]],
        subplot_titles=("Ertragssteigerung und ROI", "ROI nach Kultur"),
        horizontal_spacing=0.15
    )
    
    # Balkendiagramm für Ertragssteigerung
    fig.add_trace(
        go.Bar(
            x=product_data['Kultur'],
            y=product_data['Ertragssteigerung (t/ha)'],
            name='Ertragssteigerung (t/ha)',
            marker_color=syngenta_colors['green']
        ),
        row=1,
        col=1
    )
    
    # Zweite Y-Achse für ROI
    fig.add_trace(
        go.Scatter(
            x=product_data['Kultur'],
            y=product_data['ROI'],
            mode='markers',
            name='ROI',
            marker=dict(size=12, color=syngenta_colors['turquoise'])
        ),
        row=1,
        col=1,
        secondary_y=True
    )
    
    # ROI-Vergleich als Donut-Chart
    fig.add_trace(
        go.Pie(
            labels=product_data['Kultur'],
            values=product_data['ROI'],
            hole=.4,
            marker_colors=[
                syngenta_colors['green'],
                syngenta_colors['turquoise'],
                syngenta_colors['orange'],
                syngenta_colors['pink']
            ]
        ),
        row=1,
        col=2
    )
    
    # Layout anpassen
    fig.update_layout(
        title_text=f"{product_name} - ROI und Ertrag nach Kultur",
        font=dict(family="Arial", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="simple_white",
        height=500,
        width=950
    )
    
    fig.update_yaxes(title_text="Ertragssteigerung (t/ha)", row=1, col=1)
    fig.update_yaxes(title_text="Return on Investment (ROI)", row=1, col=1, secondary_y=True)
    
    return fig

# Visualisierung der Ertragssteigung bei Stressbedingungen
def plot_stress_performance(stress_data):
    fig = go.Figure()
    
    for i, stress_type in enumerate(['Kälte', 'Hitze', 'Trockenheit']):
        colors = [syngenta_colors['turquoise'], syngenta_colors['background']]
        
        fig.add_trace(go.Bar(
            x=[stress_type, stress_type],
            y=[stress_data[stress_type][0], stress_data[stress_type][1]],
            name=['Mit Stress Buster', 'Ohne Behandlung'][i % 2],
            marker_color=[syngenta_colors['turquoise'], syngenta_colors['background']][i % 2],
            text=[f"+{stress_data[stress_type][0]}%", "Basis"],
            textposition='outside',
            width=0.4,
            offset=[-0.2, 0.2][i % 2]
        ))
    
    # Layout anpassen
    fig.update_layout(
        title_text="Stress Buster - Ertragssteigerung unter Stressbedingungen",
        xaxis=dict(title='Stresstyp'),
        yaxis=dict(title='Ertragssteigerung (%)'),
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="simple_white",
        height=450,
        width=750
    )
    
    return fig

# Wissenschaftliche Grundlagen als Infografik
def create_science_infographic(science_data, product_name, color_main):
    fig = go.Figure()
    
    # Y-Positionen für jede Kategorie
    y_positions = list(range(len(science_data['Kategorie'])))
    
    # Punkte für Kategorien
    fig.add_trace(go.Scatter(
        x=[0] * len(y_positions),
        y=y_positions,
        mode='markers',
        marker=dict(size=25, color=color_main),
        text=science_data['Kategorie'],
        textposition="middle right",
        hoverinfo="text",
        name=""
    ))
    
    # Texte für die Beschreibungen
    for i, (cat, desc) in enumerate(zip(science_data['Kategorie'], science_data['Beschreibung'])):
        fig.add_annotation(
            x=0.5,
            y=y_positions[i],
            text=f"<b>{cat}</b>: {desc}",
            showarrow=False,
            font=dict(
                family="Arial",
                size=14,
                color="#333"
            ),
            align="left",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#f9f9f9",
            opacity=0.8
        )
    
    # Layout anpassen
    fig.update_layout(
        title_text=f"Wissenschaft hinter {product_name}",
        showlegend=False,
        plot_bgcolor='white',
        width=800,
        height=400,
        margin=dict(l=20, r=20, t=80, b=20),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.2, 1]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-1, len(y_positions)]
        )
    )
    
    return fig

# Erstellen der Dashboard-Anwendung
app = dash.Dash(__name__)

# Layout definieren
app.layout = html.Div(
    style={'backgroundColor': syngenta_colors['background'], 'padding': '20px'},
    children=[
        html.Div(
            style={
                'backgroundColor': syngenta_colors['white'],
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.1)'
            },
            children=[
                html.H1(
                    "Syngenta Biologicals - Produktanalyse",
                    style={'textAlign': 'center', 'color': syngenta_colors['dark_turquoise']}
                ),
        
                html.Div(
                    style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'},
                    children=[
                        html.Img(
                            src='https://www.syngenta.com/sites/corp/themes/syngenta/logo.svg',
                            style={'height': '60px'}
                        )
                    ]
                ),
        
                # Tabs für Produkte
                dcc.Tabs(
                    id='product-tabs', 
                    value='stress-buster', 
                    children=[
                        dcc.Tab(
                            label='Stress Buster', 
                            value='stress-buster',
                            style={
                                'borderBottom': f'3px solid {syngenta_colors["turquoise"]}',
                                'padding': '10px', 
                                'fontWeight': 'bold'
                            },
                            selected_style={
                                'borderBottom': f'3px solid {syngenta_colors["turquoise"]}',
                                'padding': '10px', 
                                'fontWeight': 'bold', 
                                'backgroundColor': '#f0f0f0'
                            }
                        ),
                        dcc.Tab(
                            label='Yield Booster', 
                            value='yield-booster',
                            style={
                                'borderBottom': f'3px solid {syngenta_colors["green"]}',
                                'padding': '10px', 
                                'fontWeight': 'bold'
                            },
                            selected_style={
                                'borderBottom': f'3px solid {syngenta_colors["green"]}',
                                'padding': '10px', 
                                'fontWeight': 'bold', 
                                'backgroundColor': '#f0f0f0'
                            }
                        ),
                    ]
                ),
        
                # Inhalt basierend auf Tab-Auswahl
                html.Div(id='tab-content')
            ]
        )
    ]
)

# Callback für Tab-Inhalt
@app.callback(
    Output('tab-content', 'children'),
    Input('product-tabs', 'value')
)
def render_content(tab):
    if tab == 'stress-buster':
        # Stress Buster Inhalt
        stress_fig = plot_stress_performance(stress_buster_data)
        science_fig = create_science_infographic(stress_science_data, "Stress Buster", syngenta_colors['turquoise'])
        
        return html.Div([
            html.H2("Stress Buster", style={'color': syngenta_colors['dark_turquoise']}),
            
            html.Div(
                style={'backgroundColor': '#f9f9f9', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'},
                children=[
                    html.H3("Produktbeschreibung"),
                    html.P(
                        "Der Stress Buster ist ein Biostimulant, der Pflanzen dabei hilft, abiotischen Stress zu "
                        "überwinden und gleichzeitig die Erträge zu sichern. Das Produkt kann sowohl präventiv als "
                        "auch bei auftretendem Stress angewendet werden."
                    )
                ]
            ),
            
            html.H3("Leistung unter Stressbedingungen"),
            dcc.Graph(figure=stress_fig),
            
            html.Div(
                style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '30px'},
                children=[
                    html.Div(
                        style={
                            'width': '30%',
                            'backgroundColor': '#f0f9f9',
                            'padding': '20px',
                            'borderRadius': '10px',
                            'boxShadow': '0 2px 4px 0 rgba(0, 0, 0, 0.05)'
                        },
                        children=[
                            html.H4("ROI Highlights", style={'color': syngenta_colors['turquoise']}),
                            html.Ul([
                                html.Li("Obst: 10,5:1"),
                                html.Li("Gemüse: 11,6:1"),
                                html.Li("Reihenkulturen: 3,9:1")
                            ]),
                            html.P("Basierend auf durchschnittlichen Werten im europäischen Markt")
                        ]
                    ),
                    
                    html.Div(
                        style={'width': '65%'},
                        children=[
                            html.H3("Wissenschaftliche Grundlagen"),
                            dcc.Graph(figure=science_fig)
                        ]
                    )
                ]
            )
        ])
    
    elif tab == 'yield-booster':
        # Yield Booster Inhalt
        roi_fig = plot_roi_comparison(yield_booster_data, "Yield Booster")
        science_fig = create_science_infographic(yield_science_data, "Yield Booster", syngenta_colors['green'])
        
        return html.Div([
            html.H2("Yield Booster", style={'color': syngenta_colors['dark_turquoise']}),
            
            html.Div(
                style={'backgroundColor': '#f9f9f9', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'},
                children=[
                    html.H3("Produktbeschreibung"),
                    html.P(
                        "Der Yield Booster ist ein Biostimulant für Reihenkulturen, der höchste Produktivität und "
                        "Rendite für Landwirte sicherstellt. Die Lösung steigert die Pflanzenproduktivität durch "
                        "besseren Transport von Zuckern und Nährstoffen, Förderung der Zellteilung sowie "
                        "Fettsäurebiosynthese und -transport."
                    )
                ]
            ),
            
            html.H3("ROI und Ertragssteigerung"),
            dcc.Graph(figure=roi_fig),
            
            html.H3("Wissenschaftliche Grundlagen"),
            dcc.Graph(figure=science_fig)
        ])

# Run the app (updated method)
if __name__ == '__main__':
    app.run(debug=True)