# dashboard/app.py
"""DevOps Monitoring Dashboard — Streamlit frontend."""
import os
import time
import httpx
import pandas as pd
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "")

st.set_page_config(
    page_title="DevOps Monitor",
    page_icon="📡",
    layout="wide",
)

st.title("📡 DevOps Monitoring Dashboard")

tab_metrics, tab_servers = st.tabs(["📊 Métriques Système", "🖥️ Statut des Serveurs"])


# ─── Tab 1: System Metrics ────────────────────────────────────────────────────

with tab_metrics:
    st.subheader("Métriques système en temps réel")

    # Initialize history in session state
    if "history" not in st.session_state:
        st.session_state.history = []

    @st.cache_data(ttl=1)
    def fetch_metrics():
        try:
            resp = httpx.get(f"{API_BASE_URL}/metrics", timeout=3)
            return resp.json()
        except Exception:
            return None

    metrics = fetch_metrics()

    if metrics:
        col1, col2, col3 = st.columns(3)
        col1.metric("🖥️ CPU", f"{metrics['cpu_percent']:.1f}%")
        col2.metric("🧠 Mémoire", f"{metrics['memory_percent']:.1f}%",
                    f"{metrics['memory_used_gb']:.1f}/{metrics['memory_total_gb']:.1f} GB")
        col3.metric("💾 Disque", f"{metrics['disk_percent']:.1f}%",
                    f"{metrics['disk_used_gb']:.1f}/{metrics['disk_total_gb']:.1f} GB")

        # Append to rolling history (max 60 points)
        st.session_state.history.append({
            "time": time.strftime("%H:%M:%S"),
            "CPU %": metrics["cpu_percent"],
            "Mémoire %": metrics["memory_percent"],
            "Disque %": metrics["disk_percent"],
        })
        if len(st.session_state.history) > 60:
            st.session_state.history = st.session_state.history[-60:]

        df = pd.DataFrame(st.session_state.history).set_index("time")
        st.line_chart(df)
    else:
        st.error("Impossible de contacter l'API. Vérifiez qu'elle est bien démarrée.")

    if st.button("🔄 Rafraîchir"):
        st.rerun()


# ─── Tab 2: Server Status ─────────────────────────────────────────────────────

with tab_servers:
    st.subheader("Serveurs surveillés")

    @st.cache_data(ttl=5)
    def fetch_servers():
        try:
            resp = httpx.get(f"{API_BASE_URL}/servers", timeout=3)
            return resp.json()
        except Exception:
            return []

    servers = fetch_servers()

    if servers:
        df = pd.DataFrame(servers)

        def color_status(val):
            colors = {"UP": "background-color: #10b981; color: white",
                      "DEGRADED": "background-color: #f59e0b; color: white",
                      "DOWN": "background-color: #ef4444; color: white",
                      "unknown": "background-color: #6b7280; color: white"}
            return colors.get(val, "")

        styled = df.style.map(color_status, subset=["status"])
        st.dataframe(styled, use_container_width=True)
    else:
        st.info("Aucun serveur enregistré.")

    st.divider()
    st.subheader("➕ Enregistrer un nouveau serveur")

    with st.form("register_server"):
        name = st.text_input("Nom du serveur", placeholder="api-prod-1")
        host = st.text_input("Hôte", placeholder="httpbin.org")
        port = st.number_input("Port", min_value=1, max_value=65535, value=443)
        tags = st.text_input("Tags (séparés par des virgules)", placeholder="prod, api")
        submitted = st.form_submit_button("Enregistrer")

        if submitted and name and host:
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            try:
                resp = httpx.post(
                    f"{API_BASE_URL}/servers",
                    json={"name": name, "host": host, "port": port, "tags": tag_list},
                    headers={"X-API-Key": API_KEY},
                    timeout=5,
                )
                if resp.status_code == 201:
                    st.success(f"Serveur '{name}' enregistré avec succès !")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Erreur {resp.status_code}: {resp.json().get('detail')}")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")
