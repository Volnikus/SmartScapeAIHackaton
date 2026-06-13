import streamlit as st
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
import warnimport streamlit as st
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from datetime import datetime
import time
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AI Скорая — Астана",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--sidebar-grad) !important;
    border-right: 1px solid var(--sidebar-border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

.main-header {
    background: linear-gradient(135deg, rgba(59,130,246,0.12) 0%, rgba(6,182,212,0.08) 50%, rgba(139,92,246,0.12) 100%);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 20px;
    padding: 26px 36px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
}

.main-header h1 {
    font-size: 1.9rem;
    font-weight: 800;
    background: var(--title-grad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.main-header p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin-top: 6px;
}

.metric-card {
    background: var(--card-grad);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    box-shadow: var(--card-shadow);
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: var(--card-hover-border);
    box-shadow: var(--card-hover-shadow);
}

.metric-card .icon { font-size: 1.7rem; margin-bottom: 6px; }
.metric-card .value {
    font-size: 1.8rem;
    font-weight: 800;
    background: var(--value-grad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-card .label {
    color: var(--text-secondary);
    font-size: 0.78rem;
    font-weight: 500;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-blue::after { background: linear-gradient(90deg, #3b82f6, #06b6d4); }
.metric-green::after { background: linear-gradient(90deg, #10b981, #34d399); }
.metric-red::after { background: linear-gradient(90deg, #ef4444, #f97316); }
.metric-purple::after { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }

.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 22px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title .bar {
    width: 4px;
    height: 22px;
    background: linear-gradient(180deg, #3b82f6, #8b5cf6);
    border-radius: 2px;
}

.recommendation-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.08) 0%, rgba(139,92,246,0.08) 100%);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 16px;
    padding: 20px 22px;
    margin: 8px 0;
}

.recommendation-card h4 {
    color: var(--accent-blue);
    font-weight: 700;
    margin: 0 0 8px 0;
}

.recommendation-card p {
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.7;
}

.recommendation-card p b { color: var(--text-primary); }

.sidebar-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 8px;
}

[data-testid="stSlider"] label,
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
    font-weight: 500 !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 11px 22px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(59,130,246,0.3) !important;
}

div.stButton > button:disabled {
    background: var(--bg-secondary) !important;
    color: var(--text-secondary) !important;
    opacity: 0.55 !important;
    box-shadow: none !important;
    transform: none !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
header[data-testid="stHeader"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

[data-testid="stMainBlockContainer"] {
    background: var(--bg-primary) !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: var(--bg-card) !important;
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
    border-radius: 10px !important;
}

[data-baseweb="select"] input { color: var(--text-primary) !important; }
[data-baseweb="select"] svg { fill: var(--text-secondary) !important; }

[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
[data-baseweb="menu"] ul,
[role="listbox"],
[role="listbox"] li,
[role="option"] {
    background-color: var(--menu-bg) !important;
    background: var(--menu-bg) !important;
    color: var(--text-primary) !important;
}

[role="option"]:hover,
div[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] [aria-selected="true"] {
    background-color: var(--menu-hover) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
    border-radius: 10px !important;
}

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
.stSlider label,
.stSelectbox label,
.stRadio label,
.stCheckbox label {
    color: var(--text-primary) !important;
}

[data-testid="stTabs"] button { color: var(--text-secondary) !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent-blue) !important;
    border-bottom-color: var(--accent-blue) !important;
}

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--scrollbar); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--scrollbar-hover); }

[data-testid="stMetric"],
[data-testid="stMetric"] label,
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    background: transparent !important;
}

[data-testid="stForm"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    background: transparent !important;
}

.dist-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Inter', sans-serif;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border-color);
    background: var(--bg-card);
}

.dist-table th {
    background: var(--bg-secondary);
    color: var(--text-secondary);
    text-align: left;
    padding: 10px 13px;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    font-weight: 600;
    border-bottom: 1px solid var(--border-color);
}

.dist-table td {
    padding: 10px 13px;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border-color);
    font-size: 0.86rem;
}

.dist-table tr:last-child td { border-bottom: none; }
.dist-table tbody tr:hover td { background: var(--menu-hover); }

.ops-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.74rem;
    font-weight: 700;
    white-space: nowrap;
}

.appr-card {
    background: linear-gradient(135deg, rgba(239,68,68,0.16), rgba(239,68,68,0.05));
    border: 1px solid rgba(239,68,68,0.45);
    border-left: 5px solid #ef4444;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 10px 0 8px 0;
}

.appr-card h4 { color: #ef4444; margin: 0 0 6px 0; font-weight: 800; font-size: 1.05rem; }
.appr-card .sit { color: var(--text-primary); margin: 0 0 8px 0; line-height: 1.55; }
.appr-card .dec { color: var(--text-secondary); margin: 0; line-height: 1.55; }
.appr-card .dec b { color: var(--accent-blue); }

.status-block {
    background: var(--card-grad);
    border: 1px solid var(--border-color);
    border-radius: 18px;
    padding: 24px 28px;
    box-shadow: var(--card-shadow);
}

.log-list { max-height: 420px; overflow-y: auto; padding-right: 4px; }
.log-item {
    border-left: 3px solid var(--accent-blue);
    background: var(--bg-secondary);
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 8px;
}
.log-item .t { font-size: 0.7rem; color: var(--text-secondary); font-weight: 600; }
.log-item .a { font-size: 0.88rem; color: var(--text-primary); font-weight: 700; margin: 2px 0; }
.log-item .r { font-size: 0.78rem; color: var(--text-secondary); }

</style>
"""


THEMES = {
    "Светлая": {
        "bg_primary": "#f1f5f9", "bg_secondary": "#ffffff", "bg_card": "#ffffff",
        "accent_blue": "#2563eb", "accent_cyan": "#0891b2", "accent_emerald": "#059669",
        "accent_red": "#dc2626", "accent_amber": "#d97706", "accent_purple": "#7c3aed",
        "text_primary": "#1e293b", "text_secondary": "#64748b", "border": "#e2e8f0",
        "sidebar_grad": "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)",
        "sidebar_border": "#e2e8f0",
        "card_grad": "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
        "card_shadow": "0 1px 3px rgba(15,23,42,0.06), 0 1px 2px rgba(15,23,42,0.04)",
        "card_hover_shadow": "0 12px 30px rgba(15,23,42,0.10)",
        "card_hover_border": "rgba(37,99,235,0.4)",
        "value_grad": "linear-gradient(135deg, #2563eb, #7c3aed)",
        "title_grad": "linear-gradient(135deg, #2563eb, #7c3aed, #0891b2)",
        "menu_bg": "#ffffff", "menu_hover": "rgba(37,99,235,0.10)",
        "tag_bg": "rgba(37,99,235,0.12)", "tag_text": "#1d4ed8",
        "scrollbar": "#cbd5e1", "scrollbar_hover": "#94a3b8",
        "map_tiles": "light_all", "map_name": "Light",
        "popup_bg": "#ffffff", "popup_text": "#1e293b", "popup_value": "#0f172a",
        "popup_sub": "#64748b", "popup_shadow": "0 6px 20px rgba(15,23,42,0.15)",
        "label_color": "#0f172a", "label_shadow": "rgba(255,255,255,0.9)",
        "green": "#059669", "footer": "#64748b",
    },
    "Тёмная": {
        "bg_primary": "#0a0e1a", "bg_secondary": "#111827", "bg_card": "#1a1f36",
        "accent_blue": "#3b82f6", "accent_cyan": "#06b6d4", "accent_emerald": "#10b981",
        "accent_red": "#ef4444", "accent_amber": "#f59e0b", "accent_purple": "#8b5cf6",
        "text_primary": "#f1f5f9", "text_secondary": "#94a3b8", "border": "#1e293b",
        "sidebar_grad": "linear-gradient(180deg, #0f1629 0%, #1a1040 100%)",
        "sidebar_border": "rgba(59, 130, 246, 0.15)",
        "card_grad": "linear-gradient(135deg, #1a1f36 0%, rgba(30,41,59,0.8) 100%)",
        "card_shadow": "0 1px 3px rgba(0,0,0,0.35)",
        "card_hover_shadow": "0 12px 40px rgba(59,130,246,0.15)",
        "card_hover_border": "rgba(59,130,246,0.3)",
        "value_grad": "linear-gradient(135deg, #60a5fa, #a78bfa)",
        "title_grad": "linear-gradient(135deg, #60a5fa, #a78bfa, #06b6d4)",
        "menu_bg": "#1e293b", "menu_hover": "rgba(59,130,246,0.2)",
        "tag_bg": "rgba(59,130,246,0.2)", "tag_text": "#93c5fd",
        "scrollbar": "#334155", "scrollbar_hover": "#475569",
        "map_tiles": "dark_all", "map_name": "Dark",
        "popup_bg": "#1a1f36", "popup_text": "#f1f5f9", "popup_value": "#ffffff",
        "popup_sub": "#94a3b8", "popup_shadow": "0 6px 20px rgba(0,0,0,0.5)",
        "label_color": "#ffffff", "label_shadow": "rgba(0,0,0,0.8)",
        "green": "#34d399", "footer": "#475569",
    },
}


def apply_theme(T):
    st.markdown(f"""
    <style>
    :root {{
        --bg-primary: {T['bg_primary']};
        --bg-secondary: {T['bg_secondary']};
        --bg-card: {T['bg_card']};
        --accent-blue: {T['accent_blue']};
        --accent-cyan: {T['accent_cyan']};
        --accent-emerald: {T['accent_emerald']};
        --accent-red: {T['accent_red']};
        --accent-amber: {T['accent_amber']};
        --accent-purple: {T['accent_purple']};
        --text-primary: {T['text_primary']};
        --text-secondary: {T['text_secondary']};
        --border-color: {T['border']};
        --sidebar-grad: {T['sidebar_grad']};
        --sidebar-border: {T['sidebar_border']};
        --card-grad: {T['card_grad']};
        --card-shadow: {T['card_shadow']};
        --card-hover-shadow: {T['card_hover_shadow']};
        --card-hover-border: {T['card_hover_border']};
        --value-grad: {T['value_grad']};
        --title-grad: {T['title_grad']};
        --menu-bg: {T['menu_bg']};
        --menu-hover: {T['menu_hover']};
        --tag-bg: {T['tag_bg']};
        --tag-text: {T['tag_text']};
        --scrollbar: {T['scrollbar']};
        --scrollbar-hover: {T['scrollbar_hover']};
    }}
    </style>
    """, unsafe_allow_html=True)
    st.markdown(BASE_CSS, unsafe_allow_html=True)


DISTRICTS = {
    "Есиль": {"lat": 51.145, "lon": 71.470, "elderly_ratio": 0.12, "base_calls": 8},
    "Алматы р-н": {"lat": 51.100, "lon": 71.430, "elderly_ratio": 0.22, "base_calls": 12},
    "Сарыарка": {"lat": 51.160, "lon": 71.410, "elderly_ratio": 0.18, "base_calls": 10},
    "Байконур": {"lat": 51.120, "lon": 71.380, "elderly_ratio": 0.20, "base_calls": 9},
    "Нура": {"lat": 51.180, "lon": 71.350, "elderly_ratio": 0.15, "base_calls": 7},
}

HOLIDAYS = [
    "Нет", "Наурыз", "День Республики", "День Независимости",
    "День Конституции", "День Первого Президента", "Новый Год"
]

HOLIDAY_DATES = {
    "Наурыз": [(3, 21), (3, 22), (3, 23)],
    "День Республики": [(10, 25)],
    "День Независимости": [(12, 16), (12, 17)],
    "День Конституции": [(8, 30)],
    "День Первого Президента": [(12, 1)],
    "Новый Год": [(1, 1), (1, 2)],
}

MACHINE_COUNT = 10
REFRESH_SECONDS = 30
CALL_INTERVAL = 120

STATUS_FREE = "Свободна"
STATUS_ENROUTE = "В пути"
STATUS_ONSCENE = "На вызове"

STATUS_COLOR = {
    STATUS_FREE: "#10b981",
    STATUS_ENROUTE: "#f59e0b",
    STATUS_ONSCENE: "#ef4444",
}

CATEGORIES = {
    1: ("Угроза жизни", "#ef4444"),
    2: ("Срочный", "#f59e0b"),
    3: ("Неотложный", "#3b82f6"),
    4: ("Плановый", "#10b981"),
}

STREETS = {
    "Есиль": ["пр. Мангилик Ел", "ул. Сыганак", "ул. Кабанбай батыра", "пр. Туран"],
    "Алматы р-н": ["ул. Бейбитшилик", "пр. Богенбай батыра", "ул. Жубанова", "ул. Пушкина"],
    "Сарыарка": ["пр. Абая", "ул. Сейфуллина", "ул. Иманова", "ул. Жанибека"],
    "Байконур": ["ул. Кенесары", "пр. Республики", "ул. Майлина", "ул. Бараева"],
    "Нура": ["ул. Кошкарбаева", "ул. Тлендиева", "ул. Акжол", "ул. Шынтас"],
}


@st.cache_data
def generate_dataset(n=50000):
    np.random.seed(42)
    records = []
    district_names = list(DISTRICTS.keys())

    for _ in range(n):
        hour = np.random.randint(0, 24)
        dow = np.random.randint(0, 7)
        month = np.random.randint(1, 13)
        district = np.random.choice(district_names)
        info = DISTRICTS[district]

        if month in [12, 1, 2]:
            temp = np.random.normal(-18, 10)
        elif month in [3, 4, 5]:
            temp = np.random.normal(5, 8)
        elif month in [6, 7, 8]:
            temp = np.random.normal(28, 5)
        else:
            temp = np.random.normal(8, 7)
        temp = np.clip(temp, -42, 42)

        ice = 1 if (temp < -5 and np.random.random() < 0.4) else 0
        precip = np.random.exponential(2) if np.random.random() < 0.3 else 0.0
        pressure = np.random.normal(740, 10)

        day_of_month = np.random.randint(1, 29)
        holiday = "Нет"
        for h_name, dates in HOLIDAY_DATES.items():
            for m, d in dates:
                if month == m and day_of_month == d:
                    holiday = h_name
                    break

        event = 1 if np.random.random() < 0.08 else 0
        elderly = info["elderly_ratio"]

        calls = info["base_calls"]

        if 7 <= hour <= 9:
            calls *= 1.3
        elif 17 <= hour <= 20:
            calls *= 1.5
        elif 0 <= hour <= 5:
            calls *= 0.5

        if dow == 4 and 18 <= hour <= 23:
            calls *= 1.6
        if dow in [5, 6]:
            calls *= 1.2

        if temp < -25:
            calls *= 1.7
        elif temp < -15:
            calls *= 1.3

        if ice:
            calls *= 1.4
        if precip > 5:
            calls *= 1.2

        if holiday == "Наурыз" and district == "Есиль":
            calls *= 2.2
        elif holiday == "Наурыз":
            calls *= 1.5
        elif holiday != "Нет":
            calls *= 1.4

        if event:
            calls *= 1.5

        calls *= (1 + elderly * 2)
        calls += np.random.normal(0, calls * 0.15)
        calls = max(0, int(round(calls)))

        records.append({
            "hour": hour, "day_of_week": dow, "month": month, "district": district,
            "temperature": round(temp, 1), "ice": ice, "precipitation": round(precip, 1),
            "pressure": round(pressure, 1), "holiday": holiday, "event": event,
            "elderly_ratio": elderly, "calls": calls,
        })

    return pd.DataFrame(records)


@st.cache_resource
def train_model(df):
    cat_cols = ["district", "day_of_week", "month", "holiday"]
    for c in cat_cols:
        df[c] = df[c].astype("category")

    features = [
        "hour", "day_of_week", "month", "district",
        "temperature", "ice", "precipitation", "pressure",
        "holiday", "event", "elderly_ratio"
    ]
    X = df[features]
    y = df["calls"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = lgb.LGBMRegressor(
        num_leaves=64, learning_rate=0.05, n_estimators=500,
        categorical_feature=cat_cols, verbose=-1, random_state=42, n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    return model, mae, rmse


def predict_for_districts(model, hour, dow, month, temp, ice, precip, pressure, holiday, event):
    rows = []
    for name, info in DISTRICTS.items():
        rows.append({
            "hour": hour, "day_of_week": dow, "month": month, "district": name,
            "temperature": temp, "ice": ice, "precipitation": precip, "pressure": pressure,
            "holiday": holiday, "event": event, "elderly_ratio": info["elderly_ratio"],
        })
    pred_df = pd.DataFrame(rows)
    for c in ["district", "day_of_week", "month", "holiday"]:
        pred_df[c] = pred_df[c].astype("category")

    preds = model.predict(pred_df)
    preds = np.clip(preds, 0, None)
    return {name: round(float(p), 1) for name, p in zip(DISTRICTS.keys(), preds)}


def detect_holiday(month, day):
    for name, dates in HOLIDAY_DATES.items():
        for m, d in dates:
            if month == m and day == d:
                return name
    return "Нет"


def current_context():
    now = datetime.now()
    month = now.month
    if month in [12, 1, 2]:
        base_temp = -18
    elif month in [3, 4, 5]:
        base_temp = 5
    elif month in [6, 7, 8]:
        base_temp = 28
    else:
        base_temp = 8
    return now.hour, now.weekday(), month, base_temp


def get_env():
    hour, dow, month, base_temp = current_context()
    temp = int(st.session_state.get("env_temp", base_temp))
    ice = 1 if st.session_state.get("env_ice", base_temp < -5) else 0
    holiday = detect_holiday(month, datetime.now().day)
    return hour, dow, month, temp, ice, holiday


def jitter(lat, lon, scale=0.012):
    return lat + np.random.normal(0, scale), lon + np.random.normal(0, scale * 1.2)


def gdist(a_lat, a_lon, b_lat, b_lon):
    return float(np.hypot(a_lat - b_lat, a_lon - b_lon))


def eta_minutes(d):
    return int(np.clip(round(d * 160 + 3), 3, 18))


def risk_color(ratio):
    if ratio > 0.7:
        return "#ef4444", "ВЫСОКИЙ"
    if ratio > 0.4:
        return "#f59e0b", "СРЕДНИЙ"
    return "#10b981", "НИЗКИЙ"


def status_badge(status):
    c = STATUS_COLOR[status]
    return f'<span class="ops-badge" style="background:{c}22;color:{c};border:1px solid {c}66;">{status}</span>'


def cat_badge(cat):
    name, c = CATEGORIES[cat]
    return f'<span class="ops-badge" style="background:{c}22;color:{c};border:1px solid {c}66;">Кат {cat} · {name}</span>'


def active_calls():
    return [c for c in st.session_state.calls if c["status"] == "active"]


def find_call(cid):
    for c in st.session_state.calls:
        if c["id"] == cid:
            return c
    return None


def log_ai(action, reason):
    st.session_state.ai_log.insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "action": action, "reason": reason,
    })
    st.session_state.ai_log = st.session_state.ai_log[:60]


def assign_nearest(call):
    if call["assigned"] is not None:
        return None
    free = [m for m in st.session_state.machines if m["status"] == STATUS_FREE]
    if not free:
        return None
    nearest = min(free, key=lambda m: gdist(m["lat"], m["lon"], call["lat"], call["lon"]))
    nearest["status"] = STATUS_ENROUTE
    nearest["call_id"] = call["id"]
    nearest["district"] = call["district"]
    nearest["last_ai"] = f"Назначена на вызов #{call['id']} ({call['district']})"
    call["assigned"] = nearest["id"]
    log_ai(
        f"Бригада #{nearest['id']} → вызов #{call['id']}",
        f"Ближайшая свободная бригада · {CATEGORIES[call['category']][0]} · {call['district']}",
    )
    return nearest


def spawn_call(initial=False):
    names = list(DISTRICTS.keys())
    weights = np.array([DISTRICTS[n]["base_calls"] for n in names], dtype=float)
    weights /= weights.sum()
    d = str(np.random.choice(names, p=weights))
    info = DISTRICTS[d]
    cat = int(np.random.choice([1, 2, 3, 4], p=[0.12, 0.23, 0.35, 0.30]))
    lat, lon = jitter(info["lat"], info["lon"], 0.010)
    st.session_state.call_seq += 1
    cid = st.session_state.call_seq
    addr = f"{np.random.choice(STREETS[d])}, {np.random.randint(1, 120)}"
    call = {
        "id": cid, "district": d, "category": cat, "lat": lat, "lon": lon,
        "address": addr, "assigned": None, "status": "active",
        "accepted": False, "created": datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state.calls.append(call)
    log_ai(f"Новый вызов #{cid} · {d}", f"Категория {cat} — {CATEGORIES[cat][0]}, {addr}")
    assign_nearest(call)
    if cat == 1:
        add_pending(
            f"cat1:{cid}", "Вызов категории 1 — угроза жизни",
            f"Поступил вызов #{cid} ({d}, {addr}) с угрозой жизни.",
            f"Назначить ближайшую свободную бригаду на вызов #{cid} в приоритетном порядке.",
            "priority", {"call_id": cid},
        )
    if len(st.session_state.calls) > 50:
        st.session_state.calls = st.session_state.calls[-50:]
    return call


def add_pending(key, title, situation, ai_decision, action_type, extra=None):
    now = time.time()
    muted = st.session_state.muted.get(key)
    if muted and now - muted < CALL_INTERVAL:
        return
    if any(p["key"] == key for p in st.session_state.pending_approval):
        return
    st.session_state.pending_approval.append({
        "key": key, "title": title, "situation": situation,
        "ai_decision": ai_decision, "type": action_type, "extra": extra or {},
    })
    log_ai(f"⏳ Запрос одобрения · {title}", situation)


def apply_decision(p):
    t = p["type"]
    if t == "reinforce":
        log_ai(f"✅ Усиление района {p['extra'].get('district', '')}",
               "Одобрено: 2 резервные бригады направлены в зону")
    elif t == "request_reserve":
        log_ai("✅ Запрос резерва одобрен", "Вызваны 3 бригады с соседней подстанции")
    elif t == "concentrate":
        log_ai("✅ Концентрация бригад",
               f"Свободные бригады стянуты в {', '.join(p['extra'].get('districts', []))}")
    elif t == "manual_mode":
        log_ai("✅ Ручной режим включён", "Текущая расстановка бригад зафиксирована")
    elif t == "priority":
        log_ai(f"✅ Приоритетный выезд по вызову #{p['extra'].get('call_id', '')}",
               "Одобрено: бригада следует в приоритетном режиме")
    else:
        log_ai(f"✅ Решение одобрено · {p['title']}", p["ai_decision"])


def resolve_pending(p, approved, manual_text=""):
    st.session_state.pending_approval = [
        x for x in st.session_state.pending_approval if x["key"] != p["key"]
    ]
    st.session_state.muted[p["key"]] = time.time()
    if approved:
        apply_decision(p)
    else:
        log_ai(f"✖ Отклонено · {p['title']}",
               f"Ручное решение диспетчера: {manual_text.strip() or 'без комментария'}")
    st.session_state.rejecting = None


def rebalance_patrol(predictions):
    free = [m for m in st.session_state.machines if m["status"] == STATUS_FREE]
    if not free:
        return
    ranked = sorted(DISTRICTS.keys(), key=lambda d: -predictions[d])
    slots = []
    for d in ranked:
        slots.extend([d] * max(1, ambulance_slots(predictions[d])))
    for idx, m in enumerate(free):
        target = slots[idx % len(slots)]
        if m["district"] != target:
            info = DISTRICTS[target]
            m["lat"], m["lon"] = jitter(info["lat"], info["lon"])
            m["district"] = target
            m["last_ai"] = f"Перенаправлена на патрулирование · {target}"
            log_ai(f"Бригада #{m['id']} → патруль {target}",
                   f"Зона риска: прогноз {predictions[target]:.0f} вызовов/час")


def ambulance_slots(calls):
    if calls <= 6:
        return 1
    if calls <= 14:
        return 2
    if calls <= 24:
        return 3
    return 4


def compute_confidence(predictions, anomaly_threshold):
    mx = max(predictions.values()) or 1
    red = sum(1 for d in DISTRICTS if predictions[d] / mx > 0.7)
    anom = sum(1 for d in DISTRICTS if predictions[d] > anomaly_threshold)
    conf = 0.93 - 0.07 * red - 0.06 * anom + np.random.uniform(-0.06, 0.03)
    return float(np.clip(conf, 0.45, 0.99))


def evaluate_criteria(predictions, anomaly_threshold, confidence):
    machines = st.session_state.machines
    free = [m for m in machines if m["status"] == STATUS_FREE]
    mx = max(predictions.values()) or 1
    red = [d for d in DISTRICTS if predictions[d] / mx > 0.7]

    for d in DISTRICTS:
        if predictions[d] > anomaly_threshold:
            add_pending(
                f"anomaly:{d}", f"Аномальная нагрузка · {d}",
                f"Прогноз {predictions[d]:.0f} вызовов/час в районе {d} превышает порог μ+2σ ({anomaly_threshold:.0f}).",
                f"Перевести 2 резервные бригады в район {d} и поднять статус готовности.",
                "reinforce", {"district": d},
            )

    if not free:
        add_pending(
            "all_busy", "Все бригады заняты",
            "Сейчас на линии нет ни одной свободной бригады.",
            "Запросить 3 резервные бригады с соседней подстанции.",
            "request_reserve",
        )

    if len(red) >= 2:
        key = "double_red:" + "|".join(sorted(red[:2]))
        add_pending(
            key, "Две зоны высокого риска",
            f"Районы {', '.join(red)} одновременно в красной зоне.",
            f"Сконцентрировать свободные бригады в {red[0]} и {red[1]}, придержать плановые выезды.",
            "concentrate", {"districts": red[:2]},
        )

    if confidence < 0.70:
        add_pending(
            "low_conf", "Низкая уверенность модели",
            f"Уверенность прогноза {confidence * 100:.0f}% — ниже порога 70%.",
            "Перейти на ручное распределение и удержать текущую расстановку бригад.",
            "manual_mode",
        )


def maybe_generate_call():
    if time.time() - st.session_state.last_call_gen >= CALL_INTERVAL:
        spawn_call()
        st.session_state.last_call_gen = time.time()


def assign_pending_calls():
    for c in active_calls():
        if c["assigned"] is None:
            assign_nearest(c)


def ai_step(model, anomaly_threshold):
    hour, dow, month, temp, ice, holiday = get_env()
    predictions = predict_for_districts(model, hour, dow, month, temp, ice, 0.0, 740, holiday, 0)
    st.session_state.confidence = compute_confidence(predictions, anomaly_threshold)
    maybe_generate_call()
    rebalance_patrol(predictions)
    assign_pending_calls()
    evaluate_criteria(predictions, anomaly_threshold, st.session_state.confidence)
    return predictions


def init_state():
    if st.session_state.get("ops_init"):
        return
    np.random.seed(7)
    names = list(DISTRICTS.keys())
    machines = []
    for i in range(1, MACHINE_COUNT + 1):
        d = names[(i - 1) % len(names)]
        info = DISTRICTS[d]
        lat, lon = jitter(info["lat"], info["lon"])
        machines.append({
            "id": i, "district": d, "status": STATUS_FREE,
            "lat": lat, "lon": lon, "call_id": None,
            "last_ai": "Патрулирование района",
        })
    st.session_state.machines = machines
    st.session_state.calls = []
    st.session_state.ai_log = []
    st.session_state.pending_approval = []
    st.session_state.muted = {}
    st.session_state.call_seq = 0
    st.session_state.last_call_gen = time.time()
    st.session_state.rejecting = None
    st.session_state.confidence = 0.9
    st.session_state.ops_init = True
    log_ai("Система запущена", "На линию заступила смена: 10 бригад")
    for _ in range(3):
        spawn_call(initial=True)


def base_map(center, zoom, T):
    m = folium.Map(location=center, zoom_start=zoom, tiles=None)
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/" + T["map_tiles"] + "/{z}/{x}/{y}{r}.png",
        attr="CartoDB", name=T["map_name"],
    ).add_to(m)
    return m


def build_dispatch_map(predictions, T):
    m = base_map([51.14, 71.42], 12, T)
    max_calls = max(predictions.values()) or 1

    heat_data = []
    for name, info in DISTRICTS.items():
        intensity = max(0.2, predictions[name] / max_calls)
        for _ in range(int(predictions[name] * 3) + 5):
            lat, lon = jitter(info["lat"], info["lon"], 0.013)
            heat_data.append([lat, lon, intensity])

    HeatMap(
        heat_data, radius=22, blur=18, max_zoom=13,
        gradient={"0.2": "#10b981", "0.4": "#34d399", "0.5": "#fbbf24",
                  "0.7": "#f97316", "0.85": "#ef4444", "1.0": "#dc2626"},
    ).add_to(m)

    for name, info in DISTRICTS.items():
        ratio = predictions[name] / max_calls
        color, level = risk_color(ratio)
        folium.CircleMarker(
            location=[info["lat"], info["lon"]], radius=10 + ratio * 16,
            color=color, fill=True, fill_color=color, fill_opacity=0.18, weight=2,
            popup=folium.Popup(
                f'<div style="font-family:Inter,sans-serif;background:{T["popup_bg"]};'
                f'color:{T["popup_text"]};padding:12px 16px;border-radius:12px;border:1px solid {color}55;">'
                f'<b style="color:{color};">{name}</b><br>'
                f'<span style="font-size:20px;font-weight:800;color:{T["popup_value"]};">{predictions[name]:.0f}</span>'
                f' вызовов/час<br><span style="font-size:11px;color:{T["popup_sub"]};">Риск: {level}</span></div>',
                max_width=220),
        ).add_to(m)
        folium.Marker(
            location=[info["lat"] + 0.022, info["lon"]],
            icon=folium.DivIcon(html=(
                f'<div style="font-family:Inter,sans-serif;font-size:11px;font-weight:700;'
                f'color:{T["label_color"]};text-align:center;text-shadow:0 1px 4px {T["label_shadow"]};'
                f'white-space:nowrap;">{name}</div>')),
        ).add_to(m)

    for c in active_calls():
        cat_name, cat_color = CATEGORIES[c["category"]]
        assigned = f"🚑 #{c['assigned']}" if c["assigned"] else "ожидает"
        folium.Marker(
            location=[c["lat"], c["lon"]],
            popup=folium.Popup(
                f'<div style="font-family:Inter,sans-serif;background:{T["popup_bg"]};'
                f'color:{T["popup_text"]};padding:12px 16px;border-radius:12px;border:1px solid {cat_color}66;">'
                f'<b style="color:{cat_color};">Вызов #{c["id"]} · Кат {c["category"]}</b><br>'
                f'{cat_name}<br><span style="font-size:12px;color:{T["popup_sub"]};">{c["district"]}, {c["address"]}</span>'
                f'<br>Бригада: {assigned}</div>', max_width=240),
            icon=folium.DivIcon(html=(
                f'<div style="font-size:18px;text-align:center;'
                f'text-shadow:0 1px 4px {T["label_shadow"]};">📞</div>')),
        ).add_to(m)

    for mac in st.session_state.machines:
        color = STATUS_COLOR[mac["status"]]
        folium.CircleMarker(
            location=[mac["lat"], mac["lon"]], radius=9, color=color,
            fill=True, fill_color=color, fill_opacity=0.9, weight=2,
            popup=folium.Popup(
                f'<div style="font-family:Inter,sans-serif;background:{T["popup_bg"]};'
                f'color:{T["popup_text"]};padding:12px 16px;border-radius:12px;border:1px solid {color}66;">'
                f'<b style="color:{color};">🚑 Бригада #{mac["id"]}</b><br>'
                f'{mac["district"]}<br><span style="font-size:12px;color:{T["popup_sub"]};">{mac["status"]}</span>'
                f'<br><span style="font-size:11px;color:{T["popup_sub"]};">{mac["last_ai"]}</span></div>',
                max_width=240),
        ).add_to(m)
        folium.Marker(
            location=[mac["lat"], mac["lon"]],
            icon=folium.DivIcon(html=(
                f'<div style="font-family:Inter,sans-serif;font-size:10px;font-weight:800;'
                f'color:#fff;text-align:center;width:18px;margin-top:-6px;">{mac["id"]}</div>')),
        ).add_to(m)

    return m


def build_route_map(start, end, T, line_color, start_emoji, end_emoji, end_color):
    m = base_map([(start[0] + end[0]) / 2, (start[1] + end[1]) / 2], 13, T)
    folium.PolyLine([start, end], color=line_color, weight=4, opacity=0.85, dash_array="10,6").add_to(m)
    folium.Marker(location=start, icon=folium.DivIcon(html=(
        f'<div style="font-size:22px;text-shadow:0 1px 4px {T["label_shadow"]};">{start_emoji}</div>'))).add_to(m)
    folium.CircleMarker(location=end, radius=10, color=end_color, fill=True,
                        fill_color=end_color, fill_opacity=0.6, weight=2).add_to(m)
    folium.Marker(location=end, icon=folium.DivIcon(html=(
        f'<div style="font-size:20px;text-shadow:0 1px 4px {T["label_shadow"]};">{end_emoji}</div>'))).add_to(m)
    m.fit_bounds([start, end], padding=(60, 60))
    return m


def render_metrics(predictions):
    c1, c2, c3, c4 = st.columns(4)
    active = len(active_calls())
    with c1:
        st.markdown("""
        <div class="metric-card metric-blue">
            <div class="icon">🚑</div>
            <div class="value">63 / 145</div>
            <div class="label">Машин на линии</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card metric-green">
            <div class="icon">📞</div>
            <div class="value">~1 900</div>
            <div class="label">Вызовов в сутки</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card metric-purple">
            <div class="icon">⏱️</div>
            <div class="value">9 мин</div>
            <div class="label">Время доезда (норма)</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card metric-red">
            <div class="icon">🔴</div>
            <div class="value">{active}</div>
            <div class="label">Активных вызовов сейчас</div>
        </div>""", unsafe_allow_html=True)


def render_approvals():
    pend = st.session_state.pending_approval
    if not pend:
        return
    st.markdown('<div class="section-title"><div class="bar"></div>🛑 Требуется решение диспетчера</div>',
                unsafe_allow_html=True)
    for p in list(pend):
        st.markdown(f"""
        <div class="appr-card">
            <h4>⚠️ {p['title']}</h4>
            <p class="sit">{p['situation']}</p>
            <p class="dec">Предложение AI: <b>{p['ai_decision']}</b></p>
        </div>""", unsafe_allow_html=True)
        b1, b2, _ = st.columns([1, 1, 2])
        if b1.button("✅ Одобрить", key=f"ap_{p['key']}"):
            resolve_pending(p, True)
            st.rerun()
        if b2.button("✖ Отклонить", key=f"rj_{p['key']}"):
            st.session_state.rejecting = p["key"]
            st.rerun()
        if st.session_state.rejecting == p["key"]:
            txt = st.text_input("Ваше решение (вручную):", key=f"mt_{p['key']}")
            if st.button("Подтвердить решение", key=f"cf_{p['key']}"):
                resolve_pending(p, False, txt)
                st.rerun()


def render_panel():
    tab_m, tab_c, tab_l = st.tabs(["🚑 Машины", "📞 Вызовы", "🤖 Лог AI"])

    with tab_m:
        rows = "".join(
            f"<tr><td><b>🚑 {m['id']}</b></td><td>{m['district']}</td>"
            f"<td>{status_badge(m['status'])}</td><td>{m['last_ai']}</td></tr>"
            for m in st.session_state.machines
        )
        st.markdown(
            '<table class="dist-table"><thead><tr><th>№</th><th>Район</th>'
            '<th>Статус</th><th>Действие AI</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>', unsafe_allow_html=True)

    with tab_c:
        calls = active_calls()
        if not calls:
            st.markdown('<div class="recommendation-card"><p>Нет активных вызовов.</p></div>',
                        unsafe_allow_html=True)
        else:
            rows = "".join(
                f"<tr><td><b>#{c['id']}</b></td><td>{c['district']}</td>"
                f"<td>{cat_badge(c['category'])}</td>"
                f"<td>{'🚑 #' + str(c['assigned']) if c['assigned'] else '—'}</td></tr>"
                for c in sorted(calls, key=lambda x: x["category"])
            )
            st.markdown(
                '<table class="dist-table"><thead><tr><th>№</th><th>Район</th>'
                '<th>Категория</th><th>Машина</th></tr></thead>'
                f'<tbody>{rows}</tbody></table>', unsafe_allow_html=True)

    with tab_l:
        items = "".join(
            f'<div class="log-item"><div class="t">{e["time"]}</div>'
            f'<div class="a">{e["action"]}</div><div class="r">{e["reason"]}</div></div>'
            for e in st.session_state.ai_log
        )
        st.markdown(f'<div class="log-list">{items}</div>', unsafe_allow_html=True)


def render_dispatcher(model, T, anomaly_threshold):
    st.markdown("""
    <div class="main-header">
        <h1>🧭 Панель диспетчера</h1>
        <p>Оперативное управление бригадами скорой помощи · Астана</p>
    </div>""", unsafe_allow_html=True)

    @st.fragment(run_every=REFRESH_SECONDS)
    def live():
        predictions = ai_step(model, anomaly_threshold)
        render_metrics(predictions)
        render_approvals()

        col_map, col_panel = st.columns([3, 2])
        with col_map:
            st.markdown('<div class="section-title"><div class="bar"></div>🗺️ Оперативная карта</div>',
                        unsafe_allow_html=True)
            st_folium(build_dispatch_map(predictions, T), width=None, height=560,
                      returned_objects=[], key="dispatch_map")
            st.caption(f"AI обновляет обстановку каждые {REFRESH_SECONDS} сек · "
                       f"уверенность модели {st.session_state.confidence * 100:.0f}%")
        with col_panel:
            st.markdown('<div class="section-title"><div class="bar"></div>🎛️ Панель управления</div>',
                        unsafe_allow_html=True)
            render_panel()

    live()


def render_driver(model, T, anomaly_threshold):
    sel = int(st.session_state.get("driver_machine", 1))

    st.markdown("""
    <div class="main-header">
        <h1>🚑 Кабина водителя</h1>
        <p>Задания от AI-диспетчера и навигация по маршруту</p>
    </div>""", unsafe_allow_html=True)

    @st.fragment(run_every=REFRESH_SECONDS)
    def live():
        ai_step(model, anomaly_threshold)
        machine = next(m for m in st.session_state.machines if m["id"] == sel)
        status = machine["status"]
        color = STATUS_COLOR[status]

        st.markdown(f"""
        <div class="status-block">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:0.78rem;color:var(--text-secondary);
                                text-transform:uppercase;letter-spacing:1px;">Бригада</div>
                    <div style="font-size:2.4rem;font-weight:800;color:{color};">🚑 {machine['id']}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.78rem;color:var(--text-secondary);">Район патрулирования</div>
                    <div style="font-size:1.25rem;font-weight:700;">{machine['district']}</div>
                    <div style="margin-top:10px;">{status_badge(status)}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        call = find_call(machine["call_id"]) if machine["call_id"] else None

        if call and call["status"] == "active":
            cat_name, cat_color = CATEGORIES[call["category"]]
            d = gdist(machine["lat"], machine["lon"], call["lat"], call["lon"])
            eta = eta_minutes(d)
            st.markdown('<div class="section-title"><div class="bar"></div>🚨 Активный вызов</div>',
                        unsafe_allow_html=True)
            st.markdown(f"""
            <div class="recommendation-card" style="border-color:{cat_color}55;">
                <h4 style="color:{cat_color};">Вызов #{call['id']} · {cat_name}</h4>
                <p>
                    Адрес: <b>{call['district']}, {call['address']}</b><br>
                    Категория: <b>{call['category']} — {cat_name}</b><br>
                    Расчётное время в пути: <b>{eta} мин</b>
                </p>
            </div>""", unsafe_allow_html=True)
            route = build_route_map(
                (machine["lat"], machine["lon"]), (call["lat"], call["lon"]),
                T, cat_color, "🚑", "📞", cat_color)
            st_folium(route, width=None, height=420, returned_objects=[], key="route_map")
        else:
            info = DISTRICTS[machine["district"]]
            target = (info["lat"] + 0.014, info["lon"] + 0.02)
            st.markdown('<div class="section-title"><div class="bar"></div>🧭 Задание</div>',
                        unsafe_allow_html=True)
            st.markdown(f"""
            <div class="recommendation-card">
                <h4>Патрулировать район {machine['district']}</h4>
                <p>
                    Свободный статус — следуйте по маршруту патрулирования.<br>
                    Последнее указание AI: <b>{machine['last_ai']}</b>
                </p>
            </div>""", unsafe_allow_html=True)
            route = build_route_map(
                (machine["lat"], machine["lon"]), target,
                T, "#f59e0b", "🚑", "📍", "#f59e0b")
            st_folium(route, width=None, height=420, returned_objects=[], key="route_map")

        st.markdown('<div class="section-title"><div class="bar"></div>🎮 Действия</div>',
                    unsafe_allow_html=True)
        a, b, cc = st.columns(3)
        accept = a.button("📞 Принять вызов", disabled=(status != STATUS_ENROUTE))
        onsite = b.button("📍 На месте", disabled=(status != STATUS_ENROUTE))
        done = cc.button("✅ Вызов завершён", disabled=(status not in (STATUS_ENROUTE, STATUS_ONSCENE)))

        if accept and call:
            call["accepted"] = True
            machine["last_ai"] = f"Приняла вызов #{call['id']}"
            log_ai(f"Бригада #{machine['id']} приняла вызов #{call['id']}", "Подтверждение водителя")
            st.rerun()
        if onsite and call:
            machine["status"] = STATUS_ONSCENE
            machine["last_ai"] = f"На месте · вызов #{call['id']}"
            log_ai(f"Бригада #{machine['id']} на месте", f"Вызов #{call['id']} · {call['district']}")
            st.rerun()
        if done and call:
            call["status"] = "resolved"
            machine["status"] = STATUS_FREE
            machine["call_id"] = None
            machine["last_ai"] = "Вызов завершён · патрулирование"
            info = DISTRICTS[machine["district"]]
            machine["lat"], machine["lon"] = jitter(info["lat"], info["lon"])
            log_ai(f"Бригада #{machine['id']} завершила вызов #{call['id']}",
                   "Бригада снова на линии")
            st.rerun()

        if status == STATUS_FREE:
            st.caption("Нет активного вызова — патрулирование района. Ожидайте назначение AI.")

    live()


def main():
    theme_name = "Тёмная" if st.session_state.get("dark_theme", False) else "Светлая"
    T = THEMES[theme_name]
    apply_theme(T)

    df = generate_dataset()
    model, _, _ = train_model(df)
    anomaly_threshold = float(df["calls"].mean() + 2 * df["calls"].std())

    init_state()

    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:16px 0 8px 0;">
            <div style="font-size:2.5rem;">🚑</div>
            <div style="font-size:1.1rem;font-weight:700;
                        background:{T['title_grad']};
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                AI Скорая · Астана
            </div>
            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:2px;">
                Операционная система диспетчеризации
            </div>
        </div>""", unsafe_allow_html=True)

        st.toggle("🌙 Тёмная тема", key="dark_theme")
        st.markdown("---")

        st.markdown('<div class="sidebar-label">🖥️ Рабочее место</div>', unsafe_allow_html=True)
        page = st.radio("Панель", ["🧭 Диспетчер", "🚑 Водитель"], key="page", label_visibility="collapsed")

        if page == "🚑 Водитель":
            st.markdown('<div class="sidebar-label">🚑 Моя бригада</div>', unsafe_allow_html=True)
            st.selectbox("Номер машины", list(range(1, MACHINE_COUNT + 1)), key="driver_machine")

        st.markdown("---")
        st.markdown('<div class="sidebar-label">🌡️ Условия среды</div>', unsafe_allow_html=True)
        _, _, _, base_temp = current_context()
        st.slider("Температура (°C)", -42, 42, int(base_temp), key="env_temp")
        st.checkbox("Гололёд", value=base_temp < -5, key="env_ice")

        st.markdown("---")
        if st.button("⟳ Обновить сейчас"):
            st.rerun()
        st.caption(f"AI-цикл: {REFRESH_SECONDS} сек · новый вызов раз в {CALL_INTERVAL // 60} мин")

    if page == "🧭 Диспетчер":
        render_dispatcher(model, T, anomaly_threshold)
    else:
        render_driver(model, T, anomaly_threshold)


if __name__ == "__main__":
    main()
ings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AI Диспетчер — Астана",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a1f36;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-emerald: #10b981;
    --accent-red: #ef4444;
    --accent-amber: #f59e0b;
    --accent-purple: #8b5cf6;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border-color: #1e293b;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1629 0%, #1a1040 100%) !important;
    border-right: 1px solid rgba(59, 130, 246, 0.15) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

.main-header {
    background: linear-gradient(135deg, rgba(59,130,246,0.12) 0%, rgba(6,182,212,0.08) 50%, rgba(139,92,246,0.12) 100%);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 20px;
    padding: 32px 40px;
    margin-bottom: 28px;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(59,130,246,0.06) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(139,92,246,0.06) 0%, transparent 50%);
    animation: pulse-bg 8s ease-in-out infinite;
}

@keyframes pulse-bg {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}

.main-header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    position: relative;
    z-index: 1;
}

.main-header p {
    color: var(--text-secondary);
    font-size: 1rem;
    margin-top: 6px;
    position: relative;
    z-index: 1;
}

.metric-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, rgba(30,41,59,0.8) 100%);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(59,130,246,0.3);
    box-shadow: 0 12px 40px rgba(59,130,246,0.1);
}

.metric-card .icon { font-size: 2rem; margin-bottom: 8px; }
.metric-card .value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-card .label {
    color: var(--text-secondary);
    font-size: 0.85rem;
    font-weight: 500;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-blue::after { background: linear-gradient(90deg, #3b82f6, #06b6d4); }
.metric-green::after { background: linear-gradient(90deg, #10b981, #34d399); }
.metric-red::after { background: linear-gradient(90deg, #ef4444, #f97316); }
.metric-purple::after { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }

.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title .bar {
    width: 4px;
    height: 24px;
    background: linear-gradient(180deg, #3b82f6, #8b5cf6);
    border-radius: 2px;
}

.risk-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.82rem;
    letter-spacing: 0.3px;
}

.risk-high {
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.3);
}
.risk-medium {
    background: rgba(245,158,11,0.15);
    color: #fbbf24;
    border: 1px solid rgba(245,158,11,0.3);
}
.risk-low {
    background: rgba(16,185,129,0.15);
    color: #34d399;
    border: 1px solid rgba(16,185,129,0.3);
}

.recommendation-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.08) 0%, rgba(139,92,246,0.08) 100%);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 16px;
    padding: 24px;
    margin: 8px 0;
}

.recommendation-card h4 {
    color: #60a5fa;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.recommendation-card p {
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.6;
}

.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
}

div[data-testid="stDataFrame"] > div {
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

.sidebar-section {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}

.sidebar-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 8px;
}

[data-testid="stSlider"] label,
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stCheckbox"] label {
    font-weight: 500 !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(59,130,246,0.3) !important;
}

.ambulance-count {
    font-size: 1.8rem;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

DISTRICTS = {
    "Есиль": {"lat": 51.145, "lon": 71.470, "elderly_ratio": 0.12, "base_calls": 8},
    "Алматы р-н": {"lat": 51.100, "lon": 71.430, "elderly_ratio": 0.22, "base_calls": 12},
    "Сарыарка": {"lat": 51.160, "lon": 71.410, "elderly_ratio": 0.18, "base_calls": 10},
    "Байконур": {"lat": 51.120, "lon": 71.380, "elderly_ratio": 0.20, "base_calls": 9},
    "Нура": {"lat": 51.180, "lon": 71.350, "elderly_ratio": 0.15, "base_calls": 7},
}

HOLIDAYS = [
    "Нет", "Наурыз", "День Республики", "День Независимости",
    "День Конституции", "День Первого Президента", "Новый Год"
]

HOLIDAY_DATES = {
    "Наурыз": [(3, 21), (3, 22), (3, 23)],
    "День Республики": [(10, 25)],
    "День Независимости": [(12, 16), (12, 17)],
    "День Конституции": [(8, 30)],
    "День Первого Президента": [(12, 1)],
    "Новый Год": [(1, 1), (1, 2)],
}


@st.cache_data
def generate_dataset(n=50000):
    np.random.seed(42)
    records = []

    district_names = list(DISTRICTS.keys())

    for _ in range(n):
        hour = np.random.randint(0, 24)
        dow = np.random.randint(0, 7)
        month = np.random.randint(1, 13)
        district = np.random.choice(district_names)
        info = DISTRICTS[district]

        if month in [12, 1, 2]:
            temp = np.random.normal(-18, 10)
        elif month in [3, 4, 5]:
            temp = np.random.normal(5, 8)
        elif month in [6, 7, 8]:
            temp = np.random.normal(28, 5)
        else:
            temp = np.random.normal(8, 7)
        temp = np.clip(temp, -42, 42)

        ice = 1 if (temp < -5 and np.random.random() < 0.4) else 0
        precip = np.random.exponential(2) if np.random.random() < 0.3 else 0.0
        pressure = np.random.normal(740, 10)

        day_of_month = np.random.randint(1, 29)
        holiday = "Нет"
        for h_name, dates in HOLIDAY_DATES.items():
            for m, d in dates:
                if month == m and day_of_month == d:
                    holiday = h_name
                    break

        event = 1 if np.random.random() < 0.08 else 0
        elderly = info["elderly_ratio"]

        calls = info["base_calls"]

        if 7 <= hour <= 9:
            calls *= 1.3
        elif 17 <= hour <= 20:
            calls *= 1.5
        elif 0 <= hour <= 5:
            calls *= 0.5

        if dow == 4 and 18 <= hour <= 23:
            calls *= 1.6
        if dow in [5, 6]:
            calls *= 1.2

        if temp < -25:
            calls *= 1.7
        elif temp < -15:
            calls *= 1.3

        if ice:
            calls *= 1.4
        if precip > 5:
            calls *= 1.2

        if holiday == "Наурыз" and district == "Есиль":
            calls *= 2.2
        elif holiday == "Наурыз":
            calls *= 1.5
        elif holiday != "Нет":
            calls *= 1.4

        if event:
            calls *= 1.5

        calls *= (1 + elderly * 2)

        calls += np.random.normal(0, calls * 0.15)
        calls = max(0, int(round(calls)))

        records.append({
            "hour": hour,
            "day_of_week": dow,
            "month": month,
            "district": district,
            "temperature": round(temp, 1),
            "ice": ice,
            "precipitation": round(precip, 1),
            "pressure": round(pressure, 1),
            "holiday": holiday,
            "event": event,
            "elderly_ratio": elderly,
            "calls": calls,
        })

    return pd.DataFrame(records)


@st.cache_resource
def train_model(df):
    cat_cols = ["district", "day_of_week", "month", "holiday"]
    for c in cat_cols:
        df[c] = df[c].astype("category")

    features = [
        "hour", "day_of_week", "month", "district",
        "temperature", "ice", "precipitation", "pressure",
        "holiday", "event", "elderly_ratio"
    ]

    X = df[features]
    y = df["calls"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = lgb.LGBMRegressor(
        num_leaves=64,
        learning_rate=0.05,
        n_estimators=500,
        categorical_feature=["district", "day_of_week", "month", "holiday"],
        verbose=-1,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    importance = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)

    return model, mae, rmse, y_test.values, y_pred, importance


def predict_for_districts(model, hour, dow, month, temp, ice, precip, pressure, holiday, event):
    rows = []
    for name, info in DISTRICTS.items():
        rows.append({
            "hour": hour,
            "day_of_week": dow,
            "month": month,
            "district": name,
            "temperature": temp,
            "ice": ice,
            "precipitation": precip,
            "pressure": pressure,
            "holiday": holiday,
            "event": event,
            "elderly_ratio": info["elderly_ratio"],
        })
    pred_df = pd.DataFrame(rows)
    cat_cols = ["district", "day_of_week", "month", "holiday"]
    for c in cat_cols:
        pred_df[c] = pred_df[c].astype("category")

    preds = model.predict(pred_df)
    preds = np.clip(preds, 0, None)
    return {name: round(p, 1) for name, p in zip(DISTRICTS.keys(), preds)}


def build_map(predictions):
    m = folium.Map(location=[51.14, 71.42], zoom_start=12, tiles=None)

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="CartoDB",
        name="Dark",
    ).add_to(m)

    max_calls = max(predictions.values()) if max(predictions.values()) > 0 else 1

    heat_data = []
    for name, info in DISTRICTS.items():
        calls = predictions[name]
        ratio = calls / max_calls
        intensity = max(0.2, ratio)

        for _ in range(int(calls * 3) + 5):
            lat = info["lat"] + np.random.normal(0, 0.012)
            lon = info["lon"] + np.random.normal(0, 0.015)
            heat_data.append([lat, lon, intensity])

    HeatMap(
        heat_data,
        radius=22,
        blur=18,
        max_zoom=13,
        gradient={
            "0.2": "#10b981",
            "0.4": "#34d399",
            "0.5": "#fbbf24",
            "0.7": "#f97316",
            "0.85": "#ef4444",
            "1.0": "#dc2626",
        },
    ).add_to(m)

    for name, info in DISTRICTS.items():
        calls = predictions[name]
        ratio = calls / max_calls

        if ratio > 0.7:
            color = "#ef4444"
            level = "ВЫСОКИЙ"
        elif ratio > 0.4:
            color = "#f59e0b"
            level = "СРЕДНИЙ"
        else:
            color = "#10b981"
            level = "НИЗКИЙ"

        popup_html = f"""
        <div style="font-family:Inter,sans-serif;background:#1a1f36;color:#f1f5f9;
                     padding:14px 18px;border-radius:12px;min-width:180px;
                     border:1px solid {color}40;">
            <div style="font-weight:700;font-size:14px;color:{color};margin-bottom:6px;">
                {name}
            </div>
            <div style="font-size:22px;font-weight:800;color:#fff;">
                {calls} вызовов
            </div>
            <div style="font-size:11px;color:#94a3b8;margin-top:4px;">
                Риск: {level}
            </div>
        </div>
        """

        folium.CircleMarker(
            location=[info["lat"], info["lon"]],
            radius=12 + ratio * 18,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.35,
            weight=2,
            popup=folium.Popup(popup_html, max_width=220),
        ).add_to(m)

        folium.Marker(
            location=[info["lat"], info["lon"]],
            icon=folium.DivIcon(html=f"""
                <div style="font-family:Inter,sans-serif;font-size:11px;font-weight:700;
                            color:#fff;text-align:center;text-shadow:0 1px 4px rgba(0,0,0,0.8);
                            white-space:nowrap;">
                    {name}
                </div>
            """),
        ).add_to(m)

    return m


def ambulance_recommendation(calls):
    if calls <= 5:
        return 1
    elif calls <= 10:
        return 2
    elif calls <= 18:
        return 3
    elif calls <= 28:
        return 5
    else:
        return 7


def main():
    df = generate_dataset()
    model, mae, rmse, y_test, y_pred, importance = train_model(df)

    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:16px 0 8px 0;">
            <div style="font-size:2.5rem;">🚑</div>
            <div style="font-size:1.1rem;font-weight:700;
                        background:linear-gradient(135deg,#60a5fa,#a78bfa);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                AI Диспетчер
            </div>
            <div style="font-size:0.75rem;color:#64748b;margin-top:2px;">
                Астана · Управление скорой помощью
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown('<div class="sidebar-label">⏰ Время</div>', unsafe_allow_html=True)
        hour = st.slider("Час", 0, 23, 14)
        dow = st.selectbox("День недели", list(range(7)),
                           format_func=lambda x: ["Пн","Вт","Ср","Чт","Пт","Сб","Вс"][x], index=4)
        month = st.selectbox("Месяц", list(range(1, 13)),
                             format_func=lambda x: ["Янв","Фев","Мар","Апр","Май","Июн",
                                                    "Июл","Авг","Сен","Окт","Ноя","Дек"][x-1], index=0)

        st.markdown("---")
        st.markdown('<div class="sidebar-label">🌡️ Погода</div>', unsafe_allow_html=True)
        temp = st.slider("Температура (°C)", -42, 42, -10)
        ice = st.checkbox("Гололёд")
        precip = st.slider("Осадки (мм)", 0.0, 20.0, 0.0, step=0.5)
        pressure = st.slider("Давление (мм рт.ст.)", 710, 770, 740)

        st.markdown("---")
        st.markdown('<div class="sidebar-label">🎉 События</div>', unsafe_allow_html=True)
        holiday = st.selectbox("Праздник", HOLIDAYS)
        event = st.checkbox("Крупное событие в районе")

    st.markdown("""
    <div class="main-header">
        <h1>🚑 AI Диспетчер скорой помощи</h1>
        <p>Прогнозирование нагрузки и оптимальное распределение бригад по районам Астаны</p>
    </div>
    """, unsafe_allow_html=True)

    predictions = predict_for_districts(
        model, hour, dow, month, temp, int(ice), precip, pressure, holiday, int(event)
    )

    total_calls = sum(predictions.values())
    total_ambulances = sum(ambulance_recommendation(c) for c in predictions.values())
    max_district = max(predictions, key=predictions.get)
    max_calls = predictions[max_district]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card metric-blue">
            <div class="icon">📊</div>
            <div class="value">{total_calls:.0f}</div>
            <div class="label">Прогноз вызовов</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card metric-green">
            <div class="icon">🚑</div>
            <div class="value">{total_ambulances}</div>
            <div class="label">Бригад требуется</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card metric-red">
            <div class="icon">⚠️</div>
            <div class="value">{max_district}</div>
            <div class="label">Макс. нагрузка</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card metric-purple">
            <div class="icon">🎯</div>
            <div class="value">{max_calls:.0f}</div>
            <div class="label">Вызовов в пике</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
        <div class="bar"></div>
        🗺️ Карта риска — Астана
    </div>
    """, unsafe_allow_html=True)

    m = build_map(predictions)
    st_folium(m, width=None, height=520, returned_objects=[])

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("""
        <div class="section-title">
            <div class="bar"></div>
            📋 Распределение бригад по районам
        </div>
        """, unsafe_allow_html=True)

        table_data = []
        for name, calls in sorted(predictions.items(), key=lambda x: -x[1]):
            amb = ambulance_recommendation(calls)
            ratio = calls / max_calls if max_calls > 0 else 0
            if ratio > 0.7:
                risk = "🔴 Высокий"
            elif ratio > 0.4:
                risk = "🟡 Средний"
            else:
                risk = "🟢 Низкий"
            table_data.append({
                "Район": name,
                "Прогноз вызовов": calls,
                "Уровень риска": risk,
                "Бригад": amb,
            })

        st.dataframe(
            pd.DataFrame(table_data),
            use_container_width=True,
            hide_index=True,
            height=240,
        )

    with col_right:
        st.markdown("""
        <div class="section-title">
            <div class="bar"></div>
            💡 Рекомендация дня
        </div>
        """, unsafe_allow_html=True)

        sorted_districts = sorted(predictions.items(), key=lambda x: -x[1])
        top2 = sorted_districts[:2]

        for rank, (name, calls) in enumerate(top2, 1):
            amb = ambulance_recommendation(calls)
            emoji = "🥇" if rank == 1 else "🥈"
            st.markdown(f"""
            <div class="recommendation-card">
                <h4>{emoji} {name}</h4>
                <p>
                    Прогноз: <b>{calls:.0f}</b> вызовов/час<br>
                    Рекомендуется направить <b>{amb}</b> бригад заранее<br>
                    Доля пожилых: <b>{DISTRICTS[name]['elderly_ratio']*100:.0f}%</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        if len(sorted_districts) >= 3:
            least = sorted_districts[-1]
            st.markdown(f"""
            <div class="recommendation-card" style="border-color:rgba(16,185,129,0.3);">
                <h4 style="color:#34d399;">♻️ Перераспределение</h4>
                <p>
                    Район <b>{least[0]}</b> имеет минимальную нагрузку ({least[1]:.0f} вызовов).
                    Перенаправьте свободные бригады в <b>{top2[0][0]}</b> и <b>{top2[1][0]}</b>.
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
        <div class="bar"></div>
        📈 Метрики модели
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="metric-card metric-blue">
            <div class="icon">📏</div>
            <div class="value">{mae:.2f}</div>
            <div class="label">MAE</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card metric-green">
            <div class="icon">📐</div>
            <div class="value">{rmse:.2f}</div>
            <div class="label">RMSE</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card metric-purple">
            <div class="icon">🧠</div>
            <div class="value">50 000</div>
            <div class="label">Обучающих записей</div>
        </div>""", unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("""
        <div class="section-title">
            <div class="bar"></div>
            🎯 Реальные vs Предсказанные
        </div>
        """, unsafe_allow_html=True)

        sample_idx = np.random.RandomState(42).choice(len(y_test), size=min(500, len(y_test)), replace=False)
        sample_idx = np.sort(sample_idx)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(sample_idx))),
            y=y_test[sample_idx],
            mode="lines",
            name="Реальные",
            line=dict(color="#3b82f6", width=1.5),
            opacity=0.7,
        ))
        fig.add_trace(go.Scatter(
            x=list(range(len(sample_idx))),
            y=y_pred[sample_idx],
            mode="lines",
            name="Предсказанные",
            line=dict(color="#f59e0b", width=1.5),
            opacity=0.7,
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=40, r=20, t=30, b=40),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=12)
            ),
            xaxis=dict(title="Наблюдение", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="Вызовы", gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.markdown("""
        <div class="section-title">
            <div class="bar"></div>
            🏆 Feature Importance
        </div>
        """, unsafe_allow_html=True)

        fig2 = go.Figure()
        imp = importance.sort_values("importance", ascending=True)

        colors = px.colors.sequential.Viridis
        n = len(imp)
        bar_colors = [colors[int(i / n * (len(colors) - 1))] for i in range(n)]

        fig2.add_trace(go.Bar(
            y=imp["feature"],
            x=imp["importance"],
            orientation="h",
            marker=dict(
                color=bar_colors,
                line=dict(width=0),
            ),
        ))
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=100, r=20, t=30, b=40),
            xaxis=dict(title="Важность", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div style="text-align:center;padding:32px 0 16px 0;color:#475569;font-size:0.8rem;">
        AI Диспетчер v1.0 · Астана · Разработано для хакатона SmartScape
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
