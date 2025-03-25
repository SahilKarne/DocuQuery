import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import io

load_dotenv()
history = []
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-pro')

def chat_with_pdf(text, prompt):
    pdf_text = ""
    for data in text:
        pdf_text += data
    response = model.generate_content(prompt + " The pdf document text is given as: " + pdf_text)
    history.append([prompt, response.text])
    return response.text

def chat_with_csv(df, prompt):
    # Create a description of the dataframe
    df_info = f"DataFrame shape: {df.shape}\n"
    df_info += f"Columns: {', '.join(df.columns.tolist())}\n"
    df_info += f"Sample data (first 5 rows):\n{df.head().to_string()}\n"

    # Send to Gemini
    query = f"""Based on the following dataframe:
    {df_info}

    Answer this question: {prompt}

    Provide detailed analysis and explanations.
    """

    response = model.generate_content(query)
    history.append([prompt, response.text])
    return response.text

def generate_simple_plot(df, query):
    """Generate a simple plot based on the query"""
    try:
        # Ask Gemini for plotting instructions
        plot_query = f"""
        Given this DataFrame with columns: {', '.join(df.columns.tolist())}
        And sample data: {df.head().to_string()}

        For the query: "{query}"

        Generate Python code using only matplotlib.pyplot to create an appropriate visualization.
        Return ONLY executable Python code without explanations.
        The code should:
        1. Select relevant columns from the dataframe
        2. Create a simple but informative plot (bar, line, scatter, etc.) based on the query
        3. Add appropriate labels and title
        4. Not use plt.show()

        The code will be executed directly with the 'df' variable already available.
        """

        response = model.generate_content(plot_query)
        plot_code = response.text

        # Clean up the code if it's wrapped in markdown code blocks
        if "python" in plot_code:
            plot_code = plot_code.split("python")[1].split("")[0].strip()
        elif "" in plot_code:
            plot_code = plot_code.split("```")[1].strip()

        # Create a new figure
        plt.figure(figsize=(10, 6))

        # Execute the code with the dataframe
        exec_vars = {'df': df, 'plt': plt}
        exec(plot_code, globals(), exec_vars)

        # Convert the plot to an image buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf, None

    except Exception as e:
        # If there's an error, return a simple default plot
        plt.figure(figsize=(10, 6))
        if df.select_dtypes(include=['number']).columns.any():
            # Get first numeric column
            numeric_col = df.select_dtypes(include=['number']).columns[0]
            df[numeric_col].plot(kind='bar')
            plt.title(f"Simple plot of {numeric_col}")
            plt.tight_layout()
        else:
            # No numeric columns, just show text
            plt.text(0.5, 0.5, "Could not create plot - no numeric data found",
                     horizontalalignment='center', verticalalignment='center')

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf, str(e)

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdf_file as file:
        reader = PdfReader(file)
        for page in reader.pages:
            st_text = page.extract_text()
            text += st_text
    return text

def display_history():
    if history:
        for i, entry in enumerate(history):
            if len(entry) == 2:
                st.write(f"Query {i+1}: {entry[0]}")
                st.write(f"Response: {entry[1]}")
                st.markdown("---")
            else:
                st.write("Invalid history entry at index", i)

# Page Configuration
st.set_page_config(layout="wide")
st.title("ChatWithFiles powered by LLM")

# CSV Section
all_csv = st.file_uploader("Upload your CSV file", type=['csv'], accept_multiple_files=True)

if all_csv:
    selected_file = st.selectbox("Select a CSV file", [file.name for file in all_csv])
    selected_index = [file.name for file in all_csv].index(selected_file)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("CSV uploaded successfully")
        data = []
        for file in all_csv:
            data.append(pd.read_csv(file))
        st.dataframe(data[selected_index])

    with col2:
        st.info("Chat with your CSV")
        input_text = st.text_area("Enter your query", key="csv_query")
        if input_text and input_text.strip():
            col1, col2 = st.columns([1, 4])
            if col1.button("Ask Query", key="ask_query_csv"):
                st.info("Your query: " + input_text)
                result = chat_with_csv(data[selected_index], input_text)
                st.download_button(
                    label="Download Result as Text",
                    data=f"Query: {input_text}\nResult: {result}",
                    file_name="csv_result.txt",
                    mime="text/plain"
                )
                st.success(result)

            if col2.button("Plot Graph"):
                st.info("Your query: " + input_text)
                plot_buffer, error = generate_simple_plot(data[selected_index], input_text)

                if error:
                    st.warning(f"Generated a simple plot due to error: {error}")

                st.image(plot_buffer, caption=f"Plot for: {input_text}")

                # Add download button for the plot
                st.download_button(
                    label="Download Plot",
                    data=plot_buffer,
                    file_name="plot.png",
                    mime="image/png"
                )

# PDF Section
input_pdf = st.file_uploader("Upload your PDF file", type=['pdf'], accept_multiple_files=True)

if input_pdf:
    selected_pdf = st.selectbox("Select a PDF file", [file.name for file in input_pdf], key="pdf_selector")
    selected_pdf_index = [file.name for file in input_pdf].index(selected_pdf)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("PDF uploaded successfully")
        text = []
        for file in input_pdf:
            text.append(extract_text_from_pdf(file))

        st.text_area("PDF Text", text[selected_pdf_index], height=500)

    with col2:
        st.info("Chat with your PDF")
        input_text = st.text_area("Enter your query", key="pdf_query")
        if input_text and input_text.strip():
            if st.button("Ask Query", key="ask_query_pdf"):
                st.info(f"Your query: {input_text}")
                result = chat_with_pdf(text, input_text)
                st.download_button(
                    label="Download Result as Text",
                    data=f"Query: {input_text}\nResult: {result}",
                    file_name="pdf_result.txt",
                    mime="text/plain"
                )
                st.success(result)

# Display chat history at the bottom
st.markdown("## Chat History")
display_history()