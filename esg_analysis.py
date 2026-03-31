import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ১. পেজ সেটআপ (এটি সবার উপরে থাকতে হবে)
st.set_page_config(page_title="WAVE Foundation | ESG Dashboard", layout="wide")

# ২. কাস্টম সিএসএস (ডিজাইন উন্নত করার জন্য)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #064e3b 0%, #022c22 100%);
        border-radius: 15px;
        border-bottom: 4px solid #10b981;
        margin-bottom: 30px;
    }
    .impact-banner {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #2ea043;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. ব্র্যান্ডিং সেকশন
st.markdown("""
    <div class="main-header">
        <h1 style='margin:0; font-size: 36px; color: #10b981;'>WAVE Foundation</h1>
        <p style='margin:0; font-size: 18px; color: #94a3b8;'>ESG Impact Intelligence Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

# ৪. ডাটা লোডিং ফাংশন
def load_esg_data(sheet):
    try:
        df = pd.read_excel("data.xlsx", sheet_name=sheet)
        df.columns = df.columns.str.strip()
        df['Data Input'] = pd.to_numeric(df['Data Input'], errors='coerce')
        return df.dropna(subset=['Metric / KPI'])
    except Exception:
        return pd.DataFrame()

# ৫. সাইডবার নেভিগেশন
selection = st.sidebar.radio("Navigate ESG Pillars", ["Environmental (E)", "Social (S)", "Governance (G)", "Innovation Lab 💡"])

# ৬. আইকন ও কালার লজিক
if selection == "Environmental (E)":
    title_text, bar_color = "🌍 Environmental (E) Impact Analytics", '#2ea043'
elif selection == "Social (S)":
    title_text, bar_color = "🤝 Social (S) Impact Analytics", '#1f6feb'
elif selection == "Governance (G)":
    title_text, bar_color = "⚖️ Governance (G) Impact Analytics", '#da3633'
else:
    title_text, bar_color = "💡 Innovation Lab: Strategic Storytelling", '#58a6ff'

# --- ৭. ড্যাশবোর্ড কন্টেন্ট ---
if selection != "Innovation Lab 💡":
    st.header(title_text)
    data = load_esg_data(selection)

    if not data.empty:
        st.markdown("---")
        col_viz, col_data = st.columns([1.6, 1.4])
        
        with col_viz:
            st.subheader("📊 High-Impact Visualization")
            if selection == "Environmental (E)":
                fig = px.area(data, x='Metric / KPI', y='Data Input', markers=True, color_discrete_sequence=[bar_color])
            elif selection == "Social (S)":
                fig = px.bar(data, x='Data Input', y='Metric / KPI', orientation='h', text_auto='.2s', color_discrete_sequence=[bar_color])
            else:
                fig = px.pie(data, values='Data Input', names='Metric / KPI', hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu)
            
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), height=550)
            st.plotly_chart(fig, use_container_width=True)

        with col_data:
            st.subheader("📑 Strategic Data Matrix")
            st.dataframe(data[['Metric / KPI', 'Data Input', 'Unit']].fillna("-"), use_container_width=True, height=550, hide_index=True)
    else:
        st.warning("Sheet data not found or Excel file missing.")

# --- ৮. ইনোভেশন ল্যাব ---
else:
    st.header(title_text)
    st.markdown("""
    <div class="impact-banner">
        <h2 style='color: #34d399;'>WAVE Foundation: Transforming Justice ⚖️</h2>
        <p style='font-size: 18px;'>
            <b>WAVE Foundation</b> সফলভাবে বাংলাদেশের প্রতিটি ইউনিয়ন পরিষদে <b>গ্রাম আদালত (Phase III)</b> প্রকল্পের মাধ্যমে স্বচ্ছতা ও জবাবদিহিতা নিশ্চিত করছে। 
            ইউরোপীয় ইউনিয়ন এবং UNDP-র কারিগরি সহায়তায় আমরা সাধারণ মানুষের দোরগোড়ায় দ্রুত বিচার পৌঁছে দিচ্ছি।
        </p>
    </div>
    """, unsafe_allow_html=True)

    comparison_df = pd.DataFrame({
        "Feature": ["Time to Resolve", "Legal Cost", "Accessibility"],
        "Traditional Courts": ["180+ Days", "High Expense", "District Level"],
        "Village Courts (WAVE)": ["7-15 Days", "Zero Cost", "Union Level"]
    })
    st.table(comparison_df)
