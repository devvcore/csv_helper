import streamlit as st
import pandas as pd
import io

# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(page_title="CSV Combiner & Column Editor", page_icon="🗂")

st.title("🗂 CSV Combiner & Column Editor")
st.write("Upload multiple CSV files to combine them, add new columns, and edit column values with optional Variables.")

# -----------------------------------------------------------------------------
# File upload
# -----------------------------------------------------------------------------
uploaded_files = st.file_uploader(
    "Choose CSV files",
    accept_multiple_files=True,
    type=["csv"],
    key="combiner_files",
)

# We'll store the combined dataframe in the session state under its own key to
# avoid clashes with other pages.
SESSION_KEY = "combiner_df"

if uploaded_files:
    # Combine files only the first time or if we haven't done so yet.
    if SESSION_KEY not in st.session_state:
        dataframes = []
        for file in uploaded_files:
            try:
                df = pd.read_csv(file)
                dataframes.append(df)
                st.success(f"Loaded {file.name} (rows: {len(df)}, cols: {len(df.columns)})")
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")

        if dataframes:
            try:
                combined_df = pd.concat(dataframes, ignore_index=True)
                st.session_state[SESSION_KEY] = combined_df.copy()
                st.success(f"Combined {len(dataframes)} file(s) → **{len(combined_df)}** total rows")
            except Exception as e:
                st.error(f"Error combining files: {e}")
    else:
        combined_df = st.session_state[SESSION_KEY]

    # -------------------------------------------------------------------------
    # Dataset overview
    # -------------------------------------------------------------------------
    st.subheader("Current Dataset")
    st.write(f"Shape: {combined_df.shape[0]} rows × {combined_df.shape[1]} columns")

    # -------------------------------------------------------------------------
    # Column management
    # -------------------------------------------------------------------------
    st.subheader("Column Management")

    # Add new column ----------------------------------------------------------
    with st.expander("➕ Add New Column"):
        new_col_name = st.text_input("Column name", key="new_col_name")
        default_val = st.text_input("Default value (optional)", key="new_col_default")

        if st.button("Add Column", key="add_col_btn"):
            if not new_col_name:
                st.error("Please provide a column name.")
            elif new_col_name in combined_df.columns:
                st.error("Column already exists.")
            else:
                st.session_state[SESSION_KEY][new_col_name] = default_val
                st.success(f"Added column **{new_col_name}** with default '{default_val}'")

    # Set values for all rows --------------------------------------------------
    with st.expander("✏️ Set Values for All Rows"):
        cols = list(combined_df.columns)
        target_col = st.selectbox("Select column to modify", cols, key="set_val_col")
        variable_val = st.text_input(
            "Value or variable (use {column_name} placeholders)",
            help="Example: 'mr. {firstname} {lastname}'",
            key="variable_val_input",
        )

        st.write("Available variables:", ", ".join([f"{{{col}}}" for col in cols]))

        if st.button("Apply", key="apply_val_btn") and variable_val is not None:
            if "{" in variable_val and "}" in variable_val:
                # variable mode
                try:
                    formatted = []
                    for _, row in combined_df.iterrows():
                        mapping = {col: ("" if pd.isna(row[col]) else str(row[col])) for col in cols}
                        formatted.append(variable_val.format(**mapping))
                    st.session_state[SESSION_KEY][target_col] = formatted
                    st.success(f"Applied variable to column **{target_col}**")
                except KeyError as e:
                    st.error(f"variable references unknown column: {e.args[0]}")
                except Exception as ex:
                    st.error(f"Error applying variable: {ex}")
            else:
                # Static value mode
                try:
                    # Convert numeric strings to numbers where appropriate
                    if variable_val.replace(".", "").replace("-", "").isdigit():
                        variable_val = float(variable_val) if "." in variable_val else int(variable_val)
                except Exception:
                    pass
                st.session_state[SESSION_KEY][target_col] = variable_val
                st.success(f"Set all rows in **{target_col}** to '{variable_val}'")

    # -------------------------------------------------------------------------
    # Preview & download
    # -------------------------------------------------------------------------
    st.subheader("Preview")
    st.dataframe(st.session_state[SESSION_KEY].head(10), use_container_width=True)

    st.subheader("Column Info")
    info_df = pd.DataFrame({
        "Column": combined_df.columns,
        "Data Type": combined_df.dtypes.astype(str).values,
        "Non-null": combined_df.count().values,
        "Null": combined_df.isnull().sum().values,
    })
    st.dataframe(info_df, use_container_width=True)

    st.subheader("Download")
    buffer = io.StringIO()
    st.session_state[SESSION_KEY].to_csv(buffer, index=False)
    st.download_button(
        "⬇️ Download Combined CSV",
        data=buffer.getvalue(),
        file_name="combined_data.csv",
        mime="text/csv",
    )

    if st.checkbox("Show full dataframe", key="show_full_df"):
        st.dataframe(st.session_state[SESSION_KEY], use_container_width=True)
else:
    st.info("👆 Upload one or more CSV files to get started.") 