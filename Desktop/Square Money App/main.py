import pandas as pd
import altair as alt
import streamlit as st

#Sidebar -- Select
servers = ["Server 1", "Server 2", "Server 3", "Server 4", "Server 5"] # TODO Add names
bussers = ["Busser 1", "Busser 2", "Busser 3"]
runners = ["Runner 1", "Runner 2", "Runner 3"]

st.sidebar.header("Data")
servers_on = st.sidebar.multiselect("Servers on:", servers,)
tips = []
for server in servers_on: #Makes sure inputs are a number, adds them to list tips which will be used for pd df
    tip = st.sidebar.text_input(f"{server} tips:").strip()
    try:
        tips.append(float(tip))
        # st.sidebar.text(f"Nice job {server}!")# TODO -- Shit on underperforming severs
    except:
        st.sidebar.text("Please enter server's tips in number format")

bussers_on = st.sidebar.multiselect("Bussers on:", bussers) 

runners_on = st.sidebar.multiselect("Runners on:", runners)

end_shift_time = st.sidebar.selectbox("What time did we close today?", ["9:00", "10:00"] )
if end_shift_time == "9:00":
    end_shift_time = 2100
else:
    end_shift_time = 2200


time_worked_servers = {}
for server in servers_on:
    time_worked_servers[server] = end_shift_time
    
earlybird_response = st.sidebar.multiselect("Did anyone leave early?", ["Server", "Busser"])
if "Server" in earlybird_response:
    earlybirds = st.sidebar.multiselect("Which server(s)?", servers_on)
    for earlybird in earlybirds:
        time = st.sidebar.text_input(f"Time {earlybird} left:").strip()
        try:
            time_worked_servers[earlybird] = int(time)  ##Make Dict pointing server:time left
        except:
            st.sidebar.text("Please enter time in 24hr format (ex. 7:30 = 1930)")
        
time_worked_bussers = {}
for busser in bussers_on:
    time_worked_bussers[busser] = end_shift_time
    
if "Busser" in earlybird_response:
    earlybirds = st.sidebar.multiselect("Which busser(s)?", bussers_on)
    for earlybird in earlybirds:
        time = st.sidebar.text_input(f"Time {earlybird} left:").strip()
        try:
            time_worked_bussers[earlybird] = int(time)  ##Make Dict pointing busser:time_4left
        except:
            st.sidebar.text("Please enter time in 24hr format (ex. 7:30 = 1930)") 
#     
##           
###
####
##### Mathy math time
total_tips = sum(tips)
runners_cut = len(servers_on)* len(runners_on) * 10 #runners get 10 dollars per server each
if bussers_on == 1:
    bussers_cut = 0.1 * total_tips
else:
    bussers_cut = 0.15 * total_tips

servers_cut = total_tips - runners_cut - bussers_cut


for server in time_worked_servers:
    time_worked_servers[server] -= 1700
for busser in time_worked_bussers:  # Now, instead of being {person : time they left}, it is {person : hours they worked}
    time_worked_bussers[busser] -= 1700


percentage_of_server_cut = {} #These are respective cut, so 15% is 15% of server cut, not total tips
percentage_of_busser_cut = {}

total_hours_worked_servers = sum(time_worked_servers.values())
total_hours_worked_bussers = sum(time_worked_bussers.values())
for server in servers_on:
    percentage = round(time_worked_servers[server] / total_hours_worked_servers, 3)
    percentage_of_server_cut[server] = percentage
#                                                     # creates dictionaries like this: {person : percentage of respective cut}
for busser in bussers_on:
    percentage = round(time_worked_bussers[busser] / total_hours_worked_bussers, 3)
    percentage_of_busser_cut[busser] = percentage
# print(f"{percentage_of_server_cut} \n {percentage_of_busser_cut}")

money_earned_servers = {}
money_earned_bussers = {}

for server in servers_on:
    money_earned = round(percentage_of_server_cut[server] * servers_cut, 2)
    money_earned_servers[server] = money_earned
for busser in bussers_on:
    money_earned = round(percentage_of_busser_cut[busser] * bussers_cut, 2)
    money_earned_bussers[busser] = money_earned
    
# print(money_earned_bussers, money_earned_servers)

#
##
###
####
##### Constructing Dataframe
combined_names = list(money_earned_servers.keys()) + list(money_earned_bussers.keys())
combined_money_earned = list(money_earned_servers.values()) + list(money_earned_bussers.values())
combined_hours_worked = list(time_worked_servers.values()) + list(time_worked_bussers.values())
data = {
    "Name": combined_names,
    "Money Made": combined_money_earned,
    "Hours Worked": combined_hours_worked
}

df = pd.DataFrame(data)
print(df)
