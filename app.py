import streamlit as st

# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simple tools from Devcore",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Home page content
# -----------------------------------------------------------------------------
st.title("📊 Simple tools from Devcore")
st.markdown("### Your one-stop solution for CSV file manipulation and analysis")

st.divider()

# Feature overview
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ## 🗂 CSV Combiner & Column Editor
    
    **Perfect for data consolidation and enhancement**
    
    ✅ **Combine multiple CSV files** into a single dataset  
    ✅ **Add new columns** with custom default values  
    ✅ **variable system** - Use `{column_name}` to reference other columns  
    ✅ **Bulk value updates** - Set values for entire columns at once  
    ✅ **Data preview** and column statistics  
    ✅ **Download combined results** as CSV  
    
    **Example variable usage:**
    - `mr. {firstname} {lastname}` → "mr. John Smith"
    - `Order #{order_id} - {customer}` → "Order #12345 - Jane Doe"
    """)

with col2:
    st.markdown("""
    ## 📊 CSV Row Comparison Tool
    
    **Find differences between datasets**
    
    ✅ **Compare two groups** of CSV files  
    ✅ **Find missing rows** - Identify entries in Group B not present in Group A  
    ✅ **Flexible column matching** - Compare any columns between groups  
    ✅ **Summary statistics** - Match rates and totals  
    ✅ **Export results** - Download missing rows as CSV  
    
    **Common use cases:**
    - Find leads you haven't contacted yet
    - Identify new entries in updated datasets  
    - Compare inventory lists
    - Audit data completeness
    """)

st.divider()

# Quick start guide
st.markdown("""
## 🚀 Quick Start Guide

1. **Choose your tool** from the sidebar on the left
2. **Upload your CSV files** using the file uploader
3. **Follow the on-screen instructions** for each tool
4. **Download your results** when ready

---

### 💡 Tips for Best Results

- **File formats**: Only CSV files are supported
- **Column names**: Make sure your CSV files have clear, consistent column headers
- **File size**: For large files, processing may take a few moments
- **Variables**: Use curly braces `{column_name}` to reference other columns in the combiner tool
- **Encoding**: UTF-8 encoding is recommended for international characters

---

### 🔧 Technical Details

- Built with **Streamlit** for an interactive web interface
- Uses **pandas** for efficient data processing
- Supports **multiple file uploads** simultaneously
- **Session state management** keeps your data between page switches
- **Real-time preview** of your data transformations

---

*Select a tool from the sidebar to get started!*
""")

# Footer
st.markdown("---")
st.markdown("*CSV Tools Hub - Making data manipulation simple and efficient*") 
