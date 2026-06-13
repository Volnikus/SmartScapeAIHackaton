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
import warnings
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
