import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CSV Data Visualizer", layout="wide")

st.title("CSV Data Visualizer")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        st.subheader("Data Analysis & Visualization")
        
        # Identify columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        st.write(f"**Numeric Columns:** {', '.join(numeric_cols)}")
        st.write(f"**Categorical Columns:** {', '.join(categorical_cols)}")
        
        # Visualization Logic
        if len(numeric_cols) >= 2:
            st.write("### Scatter Plot (Numeric vs Numeric)")
            x_axis = st.selectbox("Select X-axis", numeric_cols, index=0)
            y_axis = st.selectbox("Select Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
            color_col = st.selectbox("Select Color (Optional)", ["None"] + categorical_cols)
            
            color = None if color_col == "None" else color_col
            
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color, title=f"{y_axis} vs {x_axis}")
            st.plotly_chart(fig, use_container_width=True)

        if len(numeric_cols) > 0:
            st.write("### Histogram / Distribution")
            hist_col = st.selectbox("Select Column for Histogram", numeric_cols)
            fig_hist = px.histogram(df, x=hist_col, title=f"Distribution of {hist_col}")
            st.plotly_chart(fig_hist, use_container_width=True)
            
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            st.write("### Bar Chart (Categorical vs Numeric)")
            cat_x = st.selectbox("Select Category", categorical_cols)
            num_y = st.selectbox("Select Numeric Value", numeric_cols)
            agg_func = st.selectbox("Aggregation", ["mean", "sum", "count"])
            
            if agg_func == "count":
                df_grouped = df.groupby(cat_x).size().reset_index(name='count')
                fig_bar = px.bar(df_grouped, x=cat_x, y='count', title=f"Count by {cat_x}")
            else:
                df_grouped = df.groupby(cat_x)[num_y].agg(agg_func).reset_index()
                fig_bar = px.bar(df_grouped, x=cat_x, y=num_y, title=f"{agg_func.capitalize()} of {num_y} by {cat_x}")
            
            st.plotly_chart(fig_bar, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Awaiting CSV file to be uploaded.")
