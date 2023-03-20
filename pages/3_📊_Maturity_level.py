import streamlit as st
import pandas as pd
import csv
import json
import plotly.graph_objects as go
import plotly


st.set_page_config(page_title="Maturity Level", 
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

if 'company_mat' not in st.session_state:
    st.session_state["company_mat"] = ""
if 'sheet_mat' not in st.session_state:
    st.session_state["sheet_mat"] = ""

worksheet_list = ["1. Forecasting - Demand Planning", "2. New Product Development", "3. Production Planning", "4. Inventory Management", 
                  "5. Strategic Sourcing", "6. Procurement", "7. Sales & Ops Planning", "8. Distribution & Whse Mgt", 
                  "9. Transportation", "10. Master Data", "11. IT Systems", "12. Metrics", 
                  "13. LS Manufacturing", "14. LS New Product Development"]

worksheet_list_wo_num = ["Forecasting - Demand Planning", "New Product Development", "Production Planning", "Inventory Management", "Strategic Sourcing",
                  "Procurement", "Sales & Ops Planning", "Distribution & Whse Mgt", "Transportation", "Master Data",
                  "IT Systems", "Metrics", "LS Manufacturing", "LS New Product Development"]

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

with open('Clarkston_questionnaire.json', 'r') as f:
  questionnaire_data = json.load(f)


def get_score_data(sheet, company):
    dummy_data = pd.read_csv("./"+ company +"_sheet_dummy_data/"+sheet+".csv",index_col=[0])
    dummy_data.rename(columns = {'0':'0.0', '1':'1.0', '2': '2.0'}, inplace = True)
    maturity_weight_list = []
    for i in questionnaire_data[sheet]:
        maturity_weight_list.append(questionnaire_data[sheet][i])
    always_list = [0]*len(maturity_weight_list)
    never_list = [0]*len(maturity_weight_list)
    dk_list = [0]*len(maturity_weight_list)
    for i in dummy_data.columns:
        if '0.' in i:
            always_list += dummy_data[i]
        elif '1.' in i:
            never_list += dummy_data[i]
        elif '2.' in i:
            dk_list += dummy_data[i]
    dummy_data['Always/Frequent'] = always_list
    dummy_data['Rarely/Never'] = never_list
    dummy_data["Don't_Know/NA"] = dk_list
    dummy_data['Level'] = maturity_weight_list
    maturity_score_list = []
    for i in range(len(maturity_weight_list)):
        if always_list[i] == 0:
            if never_list[i] == 0:
                maturity_score = 0
            else:
                maturity_score = 1
                
        else:
            if always_list[i] > never_list[i]:
                maturity_score = round(((1 - (never_list[i]/(always_list[i] + never_list[i]))) * maturity_weight_list[i]), 1)
            else:
                maturity_score = 1
        maturity_score_list.append(maturity_score)
        
    dummy_data['Total_Score'] = maturity_score_list
    
    return dummy_data, maturity_weight_list


st.sidebar.header("Filter Here:")

company_name = st.sidebar.selectbox("Select Companies", company_list)

add_sheet = st.sidebar.selectbox(
    "Select Sheets",
    worksheet_list
)

st.sidebar.write("Click to Show Overall Maturity Level")


    
st.title("Supply Chain Maturity Level")
st.markdown("---")



for com in company_list:
    if company_name == com:
        st.session_state.company_mat = com
        #st.subheader(":blue[Company:] "+ st.session_state.company_mat)
        

question_list = []
ms_list = []
for sheet in questionnaire_data:
    question_list.append(questionnaire_data[sheet])
    
    sheet_name = str(list(questionnaire_data).index(sheet)+1) + ". "+ sheet
    if add_sheet == (sheet_name):
        st.session_state.sheet_mat = sheet
        #st.subheader(":blue[Sheet:] "+ sheet )

        
score_data, maturity_weight_list = get_score_data(st.session_state.sheet_mat, st.session_state.company_mat)    
averge_score = round(score_data['Total_Score'].mean(),2)
total_always = score_data['Always/Frequent'].sum()
total_never = score_data['Rarely/Never'].sum()
total_always_percentage = round(total_always/(total_always+total_never),3)
total_never_percentage = round(total_never/(total_never+total_always),3)

level3_num = maturity_weight_list.count(3)
averge_score_level3 = round(score_data['Total_Score'][:level3_num].mean(),2)
always_level3 = score_data['Always/Frequent'][:level3_num].sum()
never_level3 = score_data['Rarely/Never'][:level3_num].sum()
always_level3_percentage = round(always_level3/(always_level3+never_level3),3)
never_level3_percentage = round(never_level3/(never_level3+always_level3),3)


placeholder = st.empty()
with placeholder.container():
    btn_mat = st.sidebar.button("Overall Maturity Level")
    
    st.subheader(st.session_state.company_mat + " | " + st.session_state.sheet_mat)
    st.header(":blue[Diagnostic Results:] ")
    

    
    #plotly
    
    #if st.sidebar.button("Show Maturity Level"):
        
    col1, col2 = st.columns((1,1))
    
    with col1:
        
        fig2 = go.Figure(data=go.Scatterpolar(
            r = score_data['Total_Score'],
            theta=["Q"+str(i+1) for i in range(len(maturity_weight_list))],
            fill = 'toself',
            name = "All Level",
            marker_size = 1
        ))
        
        fig2.add_trace(go.Scatterpolar(
            r = score_data['Total_Score'][:level3_num],
            theta=["Q"+str(i+1) for i in range(level3_num)],
            fill='toself',
            name='Level 3',
            marker_color="dark grey",
            marker_size = 1
        ))
        
        fig2.update_layout(
          polar=dict(
            radialaxis=dict(
              visible=True
            ),
          ),
          showlegend = True,
          title = "Scores of Each Question"
        )
        
        st.plotly_chart(fig2, use_container_width=True, theme = "streamlit")
        
        
    with col2:
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=['Level 3', 'All Level'],
            x=[always_level3_percentage, total_always_percentage],
            name='Always/Frequent',
            orientation='h',
            marker=dict(
                color='rgba(255, 47, 12, 0.55)',
                line=dict(color='rgba(255, 47, 12, 0.7)', width=2)
            )
        ))
        fig.add_trace(go.Bar(
            y=['Level 3', 'All Level'],
            x=[never_level3_percentage, total_never_percentage],
            name='Rarely/Never',
            orientation='h',
            marker=dict(
                color='rgba(19, 11, 12, 0.4)',
                line=dict(color='rgba(19, 11, 12, 0.5)', width=2)
            )
        ))
        
        fig.update_layout(
            xaxis=dict(
                showgrid=True,
                showline=True,
                zeroline=True,
             
            ),
            yaxis=dict(
                showgrid=False,
                showline=True,
                zeroline=True,
            ),
            barmode='stack',
            showlegend=True,
            title = "Percentage of Responses"
        )
        
        annotations = []
        fig.update_xaxes(tickformat=".0%")
        annotations.append(dict(xref='x', yref='y',
                                x=total_always_percentage / 2, y="All Level",
                                text= "{:.1%}".format(total_always_percentage),
                                font=dict(family='Arial', size=18,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
        annotations.append(dict(xref='x', yref='y',
                                x=always_level3_percentage / 2, y="Level 3",
                                text= "{:.1%}".format(always_level3_percentage),
                                font=dict(family='Arial', size=18,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
        space_1 = round(total_always_percentage,2)
        space_2 = round(always_level3_percentage,2)
        annotations.append(dict(xref='x', yref='y',
                                x= space_1 + total_never_percentage / 2, y="All Level",
                                text= "{:.1%}".format(total_never_percentage), 
                                font=dict(family='Arial', size=18,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
        annotations.append(dict(xref='x', yref='y',
                                x= space_2 + never_level3_percentage / 2, y="Level 3",
                                text= "{:.1%}".format(never_level3_percentage), 
                                font=dict(family='Arial', size=18,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
        
        fig.update_layout(annotations=annotations)
        
        st.plotly_chart(fig, use_container_width=True, theme = "streamlit")
        
        
    st.header(":red[Original Data:] ")
    
    col3, col4 = st.columns((1, 1))
    
    
    with col3:
        st.subheader("Scores of Each Question")
        data_2 = score_data[["Level", "Total_Score", "Always/Frequent", "Rarely/Never", "Don't_Know/NA"]]
        data_2["Descriptions"] = list(questionnaire_data[st.session_state.sheet_mat])
        idx = ["Q"+str(i+1) for i in range(len(maturity_weight_list))]
        data_2 = data_2.set_axis(idx, axis='index')
        st.dataframe(data_2, use_container_width=True)  
        
        
    with col4:
        st.subheader("Percentage of Responses")
        data = [[averge_score_level3, always_level3_percentage, never_level3_percentage], [averge_score, total_always_percentage, total_never_percentage]]
        idx, col = ['Level 3', "All Level"], ["Average Score", "Always/Frequent","Rarely/Never"] 
        df = pd.DataFrame(data, index=idx, columns=col)
        df_style = df.style.format({'Average Score': "{:.2f}",'Always/Frequent': "{:.1%}",'Rarely/Never': "{:.1%}"})
        st.dataframe(df_style, use_container_width=True)
    

#If btn is pressed or True
if btn_mat:
    #This would empty everything inside the container
    placeholder.empty()
    st.header(":blue[Overall Diagnostic Results:] ") 
    score_overall_total = []
    score_overall_level3 = []
    for s in questionnaire_data:
        score_data, maturity_weight_list = get_score_data(s, st.session_state.company_mat) 
        averge_score = round(score_data['Total_Score'].mean(),2)
        level3_num = maturity_weight_list.count(3)
        averge_score_level3 = round(score_data['Total_Score'][:level3_num].mean(),2)
        
        score_overall_total.append(averge_score)
        score_overall_level3.append(averge_score_level3)
    
    col5, col6 = st.columns((1,1))
    
    with col5:
        fig_all_level3 = go.Figure(data=go.Scatterpolar(
          r = score_overall_level3,
          theta = worksheet_list_wo_num,
          fill = 'toself'
          
        ))
        
        fig_all_level3.update_layout(
          polar=dict(
            radialaxis=dict(
              visible=True
            ),
          ),
          showlegend=False,
          title='Level 3'
          
        )
        
        st.plotly_chart(fig_all_level3, use_container_width=True, theme = "streamlit")
        
        
    with col6:
        fig_all = go.Figure(data=go.Scatterpolar(
          r = score_overall_total,
          theta = worksheet_list_wo_num,
          fill = 'toself',
          textposition = 'top center'
        ))
        
        fig_all.update_layout(
          polar=dict(
            radialaxis=dict(
              visible=True
            ),
          ),
          showlegend=False,
          title='All Level'
          
        )
        
        st.plotly_chart(fig_all, use_container_width=True, theme = "streamlit")
        
    st.header(":red[Original Data:] ")
    
    col7, col8 = st.columns((1, 1))
    
    
    with col7:
        st.subheader("Level 3")
        idx = worksheet_list_wo_num
        data_overall_level3 = pd.Series(score_overall_level3, index = idx, name="Average of Total Scores")
        st.dataframe(data_overall_level3, use_container_width=True)  
        
        
    with col8:
        st.subheader("All Level")
        idx = worksheet_list_wo_num
        data_overall_total = pd.Series(score_overall_total, index = idx, name="Average of Total Scores")
        st.dataframe(data_overall_total, use_container_width=True)  
    

