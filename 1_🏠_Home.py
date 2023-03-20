import streamlit as st
import pandas as pd
import csv
import json

st.set_page_config(page_title="Supply Chain Management Home page", 
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

t1, t2 = st.columns((2,1)) 

t1.image('images/Company logo.jpeg', width = None)
#t2.title(":blue[Supply Chain Management Tool]")

t2.markdown(" **Tel:** 01392 451192")
t2.markdown(" **Website:** https://www.swast.nhs.uk")
t2.markdown(" **Email:** data.science@swast.nhs.uk")


st.markdown("---")

#st.subheader("**tel:** 01392 451192 **| website:** https://www.swast.nhs.uk **| email:** mailto:data.science@swast.nhs.uk", anchor = None)

st.subheader('Questionnaire Page - Data Collection')
st.write(
     """
     The Diagnostic has several purposes:
    
     1. Introduce each contributor in the supply chain planning process to best practice concepts. 
     The effort to respond to the survey encourages the participants to start thinking about what best practices 
     are and how these may apply to their working environment.
     2. Measure each individual’s understanding of how the company conducts supply chain management.
     3. Measure each functional area’s perception of how the company performs supply chain processes. The degree of answer inconsistency
        between functional areas is an indicator of how “siloed” the company’s departments may be operating.
     4. Determine how the company actually executes best practices vs. management perception vs. participant’s perception.
     5. Helps determine focus areas for follow-on improvement.
     """
 )

st.subheader('Maturity Level Page - Visualization')
st.write(
     """
      There are five levels of maturity that are measured by this tool.  The answers to the survey questions automatically calculate the overall Maturity Level for the company.  They are as follows:
    
     1. "Innocence"  An organization that exhibits few process centric capabilities.  Ad hoc activities are the norm in lieu of repeatable, 
    in-control processes.
     2. "Awareness"  An organization that has a rudimentary, loosely woven set of process capabilities in place.
     3. "Managing"  An organization that has implemented basic, in-control process capabilities within its own company boundaries
     4. "Optimizing"  An organization that has not only developed process capabilities, but also actively integrates them into its 
     daily operations across functional boundaries, business units, other organizational barriers and (to some degree) with its customers 
     and suppliers
     5. "Leading"  An organization that has differentiated itself based upon integrated process capabilities which extend to both customers 
     and suppliers in a way that has simultaneously redefined those capabilities
     """ )
