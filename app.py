import dash
from dash import dcc, html, Input, Output, State, dash_table
import sqlite3
import pandas as pd


app = dash.Dash(__name__)  # Usuwamy przekazanie server
app.title = "Twoja Aplikacja"

# Funkcja do pobierania danych z bazy SQLite
def fetch_data():
    conn = sqlite3.connect(r"C:\Users\kacpr\OneDrive - Akademia Górniczo-Hutnicza im. Stanisława Staszica w Krakowie\Licencjat\Python rzeczy\budzetdash\baza1.db")  # Ścieżka do pliku SQLite
    df = pd.read_sql_query("SELECT * FROM dane", conn)
    conn.close()
    return df

# Layout aplikacji
app.layout = html.Div([
    html.H3("Edycja danych z SQLite"),
    dash_table.DataTable(
        id="table",
        columns=[{"name": col, "id": col, "editable": True} for col in fetch_data().columns],
        data=fetch_data().to_dict("records"),
        row_deletable=True
    ),
    html.Button("Zapisz zmiany", id="save-btn", n_clicks=0),
    html.Div(id="output-msg")
])

# Callback do zapisywania zmian w bazie
@app.callback(
    Output("output-msg", "children"),
    Input("save-btn", "n_clicks"),
    State("table", "data")
)
def update_database(n_clicks, rows):
    if n_clicks > 0:
        df = pd.DataFrame(rows)
        conn = sqlite3.connect(r"C:\Users\kacpr\OneDrive - Akademia Górniczo-Hutnicza im. Stanisława Staszica w Krakowie\Licencjat\Python rzeczy\budzetdash\baza1.db")
        df.to_sql("dane", conn, if_exists="replace", index=False)  # Nadpisuje tabelę
        conn.close()
        return "Dane zapisane do bazy!"
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)
