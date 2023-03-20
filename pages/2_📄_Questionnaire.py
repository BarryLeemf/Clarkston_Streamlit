import streamlit as st
import pandas as pd
import csv
import json
import datetime
import time


st.set_page_config(page_title="Supply Chain Questionnaire", 
                   layout="wide")
st.markdown(
    """
    <style>
    .css-18ni7ap.e8zbici2 {
        background-color: rgba(0, 0, 0, 0.8) ;
        background-repeat: no-repeat;
        background-image: url('https://clarkstonconsulting.com/wp-content/uploads/2021/11/Clarkston_Consulting_Logo_white-text-475x100-1.png');
        background-size: contain;
        background-repeat: no-repeat;
        width: 100%;
        height: 70px;
        background-position: 93%;
    }
    .e1fb0mya1.css-fblp2m.ex0cdmw0{
        background-color: rgba(256, 256, 256, 0.5) ;
    }
    .css-79elbk.e1fqkh3o10 {
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7) 68px, transparent 0%);
    }
    
    </style>
    """,
    unsafe_allow_html=True
    )


if 'company_q' not in st.session_state:
    st.session_state["company_q"] = ""
if 'sheet_q' not in st.session_state:
    st.session_state["sheet_q"] = ""
if 'role_q' not in st.session_state:
    st.session_state["role_q"] = ""
if 'time_q' not in st.session_state:
    st.session_state['time_q'] = 0
    
    
worksheet_list = ["1. Forecasting - Demand Planning", "2. New Product Development", "3. Production Planning", "4. Inventory Management", 
                  "5. Strategic Sourcing", "6. Procurement", "7. Sales & Ops Planning", "8. Distribution & Whse Mgt", 
                  "9. Transportation", "10. Master Data", "11. IT Systems", "12. Metrics", 
                  "13. LS Manufacturing", "14. LS New Product Development"]
company_list = [
    "Apple",
    "Amazon",
    "Google",
    "Netflix",
    "Meta",
    "Microsoft",
    "Tesla",
    "Intel",
    "IBM",
    "Oracle"]

role_list = [
    "1. Director, Information Services/IT-1 IT-1",
    "2. Systems Analyst/IT-2 IT-2",
    "3. Director of Sales/Marketing/Sales-Marketing1 Sales-Marketing1",
    "4. Senior Product Manager/Prod Mgr 1 Prod Mgr 1",
    "5. Sales Representative/Sales Rep1 Sales Rep1",
    "6. Manager, Demand Planning/Demand Plan1 Demand Plan1	",
    "7. Promotions Analyst/Demand Plan2 Demand Plan2",
    "8. Manager, Production Planning/Prod1 Prod1",
    "9. Production Planner/Prod2 Prod2",
    "10. Director, Distribution & Logistics/Dist1 Dist1	",
    "11. Distribution & Logistics Supervisor/Dist2 Dist2",
    "12. Distribution & Logistics Analyst/Dist3 Dist3",
    "13. Director, Purchasing & Strategic Sourcing/Purchasing1 Purchasing1",
    "14. Planner/Buyer/Purchasing2 Purchasing2",
    "15. Sourcing Analyst/Sourcing1 Sourcing1",
    "16. Manager, Quality Assurance/QA Mgr1 QA Mgr1	",
    "17. QA Analyst/QA Analyst1 QA Analyst1	",
    "18. Manager, Quality Control/QC Mgr1 QC Mgr1",
    "19. Director, Customer Service/Cust Serv1 Cust Serv1",
    "20. Supervisor, Customer Service/Cust Serv2 Cust Serv2	",
    "21. Customer Service Representative/Cust Serv3 Cust Serv3"]

options = ["Don't Know/NA", "Rarely/Never", "Always/Frequent" ]

with open('Clarkston_questionnaire.json', 'r') as f:
  questionnaire_data = json.load(f)


st.title("Supply Chain Management Questionnaire")
st.markdown("---")

st.sidebar.header("Filter Here:")

company_name = st.sidebar.selectbox(
    "Select Companies",
    company_list
 )

add_sheet = st.sidebar.selectbox(
    "Select Sheets",
    worksheet_list
)

add_role = st.sidebar.selectbox(
    "Select Roles",
    role_list
 )

    
current_date = datetime.date.today()
current_time = datetime.datetime.now()

#st.write("Current Time: ", ":green["+current_time.strftime("%m-%d-%Y %H:%M:%S")+"]")
st.write("Current Time: ", current_time)
st.sidebar.write("Click the Start Button to Begin")
if st.sidebar.button("START"):
    st.session_state.time_q = time.time()
    st.sidebar.write("Started")

for com in company_list:
    if company_name == com:
        st.session_state.company_q = com
        st.subheader(":blue[Company:] " + st.session_state.company_q)

# Choose Sheets        
for sheet in questionnaire_data:
    sheet_name = str(list(questionnaire_data).index(sheet)+1) + ". "+ sheet
    if add_sheet == (sheet_name):
        st.session_state.sheet_q = sheet
        st.subheader(":blue[Sheet:] " + st.session_state.sheet_q)
        
# Choose roles
for role in role_list:
   if add_role == role:       
       st.session_state.role_q = role
       st.subheader(":blue[Role:] " + st.session_state.role_q)
        
#st.subheader(st.session_state.company_q + " | " + st.session_state.sheet_q )   
#st.subheader( st.session_state.role_q)     
#st.header(":blue[Questions:]")
        
radio_result = [] 

# Answer questions
# To asign questions to two columns
col1, col2 = st.columns(2)
count = 0
for q in questionnaire_data[st.session_state.sheet_q]:
    if count%2==0:
        with col1:
            
            add_radio = st.radio(
                q.replace(". ","."),
                options,
                horizontal = True
            )
    else:
        with col2:
            
            add_radio = st.radio(
                q.replace(". ","."),
                options,
                horizontal = True
            )
    
    # Gather all results
    radio_result.append(add_radio)
    count+=1
    

#Click the save button to local csv file
if st.button("SAVE"):

    end_time = time.time()
    now = datetime.datetime.now()
    submit_time = now.strftime("%H:%M:%S")
    fill_duration = round(end_time - st.session_state.time_q, 3)
    st.session_state.time_q = 0
    
    st.write("You spent " + str(fill_duration) + " secs filling this sheet")
    with open(company_name +"_original_data.csv", mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([st.session_state.sheet_q, st.session_state.role_q, current_date, submit_time, fill_duration, radio_result])
    
        st.success("Data Saved!")
   
     
    
