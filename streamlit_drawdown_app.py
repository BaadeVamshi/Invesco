import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date

st.set_page_config(layout="wide", page_title="Drawdown % - MSFT vs NFLX")
st.title("Monthly Drawdown % — MSFT vs NFLX")

msft_file = st.file_uploader("Upload MSFT Monthly File (.xlsx)", type=["xlsx"])
nflx_file = st.file_uploader("Upload NFLX Monthly File (.xlsx)", type=["xlsx"])

if msft_file and nflx_file:

    def load_any_sheet(file):
        # try names first, otherwise first sheet
        for name in ("MSFT_Monthly", "NFLX_Monthly"):
            try:
                df = pd.read_excel(file, sheet_name=name, parse_dates=["date"])
                return df
            except Exception:
                pass
        # fallback: first sheet
        df = pd.read_excel(file, parse_dates=["date"])
        return df

    msft = load_any_sheet(msft_file).assign(ticker="MSFT")
    nflx = load_any_sheet(nflx_file).assign(ticker="NFLX")

    # basic validation
    required = {"date", "close"}
    if not required.issubset(set(msft.columns)) or not required.issubset(set(nflx.columns)):
        st.error("Both files must contain at least 'date' and 'close' columns.")
    else:
        df = pd.concat([msft, nflx], ignore_index=True)
        df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

        # ---------- Calculate drawdown (fixed) ----------
        df["Return"] = df.groupby("ticker")["close"].pct_change()

        # IMPORTANT: use transform so the result aligns to df.index
        df["Rebase to 100"] = df.groupby("ticker")["Return"].transform(
            lambda r: (1 + r.fillna(0)).cumprod() * 100
        )

        # Peak and Drawdown - use transform to keep alignment
        df["Peak"] = df.groupby("ticker")["Rebase to 100"].transform("cummax")
        df["Drawdown"] = df["Rebase to 100"] / df["Peak"] - 1
        df["Drawdown_pct"] = (df["Drawdown"] * 100).round(2)

        # ---------- Date range filter (robust) ----------
        min_date = df["date"].min()
        max_date = df["date"].max()

        # Convert pandas timestamps to native python datetime objects (Streamlit prefers these)
        def to_py_dt(x):
            if pd.isna(x):
                return None
            if isinstance(x, (pd.Timestamp, pd.DatetimeTZDtype)) or hasattr(x, "to_pydatetime"):
                try:
                    return x.to_pydatetime()
                except Exception:
                    # fallback
                    return pd.to_datetime(x).to_pydatetime()
            if isinstance(x, (datetime, date)):
                return x
            # try parse
            return pd.to_datetime(x).to_pydatetime()

        py_min = to_py_dt(min_date)
        py_max = to_py_dt(max_date)

        # If conversion succeeded use st.slider (datetime), else fallback to date_input
        if py_min is not None and py_max is not None:
            start, end = st.slider(
                "Select Date Range",
                min_value=py_min,
                max_value=py_max,
                value=(py_min, py_max),
                format="YYYY-MM"
            )
            # ensure we have datetimes (not date objects)
            start = pd.to_datetime(start)
            end = pd.to_datetime(end)
        else:
            st.warning("Using date picker because automatic date conversion failed.")
            dvals = df["date"].dropna().sort_values().unique()
            # best-effort: convert list to python date for widget
            d0 = pd.to_datetime(dvals[0]).date()
            dN = pd.to_datetime(dvals[-1]).date()
            picked = st.date_input("Select date range", value=(d0, dN), min_value=d0, max_value=dN)
            # convert back to timestamps
            start = pd.to_datetime(picked[0])
            end = pd.to_datetime(picked[1])

        df_filtered = df[(df["date"] >= start) & (df["date"] <= end)].copy()

        # ---------- Plot ----------
        fig = go.Figure()
        for ticker in df_filtered["ticker"].unique():
            d = df_filtered[df_filtered["ticker"] == ticker]
            if d.empty:
                continue

            fig.add_trace(
                go.Scatter(
                    x=d["date"],
                    y=d["Drawdown_pct"],
                    mode="lines",
                    fill="tozeroy",
                    name=f"{ticker} Drawdown %",
                    hovertemplate="%{x|%Y-%m}: %{y:.2f}%<extra></extra>",
                )
            )

            # protect against all-NaN drawdown_pct
            if d["Drawdown_pct"].dropna().size > 0:
                min_idx = d["Drawdown_pct"].idxmin()
                min_row = d.loc[min_idx]
                fig.add_trace(
                    go.Scatter(
                        x=[min_row["date"]],
                        y=[min_row["Drawdown_pct"]],
                        mode="markers+text",
                        marker=dict(size=9),
                        text=[f"Max Drop: {min_row['Drawdown_pct']}%"],
                        textposition="bottom center",
                        showlegend=False,
                    )
                )

        fig.update_layout(
            title="Monthly Drawdown % Area Chart",
            xaxis_title="Date",
            yaxis_title="Drawdown (%)",
            hovermode="x unified",
            legend=dict(orientation="h", y=1.05),
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------- Max drawdown table ----------
        st.subheader("Max Drawdown Summary (selected range)")
        rows = []
        for ticker in df_filtered["ticker"].unique():
            d = df_filtered[df_filtered["ticker"] == ticker]
            if d["Drawdown_pct"].dropna().empty:
                continue
            row = d.loc[d["Drawdown_pct"].idxmin(), ["date", "Drawdown_pct", "close"]]
            rows.append({"ticker": ticker, "date": row["date"], "Max Drawdown (%)": row["Drawdown_pct"], "Close": row["close"]})

        if rows:
            summary = pd.DataFrame(rows)
            summary["Month of Max Drop"] = pd.to_datetime(summary["date"]).dt.strftime("%Y-%m")
            st.dataframe(summary[["ticker", "Month of Max Drop", "Max Drawdown (%)", "Close"]].rename(columns={"ticker":"Ticker"}))
        else:
            st.info("No valid drawdown values in the selected range.")
else:
    st.info("Please upload both MSFT & NFLX files to continue.")
