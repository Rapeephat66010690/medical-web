import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าแดชบอร์ดขยายเต็มหน้าจอ (Wide Mode) และปรับธีมโครงสร้างหลัก
st.set_page_config(page_title="US AI Sector Momentum Dashboard", layout="wide")

# สไตล์อินเตอร์เฟสและระบบเมาส์ชี้แบบทางการ (Professional Style Layout)
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], .main {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Cpath d='M4,2 L4,26 L11,19 L19,30 L23,27 L15,17 L24,17 Z' fill='%23111111' stroke='%23ffffff' stroke-width='2.5' filter='drop-shadow(0px 3px 3px rgba(0,0,0,0.6))'/%3E%3C/svg%3E"), auto !important;
        }
        button, a, [role=\"button\"], .js-plotly-plot .textlayer, .main-svg, .bars {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Cpath d='M8,12 L8,18 L10,18 L10,5 C10,3.5 11.5,3 12.5,3 C13.5,3 15,3.5 15,5 L15,11 C15,11 16,9.5 17.5,9.5 C19,9.5 20,11 20,12.5 L20,14 C20,14 21,12.5 22.5,12.5 C24,12.5 25,14 25,15.5 L25,21 C25,26 21,30 16,30 L13,30 C9,27 6,24 6,19 L6,12 Z' fill='%23111111' stroke='%23ffffff' stroke-width='2.5' filter='drop-shadow(0px 3px 3px rgba(0,0,0,0.6))'/%3E%3C/svg%3E"), pointer !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 15px !important;
            font-weight: bold !important;
            padding: 10px 18px !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. ฐานข้อมูลกลุ่มอุตสาหกรรม AI (อัปเดตใหม่ 8 กลุ่มตามคำสั่ง - แก้ไขเฉพาะส่วนนี้)
ai_universe_data = [
    # 1) Power
    {"Ticker": "ETN", "Name": "Eaton Corporation", "Group": "1) Power"},
    {"Ticker": "PWR", "Name": "Quanta Services", "Group": "1) Power"},
    {"Ticker": "HUBB", "Name": "Hubbell Incorporated", "Group": "1) Power"},
    {"Ticker": "NVT", "Name": "nVent Electric", "Group": "1) Power"},
    {"Ticker": "EME", "Name": "EMCOR Group", "Group": "1) Power"},
    {"Ticker": "ABB", "Name": "ABB Ltd", "Group": "1) Power"},
    {"Ticker": "SU.PA", "Name": "Schneider Electric", "Group": "1) Power"},
    {"Ticker": "SIEGY", "Name": "Siemens AG", "Group": "1) Power"},
    {"Ticker": "LEGRY", "Name": "Legrand SA", "Group": "1) Power"},
    {"Ticker": "ATKR", "Name": "Atkore Inc.", "Group": "1) Power"},
    {"Ticker": "PRYMY", "Name": "Prysmian S.p.A.", "Group": "1) Power"},
    {"Ticker": "GEV", "Name": "GE Vernova", "Group": "1) Power"},
    {"Ticker": "HITAY", "Name": "Hitachi Ltd.", "Group": "1) Power"},
    {"Ticker": "FUJIY", "Name": "Fuji Electric", "Group": "1) Power"},
    {"Ticker": "MELCOY", "Name": "Mitsubishi Electric", "Group": "1) Power"},

    # 2) Data Center Capacity
    {"Ticker": "IREN", "Name": "IREN Inc.", "Group": "2) Data Center Capacity"},
    {"Ticker": "CRWV", "Name": "CoreWeave (Proxy/OTC)", "Group": "2) Data Center Capacity"},
    {"Ticker": "CORZ", "Name": "Core Scientific", "Group": "2) Data Center Capacity"},
    {"Ticker": "CIFR", "Name": "Cipher Mining", "Group": "2) Data Center Capacity"},
    {"Ticker": "WULF", "Name": "TeraWulf Inc.", "Group": "2) Data Center Capacity"},
    {"Ticker": "HUT", "Name": "Hut 8 Corp", "Group": "2) Data Center Capacity"},
    {"Ticker": "RIOT", "Name": "Riot Platforms", "Group": "2) Data Center Capacity"},
    {"Ticker": "CLSK", "Name": "CleanSpark Inc.", "Group": "2) Data Center Capacity"},
    {"Ticker": "EQIX", "Name": "Equinix Inc.", "Group": "2) Data Center Capacity"},
    {"Ticker": "DLR", "Name": "Digital Realty Trust", "Group": "2) Data Center Capacity"},
    {"Ticker": "IRM", "Name": "Iron Mountain", "Group": "2) Data Center Capacity"},
    {"Ticker": "GDS", "Name": "GDS Holdings", "Group": "2) Data Center Capacity"},
    {"Ticker": "NXT.AX", "Name": "NEXTDC Limited", "Group": "2) Data Center Capacity"},
    {"Ticker": "DCI.AX", "Name": "Data Centre Investment", "Group": "2) Data Center Capacity"},
    {"Ticker": "9688.HK", "Name": "GDS Holdings (HK)", "Group": "2) Data Center Capacity"},

    # 3) Cooling
    {"Ticker": "VRT", "Name": "Vertiv Holdings", "Group": "3) Cooling"},
    {"Ticker": "TT", "Name": "Trane Technologies", "Group": "3) Cooling"},
    {"Ticker": "CARR", "Name": "Carrier Global", "Group": "3) Cooling"},
    {"Ticker": "JCI", "Name": "Johnson Controls", "Group": "3) Cooling"},
    {"Ticker": "MOD", "Name": "Modine Manufacturing", "Group": "3) Cooling"},
    {"Ticker": "LII", "Name": "Lennox International", "Group": "3) Cooling"},
    {"Ticker": "AAON", "Name": "AAON Inc.", "Group": "3) Cooling"},
    {"Ticker": "SPXC", "Name": "SPX Technologies", "Group": "3) Cooling"},
    {"Ticker": "MUNTERS.ST", "Name": "Munters Group AB", "Group": "3) Cooling"},
    {"Ticker": "DAIKY", "Name": "Daikin Industries", "Group": "3) Cooling"},
    {"Ticker": "BOYD", "Name": "Boyd Corporation (Private/Proxy)", "Group": "3) Cooling"},
    {"Ticker": "RITTAL", "Name": "Rittal GmbH (Private/Proxy)", "Group": "3) Cooling"},
    {"Ticker": "STULZ", "Name": "Stulz GmbH (Private/Proxy)", "Group": "3) Cooling"},
    {"Ticker": "AIRE", "Name": "Aire Control", "Group": "3) Cooling"},
    {"Ticker": "BALT", "Name": "Baltimore Aircoil (Proxy)", "Group": "3) Cooling"},

    # 4) Networking
    {"Ticker": "ANET", "Name": "Arista Networks", "Group": "4) Networking"},
    {"Ticker": "CSCO", "Name": "Cisco Systems", "Group": "4) Networking"},
    {"Ticker": "CIEN", "Name": "Ciena Corporation", "Group": "4) Networking"},
    {"Ticker": "JNPR", "Name": "Juniper Networks", "Group": "4) Networking"},
    {"Ticker": "FFIV", "Name": "F5 Inc.", "Group": "4) Networking"},
    {"Ticker": "COMM", "Name": "CommScope Holding", "Group": "4) Networking"},
    {"Ticker": "EXTR", "Name": "Extreme Networks", "Group": "4) Networking"},
    {"Ticker": "CALX", "Name": "Calix Inc.", "Group": "4) Networking"},
    {"Ticker": "ADTN", "Name": "ADTRAN Holdings", "Group": "4) Networking"},
    {"Ticker": "RBBN", "Name": "Ribbon Communications", "Group": "4) Networking"},
    {"Ticker": "NOK", "Name": "Nokia Corp", "Group": "4) Networking"},
    {"Ticker": "ERIC", "Name": "Ericsson", "Group": "4) Networking"},
    {"Ticker": "INFN", "Name": "Infinera Corporation", "Group": "4) Networking"},
    {"Ticker": "NETGEAR", "Name": "Netgear Inc.", "Group": "4) Networking"},
    {"Ticker": "UI", "Name": "Ubiquiti Inc.", "Group": "4) Networking"},

    # 5) Photonics / Optical
    {"Ticker": "CRDO", "Name": "Credo Technology", "Group": "5) Photonics / Optical"},
    {"Ticker": "LITE", "Name": "Lumentum Holdings", "Group": "5) Photonics / Optical"},
    {"Ticker": "COHR", "Name": "Coherent Corp.", "Group": "5) Photonics / Optical"},
    {"Ticker": "AAOI", "Name": "Applied Optoelectronics", "Group": "5) Photonics / Optical"},
    {"Ticker": "FN", "Name": "Fabrinet", "Group": "5) Photonics / Optical"},
    {"Ticker": "MTSI", "Name": "MACOM Technology", "Group": "5) Photonics / Optical"},
    {"Ticker": "IPGP", "Name": "IPG Photonics", "Group": "5) Photonics / Optical"},
    {"Ticker": "LWLG", "Name": "Lightwave Logic", "Group": "5) Photonics / Optical"},
    {"Ticker": "POET", "Name": "POET Technologies", "Group": "5) Photonics / Optical"},
    {"Ticker": "VIAV", "Name": "Viavi Solutions", "Group": "5) Photonics / Optical"},
    {"Ticker": "LUNA", "Name": "Luna Innovations", "Group": "5) Photonics / Optical"},
    {"Ticker": "EMKR", "Name": "EMCORE Corporation", "Group": "5) Photonics / Optical"},
    {"Ticker": "APH", "Name": "Amphenol Corp.", "Group": "5) Photonics / Optical"},
    {"Ticker": "GLW", "Name": "Corning Inc.", "Group": "5) Photonics / Optical"},
    {"Ticker": "FNSR", "Name": "Finisar (by Coherent)", "Group": "5) Photonics / Optical"},

    # 6) Memory (HBM)
    {"Ticker": "MU", "Name": "Micron Technology", "Group": "6) Memory (HBM)"},
    {"Ticker": "000660.KS", "Name": "SK Hynix", "Group": "6) Memory (HBM)"},
    {"Ticker": "005930.KS", "Name": "Samsung Electronics", "Group": "6) Memory (HBM)"},
    {"Ticker": "WDC", "Name": "Western Digital", "Group": "6) Memory (HBM)"},
    {"Ticker": "STX", "Name": "Seagate Technology", "Group": "6) Memory (HBM)"},
    {"Ticker": "SIMO", "Name": "Silicon Motion", "Group": "6) Memory (HBM)"},
    {"Ticker": "UCTT", "Name": "Ultra Clean Holdings", "Group": "6) Memory (HBM)"},
    {"Ticker": "FORM", "Name": "FormFactor Inc.", "Group": "6) Memory (HBM)"},
    {"Ticker": "SYNA", "Name": "Synaptics Inc.", "Group": "6) Memory (HBM)"},
    {"Ticker": "ALAB", "Name": "Astera Labs", "Group": "6) Memory (HBM)"},
    {"Ticker": "PSTG", "Name": "Pure Storage", "Group": "6) Memory (HBM)"},
    {"Ticker": "NTAP", "Name": "NetApp Inc.", "Group": "6) Memory (HBM)"},
    {"Ticker": "ASTS", "Name": "AST SpaceMobile", "Group": "6) Memory (HBM)"},
    {"Ticker": "SMCI", "Name": "Super Micro Computer", "Group": "6) Memory (HBM)"},
    {"Ticker": "HPE", "Name": "Hewlett Packard Enterprise", "Group": "6) Memory (HBM)"},

    # 7) Semiconductor Equipment
    {"Ticker": "ASML", "Name": "ASML Holding", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "AMAT", "Name": "Applied Materials", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "LRCX", "Name": "Lam Research", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "KLAC", "Name": "KLA Corporation", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "TER", "Name": "Teradyne Inc.", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "ONTO", "Name": "Onto Innovation", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "ACLS", "Name": "Axcelis Technologies", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "VECO", "Name": "Veeco Instruments", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "CAMT", "Name": "Camtek Ltd.", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "MKSI", "Name": "MKS Instruments", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "COHU", "Name": "Cohu Inc.", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "ENTG", "Name": "Entegris Inc.", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "UCTT", "Name": "Ultra Clean (Equipment)", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "NVMI", "Name": "Nova Ltd.", "Group": "7) Semiconductor Equipment"},
    {"Ticker": "BRKS", "Name": "Brooks Automation", "Group": "7) Semiconductor Equipment"},

    # 8) AI Compute
    {"Ticker": "NVDA", "Name": "Nvidia Corp.", "Group": "8) AI Compute"},
    {"Ticker": "AMD", "Name": "Advanced Micro Devices", "Group": "8) AI Compute"},
    {"Ticker": "AVGO", "Name": "Broadcom Inc.", "Group": "8) AI Compute"},
    {"Ticker": "MRVL", "Name": "Marvell Technology", "Group": "8) AI Compute"},
    {"Ticker": "QCOM", "Name": "Qualcomm Inc.", "Group": "8) AI Compute"},
    {"Ticker": "INTC", "Name": "Intel Corp.", "Group": "8) AI Compute"},
    {"Ticker": "TXN", "Name": "Texas Instruments", "Group": "8) AI Compute"},
    {"Ticker": "ADI", "Name": "Analog Devices", "Group": "8) AI Compute"},
    {"Ticker": "NXPI", "Name": "NXP Semiconductors", "Group": "8) AI Compute"},
    {"Ticker": "ON", "Name": "ON Semiconductor", "Group": "8) AI Compute"},
    {"Ticker": "MCHP", "Name": "Microchip Technology", "Group": "8) AI Compute"},
    {"Ticker": "MPWR", "Name": "Monolithic Power Systems", "Group": "8) AI Compute"},
    {"Ticker": "QRVO", "Name": "Qorvo Inc.", "Group": "8) AI Compute"},
    {"Ticker": "SWKS", "Name": "Skyworks Solutions", "Group": "8) AI Compute"},
    {"Ticker": "ARM", "Name": "Arm Holdings", "Group": "8) AI Compute"}
]

df_base = pd.DataFrame(ai_universe_data)

# 3. ฟังก์ชันดึงราคาและคำนวณ % Change ย้อนหลังรายวัน (Cache ข้อมูล 60 วินาที)
@st.cache_data(ttl=60)
def fetch_ai_market_data(df):
    valid_tickers = [t for t in df['Ticker'].unique().tolist() if not t.endswith('_PVT') and not t.endswith('_MKT') and not t.endswith('_CE')]
    pct_dict = {}
    price_dict = {}
    
    try:
        data = yf.download(valid_tickers, period="5d", group_by="ticker", progress=False)
        for ticker in df['Ticker'].unique():
            if ticker.endswith('_PVT') or ticker.endswith('_MKT') or ticker.endswith('_CE'):
                pct_dict[ticker] = 0.0
                price_dict[ticker] = 100.0  
            elif ticker in data.columns.levels[0]:
                hist = data[ticker].dropna()
                if len(hist) >= 2:
                    prev = float(hist['Close'].iloc[-2])
                    latest = float(hist['Close'].iloc[-1])
                    pct_dict[ticker] = ((latest - prev) / prev) * 100 if prev > 0 else 0.0
                    price_dict[ticker] = latest
                else:
                    pct_dict[ticker], price_dict[ticker] = 0.0, 0.0
            else:
                pct_dict[ticker], price_dict[ticker] = 0.0, 0.0
    except:
        pass
        
    df['Price ($)'] = df['Ticker'].map(price_dict).fillna(0.0)
    df['% Change'] = df['Ticker'].map(pct_dict).fillna(0.0)
    return df

with st.spinner("กำลังประมวลผลข้อมูลราคาและโมเมนตัมตลาด..."):
    df_processed = fetch_ai_market_data(df_base.copy())

def style_positive_negative(row):
    val = row['% Change']
    color = '#00cc00' if val > 0 else ('#ff3333' if val < 0 else '#ffffff')
    styles = [''] * len(row)
    if '% Change' in row.index:
        idx = row.index.get_loc('% Change')
        styles[idx] = f'color: {color}; font-weight: bold;'
    return styles

if 'selected_group' not in st.session_state:
    st.session_state.selected_group = None

# ตั้งค่าสถานะเริ่มต้นของเงินสดสำรอง
if 'cash_reserve' not in st.session_state:
    st.session_state.cash_reserve = 5000.0

# =================================================================
# 4. การจัดการระบบแถบเมนู (Tabs)
# =================================================================
st.title("US AI Sector Momentum & Capital Flow Dashboard")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "ภาพรวมตลาด (Market Overview)", 
    "คำนวณต้นทุนถัวเฉลี่ย (USD)", 
    "My port", 
    "สัดส่วนการลงทุน (Portfolio Allocation)",
    "แนวรับ",
    "Compound Plan"
])

# -----------------------------------------------------------------
# TAB 1: ภาพรวมตลาด (Market Overview)
# -----------------------------------------------------------------
with tab1:
    if st.session_state.selected_group:
        st.markdown("### แดชบอร์ดวิเคราะห์เม็ดเงินหมุนเวียนกลุ่มอุตสาหกรรม AI")
        
        if st.button("ย้อนกลับไปหน้ากราฟหลัก", type="primary"):
            st.session_state.selected_group = None
            st.rerun()
            
        st.markdown(f"### เจาะลึกกระแสเงินทุนหุ้นในกลุ่ม: **{st.session_state.selected_group}**")
        
        df_sub = df_processed[df_processed['Group'] == st.session_state.selected_group][['Ticker', 'Name', 'Price ($)', '% Change']]
        df_sub = df_sub.sort_values(by='% Change', ascending=False).reset_index(drop=True)
         
        st.dataframe(
            df_sub.style.apply(style_positive_negative, axis=1).format({"Price ($)": "{:.2f}", "% Change": "{:+.2f}%"}),
            use_container_width=True,
            height=480
        )
    
    else:
        st.markdown("### คำแนะนำ: คลิกเลือกที่แกนรายชื่อกลุ่มหรือแท่งกราฟเพื่อเจาะลึกข้อมูลหลักทรัพย์รายตัว")
        
        df_group_flow = df_processed.groupby('Group')['% Change'].mean().reset_index()
        df_group_flow = df_group_flow.sort_values(by='% Change', ascending=True)

        fig = px.bar(
            df_group_flow,
            x='% Change',
            y='Group',
            orientation='h',
            color='% Change',
            color_continuous_scale=[[0, '#ff3333'], [0.48, '#242424'], [0.52, '#242424'], [1, '#00cc00']],
            color_continuous_midpoint=0,
            text_auto='.2f'
        )
        fig.update_layout(
            height=580,
            margin=dict(t=10, b=10, l=10, r=40),
            xaxis_title="เปอร์เซ็นต์การเคลื่อนไหวเฉลี่ยของกลุ่ม (%)",
            yaxis_title=None,
            clickmode='event+select'
        )
        fig.update_traces(textposition='outside', textfont_size=11, textfont_weight='bold')
        
        selected_point = st.plotly_chart(fig, use_container_width=True, on_select="rerun", config={'displayModeBar': False})
        
        if selected_point and "selection" in selected_point and "points" in selected_point["selection"] and len(selected_point["selection"]["points"]) > 0:
            point_data = selected_point["selection"]["points"][0]
            if "y" in point_data:
                st.session_state.selected_group = point_data["y"]
                st.rerun()

        top_group = df_group_flow.loc[df_group_flow['% Change'].idxmax()]
        worst_group = df_group_flow.loc[df_group_flow['% Change'].idxmin()]

        st.markdown("---")
        st.markdown("## สถิติและบทวิเคราะห์โมเมนตัมรายวัน (Capital Flow Analysis)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"""
            **กลุ่มที่มีโมเมนตัมเงินไหลเข้าสูงสุด:** กลุ่ม {top_group['Group']} มีค่าเฉลี่ยการเคลื่อนไหวเชิงบวกที่ระดับ {top_group['% Change']:.2f}% จัดเป็นกลุ่มผู้นำตลาดที่มีแรงซื้อสะสมหนาแน่นที่สุด
            """)
        with col2:
            st.warning(f"""
            **กลุ่มที่มีโมเมนตัมถดถอยสูงสุด:** กลุ่ม {worst_group['Group']} มีค่าเฉลี่ยการเคลื่อนไหวเชิงลบที่ระดับ {worst_group['% Change']:.2f}% บ่งชี้ถึงสภาวะการขายทำกำไรระยะสั้นของกระแสเงินทุน
            """)

# -----------------------------------------------------------------
# TAB 2: โปรแกรมคำนวณต้นทุนถัวเฉลี่ย
# -----------------------------------------------------------------
with tab2:
    st.markdown("""
        <style>
            .bright-box {
                background-color: rgba(30, 41, 59, 0.5);
                padding: 24px;
                border-radius: 12px;
                border: 1px solid #06b6d4;
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(6, 182, 212, 0.15);
            }
            .box-title {
                color: #22d3ee !important;
                font-size: 20px !important;
                font-weight: 700 !important;
                margin-bottom: 15px;
            }
            .bright-box p, .bright-box span { color: #f1f5f9 !important; }
            div[data-testid="stMetricValue"] {
                font-size: 34px !important;
                color: #10b981 !important;
                font-weight: 800 !important;
                text-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
            }
            div[data-testid="stMetricLabel"] {
                font-size: 15px !important;
                color: #cbd5e1 !important;
                font-weight: 600 !important;
            }
            .sub-text { color: #94a3b8 !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #ffffff;'>Stock Average Cost Calculator (USD)</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>โปรแกรมคำนวณและประเมินสัดส่วนต้นทุนเฉลี่ยสำหรับหุ้นต่างประเทศ (หน่วยเงินดอลลาร์สหรัฐ)</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="bright-box">', unsafe_allow_html=True)
        st.markdown('<p class="box-title">1. ข้อมูลหุ้นปัจจุบันในพอร์ตรวม</p>', unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            current_shares = st.number_input("จำนวนหุ้นรวมที่มีอยู่ปัจจุบัน (Shares)", min_value=0.0, value=1000.0, step=100.0, key="nav_shares")
        with col_c2:
            current_avg_price = st.number_input("ราคาต้นทุนเฉลี่ยปัจจุบัน ($ USD / Share)", min_value=0.0, value=100.0, step=1.0, key="nav_avg_price")
        
        current_investment = current_shares * current_avg_price
        st.metric(label="มูลค่าต้นทุนรวมทั้งหมด ณ ปัจจุบัน (Total Current Invested)", value=f"${current_investment:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    col_layout1, col_layout2 = st.columns(2)
    with col_layout1:
        st.markdown('<div class="bright-box">', unsafe_allow_html=True)
        st.markdown('<p class="box-title">ฟังก์ชันกำหนดเป้าหมายราคาเฉลี่ย</p>', unsafe_allow_html=True)
        target_avg_price = st.number_input("ราคาต้นทุนเฉลี่ยเป้าหมายที่ต้องการ ($ USD)", min_value=0.0, value=90.0, step=1.0)
        market_price_1 = st.number_input("ราคาซื้อขายของหุ้นในตลาด ณ ปัจจุบัน ($ USD)", min_value=0.0, value=80.0, step=1.0, key="m1")
        
        if st.button("คำนวณจำนวนเงินที่ต้องใช้ซื้อเพิ่ม", type="primary", use_container_width=True):
            if target_avg_price == market_price_1:
                st.error("ระบบไม่สามารถประมวลผลได้เนื่องจากราคาเฉลี่ยเป้าหมายมีค่าเท่ากับราคาตลาดปัจจุบัน")
            elif current_avg_price > target_avg_price and market_price_1 >= target_avg_price:
                st.error("การคำนวณล้มเหลว: ราคาตลาดปัจจุบันที่เข้าซื้อต้องต่ำกว่าราคาเป้าหมาย")
            elif current_avg_price < target_avg_price and market_price_1 <= target_avg_price:
                st.error("การคำนวณล้มเหลว: ราคาตลาดปัจจุบันที่เข้าซื้อต้องสูงกว่าราคาเป้าหมาย")
            else:
                required_shares = (current_shares * (current_avg_price - target_avg_price)) / (target_avg_price - market_price_1)
                required_fund = required_shares * market_price_1
                st.success(f"ต้องซื้อเพิ่มจำนวน: {required_shares:,.2f} หุ้น | คิดเป็นเงินที่ต้องใช้เพิ่ม: ${required_fund:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_layout2:
        st.markdown('<div class="bright-box">', unsafe_allow_html=True)
        st.markdown('<p class="box-title">ฟังก์ชันคำนวณจากงบประมาณซื้อเพิ่ม</p>', unsafe_allow_html=True)
        additional_fund = st.number_input("จำนวนเงินงบประมาณที่คุณต้องการลงทุนเพิ่ม ($ USD)", min_value=0.0, value=5000.0, step=500.0)
        market_price_2 = st.number_input("ราคาซื้อขายของหุ้นในตลาด ณ ปัจจุบัน ($ USD)", min_value=0.0, value=80.0, step=1.0, key="m2")
        
        if st.button("คำนวณต้นทุนเฉลี่ยใหม่หลังซื้อเพิ่ม", type="primary", use_container_width=True):
            if market_price_2 > 0:
                new_shares = additional_fund / market_price_2
                total_shares_new = current_shares + new_shares
                total_cost_new = current_investment + additional_fund
                new_avg_cost = total_cost_new / total_shares_new
                st.info(f"คุณจะได้หุ้นเพิ่ม: {new_shares:,.2f} หุ้น | ต้นทุนถัวเฉลี่ยใหม่จะลดลง/เพิ่มขึ้นอยู่ที่: ${new_avg_cost:,.2f} ต่อหุ้น")
            else:
                st.error("กรุณาระบุราคาตลาดปัจจุบันให้มากกว่า 0")
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------
# TAB 3: My port
# -----------------------------------------------------------------
with tab3:
    st.markdown("""
        <style>
            div[data-baseweb="input"] {
                border: none !important;
                box-shadow: none !important;
            }
            .stTextInput input:focus, .stNumberInput input:focus {
                border-color: #22d3ee !important;
                box-shadow: 0 0 5px rgba(34, 211, 238, 0.4) !important;
            }
            .portfolio-box {
                background-color: #111827;
                padding: 22px;
                border-radius: 12px;
                border: 1px solid #1f2937;
                margin-bottom: 20px;
            }
            .neon-title {
                color: #00ffcc !important;
                font-size: 22px !important;
                font-weight: 800 !important;
                margin-bottom: 5px;
            }
            .neon-cyan { color: #22d3ee !important; font-weight: bold; }
            .neon-gold { color: #f59e0b !important; font-weight: bold; }
            .neon-green { color: #00ffcc !important; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color: #ffffff;'>My Personal AI Portfolio</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>ระบบจำลองพอร์ตลงทุนหลักทรัพย์อิสระ ค้นหาราคาเรียลไทม์ผ่านชื่อย่อตลาดหลักทรัพย์โดยตรง</p>", unsafe_allow_html=True)

    if 'my_portfolio' not in st.session_state:
        st.session_state.my_portfolio = []

    # ส่วนการจัดการเงินสดสำรอง
    st.markdown('<div class="portfolio-box">', unsafe_allow_html=True)
    st.markdown('<p class="neon-title" style="color:#f59e0b !important;">การจัดการเงินสดสำรอง (Cash Balance)</p>', unsafe_allow_html=True)
    
    with st.form(key="cash_balance_form", clear_on_submit=False):
        col_cash_input, col_cash_btn = st.columns([4, 1])
        with col_cash_input:
            cash_value = st.number_input(
                "ระบุจำนวนเงินสดสำรองที่มีอยู่ปัจจุบัน ($ USD)", 
                min_value=0.0, 
                value=st.session_state.cash_reserve, 
                step=500.0,
                label_visibility="collapsed"
            )
        with col_cash_btn:
            submit_cash = st.form_submit_button("Submit", use_container_width=True)
            if submit_cash:
                st.session_state.cash_reserve = cash_value
                st.toast("อัปเดตมูลค่าเงินสดสำรองเรียบร้อยแล้ว!")
    st.markdown('</div>', unsafe_allow_html=True)

    # ส่วนเพิ่มหุ้นเข้าพอร์ต
    st.markdown('<div class="portfolio-box">', unsafe_allow_html=True)
    st.markdown('<p class="neon-title">พิมพ์ชื่อย่อหุ้นเพื่อบันทึกเข้าพอร์ต</p>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    
    with col_f1:
        custom_ticker = st.text_input("ชื่อย่อหลักทรัพย์ (Ticker เช่น NVDA, AAPL, PLTR, MSTR)", value="", key="clean_ticker_input").strip().upper()
        
        current_market_p = 0.0
        if custom_ticker:
            try:
                ticker_data = yf.Ticker(custom_ticker)
                ticker_hist = ticker_data.history(period="1d")
                if not ticker_hist.empty:
                    current_market_p = float(ticker_hist['Close'].iloc[-1])
                else:
                    current_market_p = 0.0
            except:
                current_market_p = 0.0
                
    with col_f2:
        user_shares = st.number_input("จำนวนหุ้นที่ถือครอง (Shares)", min_value=0.0, value=16.0, step=1.0, key="port_shares_clean")
        
    with col_f3:
        st.markdown(f"ราคาตลาดล่าสุด: <span class='neon-cyan'>${current_market_p:,.2f}</span>", unsafe_allow_html=True)
        user_avg = st.number_input("ราคาต้นทุนเฉลี่ยของคุณ ($ USD)", min_value=0.0, value=current_market_p if current_market_p > 0 else 15.0, step=0.1, key="port_avg_clean")

    if st.button("บันทึกหุ้นเข้าพอร์ตลงทุน", type="primary", use_container_width=True, key="save_portfolio_btn"):
        if not custom_ticker:
            st.error("กรุณากรอกชื่อย่อหุ้นก่อนทำการกดบันทึก")
        elif current_market_p == 0.0:
            st.error(f"ไม่พบข้อมูลดึงราคาของหุ้น '{custom_ticker}' ได้ในขณะนี้ โปรดลองอีกครั้งหรือตรวจตัวสะกด")
        else:
            st.session_state.my_portfolio = [item for item in st.session_state.my_portfolio if item['Ticker'] != custom_ticker]
            
            st.session_state.my_portfolio.append({
                "Ticker": custom_ticker,
                "Shares": user_shares,
                "Avg Cost": user_avg,
                "Live Price": current_market_p
            })
            st.success(f"บันทึกหุ้น {custom_ticker} เข้าสู่พอร์ตของคุณเรียบร้อยแล้ว!")
            st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

    # คำนวณสรุปผลพอร์ตรวม
    if len(st.session_state.my_portfolio) > 0 or st.session_state.cash_reserve > 0:
        st.markdown("### รายการสินทรัพย์ทั้งหมดในพอร์ตของคุณ")
        
        total_stock_cost = 0.0
        total_stock_value = 0.0
        
        df_port_display = pd.DataFrame()
        
        if len(st.session_state.my_portfolio) > 0:
            df_port = pd.DataFrame(st.session_state.my_portfolio)
            
            updated_prices = []
            for idx, row in df_port.iterrows():
                try:
                    t_data = yf.Ticker(row['Ticker']).history(period="1d")
                    p_latest = float(t_data['Close'].iloc[-1]) if not t_data.empty else row['Live Price']
                except:
                    p_latest = row['Live Price']
                updated_prices.append(p_latest)
                
            df_port['Price ($)'] = updated_prices
            df_port['Total Cost ($)'] = df_port['Shares'] * df_port['Avg Cost']
            df_port['Current Value ($)'] = df_port['Shares'] * df_port['Price ($)']
            df_port['P&L ($)'] = df_port['Current Value ($)'] - df_port['Total Cost ($)']
            df_port['% P&L'] = (df_port['P&L ($)'] / df_port['Total Cost ($)']) * 100
            
            total_stock_cost = df_port['Total Cost ($)'].sum()
            total_stock_value = df_port['Current Value ($)'].sum()
            
            df_port_display = df_port[['Ticker', 'Shares', 'Avg Cost', 'Price ($)', 'Total Cost ($)', 'Current Value ($)', 'P&L ($)', '% P&L']]
            df_port_display = df_port_display.sort_values(by='P&L ($)', ascending=False).reset_index(drop=True)

        # คำนวณมูลค่ารวมทั้งพอร์ต
        total_portfolio_cost = total_stock_cost + st.session_state.cash_reserve
        total_portfolio_value = total_stock_value + st.session_state.cash_reserve
        total_portfolio_pnl = total_portfolio_value - total_portfolio_cost
        total_portfolio_pct = (total_portfolio_pnl / total_portfolio_cost * 100) if total_portfolio_cost > 0 else 0.0
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="เงินทุนรวมทั้งหมด (Total Cost + Cash)", value=f"${total_portfolio_cost:,.2f}")
        with col_m2:
            st.metric(label="มูลค่าพอร์ตรวมปัจจุบัน (Net Asset Value)", value=f"${total_portfolio_value:,.2f}")
        with col_m3:
            pnl_arrow = "🔼" if total_portfolio_pnl >= 0 else "🔽"
            st.metric(
                label=f"ผลตอบแทนหุ้นรวมทั้งหมด ({pnl_arrow} P&L Total)", 
                value=f"${total_portfolio_pnl:,.2f}", 
                delta=f"{total_portfolio_pct:+.2f}%"
            )
            
        st.markdown("---")
        
        if len(df_port_display) > 0:
            def style_port_rows(row):
                val = row['% P&L']
                color = '#00ffcc' if val > 0 else ('#ff3333' if val < 0 else '#ffffff')
                styles = [''] * len(row)
                if '% P&L' in row.index:
                    styles[row.index.get_loc('% P&L')] = f'color: {color}; font-weight: bold;'
                if 'P&L ($)' in row.index:
                    styles[row.index.get_loc('P&L ($)')] = f'color: {color}; font-weight: bold;'
                return styles

            selected_rows = st.dataframe(
                df_port_display.style.apply(style_port_rows, axis=1).format({
                    "Shares": "{:,.2f}",
                    "Avg Cost": "${:,.2f}",
                    "Price ($)": "${:,.2f}",
                    "Total Cost ($)": "${:,.2f}",
                    "Current Value ($)": "${:,.2f}",
                    "P&L ($)": "${:,.2f}",
                    "% P&L": "{:+.2f}%"
                }),
                use_container_width=True,
                on_select="rerun",
                selection_mode="single-row"
            )

            if selected_rows and "selection" in selected_rows and "rows" in selected_rows["selection"] and len(selected_rows["selection"]["rows"]) > 0:
                selected_index = selected_rows["selection"]["rows"][0]
                ticker_to_remove = df_port_display.iloc[selected_index]['Ticker']
                
                st.session_state.my_portfolio = [item for item in st.session_state.my_portfolio if item['Ticker'] != ticker_to_remove]
                st.success(f"ทำการลบหุ้น {ticker_to_remove} ออกจากพอร์ตแล้ว")
                st.rerun()
        
        st.info(f"เงินสดสำรองคงเหลือในระบบ: **${st.session_state.cash_reserve:,.2f} USD**")
        
        if st.button("ล้างข้อมูลหุ้นทั้งหมดในพอร์ต (Reset Portfolio)", type="secondary", key="reset_portfolio_btn"):
            st.session_state.my_portfolio = []
            st.session_state.cash_reserve = 0.0
            st.rerun()
    else:
        st.info("💡 พอร์ตจำลองว่างอยู่ พิมพ์สัญลักษณ์หุ้นที่คุณเป็นเจ้าของด้านบน หรือปรับแต่งเงินสดสำรองเพื่อเริ่มต้นวิเคราะห์สินทรัพย์ได้เลย!")

# -----------------------------------------------------------------
# TAB 4: สัดส่วนการลงทุน (Portfolio Allocation)
# -----------------------------------------------------------------
with tab4:
    st.markdown("<h2 style='color: #ffffff;'>สัดส่วนการลงทุน (Portfolio Allocation)</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>แผนภูมิวงกลมวิเคราะห์สัดส่วนโครงสร้างพอร์ตการถือครองสินทรัพย์ในกลุ่มอุตสาหกรรม AI (รวมเงินสดสำรอง)</p>", unsafe_allow_html=True)
    st.markdown("---")

    has_real_data = False
    if ('my_portfolio' in st.session_state and len(st.session_state.my_portfolio) > 0) or st.session_state.cash_reserve > 0:
        df_allocation_list = []
        
        if 'my_portfolio' in st.session_state and len(st.session_state.my_portfolio) > 0:
            df_alloc_base = pd.DataFrame(st.session_state.my_portfolio)
            df_alloc_base['Current Value ($)'] = df_alloc_base['Shares'] * df_alloc_base['Live Price']
            for _, row in df_alloc_base.iterrows():
                if row['Current Value ($)'] > 0:
                    df_allocation_list.append({"Asset Ticker": row['Ticker'], "Value ($)": row['Current Value ($)']})
                    has_real_data = True
                    
        if st.session_state.cash_reserve > 0:
            df_allocation_list.append({"Asset Ticker": "Cash", "Value ($)": st.session_state.cash_reserve})
            has_real_data = True
            
        if has_real_data:
            df_allocation = pd.DataFrame(df_allocation_list)
            st.success("แสดงสัดส่วนตามข้อมูลหุ้นและเงินสดสำรองจริงในพอร์ตของคุณ ณ ปัจจุบัน")

    if not has_real_data:
        st.info("ตัวอย่างการแสดงผลสัดส่วนพอร์ตการลงทุน (หากต้องการแสดงพอร์ตจริง กรุณาเพิ่มรายชื่อหุ้นในเมนู My port)")
        mock_alloc_data = [
            {"Asset Ticker": "NVDA", "Value ($)": 45000.0},
            {"Asset Ticker": "AAPL", "Value ($)": 28000.0},
            {"Asset Ticker": "PLTR", "Value ($)": 15000.0},
            {"Asset Ticker": "MSFT", "Value ($)": 12000.0}
        ]
        if st.session_state.cash_reserve > 0:
            mock_alloc_data.append({"Asset Ticker": "Cash", "Value ($)": st.session_state.cash_reserve})
        else:
            mock_alloc_data.append({"Asset Ticker": "Cash", "Value ($)": 10000.0})
            
        df_allocation = pd.DataFrame(mock_alloc_data)

    col_g1, col_g2 = st.columns([3, 2])

    with col_g1:
        neon_colors = ['#f59e0b', '#00ffcc', '#22d3ee', '#6366f1', '#f43f5e', '#10b981']
        
        fig_donut = px.pie(
            df_allocation, 
            values='Value ($)', 
            names='Asset Ticker', 
            hole=0.6,
            color_discrete_sequence=neon_colors
        )
        
        fig_donut.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='#111827', width=3))
        )
        
        fig_donut.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=50, l=10, r=10),
            height=450
        )
        
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

    with col_g2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="portfolio-box">', unsafe_allow_html=True)
        st.markdown('<p class="neon-title" style="color:#22d3ee !important;">ตารางแจกแจงสัดส่วนเปอร์เซ็นต์</p>', unsafe_allow_html=True)
        
        total_val = df_allocation['Value ($)'].sum()
        df_table_show = df_allocation.copy()
        df_table_show['% Weight'] = (df_table_show['Value ($)'] / total_val) * 100
        df_table_show = df_table_show.sort_values(by='% Weight', ascending=False).reset_index(drop=True)
        
        st.dataframe(
            df_table_show.style.format({
                "Value ($)": "${:,.2f}",
                "% Weight": "{:.2f}%"
            }),
            use_container_width=True
        )
        
        st.markdown(f"**มูลค่าสินทรัพย์รวมทั้งหมดในพอร์ต (หุ้น + เงินสด):** <span class='neon-green'>${total_val:,.2f} USD</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------
# TAB 5: แนวรับ
# -----------------------------------------------------------------
with tab5:
    st.markdown("### คํานวณแนวรับสถิติเส้นค่าเฉลี่ยเคลื่อนที่ (Moving Average Support Analysis)")
    st.write("ป้อนรหัสหุ้นเพื่อดึงข้อมูลราคาและวิเคราะห์แนวรับทางเทคนิคตามช่วงเวลาสถิติสำคัญ")
    
    ticker_input = st.text_input("ระบุสัญลักษณ์หุ้นที่ต้องการค้นหาแนวรับ:", value="NVDA", key="tab5_ticker").upper().strip()
    
    if ticker_input:
        with st.spinner("กำลังคำนวณและประมวลผลแนวรับทางเทคนิค..."):
            try:
                stock = yf.Ticker(ticker_input)
                df_hist = stock.history(period="2y")
            except:
                df_hist = pd.DataFrame()
                
            if not df_hist.empty and len(df_hist) >= 200:
                current_price = float(df_hist['Close'].iloc[-1])
                
                ema20 = float(df_hist['Close'].ewm(span=20, adjust=False).mean().iloc[-1])
                ema50 = float(df_hist['Close'].ewm(span=50, adjust=False).mean().iloc[-1])
                ema100 = float(df_hist['Close'].ewm(span=100, adjust=False).mean().iloc[-1])
                ema200 = float(df_hist['Close'].ewm(span=200, adjust=False).mean().iloc[-1])
                
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.metric(label="ชื่อบริษัทหลักทรัพย์", value=str(stock.info.get('longName', ticker_input)))
                with col_p2:
                    st.metric(label="ราคาซื้อขายล่าสุดในตลาด", value=f"${current_price:,.2f}")
                st.markdown("---")
                
                if current_price < ema200:
                    st.error(f"สถานะเทคนิคของหุ้น {ticker_input}: หุ้นตัวนี้เป็นขาลงไม่มีแนวรับ (เนื่องจากราคาวิ่งต่ำกว่าเส้นระยะยาว EMA 200 วัน)")
                else:
                    st.success(f"สถานะเทคนิคของหุ้น {ticker_input}: หุ้นยังคงเป็นแนวโน้มขาขึ้นหรือประคองตัวเหนือเส้นระยะยาวได้")
                    
                st.markdown("#### ตารางวิเคราะห์กรอบแนวรับสำคัญทางสถิติ")
                col_ema1, col_ema2, col_ema3, col_ema4 = st.columns(4)
                
                with col_ema1:
                    st.metric(label="แนวรับที่ 1 (EMA 20 วัน)", value=f"${ema20:,.2f}", delta=f"{((ema20 - current_price)/current_price)*100:+.2f}%")
                    st.caption("แนวรับระยะสั้นช่วง Momentum")
                    
                with col_ema2:
                    st.metric(label="แนวรับที่ 2 (EMA 50 วัน)", value=f"${ema50:,.2f}", delta=f"{((ema50 - current_price)/current_price)*100:+.2f}%")
                    st.caption("แนวรับระยะกลางคอยรับแรงย่อ")
                    
                with col_ema3:
                    st.metric(label="แนวรับที่ 3 (EMA 100 วัน)", value=f"${ema100:,.2f}", delta=f"{((ema100 - current_price)/current_price)*100:+.2f}%")
                    st.caption("แนวรับทางจิตวิทยาก่อนเสียทรง")
                    
                with col_ema4:
                    st.metric(label="แนวรับสุดท้าย (EMA 200 วัน)", value=f"${ema200:,.2f}", delta=f"{((ema200 - current_price)/current_price)*100:+.2f}%")
                    st.caption("แนวรับเส้นแบ่งเทรนหลักซื้อมูลค่า")
            else:
                st.error("ไม่สามารถดึงข้อมูลหุ้นดังกล่าวได้ หรือข้อมูลประวัติราคาซื้อขายย้อนหลังมีไม่เพียงพอต่อการคำนวณกรอบเทคนิค 200 วัน")

# -----------------------------------------------------------------
# TAB 6: เป้าหมายการลงทุน (Investment Goals & Compound Plan)
# -----------------------------------------------------------------
with tab6:
    st.markdown("""
        <style>
            .goal-card {
                background-color: #1e293b;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #334155;
                margin-bottom: 20px;
            }
            .goal-header {
                color: #f8fafc;
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 5px;
            }
            .goal-subtitle {
                color: #94a3b8;
                font-size: 14px;
                margin-bottom: 20px;
            }
            .section-title {
                color: #38bdf8;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="goal-header">Investment Goal Tracker</p>', unsafe_allow_html=True)
    st.markdown('<p class="goal-subtitle">แบบจำลองและวางแผนเส้นทางการลงทุนทบต้นรายเดือน มุ่งสู่เป้าหมายทางการเงินอย่างเป็นระบบ</p>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="goal-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">การตั้งค่าแผนการลงทุน</p>', unsafe_allow_html=True)
    
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        start_balance = st.number_input("เงินต้นตั้งต้น (บาท)", min_value=0.0, value=30000.0, step=5000.0)
        target_balance = st.number_input("เป้าหมายมูลค่าพอร์ตสูงสุด (บาท)", min_value=1.0, value=1000000.0, step=50000.0)
    with col_in2:
        monthly_yield = st.number_input("คาดการณ์ผลตอบแทนต่อเดือน (%)", min_value=0.0, value=2.0, step=0.5)
        monthly_deposit = st.number_input("เงินสมทบเติมเพิ่มรายเดือน (บาท)", min_value=0.0, value=10000.0, step=1000.0)
    with col_in3:
        start_date = st.date_input("วันที่เริ่มต้นดำเนินตามแผน")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if target_balance > start_balance:
        plan_data = []
        current_m_balance = start_balance
        current_date = start_date
        month_count = 1
        max_months_safety = 600
        
        while current_m_balance < target_balance and month_count <= max_months_safety:
            interest = current_m_balance * (monthly_yield / 100)
            end_balance = current_m_balance + interest + monthly_deposit
            
            plan_data.append({
                "Month": f"เดือนที่ {month_count}",
                "Date": current_date.strftime("%d/%m/%Y"),
                "Beginning (฿)": current_m_balance,
                "Profit (฿)": interest,
                "Monthly Deposit (฿)": monthly_deposit,
                "Ending (฿)": end_balance,
                "Month_Key": f"m_{month_count}_{current_date.strftime('%Y%m')}"
            })
            
            current_m_balance = end_balance
            current_date = current_date + pd.Timedelta(days=30)
            month_count += 1
            
        df_plan = pd.DataFrame(plan_data)
        
        if 'goal_checkboxes' not in st.session_state:
            st.session_state.goal_checkboxes = {}
            
        df_plan["Status"] = df_plan["Month_Key"].map(lambda x: st.session_state.goal_checkboxes.get(x, False))
        df_display = df_plan[["Status", "Month", "Date", "Beginning (฿)", "Profit (฿)", "Monthly Deposit (฿)", "Ending (฿)", "Month_Key"]]

        st.markdown('<div class="goal-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">ตารางวิเคราะห์แผนงานและเช็คลิสต์ประจำงวด</p>', unsafe_allow_html=True)
        st.info(f"จากเงินต้นตั้งต้น ฿{start_balance:,.2f} ไปถึงเป้าหมาย ฿{target_balance:,.2f} คาดว่าต้องใช้ระยะเวลาในการลงทุนรวมทั้งสิ้น {len(df_plan)} เดือน")
        
        edited_df = st.data_editor(
            df_display,
            column_config={
                "Status": st.column_config.CheckboxColumn(
                    "สำเร็จแล้ว?",
                    help="ทำเครื่องหมายถูกเมื่อคุณออมเงินและทำกำไรได้สำเร็จตามเป้าหมายของงวดเดือนนี้แล้ว",
                    default=False,
                ),
                "Month": st.column_config.TextColumn("งวดงบประมาณ", disabled=True),
                "Date": st.column_config.TextColumn("กำหนดเวลา", disabled=True),
                "Beginning (฿)": st.column_config.NumberColumn("เงินต้นงวด", format="฿%,.2f", disabled=True),
                "Profit (฿)": st.column_config.NumberColumn("กำไรเป้าหมาย", format="฿%,.2f", disabled=True),
                "Monthly Deposit (฿)": st.column_config.NumberColumn("เงินเติมสมทบ", format="฿%,.2f", disabled=True),
                "Ending (฿)": st.column_config.NumberColumn("เงินปลายงวดสะสม", format="฿%,.2f", disabled=True),
                "Month_Key": None
            },
            use_container_width=True,
            hide_index=True,
            key="goal_editor_formal"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        for idx, row in edited_df.iterrows():
            m_key = row["Month_Key"]
            st.session_state.goal_checkboxes[m_key] = row["Status"]
            
        total_months = len(df_plan)
        current_plan_keys = df_plan["Month_Key"].tolist()
        completed_months = sum(1 for k, val in st.session_state.goal_checkboxes.items() if k in current_plan_keys and val is True)
        progress_percent = (completed_months / total_months) if total_months > 0 else 0.0
        
        st.markdown('<div class="goal-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">สรุปความคืบหน้าของแผนการลงทุน (Overall Progress)</p>', unsafe_allow_html=True)
        st.progress(min(progress_percent, 1.0))
        st.success(f"ดำเนินการสำเร็จเสร็จสิ้นแล้ว {completed_months} เดือน จากแผนงานทั้งหมด {total_months} เดือน (คิดเป็นความสำเร็จ {progress_percent*100:.2f}%)")
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.warning("กรุณากำหนดระดับ 'เป้าหมายมูลค่าพอร์ตสูงสุด' ให้สูงกว่า 'เงินต้นตั้งต้น' เพื่อเริ่มระบบประมวลผลตารางแผนงาน")
