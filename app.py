import streamlit as st
import pandas as pd
import sqlite3
import queries_handler

st.title("AI-Powered SQL Query Chatbot")

# Upload multiple files
uploaded_files = st.file_uploader("Upload CSV or XLSX files", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    table_dict = {}  # Dictionary to store table names and DataFrames
    conn = sqlite3.connect(":memory:")  # In-memory SQLite DB

    for file in uploaded_files:
        file_name = file.name.split(".")[0]  # Use filename as table name
        
        # Load file into DataFrame
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        df.to_sql(file_name, conn, index=False, if_exists="replace")  # Store in SQLite
        table_dict[file_name] = df  # Save DataFrame reference

    st.success(f"Uploaded {len(uploaded_files)} files successfully!")

    # Display table structure for reference
    for table, df in table_dict.items():
        st.write(f"**Table: {table}**")
        st.dataframe(df.head())  # Show preview of each table

    # Query input
    user_query = st.text_input("Ask a question in plain English:")

    if user_query:
        sql_query = queries_handler.nl_to_sql(user_query, table_dict)  # Convert NL to SQL
        
        if sql_query:
            st.write(f"**Generated SQL Query:** `{sql_query}`")
            result_df = pd.read_sql_query(sql_query, conn)  # Execute SQL
            st.dataframe(result_df)  # Display result
        else:
            st.error("Failed to generate SQL. Try rewording your question.")
