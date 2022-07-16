from xgboost.sklearn import XGBRegressor as xgb
import load_data as load_data
from sklearn.inspection import partial_dependence
from PIL import Image
import streamlit as st
import plotly.express as px
import os
from fpdf import FPDF

from explainerdashboard import RegressionExplainer, ExplainerDashboard
import streamlit.components.v1 as components
import shutil
import numpy as np

from downloader import get_binary_file_downloader_html

shutil.rmtree('./images')
if not os.path.exists("images"):
    os.mkdir("images")

favicon = Image.open("./favicon.png")
st.set_page_config(layout="wide", page_title='AIFE', page_icon=favicon)

hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.title('AIFE Analyser')


logo = Image.open('./Logo.png')
st.image(logo, width=200)
# st.markdown("<p style='text-align: center; color: black;'><b>AI</b> <b>D</b>evelopment, <b>E</b>xplainability, and <b>A</b>bstraction  \n <br> <small><i>Minimalistic No-Code platform to convert your AI Ideas into Reality</i></small></p>", unsafe_allow_html=True)

file = None
df = None
file = st.file_uploader("Upload File", type=["csv", "tsv", "xls", "xlsx"])

if(file is None):
    st.write("1. Upload any csv, tsv, xls or xlsx file.")
    st.write("2. Choose the target variable.")
    st.write("3. Select columns to ignore.")
    st.markdown("4. <i>Run Experiment</i> and Train your model within minutes <i>(Feature Engineering & Training will be done automatically)</i>.", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<small><center><i>Note: Trained Models should not be used in production using current version of Tool.</i></center></small>", unsafe_allow_html=True)

if file is not None:
    DataLoder = load_data.DataLoader()
    df = DataLoder.load_data("upload", file_name=file)
    # if any column contains a row that is not numeric give an option to ignore that column or drop that row
    # st.write( df[~df.applymap(np.isreal).all(1)].astype(str))


if df is not None:
    with st.expander("Show Data"):
        col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
        with col2:
            st.dataframe(df.astype(str))

    _, col1, col2, col3 = st.columns([0.1, 0.4, 0.4, 0.1])
    target = "--SELECT--"
    ignore_cols = []
    with col1:
        target = st.selectbox("Select target variable", [
                              "--SELECT--"]+[x for x in df.columns])
    with col2:
        ignore_cols = st.multiselect("Select Columns to Ignore", [
                                     x for x in df.columns])

    if(len(ignore_cols) > 0):
        df = df.drop(ignore_cols, axis=1)

    if(target != "--SELECT--"):
        Y = df[target]
        X = df.drop(target, axis=1)

        model = None
        with col3:
            st.markdown("<br/>", unsafe_allow_html=True)
            start = st.button("Generate analysis")
        if start:
            model = xgb()
            with st.spinner("Training Model..."):
                model.fit(X._get_numeric_data(), np.ravel(Y, order='C'))

        if model is not None:
            st.subheader("Partial Dependence Plots")
            with st.spinner('Generating Partial Dependancy Plots (This may take some time) ...'):
                with st.expander("Partial Dependancy Plots"):
                    st_cols = st.columns([0.5, 0.5])
                    i = 0
                    j = 0
                    for col in X.columns:
                        with st_cols[i]:
                            pardep = partial_dependence(model, X, col)
                            line_plot = px.line(x=pardep[1][0], y=pardep[0][0], title=f"{target} vs {col}", labels={
                                                'x': col.upper(), 'y': target.upper()}, line_shape='spline')
                            path_name = str(col).replace(
                                "\\", "-").replace("/", "-").replace(" ", "-").replace(".", "-")
                            line_plot.write_image(
                                f"images/{j}_{path_name}.png")
                            st.plotly_chart(line_plot)
                            i = (i+1) % 2
                            j += 1
                        with st_cols[i]:
                            box_plot = px.box(
                                X, y=col, title=f"{col} Distribution", points='all')
                            path_name = str(col).replace(
                                "\\", "-").replace("/", "-").replace(" ", "-").replace(".", "-")
                            line_plot.write_image(
                                f"images/{j}_{path_name}.png")
                            st.plotly_chart(box_plot)
                            i = (i+1) % 2
                            j += 1

                    pdf = FPDF()
                    for image in os.listdir("images"):
                        pdf.add_page()
                        pdf.image(f"images/{image}", 10, 10, 200, 100)

                    pdf.output("report.pdf", "F")
                    st.markdown(get_binary_file_downloader_html(
                        "report.pdf", "report"), unsafe_allow_html=True)

            st.subheader("XAI Dashboard")
            with st.spinner('Creating Explainability Dashboard... (may take some time)'):
                with st.expander("Show XAI Dashboard"):
                    explainer = RegressionExplainer(model, X, Y,
                                                    n_jobs=4,
                                                    precision='float32',
                                                    )

                    db = ExplainerDashboard(explainer,
                                            title="Explainable AI Dashboard",
                                            shap_interaction=False,
                                            whatif=False,
                                            contributions=False,
                                            hide_poweredby=True,
                                            )

                    components.html(db.to_html(), scrolling=True, height=800)
                    st.text("\n")

st.markdown("<small><center><b>Made with ❤️ by Naval Surange</b></center></small>",
                unsafe_allow_html=True)