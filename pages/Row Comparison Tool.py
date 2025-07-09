import pandas as pd
import streamlit as st


def combine_dataframes(uploaded_files, column_name):
    """
    Combine multiple CSV files into a single DataFrame, optionally keeping only the specified column.
    """
    if not uploaded_files:
        return None

    dfs = []
    for file in uploaded_files:
        df = pd.read_csv(file)
        if column_name:
            df = df[[column_name]]
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def compare_csv_columns(df1, df2, col1_name, col2_name):
    """
    Compare values between two CSV groups to find entries in df2 that don't exist in df1.

    Args:
        df1 (DataFrame): Reference DataFrame (Group A)
        df2 (DataFrame): Target DataFrame   (Group B)
        col1_name (str): Column name in reference DataFrame
        col2_name (str): Column name in target DataFrame

    Returns:
        DataFrame: Rows from df2 where col2 values are not in df1[col1]
    """
    reference_values = set(df1[col1_name].unique())
    return df2[~df2[col2_name].isin(reference_values)]


# Streamlit page settings -----------------------------------------------------
st.set_page_config(page_title="CSV Row Comparison Tool", page_icon="📊")

st.title("📊 CSV Row Comparison Tool")

st.markdown(
    """
    ## What this page does
    **Find rows from **Group B** that are **NOT** present in **Group A**.**

    **Example:**
    - Group A contains people you **already contacted** → *John, Mary, Bob*
    - Group B is your **lead list** → *John, Mary, Sarah, Mike*
    - **Result** → *Sarah, Mike* (leads you haven't contacted yet)
    """
)

st.divider()

# Two-column layout for file uploaders ---------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Group A: Reference Files (Compare Against)")
    st.caption("Upload your *master list* or reference CSV files")
    files1 = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True, key="files1")

with col2:
    st.subheader("Group B: Target Files (Check These)")
    st.caption("Upload CSV files you want to check against Group A")
    files2 = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True, key="files2")

# Main logic ------------------------------------------------------------------
if files1 and files2:
    df1 = combine_dataframes(files1, None)
    df2 = combine_dataframes(files2, None)

    if df1 is not None and df2 is not None:
        st.success(f"Group A → {len(files1)} file(s) • **{len(df1)}** rows total")
        st.success(f"Group B → {len(files2)} file(s) • **{len(df2)}** rows total")

        st.markdown("### Select columns to compare")
        col_ref = st.selectbox("Column from Group A (reference)", df1.columns, key="ref_col")
        col_tgt = st.selectbox("Column from Group B (to check)", df2.columns, key="tgt_col")

        if st.button("🔍 Find rows NOT in Group A", type="primary"):
            result_df = compare_csv_columns(df1, df2, col_ref, col_tgt)

            st.markdown("## Results: Rows from Group B **NOT** found in Group A")
            if result_df.empty:
                st.success("🎉 All rows from Group B were found in Group A!")
            else:
                st.warning(f"Found **{len(result_df)}** row(s) from Group B missing in Group A")
                st.dataframe(result_df, use_container_width=True)

                csv = result_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Missing Rows as CSV",
                    data=csv,
                    file_name="rows_not_in_group_a.csv",
                    mime="text/csv",
                    type="primary",
                )

            # Summary metrics
            st.markdown("### Summary Statistics")
            c1, c2, c3 = st.columns(3)
            c1.metric("Group A Total", len(df1))
            c2.metric("Group B Total", len(df2))
            c3.metric("Missing from A", len(result_df))

            if len(df2) > 0:
                match_rate = ((len(df2) - len(result_df)) / len(df2)) * 100
                st.write(f"**Match Rate:** {match_rate:.1f}% of Group B rows were found in Group A")
else:
    st.info("👆 Please upload CSV files to **both** groups to begin comparison.") 