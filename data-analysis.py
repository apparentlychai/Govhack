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


def get_chart_line(data,x, y, x_label, y_label, title, hline = 0):
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
    if hline != 0:
        threshold = (alt.Chart().mark_rule(color="#ff0000", thickness = 5, strokeDash=[3,5]).encode(y=alt.datum(hline)))
        return (lines + points + tooltips + threshold).interactive()
    else:
        return (lines + points + tooltips).interactive()


def filter_key_states(data, pc_measure, n_measure, key_state):
    # First get the states with min/max values
    state_total = data.groupby(['state'], as_index=False).sum()
    state_total[pc_measure] = state_total[n_measure]/state_total['n_patients'] *100

    state_column_id = state_total.columns.get_loc("state") # Col ID of the state variable

    # String of min/max states
    max_state = state_total.iloc[state_total[pc_measure].idxmax(), state_column_id]
    min_state = state_total.iloc[state_total[pc_measure].idxmin(), state_column_id]

    # Make sure we include the key state too
    keep_states = [max_state, min_state, key_state]
    state_total = data.query('state == @keep_states')

    # Then we get the national tot
    aus_total = data.groupby(['time_period'], as_index=False).sum()
    aus_total[pc_measure] = aus_total[n_measure]/aus_total['n_patients'] *100
    aus_total.insert(state_column_id + 1, 'state', 'Australia') # +1 accounts for the group_by dropping a col

    return pd.concat([state_total, aus_total])

st.title("Data Analysis")

# st.markdown("""
# The COVID19 highlighted the ever increasing pressure on hospital Emergency Departments (ED). 
# The motivation for this project is to leverage technology to help alleviate patient flow to hospital EDs so that those who require urgent care can get the attention they need.

# # Case Study \#1: Northern Territory
# The Northern Territory is an important case study, since the ED presentation rate is **TWICE** those of other states, as seen below.
# """)

### Part 1 : ED Presentation Per Capita
st.markdown("""
## 1. Hospital ED Presentation Rate Per Capita
The hospital ED presentation rate in NT is **TWICE** that of any other state, highlighting the overcrowding issue.
""")
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
## 2. Ontime Hospital ED Treatment Commencement
According to the [Australasian College for Emergency Medicine](https://acem.org.au/Content-Sources/Advancing-Emergency-Medicine/Better-Outcomes-for-Patients/Triage) 
the maximium waiting time should be as follows, with performance threshold indicators.
| Patient Cohort/Triage | Max Waiting Time (min)| Performance Indicator Threshold | 
| --- | --- |  --- |
| ATS1 Resuscitation | 0 | 100% |
| ATS2 Emergency | 10 | 80% |
| ATS3 Urgent | 30 | 75% |
| ATS4 Semi-Urgent | 60 | 70% |
| ATS5 Non-Urgent | 120 | 70% |

Northern Territory falls below the national average in all categories, with the possible exception of Non-Urgent patient cohorts.

Northern Territory falls below the performance indicator threshold (indicated by the red dotted line) for all categories except for Non-Urgent.

NOTE: Only states with maximum and minimum values, along with Northern Territory and the National Average for clarity. Where there are only three lines, Northern Territory is the minimum.
""")

# Read Data
ontime = pd.read_csv(f'{DATA_PATH}/AIHW_ED_ontime_presentation_rate_by_state_by_cohort.csv')
perf_indicator = {
    'All' : 0,
    'Resuscitation': 100, 
    'Emergency': 80, 
    'Urgent' : 75, 
    'Semi-Urgent' : 70, 
    'Non-Urgent' : 70
}

# Fetch user request
cohort_choice = st.radio(
     "Which patient cohort/triage group are you interested in?",
     ('All', 'Resuscitation', 'Emergency', 'Urgent', 'Semi-Urgent', 'Non-Urgent'))

# Clean/filter data according to request
if cohort_choice == 'All':
    ontime = ontime
else:
    ontime = ontime.query('patient_cohort == @cohort_choice')

ontime = filter_key_states(ontime, 'pc_ontime', 'n_ontime', "NT")

ontime = ontime.groupby(['state', 'time_period'], as_index=False).sum()
ontime['pc_ontime'] = ontime['n_ontime']/ontime['n_patients'] *100

# Plot and output chart
ontime_chart = get_chart_line(ontime, 
    "time_period", "pc_ontime", 'Time Period', '% On Time',
    "Percentage of On-Time Hospital ED Treatment Commencement",
    hline=perf_indicator[cohort_choice])

st.altair_chart(
    ontime_chart.interactive(),
    use_container_width=True
)

### Part 3 : ED Presentation Departure Within 4hr Rate
st.markdown("""
## 3. Proportion of patients departing from ED within 4hrs
This is a little more convoluted since 'depart' could mean admission or discharge. Either way, Northern Territory falls below the national average.

NOTE: Only states with maximum and minimum values, along with Northern Territory and the National Average for clarity. Where there are only three lines, Northern Territory is the minimum.
""")

# Read data
within4hr = pd.read_csv(f'{DATA_PATH}/AIHW_ED_within4hr_presentation_rate_by_state_by_cohort.csv')

# Clean/filter data according to request
# cohort_choice = st.radio(
#      "Which patient cohort are you interested in?",
#      ('All patients', 'Resuscitation', 'Emergency', 'Urgent', 'Semi-Urgent', 
#      'Non-Urgent', 'Subsequently admitted patients', 'Not subsequently admitted patients'))
cohort_choice = st.radio(
     "Which patient cohort/triage group are you interested in?",
     ('All patients', 'Resuscitation', 'Emergency', 'Urgent', 'Semi-Urgent', 
     'Non-Urgent'))

within4hr = within4hr.query('patient_cohort == @cohort_choice')

within4hr = filter_key_states(within4hr, 'pc_within4hr', 'n_within4hr', "NT")

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
st.markdown("""
## 4. Median Waittime in the ED
On average Northern Territory has longer wait time than the national average.
""")


waittime = pd.read_csv(f'{DATA_PATH}/AIHW_ED_median_waittime_sample.csv')

waittime_chart = get_chart_bar(waittime, 
    "patient_cohort", "median_wait_time", 'Patient Cohort', 'Median Wait Time (Min)',
    "Median Wait Time in ED", True)

st.altair_chart(
    waittime_chart.interactive(),
    use_container_width=True
)
