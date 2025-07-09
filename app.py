import streamlit as st
import pandas as pd
import io


def main():
    st.title("CSV Combiner & Column Editor")
    st.write("Upload multiple CSV files to combine them and add/edit columns")

    # File upload
    uploaded_files = st.file_uploader(
        "Choose CSV files",
        accept_multiple_files=True,
        type=['csv']
    )

    if uploaded_files:
        # If we haven't processed these files before, or if combined_df is missing, combine them
        if 'combined_df' not in st.session_state:
            dataframes = []
            for file in uploaded_files:
                try:
                    df = pd.read_csv(file)
                    dataframes.append(df)
                    st.success(f"Loaded {file.name} with {len(df)} rows & {len(df.columns)} columns")
                except Exception as e:
                    st.error(f"Error reading {file.name}: {str(e)}")

            if dataframes:
                try:
                    combined_df = pd.concat(dataframes, ignore_index=True)
                    st.session_state.combined_df = combined_df.copy()
                    st.success(f"Combined {len(dataframes)} files into {len(combined_df)} total rows")
                except Exception as e:
                    st.error(f"Error combining files: {str(e)}")
                    return
        else:
            combined_df = st.session_state.combined_df

        # Display current dataframe info
        st.subheader("Current Dataset")
        st.write(f"Shape: {combined_df.shape[0]} rows × {combined_df.shape[1]} columns")

        # Column management section
        st.subheader("Column Management")

        # Add new columns
        with st.expander("Add New Columns"):
            new_column_name = st.text_input("New column name")
            new_column_default = st.text_input("Default value for new column (optional)")

            if st.button("Add Column"):
                if new_column_name:
                    if new_column_name not in combined_df.columns:
                        st.session_state.combined_df[new_column_name] = new_column_default
                        st.success(f"Added column '{new_column_name}' with default value '{new_column_default}'")
                    else:
                        st.error("Column name already exists")
                else:
                    st.error("Please enter a column name")

        # Set values for all rows in any column
        with st.expander("Set Values for All Rows"):
            current_columns = list(combined_df.columns)
            selected_column = st.selectbox("Select column to modify", current_columns)
            new_value = st.text_input(
                "New value for all rows in this column",
                help="Use template syntax like 'mr. {firstname} {lastname}' to reference other columns"
            )

            # Show available columns for template reference
            st.write("Available columns for templates:", ", ".join(current_columns))

            if st.button("Set Value for All Rows"):
                if selected_column and new_value is not None:
                    # Template mode
                    if '{' in new_value and '}' in new_value:
                        try:
                            formatted_values = []
                            for _, row in combined_df.iterrows():
                                template_dict = {col: ("" if pd.isna(row[col]) else str(row[col])) for col in current_columns}
                                formatted_values.append(new_value.format(**template_dict))
                            st.session_state.combined_df[selected_column] = formatted_values
                            st.success(f"Applied template to column '{selected_column}'")
                        except KeyError as e:
                            st.error(f"Column '{e.args[0]}' not found in data")
                        except Exception as e:
                            st.error(f"Error applying template: {str(e)}")
                    else:
                        # Static value mode
                        try:
                            if new_value.replace('.', '').replace('-', '').isdigit():
                                new_value = float(new_value) if '.' in new_value else int(new_value)
                        except:
                            pass
                        st.session_state.combined_df[selected_column] = new_value
                        st.success(f"Set all rows in column '{selected_column}' to '{new_value}'")

        # Display the current dataframe
        st.subheader("Preview of Combined Data")
        st.write("First 10 rows:")
        st.dataframe(st.session_state.combined_df.head(10))

        # Show data types
        st.write("Column Data Types:")
        col_info = pd.DataFrame({
            'Column': combined_df.columns,
            'Data Type': combined_df.dtypes.astype(str).values,
            'Non-null Count': combined_df.count().values,
            'Null Count': combined_df.isnull().sum().values
        })
        st.dataframe(col_info)

        # Download section
        st.subheader("Download Combined Data")
        csv_buffer = io.StringIO()
        st.session_state.combined_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Combined CSV",
            data=csv_buffer.getvalue(),
            file_name="combined_data.csv",
            mime="text/csv"
        )

        # Show full dataframe (optional)
        if st.checkbox("Show full dataframe"):
            st.dataframe(st.session_state.combined_df)

    else:
        st.info("Please upload one or more CSV files to get started")


if __name__ == "__main__":
    main() 