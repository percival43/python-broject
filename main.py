import pandas as pd
import plotly.graph_objs as go
import dash
from dash import html
from dash import dcc

pd.options.mode.chained_assignment = None
app = dash.Dash()
server = app.server
df_use = pd.read_excel("Client Data (1).xlsx", sheet_name="Clinet Base")

# this block of code imports data from source, sets first row as Column Names and Drops the first rows
df = df_use
df.columns = df.iloc[0]
df = df.iloc[1:, :]

df2 = df_use
df2.columns = df2.iloc[0]
df2 = df.iloc[1:, :]

df3 = df_use
df3.columns = df3.iloc[0]
df3 = df.iloc[1:, :]

# This piece of code groups the DataFrame by Client's ID and removes the Product Column
df_groupby = df.groupby("Clinet ID").sum()
df_groupby_product = df.groupby("პროდუქტი").sum()
df_groupby.drop("პროდუქტი", axis=1, inplace=True)
df_groupby_product.drop("Clinet ID", axis=1, inplace=True)

df2_groupby = df2.groupby("Clinet ID").sum()
df2_groupby.drop("პროდუქტი", axis=1, inplace=True)

df3_average = df3.groupby("პროდუქტი").mean()
df3_average.drop("Clinet ID", axis=1, inplace=True)

# here I've Created 3 different DataFrames for $ , KG and Quantity data
money_spent_columns = [col for col in df_groupby if col.endswith("GEL")]
df_gel = df_groupby[money_spent_columns]
kg_bought_columns = [col for col in df_groupby_product if col.endswith("KG")]
df_kg = df_groupby_product[kg_bought_columns]
q_bought_columns = [col for col in df_groupby if col.endswith("Q")]
df_q = df_groupby[q_bought_columns]
df_q_treemap = df_groupby_product[q_bought_columns]
df_q_treemap["SUM"] = df_q_treemap.sum(axis=1)
df3_average_kg = df3_average[kg_bought_columns]

print(df3_average_kg)

df2_gel = df2_groupby[money_spent_columns]
df2_gel["AVGgel"] = df2_gel.mean(axis=1)
df2_gel["Count"] = df2_gel[df2_gel[money_spent_columns] > 0].count(axis=1)


data = [
    go.Box(y=df_gel[col], name=col, boxpoints=False, hovertext="x") for col in df_gel
]
layout = go.Layout(
    title="მომხმარებლების დანახარჯები თვეების მიხედვით",
    xaxis=dict(title="თვე"),
    yaxis=dict(title="ლარი", linecolor="#000000"),
    showlegend=False,
)

data2 = [
    go.Indicator(
        value=df_gel["JulGEL"].sum(),
        number=dict(prefix="₾"),
        delta=dict(reference=df_gel["JunGEL"].sum(), relative=True,valueformat=".0%"),
        mode="number+delta",
    )
]
layout2 = go.Layout(title="ივლისი, შემოსავალი M/M")


data3 = [
    go.Indicator(
        value=df_gel["AprGEL"].sum(),
        number=dict(prefix="₾"),
        delta=dict(reference=df_gel["MarGEL"].sum(), relative=True,valueformat=".0%"),
        mode="number+delta",
    )
]
layout3 = go.Layout(title="აპრილი, შემოსავალი M/M")

# data4 = [
#     go.Scatter(
#         x=df_kg.columns, y=df_kg[df_kg.index == col].iloc[0], mode="lines", name=col
#     )
#     for col in df_kg.index
# ]
#
# layout4 = go.Layout(
#     title="პროდუქტის მოხმარება",
#     xaxis=dict(title="თვე"),
#     yaxis=dict(title="გაყიდული პროდუქტი (კგ)"),
# )


data5 = [
    go.Scatter(
        x=df2_gel["Count"],
        y=df2_gel["AVGgel"],
        mode="markers",
        marker=dict(color="rgb(130,130,255)"),
    )
]


layout5 = go.Layout(
    title="მომხმარებლების ლოიალურობა და საშუალო თვიური დანახარჯები",
    xaxis=dict(title="რამდენი თვე იყო აქტიური?"),
    yaxis=dict(title="საშუალო თვიური დანახარჯები"),
)

data6 = [
    go.Treemap(
        labels=df_q_treemap.index,
        values=df_q_treemap["SUM"],
        parents=["", "", "", "", ""],
    )
]
layout6 = go.Layout(title="გაყიდული პროდუქტის რაოდენობა წლის განმავლობაში(ცალი)")

data7 = [go.Scatter(x=df3_average_kg.columns,
                    y=df3_average_kg[df3_average_kg.index == col].iloc[0],
                    name=col,
                    mode="lines") for col in df3_average_kg.index]
layout7= go.Layout(title="პროდუქტის საშუალო თვიური მოხმარება(კგ)")


app.layout = html.Div(
    children=[
        html.Img(
            src="https://static.wixstatic.com/media/f2f256_0c58b549322044e084f9bfd2b706d038~mv2.png/v1/fill/w_560,h_420,al_c,lg_1,q_85,enc_auto/kid-potato.png",
            alt="image",
            style={"width": "6%", "display": "inline-block","left-margin":"500px"},
        ),
        html.H1(
            "სოფლის ნობათის მარკეტინგული კვლევა 🥔🌶️🧅",
            style={"text-align": "center", "width": "100%"},
        ),
        dcc.Graph(
            id="boxplot",
            figure={"data": data, "layout": layout},
            style={"width": "64%", "height": "80vh", "display": "inline-block"},
        ),
        dcc.Graph(
            id="APR income",
            figure={"data": data3, "layout": layout3},
            style={
                "width": "18%",
                "height": "30vh",
                "vertical-align": "top",
                "display": "inline-block",
                "margin-top": "250px",
            },
        ),
        dcc.Graph(
            id="DEC  income",
            figure={"data": data2, "layout": layout2},
            style={
                "width": "18%",
                "height": "30vh",
                "display": "inline-block",
                "vertical-align": "top",
                "margin-top": "250px",
            },
        ),
        dcc.Graph(id="bla chart", figure={"data": data5, "layout": layout5}),
        dcc.Graph(
            id="AvgUseMonthlyKG",
            figure={"data": data7, "layout": layout7},
            style={"width": "60%", "display": "inline-block"},
        ),
        dcc.Graph(
            id="TreeMap",
            figure={"data": data6, "layout": layout6},
            style={"width": "40%", "display": "inline-block"},
        ),
    ]
)


if __name__ == "__main__":
    app.run_server()
