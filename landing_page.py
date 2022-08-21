import enum
import streamlit as st
from helplines import HELPLINES

st.set_page_config(
    page_title="In Sight, In Mind",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://www.beyondblue.org.au/',
        'Report a bug': "https://www.govhack.org",
        'About': "# In Sight, In Mind"
    }
)

st.error("If you are facing a medical emergency, __call 000 now__.", icon="🚨")

st.info("""
__Do you need someone to talk to?__\n
At anytime, you can call Lifeline on _13 11 14_ or BeyondBlue on _1300 22 4636_.
""", icon="🌟")

st.markdown("""
## Welcome to **In Sight, In Mind** ![](https://img.icons8.com/bubbles/100/hospital.png)
This app will help you find the nearest ED or alternatives.

### How It Works
1. In the next page, you will be able to provide your location or enter an address.
2. The page will automatically update and show you nearby clinics, and the ED with the lowest wait time.
"""
)

next = st.button("Find an ED")


st.markdown("""
---
### Support Services ![](https://img.icons8.com/clouds/1x/hospital.png)
""")


regions = list(HELPLINES.keys())
for i, tab in enumerate(st.tabs(regions)):
    with tab:
        region = regions[i]
        st.header(f"{region}")
        for service, info in HELPLINES[region].items():
            st.markdown(f"""
            **{service}**  
            Main areas: {", ".join(info["purpose"]).title()}  
            Contact: {info['contact_number']}
            """)