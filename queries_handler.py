import openai

def nl_to_sql(nl_query, table_dict):
    # Extract table structures for better SQL generation
    table_info = "\n".join([f"{table}: {', '.join(df.columns)}" for table, df in table_dict.items()])

    prompt = f"""
    You are an AI that converts natural language questions into SQL queries. 
    Available tables and their columns:
    {table_info}

    Generate an SQL query that answers the following question:
    "{nl_query}"
    Ensure to use appropriate JOINs if required.
    SQL Query:
    """

    try:
        client = openai.OpenAI(api_key=" =========== Your API KEYS GO HERE ===========")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        sql_query = response.choices[0].message.content.strip()
        return sql_query
    except Exception as e:
        print(f"Error: {e}")
        return None
