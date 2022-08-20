import streamlit as st
import pandas as pd
import altair as alt

# Change this to the path where you store the data
DATA_PATH = "E:/Learning/Self-Driven/Programming/Hackathon/2022-GovHack/Govhack/data"
# DATA_FILE = "NTGovt_ED_presentation_rate_per_capita_2018-19.csv"

# There are two functions here, there should only be one. I hate this, but it works...
def get_chart_bar(data,x, y, x_label, y_label, title, stack = False):
    hover = alt.selection_single(
        fields=[x],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    if stack:
        bars = (
            alt.Chart(data, title=title)
            .mark_bar()
            .encode(
                x=alt.X(x, title=x_label),
                y=alt.Y(y, title=y_label),
                color="state",
            )
        )
    else:
        bars = (
            alt.Chart(data, title=title)
            .mark_bar()
            .encode(
                x=alt.X(x, title=x_label),
                y=alt.Y(y, title=y_label),
                # color="state",
            )
        )   
    # Draw points on the line, and highlight based on selection
    points = bars.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=x,
            y=y,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(x, title=x_label),
                alt.Tooltip(y, title=y_label),
                alt.Tooltip("state", title="State"),
            ],
        )
        .add_selection(hover)
    )
    return (bars + points + tooltips).interactive()


def get_chart_line(data,x, y, x_label, y_label, title):
    hover = alt.selection_single(
        fields=[x],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title=title)
        .mark_line()
        .encode(
            x=alt.X(x, title=x_label),
            y=alt.Y(y, title=y_label),
            color="state",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=x,
            y=y,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(x, title=x_label),
                alt.Tooltip(y, title=y_label),
                alt.Tooltip("state", title="State"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

st.title("Motivation")

st.markdown("""
The COVID19 highlighted the ever increasing pressure on hospital Emergency Departments (ED). 
The motivation for this project is to leverage technology to help alleviate patient flow to hospital EDs so that those who require urgent care can get the attention they need.

# Case Study \#1: Northern Territory
The Northern Territory is an important case study, since the ED presentation rate is **TWICE** those of other states, as seen below.
""")

### Part 1 : ED Presentation Per Capita
# Read Data
per_capita = pd.read_csv(f'{DATA_PATH}/NTGovt_ED_presentation_rate_per_capita_2018-19.csv')

# Clean Data (keep only 2018-19 and drop national)
per_capita = per_capita.query('time_period == "2018-19" & state != "Total"')

# Plot and output chart
per_capita_chart = get_chart_bar(per_capita, 
    "state", "pres_per_1000", 'State', 'Presentation Per 1000 People',
    "Hospital ED Presentations (2018-19) Per 1000 People")
st.altair_chart(
    per_capita_chart.interactive(),
    use_container_width=True
)
st.write("Source: Northern Territory Government -- [Emergency Department Care 2018-19](https://data.nt.gov.au/dataset/emergency-department-care-2018-19)")

### Part 2 : ED Presentation On Time Rate
st.markdown("""
## Ontime admission of patients in ED
*Some explanation on what ontime means.*
""")

# Read Data
ontime = pd.read_csv(f'{DATA_PATH}/AIHW_ED_ontime_presentation_rate_by_state_by_cohort.csv')

# Fetch user request
cohort_choice = st.radio(
     "Which patient cohort are you interested in?",
     ('All', 'Resuscitation', 'Emergency', 'Urgent', 'Semi-Urgent', 'Non-Urgent'))

# Clean/filter data according to request
if cohort_choice == 'All':
    ontime = ontime
else:
    ontime = ontime.query('patient_cohort == @cohort_choice')

ontime = ontime.groupby(['state', 'time_period'], as_index=False).sum()
ontime['pc_ontime'] = ontime['n_ontime']/ontime['n_patients'] *100

# Plot and output chart
ontime_chart = get_chart_line(ontime, 
    "time_period", "pc_ontime", 'Time Period', '% On Time',
    "Percentage of On-Time Hospital ED Treatment Commencement")

st.altair_chart(
    ontime_chart.interactive(),
    use_container_width=True
)

### Part 3 : ED Presentation Departure Within 4hr Rate
st.markdown("""
## Within 4 hr admission of patients in ED
*Some explanation on what this means.*
""")

# Read data
within4hr = pd.read_csv(f'{DATA_PATH}/AIHW_ED_within4hr_presentation_rate_by_state_by_cohort.csv')

# Clean/filter data according to request
# cohort_choice = st.radio(
#      "Which patient cohort are you interested in?",
#      ('All patients', 'Resuscitation', 'Emergency', 'Urgent', 'Semi-Urgent', 
#      'Non-Urgent', 'Subsequently admitted patients', 'Not subsequently admitted patients'))
cohort_choice = st.radio(
     "Which patient cohort are you interested in?",
     ('All patients', 'Resuscitation', 'Emergency', 'Urgent', 'Semi-Urgent', 
     'Non-Urgent'))

within4hr = within4hr.query('patient_cohort == @cohort_choice')

within4hr = within4hr.groupby(['state', 'time_period'], as_index=False).sum()
within4hr['pc_within4hr'] = within4hr['n_within4hr']/within4hr['n_patients'] *100

within4hr_chart = get_chart_line(within4hr, 
    "time_period", "pc_within4hr", 'Time Period', '% Within 4 hours',
    "Percentage of On-Time Hospital ED Departure within 4hr")

st.altair_chart(
    within4hr_chart.interactive(),
    use_container_width=True
)

#### Part 4: Median Wait Time
# Data sourced from https://www.aihw.gov.au/reports-data/myhospitals/hospital/h0737 (under wait time 2020-21)
waittime = pd.read_csv(f'{DATA_PATH}/AIHW_ED_median_waittime_sample.csv')

waittime_chart = get_chart_bar(waittime, 
    "patient_cohort", "median_wait_time", 'Patient Cohort', 'Median Wait Time (Min)',
    "Percentage of On-Time Hospital ED Treatment Commencement", True)

st.altair_chart(
    waittime_chart.interactive(),
    use_container_width=True
)
