import streamlit as st
import pandas as pd
import openai
import plotly.express as px
from io import StringIO, BytesIO
import PyPDF2
import docx
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import base64
from collections import Counter

#######################
# Page configuration
st.set_page_config(
    page_title="APR Tools",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

################################
# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'cover'

if 'uploaded_files_content' not in st.session_state:
    st.session_state.uploaded_files_content = []

########################
# Cover page
def cover_page():

    st.markdown("""
        <style>
            html, body {
                height: 100%;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align:center;
            }
            .stButton>button {
                padding: 20px 40px;
                font-size: 30px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                margin-left:150px;
            }
        </style>
    """, unsafe_allow_html=True)

    file_ = open("cover_page.png", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(f"""
        <div style="
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            text-align: center; 
            width: 100vw;">
            <h1 style="font-size: 2.5rem; margin-bottom: 20px;">Welcome to Appraisal Performance Review Tools</h1>
            <img src="data:image/png;base64,{data_url}" style="max-width: 100%; height: auto; margin-bottom: 20px; display: block; margin-left: auto; margin-right: auto;" width="700">
            <div style="margin-top: 20px;">
    """, unsafe_allow_html=True)

    if st.button("Click here to Start"):
        st.session_state.page = 'main'
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

    
#######################
# Main page
def main_page():

    # Function to add a new row to the DataFrame
    def add_row(title, content, genre):
        new_row = pd.DataFrame({"Title": [title], "Content": [content], "Goals & KPIs": [genre]})
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

    # Function to generate chart data
    def chart_data():
        st.session_state.chartdata = pd.DataFrame(columns=["Goals & KPIs"])
        for i, row in st.session_state.data.iterrows():
            Goals = row["Goals & KPIs"]
            new_row = pd.DataFrame({"Goals & KPIs": [Goals]})
            st.session_state.chartdata = pd.concat([st.session_state.chartdata, new_row], ignore_index=True)
        
        df = st.session_state.chartdata.groupby(['Goals & KPIs']).size().reset_index(name='count')

        with col1:
            fig = px.bar(df, x='Goals & KPIs', y='count', title='Goals & KPIs Count', text='count', width=800, height=600)
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig)

        with col2:
            fig = px.pie(df, values='count', names='Goals & KPIs', title='Goals & KPIs Distribution', width=800, height=600)
            fig.update_traces(textinfo='percent+label')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig)
            
    # Preload Data
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame(columns=["Title", "Content", "Goals & KPIs"])
        add_row("Attended Design Thinking Course", "I have attended 3 days of Design Thinking Workshop", "Keep Learning and Putting Skills into Action")
        add_row("Attended Scrum Master Course", "I have attended scrum master course", "Keep Learning and Putting Skills into Action")
        add_row("CAM Initiative", "Successfully onboarded and managed CAM Agent as preparation for CAM integration to support WOG Active Directory automatios for staff movement which follow the best practices for security and technologies", "Digital Transformation and ICT Development")
        add_row("GCC 2.0 Migration", "Succesfully led the migration of GCC 2.0 for 4 projects (UMS, DMH, eCards and FPIM) and collabrated with the Central team and assisted in AWS configuration to speed up the migration", "Digital Transformation and ICT Development")
        add_row("MOF Budget 2023", "As the Deputy Budget PM, have assisted the Budget PM to manage, organize and coordinate with multiple workstreams to ensure the smooth and successful completion of the budget 2024.", "Digital Transformation and ICT Development")
        add_row("MOF Budget 2023", "As Google Analysis engineer and budget calculator cooridinator to collabrated with central team for implementation and also introduced MIRO board for budget QA to allowed the team collabrate more effectively.", "Digital Transformation and ICT Development")
        add_row("MOF GES Survey 2023", "During the last quarter, the team has exceeding the target indicates efficient project management and effective time prioritization. This demonstrates the team commitment to meeting deadlines and delivering high-quality outcomes within specified timeframes.", "Serving with Heart Commitment and Purpose")
        add_row("Effective Coordination and Strong Organizational Skills in Managing Sustainability Initiatives", "Grace has demonstrated strong organizational and communication skills by effectively managing the submission process for the MOF-Family’s sustainability initiatives for the FY23 GreenGov report. She has ensured that a diverse range of initiatives are proposed, reflecting various themes and meeting the requirement for a waste-related story. Grace ability to coordinate with different departments and his attention to detail in consolidating and presenting the information for clearance is commendable. Her proactive approach in seeking necessary approvals and keeping relevant parties informed highlights his commitment and efficiency in fulfilling his responsibilities.", "Thinking Clearly with Making Sound Judgements")

    st.markdown("<h1 style='text-align: center;'>Annual Performance Review Tool</h1>", unsafe_allow_html=True)

    # custom CSS
    st.markdown("""
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                color: #333;
            }
            div[data-testid="stSidebarNav"] {
                display: none;
            }
            .centered-title {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }
            .centered-button {
                display: flex;
                justify-content: center;
                text-align: center;
            }
            .stRadio > div {
                display: flex;
            }
            .stRadio div label {
                margin-right: 10px;
            }
            .css-1e5imcs {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .stButton button {
                display: block;
                margin: 0 auto;
            }
            .row-widget.stButton {
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # OpenAI API Key and Base URL 
    openai.api_key = 'sk-Cw3-TaO9avFy6K9GByFYlw'
    openai.base_url = 'https://litellm.launchpad.tech.gov.sg'

    st.subheader("Step 1 : Generate Contribution Insights")

    option = st.selectbox("Choose Your Input Method", ["Upload File", "Input Text"])

    def get_summary(content):
        try:    
            prompt = (
                "From the content please write a performance review and only return the summary without any title or Performance Review Summary:."
                f"{content}"
            )
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error getting summary: {e}")
            return ""

    # To decide which genre/goals the content belongs to
    def determine_genre(summary):
        try:
            prompt = f"""
                Based on the summary, identify one of the following genres: 
                    'Stakeholder Relationship Management, 
                    Digital Transformation and ICT Development, 
                    Thinking Clearly with Making Sound Judgements, 
                    Serving with Heart Commitment and Purpose, 
                    Keep Learning and Putting Skills into Action.'
                that best relates to the content and return the genre only.

                Descriptions:
                Thinking Clearly with Making Sound Judgements:
                 - You collect and analyse different sources of information to aid your assessment of the problem at hand.
                 - You consider and evaluate possible solutions and propose the most appropriate one.
                 - Combines related ideas into single, impactful statements
                 - Evaluate solutions and propose the most appropriate one
                 - Analyze diverse information sources to assess problems
                Serving with Heart Commitment and Purpose:
                 - Serve citizens with empathy while respecting standard operating procedures and policies.
                 - Prioritise work tasks to deliver on agency and whole-of-government outcomes.
                 - Show consideration for stakeholders by engaging them throughout a project and keeping them updated on plans and progress.
                Keep Learning and Putting Skills into Action:
                 - Proactively keep up with, and apply, new knowledge in your work domain.
                 - Seek and embrace learning opportunities for personal and professional growth within and beyond your work domain.
                 - Share your learnings with colleagues and encourage them to put new knowledge into practice.
                 - Knowledge sharing from your learning
                Stakeholder Relationship Management:
                 - Develop and enhance Ops-Tech relationship with stakeholders/partners.
                 - Adocate and drive adoption of GovTech strategies and products (e.g TechStack, GovTech Standard Products) to Policy, Ops and Business to meet organisational needs.
                Digital Transformation and ICT Development:
                 - Support CIO/ISM and DSM in driving Digital Transformation in the Agency and sector by leveraging ICT as a strategic tool.
                 
                 Summary:
                 {summary}
                
                Based on the summary above, the genre is:
            """
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error determining genre: {e}")
            return "Other"

    def auto_generate_title(content):
        try:
            prompt = f"Generate title that helps on the performance review for the following content and only return the title without mention any performance review"
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )
            return response.choices[0].message.content.strip('"')
        except Exception as e:
            st.error(f"Error generating title: {e}")
            return "Untitled"

    if option == "Upload File":
        uploaded_files = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"], accept_multiple_files=True)
        if uploaded_files:
            new_files_content = []

            for uploaded_file in uploaded_files:
                # Check if the file has been uploaded before
                if uploaded_file.name in [file["name"] for file in st.session_state.uploaded_files_content]:
                    continue 

                if uploaded_file.type == "application/pdf":
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    content = ""
                    for page in range(len(pdf_reader.pages)):
                        content += pdf_reader.pages[page].extract_text()

                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    doc = docx.Document(uploaded_file)
                    content = ""
                    for para in doc.paragraphs:
                        content += para.text

                else:
                    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                    content = stringio.read()

                new_files_content.append({
                    "name": uploaded_file.name,
                    "content": content
                })

            if new_files_content:
                st.session_state.uploaded_files_content.extend(new_files_content)
                for file_content in new_files_content:
                    content = file_content["content"]
                    if content:
                        summary = get_summary(content)
                        goals = determine_genre(summary)
                        title = auto_generate_title(content)
                        add_row(title, summary, goals)
                        st.success(f"Row added successfully from file with Goals & KPIs '{goals}'!")

    else:
        with st.form(key="text_input_form"):
            title = st.text_input("Project Title")
            content = st.text_area("Add Work Description Here", "")
            goals = st.selectbox("Select Goals & KPIs", 
                                 ["Stakeholder Relationship Management", 
                                  "Digital Transformation and ICT Development", 
                                  "Serving with Heart Commitment and Purpose", 
                                  "Thinking Clearly with Making Sound Judgements", 
                                  "Keep Learning and Putting Skills into Action"]) 
            submit = st.form_submit_button()
            if submit:
                if title and content and goals:
                    add_row(title, content, goals)
                    st.success(f"Row added successfully with Goals & KPIs '{goals}'!")
                else:
                    st.error("Please fill in all fields.")

    gb = GridOptionsBuilder.from_dataframe(st.session_state.data)
    gb.configure_pagination()
    gb.configure_default_column(editable=True, resizable=True, wrapText=True)
    gb.configure_column("Title", wrapText=True, autoHeight=True, autoWidth=True)
    gb.configure_column("Content", wrapText=True, autoHeight=True, autoWidth=True)
    gb.configure_column("Goals & KPIs", wrapText=True, autoHeight=True, autoWidth=True)
    gb.configure_grid_options(domLayout='normal')
    grid_options = gb.build()

    response = AgGrid(
        st.session_state.data,
        grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED, 
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        width='100%',
        theme='streamlit'
    )

    # Update the session state data with edited values
    st.session_state.data = pd.DataFrame(response['data'])

    col1, col2 = st.columns(2)
    chart_data()

    def get_openai_response(prompt):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": prompt,
                    }],                                     
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error getting OpenAI response: {e}")
            return ""

    st.subheader("Step 2 : Generate Summary")

    formatOption = st.selectbox(
        "Format",
        ("Summarise in Paragraph", "Summarise in Bullet Point"))

    lengthOption = st.selectbox(
        "Length",
        ("Default", "Within 200 words", "Within 100 words"))


    # To prompt according to the selected summarisation 
    if formatOption == "Summarise in Bullet Point":
        format_text = """
        1. Title of the project as the header.
        2. A brief description of the tasks done and achievements.
        3. Keep each summary focused.

        Use the format below for each project summary:
        [Title]
        - Tasks Done: [Brief description of tasks]
        - Achievements: [Key achievements]

        Make sure Project Name do not have bullet point and there is bullet point for Tasks Done and Achievements.
        Make sure that Project Name, Tasks Done and Achievements in bold.
        """
    else:
        format_text = """
        1. Title of the project as the header. 
        2. Description of the tasks done and achievements.

        Make sure there is no bullet point form in this format.
        """

    # To prompt according to the selected Length
    if lengthOption == "Default":
        length_text = "Please help to write detailed summary content for each section"
    else:
        length_text = f" Please make sure to only return the summary results with a maximum length of {lengthOption} for each Summary."


    prompt_template = f"""
        I need to summarize my performance review. Help me write it in good English to better show that I performed and met my KPIs. 
        Please provide summaries for each project or title in the format specified below.

        {format_text}
        {length_text}

        Please bold the project name and use line breaks. Make sure all the font size is consistent and only display the summary results.
    """

    # To set text color to goals title
    goal_colors = {
        "Stakeholder Relationship Management": "#FF6347",  
        "Digital Transformation and ICT Development": "#32CD32", 
        "Thinking Clearly with Making Sound Judgements": "#FFD700",  
        "Serving with Heart Commitment and Purpose": "#DA70D6",  
        "Keep Learning and Putting Skills into Action": "#FF4500"  
    }

    if 'expand_all' not in st.session_state:
        st.session_state.expand_all = False

    col1, col2, col3 = st.columns([3, 1, 3])

    with col2:
        if st.button("Generate Summary", key="get_response", help="Click to generate summaries", type="primary"):
            if 'data' in st.session_state:
                with st.spinner("Generating summaries, please wait..."):
                    goal_counter = Counter()
                    
                    # To store prompts for each goal
                    prompts = {
                        "Stakeholder Relationship Management": "",
                        "Digital Transformation and ICT Development": "",
                        "Thinking Clearly with Making Sound Judgements": "",
                        "Serving with Heart Commitment and Purpose": "",
                        "Keep Learning and Putting Skills into Action": ""
                    }
                    
                    for row in st.session_state.data.itertuples():
                        Goals = getattr(row, '_3') # Getting Goals and KPIs using row number 3
                        title = row.Title
                        content = row.Content

                        if Goals in prompts:
                            prompts[Goals] += f"\nProject Name: {title}\nTasks Done: {content}\n"
                            goal_counter[Goals] += 1

                    top_goal = goal_counter.most_common(1)[0][0] if goal_counter else None

                    responses = []
                    for goal, prompt in prompts.items():
                        if prompt.strip():  
                            full_prompt = prompt_template + prompt
                            response = get_openai_response(full_prompt)
                            responses.append((goal, response))

                    st.session_state.responses = responses
                    st.session_state.top_goal = top_goal

            else:
                st.write("No data available. Please go back to the main page and enter the data.")

    # To save and restore scroll position after expand and collapse feature
    scroll_js = """
    <script>
    window.onload = function() {
        const savedScrollPosition = sessionStorage.getItem('scrollPosition');
        if (savedScrollPosition) {
            window.scrollTo(0, savedScrollPosition);
        }
    };
    window.onscroll = function() {
        sessionStorage.setItem('scrollPosition', window.scrollY);
    };
    </script>
    """

    # Function to toggle 'expand_all' state
    def toggle_expand_all():
        st.session_state.expand_all = not st.session_state.expand_all  
        st.rerun()

    if 'responses' in st.session_state:
        responses = st.session_state.responses
        top_goal = st.session_state.top_goal

        if top_goal:
            st.markdown(f"<h2 style='font-size:24px;'>Top Goal/KPI : {top_goal}</h2>", unsafe_allow_html=True)

        col_centered = st.columns([2, 1, 1, 2])
        with col_centered[1]:
            if st.button("Expand All" if not st.session_state.expand_all else "Collapse All", key="expand_collapse_button"):
                toggle_expand_all()
        with col_centered[2]:
            export_text = "\n\n".join([f"{name}:\n{response}" for name, response in st.session_state.responses])
            export_text = export_text.replace("*", "")
            st.download_button(label="Download File", data=export_text, file_name="Appraisal Summaries.txt", mime="text/plain")

        for name, response in responses:
            color = goal_colors.get(name, "#000000") 
            with st.expander(f"{name} Response - Click Here", expanded=st.session_state.expand_all):
                st.markdown(f"<h3 style='color:{color};'>{name}</h3>", unsafe_allow_html=True)
                st.write(response)

    st.components.v1.html(scroll_js, height=0)

##################
# Render the appropriate page based on the current state
if st.session_state.page == 'cover':
    cover_page()
else:
    main_page()