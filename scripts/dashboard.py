# streamlit_app.py


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="Dashboard - Colegios", initial_sidebar_state="expanded")

# ----------------------
# Parámetros y mapeos
# ----------------------
PRINCIPAL_TOTAL = 10_027_254
SAMPLE_10P = 1_002_725

school_counts_raw = {
    "El Alto (Municipio)": 524,
    "La Paz (Departamento)": 4230,
    "Cochabamba": 3700,
    "Santa Cruz": 3400,
    "Potosí": 1500,
    "Chuquisaca": 1050,
    "Oruro": 850,
    "Tarija": 800,
    "Beni": 700,
    "Pando": 250
}

la_paz_combined = school_counts_raw.get("La Paz (Departamento)", 0) + school_counts_raw.get("El Alto (Municipio)", 0)
school_counts_combined = {
    "La Paz (incl. El Alto)": la_paz_combined,
    "Cochabamba": school_counts_raw.get("Cochabamba", 0),
    "Santa Cruz": school_counts_raw.get("Santa Cruz", 0),
    "Potosí": school_counts_raw.get("Potosí", 0),
    "Chuquisaca": school_counts_raw.get("Chuquisaca", 0),
    "Oruro": school_counts_raw.get("Oruro", 0),
    "Tarija": school_counts_raw.get("Tarija", 0),
    "Beni": school_counts_raw.get("Beni", 0),
    "Pando": school_counts_raw.get("Pando", 0)
}

DEPT_MAP = {
    2.0: "La Paz (incl. El Alto)",
    6.0: "La Paz (incl. El Alto)",
    3.0: "Cochabamba",
    7.0: "Santa Cruz",
    5.0: "Potosí",
    1.0: "Chuquisaca",
    4.0: "Oruro",
    8.0: "Tarija",
    9.0: "Beni",
    10.0: "Pando"
}

SEX_MAP = {1.0: "Femenino", 1: "Femenino", 2.0: "Masculino", 2: "Masculino"}

EDLEV_MAP = {
    3.0: "Inicial (Pre-kínder / Kínder)",
    4.0: "Básico (1-5 años sistema anterior)",
    5.0: "Intermedio (6-8 años sistema anterior)",
    6.0: "Medio (9-12 años sistema anterior)",
    7.0: "Primaria (1-8 años sistema anterior)",
    8.0: "Secundaria (9-12 años sistema anterior)",
    9.0: "Primaria actual (1-6 años)",
    10.0: "Secundaria actual (7-12 años)"
}

AGE_GROUPS = [
    ("Primera infancia (0-5)", 0, 5),
    ("Niños y niñas (6-11)", 6, 11),
    ("Adolescentes (12-17)", 12, 17),
    ("Jóvenes (18)", 18, 18)
]

# ----------------------
# Paletas y mapas de color (consistentes)
# ----------------------
DEPT_PALETTE = px.colors.qualitative.Set3
AGE_PALETTE = px.colors.qualitative.Pastel1
LEVEL_PALETTE = px.colors.qualitative.Safe
SEX_COLOR_MAP = {"Femenino": "#FF6EA1", "Masculino": "#3B82F6", "Desconocido": "#9CA3AF"}
TREE_PALETTE = px.colors.qualitative.Prism

# ----------------------
# Lectura y preparación
# ----------------------
@st.cache_data(ttl=300)
def load_and_prepare(path="ColegiosFinal.csv"):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    expected_cols = ["BO2012A_SCHOOL", "BO2012A_AGE", "BO2012A_SEX", "BO2012A_EDLEV", "BO2012A_RESDEPT"]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise FileNotFoundError(f"Columnas faltantes en el CSV: {missing}.")

    df["BO2012A_AGE"] = pd.to_numeric(df["BO2012A_AGE"], errors="coerce")
    df["BO2012A_SEX"] = pd.to_numeric(df["BO2012A_SEX"], errors="coerce")
    df["BO2012A_EDLEV"] = pd.to_numeric(df["BO2012A_EDLEV"], errors="coerce")
    df["BO2012A_RESDEPT"] = pd.to_numeric(df["BO2012A_RESDEPT"], errors="coerce")

    df["department"] = df["BO2012A_RESDEPT"].map(DEPT_MAP).fillna("Desconocido")
    df["sexo"] = df["BO2012A_SEX"].map(SEX_MAP).fillna("Desconocido")
    df["nivel_educativo"] = df["BO2012A_EDLEV"].map(EDLEV_MAP).fillna("Desconocido")

    def age_group_label(age):
        try:
            age = float(age)
        except Exception:
            return "Desconocido"
        for label, low, high in AGE_GROUPS:
            if low <= age <= high:
                return label
        return "Fuera de rango"

    df["grupo_edad"] = df["BO2012A_AGE"].apply(age_group_label)

    df["department"] = df["department"].fillna("Desconocido")
    df["sexo"] = df["sexo"].fillna("Desconocido")
    df["nivel_educativo"] = df["nivel_educativo"].fillna("Desconocido")

    return df

# small helper: compute avg students per school by department 
def compute_avg_students_per_school(df_counts, schools_map):
    df = df_counts.copy()
    df["schools"] = df["department"].map(schools_map).fillna(0).astype(int)
    df["avg_per_school"] = df.apply(lambda r: (r["students"] / r["schools"]) if r["schools"] > 0 else np.nan, axis=1)
    return df

# For top/bottom per age group
def top_bottom_avg_by_age(df, schools_map, top_n=3):
    # df: full dataframe with 'department' and 'grupo_edad'
    groups = sorted(df["grupo_edad"].unique())
    top_list = []
    bottom_list = []
    for g in groups:
        tmp = df[df["grupo_edad"] == g].groupby("department").size().rename("students").reset_index()
        tmp = compute_avg_students_per_school(tmp, schools_map)
        tmp_sorted = tmp.sort_values("avg_per_school", ascending=False).reset_index(drop=True)
        # top N
        top = tmp_sorted.head(top_n).copy()
        top["grupo_edad"] = g
        top_list.append(top)
        # bottom N: ignore NaN avg (departamentos with 0 schools or NaN)
        bottom = tmp_sorted[tmp_sorted["avg_per_school"].notna()].tail(top_n).copy()
        bottom["grupo_edad"] = g
        bottom_list.append(bottom)
    top_df = pd.concat(top_list, ignore_index=True)
    bottom_df = pd.concat(bottom_list, ignore_index=True)
    return top_df, bottom_df

# prepare df scaled approx 100% (multiply counts by 10)
def simulate_100pct(df):
    # Multiply counts by 10 to approximate 100% from 10% sample
    df100 = df.copy()
    # We will use aggregated counts for charts, so multiply when aggregating
    return df100

# ----------------------
# UI - Title / Load
# ----------------------
st.markdown("<h1 style='text-align:left; color:#073763; font-size:30px; margin-bottom:0.2rem;'>📊 Analisis de datos censales para poblacion en colegios", unsafe_allow_html=True)


try:
    df = load_and_prepare("ColegiosFinal.csv")
except Exception as e:
    st.error(f"Error cargando/parseando el CSV: {e}")
    st.stop()

# ----------------------
# Sidebar filters
# ----------------------
st.sidebar.header("Filtros interactivos")
total_filtered = len(df)

dept_options = sorted(df["department"].unique())
sel_depts = st.sidebar.multiselect("Departamentos", dept_options, default=dept_options)

min_age = int(df["BO2012A_AGE"].min(skipna=True)) if not df["BO2012A_AGE"].isna().all() else 5
max_age = int(df["BO2012A_AGE"].max(skipna=True)) if not df["BO2012A_AGE"].isna().all() else 18
age_range = st.sidebar.slider("Rango de edad", min_value=min_age, max_value=max_age, value=(min_age, max_age))

sex_filter = st.sidebar.multiselect("Sexo", options=df["sexo"].unique(), default=list(df["sexo"].unique()))
nivel_filter = st.sidebar.multiselect("Nivel educativo", options=df["nivel_educativo"].unique(), default=list(df["nivel_educativo"].unique()))

df_filtered = df[
    (df["department"].isin(sel_depts)) &
    (df["sexo"].isin(sex_filter)) &
    (df["nivel_educativo"].isin(nivel_filter)) &
    (df["BO2012A_AGE"].between(age_range[0], age_range[1]))
].copy()

# ----------------------
# KPIs
# ----------------------
k1, k2, k3 = st.columns(3)
k1.markdown("<div style='text-align:left'><span style='font-size:13px; color:#475569'>Total dataset principal</span><br><b style='font-size:18px; color:#0b5ed7'>{:,}</b></div>".format(PRINCIPAL_TOTAL), unsafe_allow_html=True)
k2.markdown("<div style='text-align:left'><span style='font-size:13px; color:#475569'>10% del dataset (muestra)</span><br><b style='font-size:18px; color:#0b5ed7'>{:,}</b></div>".format(SAMPLE_10P), unsafe_allow_html=True)
k3.markdown("<div style='text-align:left'><span style='font-size:13px; color:#475569'>Total (ColegiosFinal.csv)</span><br><b style='font-size:18px; color:#0b5ed7'>{:,}</b></div>".format(total_filtered), unsafe_allow_html=True)

st.markdown("---")

# ----------------------
# Aggregations (base)
# ----------------------
dept_counts = df.groupby("department").size().rename("students").reset_index()
for d in school_counts_combined.keys():
    if d not in dept_counts["department"].values:
        dept_counts = pd.concat([dept_counts, pd.DataFrame([{"department": d, "students": 0}])], ignore_index=True)

sex_counts = df.groupby("sexo").size().rename("students").reset_index().sort_values("students", ascending=False)
age_group_counts = df.groupby("grupo_edad").size().rename("students").reset_index().sort_values("students", ascending=False)
nivel_counts = df.groupby("nivel_educativo").size().rename("students").reset_index().sort_values("students", ascending=False)

# ----------------------
# Principal charts (unchanged styling)
# ----------------------
st.markdown("<h2 style='color:#0b5ed7; margin-top:0.3rem;'>Visión general y comparativas</h2>", unsafe_allow_html=True)
col1, col2 = st.columns((2, 1))

with col1:
    st.markdown("<h3 style='color:#073763; margin-bottom:0.1rem;'>📍 Estudiantes por departamento</h3>", unsafe_allow_html=True)
    fig_dept = px.bar(
        dept_counts.sort_values("students", ascending=False),
        x="department",
        y="students",
        color="department",
        color_discrete_sequence=DEPT_PALETTE,
        labels={"students": "Total estudiantes", "department": "Departamento"},
    )
    fig_dept.update_layout(showlegend=False, template="simple_white", title=dict(text="Total de estudiantes por departamento", x=0.5, font=dict(size=18, color="#073763")), xaxis_tickangle=-45, font=dict(size=12))
    fig_dept.update_traces(marker_line_width=0.4)
    st.plotly_chart(fig_dept, use_container_width=True)

    st.markdown("<h3 style='color:#073763; margin-bottom:0.1rem;'>👥 Distribución por sexo</h3>", unsafe_allow_html=True)
    fig_sex = px.pie(sex_counts, names="sexo", values="students", title="Distribución por sexo (total)", color_discrete_map=SEX_COLOR_MAP)
    fig_sex.update_layout(title=dict(x=0.5, font=dict(size=16, color="#073763")), legend=dict(font=dict(size=12)))
    st.plotly_chart(fig_sex, use_container_width=True)

    st.markdown("<h3 style='color:#073763; margin-bottom:0.1rem;'>🧒 Distribución por grupo de edad</h3>", unsafe_allow_html=True)
    fig_age = px.bar(age_group_counts, x="grupo_edad", y="students", color="grupo_edad", color_discrete_sequence=AGE_PALETTE, labels={"students": "Total estudiantes", "grupo_edad": "Grupo etario"})
    fig_age.update_layout(title=dict(text="Total por grupo de edad", x=0.5, font=dict(size=16, color="#073763")), showlegend=False)
    fig_age.update_xaxes(tickangle=-10)
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.markdown("<h3 style='color:#073763; margin-bottom:0.1rem;'>🏫 Estudiantes por nivel educativo</h3>", unsafe_allow_html=True)
    fig_nivel = px.bar(nivel_counts, x="students", y="nivel_educativo", orientation="h", color="nivel_educativo", color_discrete_sequence=LEVEL_PALETTE, labels={"students": "Total estudiantes", "nivel_educativo": "Nivel educativo"})
    fig_nivel.update_layout(title=dict(x=0.5, text="Estudiantes por nivel educativo", font=dict(size=16, color="#073763")), showlegend=False)
    st.plotly_chart(fig_nivel, use_container_width=True)

    st.markdown("<h3 style='color:#073763; margin-bottom:0.1rem;'>📈 Estudiantes vs Unidades educativas</h3>", unsafe_allow_html=True)
    comp = dept_counts.set_index("department")["students"].rename("students").to_frame().reset_index()
    comp["schools"] = comp["department"].map(school_counts_combined).fillna(0).astype(int)
    comp["avg_students_per_school"] = comp.apply(lambda r: r["students"] / r["schools"] if r["schools"] > 0 else np.nan, axis=1)
    comp_sorted = comp.sort_values("students", ascending=False)
    fig_comp = make_subplots(specs=[[{"secondary_y": True}]])
    fig_comp.add_trace(go.Bar(x=comp_sorted["department"], y=comp_sorted["students"], name="Estudiantes", marker_color=DEPT_PALETTE), secondary_y=False)
    fig_comp.add_trace(go.Scatter(x=comp_sorted["department"], y=comp_sorted["avg_students_per_school"], mode="lines+markers", name="Promedio alumnos/escuela", marker=dict(size=8, color="#EF553B"), line=dict(width=2, color="#EF553B")), secondary_y=True)
    fig_comp.update_layout(title=dict(x=0.5, text="Estudiantes vs Unidades educativas", font=dict(size=16, color="#073763")), xaxis_tickangle=-45, template="simple_white", legend=dict(font=dict(size=12)))
    fig_comp.update_yaxes(title_text="Estudiantes", secondary_y=False)
    fig_comp.update_yaxes(title_text="Promedio alumnos/escuela", secondary_y=True)
    st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")

# ----------------------
# NUEVO: Top 3 y Bottom 3 por grupo de edad (promedio alumnos por escuela)
# ----------------------
st.markdown("<h2 style='color:#0b5ed7;'>Departamentos con MÁS / MENOS estudiantes por unidad (por grupo etario)</h2>", unsafe_allow_html=True)
st.markdown("<div style='color:#475569; font-size:13px;'>Mostramos, para cada grupo de edad, los 3 departamentos con mayor promedio de estudiantes por unidad educativa y los 3 con menor promedio (ignorando departamentos sin escuelas asignadas).</div>", unsafe_allow_html=True)

top3_df, bottom3_df = top_bottom_avg_by_age(df, school_counts_combined, top_n=3)

# Mostrar: haremos una fila por cada grupo con dos gráficos (top3 / bottom3)
age_groups_order = sorted(df["grupo_edad"].unique())

for g in age_groups_order:
    st.markdown(f"<h3 style='color:#073763; margin-bottom:0.1rem;'>🔹 {g}</h3>", unsafe_allow_html=True)
    t = top3_df[top3_df["grupo_edad"] == g].copy()
    b = bottom3_df[bottom3_df["grupo_edad"] == g].copy()

    # Top 3
    colA, colB = st.columns(2)
    with colA:
        if not t.empty:
            fig_t = px.bar(t.sort_values("avg_per_school", ascending=True), x="avg_per_school", y="department", orientation="h",
                           labels={"avg_per_school": "Promedio alumnos/escuela", "department": "Departamento"},
                           title=f"Top 3 (más) — {g}", color="department", color_discrete_sequence=DEPT_PALETTE)
            fig_t.update_layout(showlegend=False, title=dict(x=0.5, font=dict(size=14, color="#073763")))
            st.plotly_chart(fig_t, use_container_width=True)
        else:
            st.markdown("<div style='color:#475569;'>No hay datos para mostrar en Top 3.</div>", unsafe_allow_html=True)

    # Bottom 3
    with colB:
        if not b.empty:
            fig_b = px.bar(b.sort_values("avg_per_school", ascending=True), x="avg_per_school", y="department", orientation="h",
                           labels={"avg_per_school": "Promedio alumnos/escuela", "department": "Departamento"},
                           title=f"Bottom 3 (menos) — {g}", color="department", color_discrete_sequence=DEPT_PALETTE)
            fig_b.update_layout(showlegend=False, title=dict(x=0.5, font=dict(size=14, color="#073763")))
            st.plotly_chart(fig_b, use_container_width=True)
        else:
            st.markdown("<div style='color:#475569;'>No hay datos para mostrar en Bottom 3.</div>", unsafe_allow_html=True)

# Ofrecer descarga de tablas Top3/Bottom3
st.markdown("<div style='margin-top:6px;'><strong>Descargar Top3 / Bottom3 por grupo etario</strong></div>", unsafe_allow_html=True)
top_csv = top3_df.to_csv(index=False).encode("utf-8")
bottom_csv = bottom3_df.to_csv(index=False).encode("utf-8")
st.download_button("Descargar Top3 (por edad) CSV", data=top_csv, file_name="top3_por_edad.csv", mime="text/csv")
st.download_button("Descargar Bottom3 (por edad) CSV", data=bottom_csv, file_name="bottom3_por_edad.csv", mime="text/csv")

st.markdown("---")

# ----------------------
# NUEVO: Simulación ~100% (multiplicar por 10)
# ----------------------
st.markdown("<h2 style='color:#0b5ed7;'>Simulación aproximada al 100%</h2>", unsafe_allow_html=True)
st.markdown("<div style='color:#475569; font-size:13px;'>A partir de la muestra (10%), generamos una versión aproximada al 100% multiplicando los conteos por 10. Es una aproximación para comparar escalas.</div>", unsafe_allow_html=True)

show_100 = st.checkbox("Mostrar versión aproximada al 100% (multiplicar por 10)", value=False)

if show_100:
    # Recalcular agregaciones multiplicando por 10
    factor = 10
    dept_counts_100 = dept_counts.copy()
    dept_counts_100["students"] = (dept_counts_100["students"] * factor).astype(int)
    sex_counts_100 = sex_counts.copy()
    sex_counts_100["students"] = (sex_counts_100["students"] * factor).astype(int)
    nivel_counts_100 = nivel_counts.copy()
    nivel_counts_100["students"] = (nivel_counts_100["students"] * factor).astype(int)

    # Recompute avg per school for 100% (approx)
    comp100 = dept_counts_100.set_index("department")["students"].rename("students").to_frame().reset_index()
    comp100["schools"] = comp100["department"].map(school_counts_combined).fillna(0).astype(int)
    comp100["avg_students_per_school"] = comp100.apply(lambda r: r["students"] / r["schools"] if r["schools"] > 0 else np.nan, axis=1)

    st.markdown("<h3 style='color:#073763;'>🔁 Comparación: 10% vs ~100% — Estudiantes por departamento</h3>", unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        fig_dept_10 = px.bar(dept_counts.sort_values("students", ascending=False), x="department", y="students", color="department", color_discrete_sequence=DEPT_PALETTE)
        fig_dept_10.update_layout(showlegend=False, title=dict(text="10% - Estudiantes por departamento", x=0.5, font=dict(size=14, color="#073763")))
        st.plotly_chart(fig_dept_10, use_container_width=True)
    with colB:
        fig_dept_100 = px.bar(dept_counts_100.sort_values("students", ascending=False), x="department", y="students", color="department", color_discrete_sequence=DEPT_PALETTE)
        fig_dept_100.update_layout(showlegend=False, title=dict(text="~100% - Estimación (x10)", x=0.5, font=dict(size=14, color="#073763")))
        st.plotly_chart(fig_dept_100, use_container_width=True)

    # Sex pie comparison
    st.markdown("<h3 style='color:#073763;'>🔁 Distribución por sexo (10% vs ~100%)</h3>", unsafe_allow_html=True)
    colC, colD = st.columns(2)
    with colC:
        fig_sex_10 = px.pie(sex_counts, names="sexo", values="students", color_discrete_map=SEX_COLOR_MAP, title="10% - Distribución por sexo")
        fig_sex_10.update_layout(title=dict(x=0.5, font=dict(size=14, color="#073763")))
        st.plotly_chart(fig_sex_10, use_container_width=True)
    with colD:
        fig_sex_100 = px.pie(sex_counts_100, names="sexo", values="students", color_discrete_map=SEX_COLOR_MAP, title="~100% - Estimación (x10)")
        fig_sex_100.update_layout(title=dict(x=0.5, font=dict(size=14, color="#073763")))
        st.plotly_chart(fig_sex_100, use_container_width=True)

    # Nivel educativo comparison
    st.markdown("<h3 style='color:#073763;'>🔁 Estudiantes por nivel educativo (10% vs ~100%)</h3>", unsafe_allow_html=True)
    colE, colF = st.columns(2)
    with colE:
        fig_nivel_10 = px.bar(nivel_counts, x="students", y="nivel_educativo", orientation="h", color="nivel_educativo", color_discrete_sequence=LEVEL_PALETTE)
        fig_nivel_10.update_layout(title=dict(x=0.5, text="10% - Estudiantes por nivel", font=dict(size=14, color="#073763")), showlegend=False)
        st.plotly_chart(fig_nivel_10, use_container_width=True)
    with colF:
        fig_nivel_100 = px.bar(nivel_counts_100, x="students", y="nivel_educativo", orientation="h", color="nivel_educativo", color_discrete_sequence=LEVEL_PALETTE)
        fig_nivel_100.update_layout(title=dict(x=0.5, text="~100% - Estimación (x10)", font=dict(size=14, color="#073763")), showlegend=False)
        st.plotly_chart(fig_nivel_100, use_container_width=True)

    # Provide download of dept_counts_100
    st.markdown("<div style='margin-top:6px;'><strong>Descargar estimación ~100%</strong></div>", unsafe_allow_html=True)
    csv100 = dept_counts_100.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV (~100% - deptos)", data=csv100, file_name="dept_counts_approx_100pct.csv", mime="text/csv")

st.markdown("---")

# ----------------------
# Resto del dashboard (tablas, explicaciones)
# ----------------------
st.markdown("<h2 style='color:#0b5ed7;'>Porcentajes, diferencias y guías</h2>", unsafe_allow_html=True)

national_total = df.shape[0]
sex_pct = sex_counts.copy()
sex_pct["pct"] = (sex_pct["students"] / national_total * 100).round(2)

st.markdown("<h4 style='color:#073763;'>📊 Porcentaje nacional por sexo</h4>", unsafe_allow_html=True)
st.dataframe(sex_pct.style.format({"students": "{:,}", "pct": "{:.2f}%"}))

dept_pct = dept_counts.copy()
dept_pct["pct_total"] = (dept_pct["students"] / national_total * 100).round(3)
dept_pct["schools_assigned"] = dept_pct["department"].map(school_counts_combined).fillna(0).astype(int)
dept_pct["avg_students_per_school"] = dept_pct.apply(lambda r: (r["students"] / r["schools_assigned"]) if r["schools_assigned"] > 0 else np.nan, axis=1)
mean_pct = dept_pct["pct_total"].mean()
dept_pct["diff_vs_mean_pct_points"] = (dept_pct["pct_total"] - mean_pct).round(3)

st.markdown("<h4 style='color:#073763;'>📍 Comparativa por departamento</h4>", unsafe_allow_html=True)
st.dataframe(dept_pct.sort_values("students", ascending=False).reset_index(drop=True).style.format({
    "students": "{:,}", "pct_total": "{:.3f}%", "avg_students_per_school": "{:.1f}"
}))

st.markdown("<h4 style='color:#073763;'>⚖️ Porcentaje por sexo en cada departamento</h4>", unsafe_allow_html=True)
sex_dept = df.groupby(["department", "sexo"]).size().rename("count").reset_index()
sex_dept_total = sex_dept.groupby("department")["count"].sum().rename("dept_total").reset_index()
sex_dept = sex_dept.merge(sex_dept_total, on="department")
sex_dept["pct"] = (sex_dept["count"] / sex_dept["dept_total"] * 100).round(2)
fig_sex_dept = px.bar(sex_dept, x="department", y="pct", color="sexo", color_discrete_map=SEX_COLOR_MAP, title="Porcentaje por sexo dentro de cada departamento")
fig_sex_dept.update_layout(barmode="stack", xaxis_tickangle=-45, title=dict(x=0.5, font=dict(size=14, color="#073763")))
st.plotly_chart(fig_sex_dept, use_container_width=True)


