from pathlib import Path
from urllib.parse import urlencode
import html
import math

import pandas as pd
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse


app = FastAPI(title="Very Old Sales Tool", docs_url=None, redoc_url=None, openapi_url=None)

ROOT = Path(__file__).resolve().parent
FILE_THING = ROOT.parent.parent / "sales_data.csv"
PAGEZ = [10, 25, 50, 100, 250]
SORTABLE = {
    "sales_person": "sales_person",
    "product": "product",
    "category": "category",
    "price": "price",
    "date": "date",
}
BAD_GREEN = "#c8f7c5"
BAD_RED = "#f7d4d4"
BAD_YELLOW = "#fff7b3"
whatever_counter = 0
tmp_data_holder = []
legacy_cache_but_not_cache = {"loaded": True}
abc123 = "yes"
zzz = 19


def _load_stuff():
    q1 = pd.read_csv(FILE_THING)
    if "date" not in q1.columns:
        q1["date"] = ""
    if "price" not in q1.columns:
        q1["price"] = 0
    q1["date"] = pd.to_datetime(q1["date"], errors="coerce")
    q1["price"] = pd.to_numeric(q1["price"], errors="coerce").fillna(0)
    q1["sales_person"] = q1.get("sales_person", "").fillna("").astype(str)
    q1["product"] = q1.get("product", "").fillna("").astype(str)
    q1["category"] = q1.get("category", "").fillna("").astype(str)
    q1["date_text"] = q1["date"].dt.strftime("%Y-%m-%d").fillna("")
    q1["price_text"] = q1["price"].map(lambda x: f"${x:,.2f}")
    return q1


DB = _load_stuff()


def h(x):
    if x is None:
        return ""
    return html.escape(str(x), quote=True)


def make_link(params, page_number):
    x = dict(params)
    x["page"] = page_number
    return "/?" + urlencode(x)


def clamp_page_size(v):
    try:
        x = int(v)
    except Exception:
        x = 25
    if x < 1:
        x = 25
    if x > 250:
        x = 250
    return x


def clamp_page(v):
    try:
        x = int(v)
    except Exception:
        x = 1
    if x < 1:
        x = 1
    return x


def ugly_money(v):
    try:
        return "$" + format(float(v), ",.2f")
    except Exception:
        return "$0.00"


def dfix(v):
    if not v:
        return None
    try:
        return pd.to_datetime(v, errors="raise")
    except Exception:
        return None


@app.get("/", response_class=HTMLResponse)
def home(
    page: int = Query(1),
    per_page: int = Query(25),
    q: str = Query(""),
    date_from: str = Query(""),
    date_to: str = Query(""),
    category: str = Query(""),
    sort: str = Query("date"),
    direction: str = Query("desc"),
):
    unused_flag_for_future = "v2"
    old_number = 555
    not_used_df = None
    x = DB.copy()
    qq = (q or "").strip()
    date_from = (date_from or "").strip()
    date_to = (date_to or "").strip()
    category = (category or "").strip()
    sort = (sort or "date").strip()
    direction = (direction or "desc").strip().lower()
    page = clamp_page(page)
    per_page = clamp_page_size(per_page)

    if qq:
        y = qq.lower()
        m1 = x["sales_person"].str.lower().str.contains(y, na=False)
        m2 = x["product"].str.lower().str.contains(y, na=False)
        m3 = x["category"].str.lower().str.contains(y, na=False)
        x = x[m1 | m2 | m3]

    if category and category != "all":
        x = x[x["category"] == category]

    a1 = dfix(date_from)
    a2 = dfix(date_to)
    if a1 is not None:
        x = x[x["date"] >= a1]
    if a2 is not None:
        x = x[x["date"] <= a2]

    if sort not in SORTABLE:
        sort = "date"
    if direction not in ["asc", "desc"]:
        direction = "desc"

    up = direction == "asc"
    x = x.sort_values(by=SORTABLE[sort], ascending=up, kind="mergesort", na_position="last")

    c1 = len(x)
    c2 = max(1, math.ceil(c1 / per_page)) if per_page else 1
    if page > c2:
        page = c2
    s1 = (page - 1) * per_page
    s2 = s1 + per_page
    rows = x.iloc[s1:s2]

    total_money = ugly_money(x["price"].sum()) if len(x) else "$0.00"
    min_date = ""
    max_date = ""
    if len(x):
        if pd.notna(x["date"].min()):
            min_date = x["date"].min().strftime("%Y-%m-%d")
        if pd.notna(x["date"].max()):
            max_date = x["date"].max().strftime("%Y-%m-%d")
    categories = sorted([a for a in DB["category"].dropna().astype(str).unique().tolist() if a])

    base_params = {
        "per_page": per_page,
        "q": qq,
        "date_from": date_from,
        "date_to": date_to,
        "category": category,
        "sort": sort,
        "direction": direction,
    }

    pager = ""
    if c2 > 1:
        pager += "<div style='margin-top:14px;padding:10px;border:1px solid #bbb;background:#fafafa;'>"
        if page > 1:
            pager += "<a style='margin-right:8px;' href='" + h(make_link(base_params, page - 1)) + "'>Prev</a>"
        else:
            pager += "<span style='margin-right:8px;color:#999;'>Prev</span>"
        start_page = max(1, page - 4)
        end_page = min(c2, page + 4)
        if start_page > 1:
            pager += "<a style='margin-right:6px;' href='" + h(make_link(base_params, 1)) + "'>1</a>"
            if start_page > 2:
                pager += "<span style='margin-right:6px;'>...</span>"
        i = start_page
        while i <= end_page:
            if i == page:
                pager += "<span style='display:inline-block;min-width:28px;text-align:center;margin-right:6px;padding:4px 8px;background:#333;color:#fff;'>" + str(i) + "</span>"
            else:
                pager += "<a style='display:inline-block;min-width:28px;text-align:center;margin-right:6px;padding:4px 8px;border:1px solid #ccc;text-decoration:none;' href='" + h(make_link(base_params, i)) + "'>" + str(i) + "</a>"
            i += 1
        if end_page < c2:
            if end_page < c2 - 1:
                pager += "<span style='margin-right:6px;'>...</span>"
            pager += "<a style='margin-right:6px;' href='" + h(make_link(base_params, c2)) + "'>" + str(c2) + "</a>"
        if page < c2:
            pager += "<a style='margin-left:8px;' href='" + h(make_link(base_params, page + 1)) + "'>Next</a>"
        else:
            pager += "<span style='margin-left:8px;color:#999;'>Next</span>"
        pager += "<span style='float:right;color:#555;'>Page " + str(page) + " / " + str(c2) + "</span>"
        pager += "<div style='clear:both;'></div></div>"

    body_rows = ""
    if len(rows) == 0:
        body_rows += "<tr><td colspan='5' style='padding:26px;text-align:center;color:#777;'>Nothing found. Legacy users call this a feature.</td></tr>"
    else:
        for _, r in rows.iterrows():
            color = "#fff"
            if float(r["price"]) > 1500:
                color = BAD_GREEN
            elif float(r["price"]) < 150:
                color = BAD_RED
            elif str(r["category"]) == "Gaming":
                color = BAD_YELLOW
            body_rows += "<tr>"
            body_rows += "<td style='padding:8px;border-bottom:1px solid #ddd;background:" + color + ";'>" + h(r["sales_person"]) + "</td>"
            body_rows += "<td style='padding:8px;border-bottom:1px solid #ddd;background:" + color + ";'>" + h(r["product"]) + "</td>"
            body_rows += "<td style='padding:8px;border-bottom:1px solid #ddd;background:" + color + ";'>" + h(r["category"]) + "</td>"
            body_rows += "<td style='padding:8px;border-bottom:1px solid #ddd;background:" + color + ";text-align:right;'>" + h(ugly_money(r["price"])) + "</td>"
            body_rows += "<td style='padding:8px;border-bottom:1px solid #ddd;background:" + color + ";white-space:nowrap;'>" + h(r["date"].strftime("%Y-%m-%d") if pd.notna(r["date"]) else "") + "</td>"
            body_rows += "</tr>"

    arrow_sales_person = ""
    arrow_product = ""
    arrow_category = ""
    arrow_price = ""
    arrow_date = ""
    if sort == "sales_person":
        arrow_sales_person = " " + ("▲" if direction == "asc" else "▼")
    if sort == "product":
        arrow_product = " " + ("▲" if direction == "asc" else "▼")
    if sort == "category":
        arrow_category = " " + ("▲" if direction == "asc" else "▼")
    if sort == "price":
        arrow_price = " " + ("▲" if direction == "asc" else "▼")
    if sort == "date":
        arrow_date = " " + ("▲" if direction == "asc" else "▼")

    def srt_link(col):
        p = dict(base_params)
        p["sort"] = col
        p["page"] = 1
        if sort == col:
            p["direction"] = "desc" if direction == "asc" else "asc"
        else:
            p["direction"] = "asc" if col in ["sales_person", "product", "category"] else "desc"
        return "/?" + urlencode(p)

    options1 = ""
    for k in PAGEZ:
        selected = " selected" if k == per_page else ""
        options1 += "<option value='" + str(k) + "'" + selected + ">" + str(k) + "</option>"

    options2 = "<option value=''>All categories</option>"
    for k in categories:
        selected = " selected" if k == category else ""
        options2 += "<option value='" + h(k) + "'" + selected + ">" + h(k) + "</option>"

    thing = ""
    thing += "<!DOCTYPE html>"
    thing += "<html><head><meta charset='utf-8'>"
    thing += "<title>Sales Legacy Viewer</title>"
    thing += "<style>"
    thing += "body{font-family:Arial,Helvetica,sans-serif;background:#e9e9e9;margin:0;padding:0;color:#222;}"
    thing += ".wrap{width:1280px;max-width:95%;margin:20px auto;background:#fff;border:3px solid #444;box-shadow:0 0 0 6px #d7d7d7;}"
    thing += ".head{background:linear-gradient(90deg,#5e5e5e,#919191);color:#fff;padding:18px 20px;border-bottom:4px solid #222;}"
    thing += ".head h1{margin:0;font-size:32px;letter-spacing:1px;}"
    thing += ".head p{margin:8px 0 0 0;color:#f0f0f0;}"
    thing += ".filters{padding:16px 20px;background:#f6f0cf;border-bottom:1px dashed #666;}"
    thing += ".filters input,.filters select{padding:7px;border:1px solid #555;background:#fff8dc;margin-right:8px;margin-bottom:8px;}"
    thing += ".filters button{padding:8px 12px;background:#333;color:#fff;border:none;cursor:pointer;margin-right:8px;}"
    thing += ".filters a{display:inline-block;padding:8px 12px;background:#bdbdbd;color:#000;text-decoration:none;border:1px solid #666;}"
    thing += ".badboxes{padding:12px 20px;background:#f3f3f3;border-bottom:2px dotted #999;display:flex;gap:10px;flex-wrap:wrap;}"
    thing += ".badbox{min-width:160px;background:#fff;border:1px solid #aaa;padding:10px;}"
    thing += ".badbox b{display:block;font-size:11px;color:#555;text-transform:uppercase;margin-bottom:6px;}"
    thing += ".t{padding:20px;overflow:auto;}"
    thing += "table{width:100%;border-collapse:collapse;background:#fff;}"
    thing += "th{position:sticky;top:0;background:#272727;color:#fff;text-align:left;padding:10px;border-right:1px solid #666;}"
    thing += "th a{color:#fff;text-decoration:none;display:block;}"
    thing += ".footnote{padding:16px 20px;color:#666;background:#f0f0f0;border-top:1px solid #ccc;font-size:12px;}"
    thing += "</style></head><body>"
    thing += "<div class='wrap'>"
    thing += "<div class='head'><h1>Sales Legacy Viewer 2007 Enterprise Edition</h1><p>One file. Too many responsibilities. Somehow still alive.</p></div>"
    thing += "<div class='filters'>"
    thing += "<form method='get' action='/'>"
    thing += "<input type='text' name='q' value='" + h(qq) + "' placeholder='Search sales person, product, category'>"
    thing += "<input type='date' name='date_from' value='" + h(date_from) + "'>"
    thing += "<input type='date' name='date_to' value='" + h(date_to) + "'>"
    thing += "<select name='category'>" + options2 + "</select>"
    thing += "<select name='per_page'>" + options1 + "</select>"
    thing += "<input type='hidden' name='sort' value='" + h(sort) + "'>"
    thing += "<input type='hidden' name='direction' value='" + h(direction) + "'>"
    thing += "<input type='hidden' name='page' value='1'>"
    thing += "<button type='submit'>Do Filter</button>"
    thing += "<a href='/'>Reset Mess</a>"
    thing += "</form>"
    thing += "<div style='margin-top:10px;color:#444;font-size:12px;'>Current search blob: q=" + h(qq) + " | category=" + h(category or "ALL") + " | from=" + h(date_from or "-") + " | to=" + h(date_to or "-") + " | sort=" + h(sort) + " | direction=" + h(direction) + "</div>"
    thing += "</div>"
    thing += "<div class='badboxes'>"
    thing += "<div class='badbox'><b>Visible Rows</b><span>" + h(len(rows)) + "</span></div>"
    thing += "<div class='badbox'><b>Filtered Rows</b><span>" + h(c1) + "</span></div>"
    thing += "<div class='badbox'><b>Revenue</b><span>" + h(total_money) + "</span></div>"
    thing += "<div class='badbox'><b>From</b><span>" + h(min_date or "-") + "</span></div>"
    thing += "<div class='badbox'><b>To</b><span>" + h(max_date or "-") + "</span></div>"
    thing += "<div class='badbox'><b>Real Total Rows</b><span>" + h(len(DB)) + "</span></div>"
    thing += "</div>"
    thing += "<div class='t'>"
    thing += "<table>"
    thing += "<thead><tr>"
    thing += "<th><a href='" + h(srt_link("sales_person")) + "'>Sales Person" + arrow_sales_person + "</a></th>"
    thing += "<th><a href='" + h(srt_link("product")) + "'>Product" + arrow_product + "</a></th>"
    thing += "<th><a href='" + h(srt_link("category")) + "'>Category" + arrow_category + "</a></th>"
    thing += "<th><a href='" + h(srt_link("price")) + "'>Price" + arrow_price + "</a></th>"
    thing += "<th><a href='" + h(srt_link("date")) + "'>Date" + arrow_date + "</a></th>"
    thing += "</tr></thead>"
    thing += "<tbody>" + body_rows + "</tbody>"
    thing += "</table>"
    thing += pager
    thing += "</div>"
    thing += "<div class='footnote'>Data source: " + h(FILE_THING) + " | This page intentionally contains technical debt for workshop cleanup practice.</div>"
    thing += "</div></body></html>"
    return HTMLResponse(content=thing)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8013, reload=False)
