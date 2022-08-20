library(readxl)
library(dplyr)
library(tidyr)
library(ggplot2)

#### Table 1: ED Presentation Per Capita ####
# This can be found in table 2.2 of https://data.nt.gov.au/dataset/emergency-department-care-2018-19
# The dataset read in is a sanitised version of Table 2.2

raw_pres <- read_excel("raw_data/raw_ED_presentation_rate_per_capita_2018-19.xlsx")

pres_per_capita <- raw_pres %>% rename(state = `...1`) %>%
  pivot_longer(!state, names_to = "time_period", values_to = "pres_per_1000")
write.csv(pres_per_capita, "data/NTGovt_ED_presentation_rate_per_capita_2018-19.csv")

#### Table 2: ED Presentation On Time Rate ####
# This data can be found from https://myhospitalsapi.aihw.gov.au/api/v1/measure-downloads/myh-ed
raw_ontime <- read_excel('raw_data/udm-emergency-department-data.xlsx',
                         sheet = 'Patients seen on time')

# Some particular intricate cleaning reserved only for xlsx files
ontime_sliced <- raw_ontime %>% 
  slice_tail(n = nrow(raw_ontime) - 15)
ontime_cols <- c("report_unit", "report_unit_type", "state", "peer_group",
                 "time_period", "patient_cohort", "n_patients", "drop1",
                 "pc_ontime", "drop2", "peer_group_avg", "drop3")
colnames(ontime_sliced) <- ontime_cols

ontime <- ontime_sliced %>% filter(is.na(drop2)) %>% # Missing or invalid data
  filter(n_patients != "<5") %>% # those with <5 patients not reliable
  filter(!pc_ontime %in% c('NP', 'NP†', '-')) %>% # Unable to calculate/didn't meet criteria
  filter(!state %in% c('NAT', NA)) %>% # Keep only states
  mutate(n_patients = as.numeric(n_patients),
         pc_ontime = as.numeric(pc_ontime),
         n_ontime = n_patients*pc_ontime) %>%
  select(-c("drop1", "drop2", "drop3")) 

clean_ontime <- ontime %>%
  select(state, time_period, patient_cohort, n_ontime, n_patients) %>%
  group_by(state, time_period, patient_cohort) %>%
  summarise(n_ontime = sum(n_ontime),
            n_patients = sum(n_patients)) %>%
  mutate(pc_ontime = n_ontime/n_patients)

write.csv(clean_ontime, 
          "data/AIHW_ED_ontime_presentation_rate_by_state_by_cohort.csv",
          row.names = FALSE)

#### Table 3: ED Presentation Departure Within 4hr Rate ####
# This data can be found from https://myhospitalsapi.aihw.gov.au/api/v1/measure-downloads/myh-ed
raw_within4hr <- read_excel('raw_data/udm-emergency-department-data.xlsx',
                            sheet = 'Time in ED - within 4 hrs')

# Some particular intricate cleaning reserved only for xlsx files
within4hr_sliced <- raw_within4hr %>% 
  slice_tail(n = nrow(raw_within4hr) - 18)
within4hr_cols <- c("report_unit", "report_unit_type", "state", "peer_group",
                    "time_period", "patient_cohort", "n_patients", "drop1",
                    "pc_within4hr", "drop2", "peer_group_avg", "drop3")
colnames(within4hr_sliced) <- within4hr_cols

within4hr <- within4hr_sliced %>% filter(is.na(drop2)) %>% # Missing or invalid data
  filter(n_patients != "<5") %>% # those with <5 patients not reliable
  filter(!pc_within4hr %in% c('NP', 'NP†', '-')) %>% # Unable to calculate/didn't meet criteria
  filter(!state %in% c('NAT', NA)) %>% # Keep only states
  mutate(n_patients = as.numeric(n_patients),
         pc_within4hr = as.numeric(pc_within4hr),
         n_within4hr = n_patients*pc_within4hr) %>%
  select(-c("drop1", "drop2", "drop3")) 

clean_within4hr <- within4hr %>%
  select(state, time_period, patient_cohort, n_within4hr, n_patients) %>%
  group_by(state, time_period, patient_cohort) %>%
  summarise(n_within4hr = sum(n_within4hr),
            n_patients = sum(n_patients)) %>%
  mutate(pc_within4hr = n_within4hr/n_patients)

write.csv(clean_within4hr, 
          "data/AIHW_ED_within4hr_presentation_rate_by_state_by_cohort.csv",
          row.names = FALSE)

