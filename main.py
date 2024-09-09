import streamlit as st
import requests
import json

# Initialize dictionaries
with open('team_ham.json') as json_file:
    team_ham = json.load(json_file)
with open('team_red.json') as json_file:
    team_red = json.load(json_file)


spots_left_red = ''
if len(team_red.keys()) < 16:
    spots_left_red = str(16 - len(team_red.keys())) + ' spots left'
else:
    spots_left_red = 'TEAM RED IS FULL'
spots_left_ham = ''
if len(team_ham.keys()) < 16:
    spots_left_ham = str(16 - len(team_ham.keys())) + ' spots left'
else:
    spots_left_ham = 'TEAM HAM IS FULL'


# Streamlit app interface
st.title('MisSplit Team Selection')

# User input
api_key = st.text_input('Enter a public API key here:')

# Radio button for choosing the dictionary
option = st.radio('Choose which team you would like to sign up for:', (f'Team Ham: {spots_left_ham}', f'Team Red: {spots_left_red}'))

# Button to submit the input
if st.button('Submit'):
    user_info = requests.get(f'https://api.torn.com/user/?selections=basic&key={api_key}').json()
    player_id = str(user_info['player_id'])
    name = user_info['name']
    if player_id is False:
        "Double check your API, no player ID was registered."
    if player_id not in team_ham.keys() and player_id not in team_red.keys():
        if option == f'Team Ham: {spots_left_ham}':
            team_ham[player_id] = name
            with open('team_ham.json', 'w') as json_file:
                json.dump(team_ham, json_file)
            st.success(f"Congratulations {name}, you have joined Team Ham!")
        elif option == f'Team Red: {spots_left_red}':
            team_red[player_id] = name  # You can decide what value to assign
            with open('team_red.json', 'w') as file:
                json.dump(team_red, file)
            st.success(f"Congratulations {name}, you have joined Team Red!")
        else:
            "something went wrong, this is probably some kind of API error"
    else:
        if player_id in team_ham.keys():
            if option == f'Team Ham: {spots_left_ham}':
                del team_ham[player_id]
                with open('team_ham.json', 'w') as json_file:
                    json.dump(team_ham, json_file)
                st.success(f"Wow, {name}, you've abandoned Ham.")
            if option == f'Team Red: {spots_left_red}':
                st.success(f"You can't join Red, you're already on Team Ham. To ABANDON HAM HEARTLESSLY re-enter your API key and select Team Ham again, then you'll be able to help Red out, and who could blame you")
        if player_id in team_red.keys():
            if option == f'Team Red: {spots_left_red}':
                del team_red[player_id]
                with open('team_red.json', 'w') as file:
                    json.dump(team_red, file)
                st.success(f"Wow, {name}, you've abandoned Red.")
            if option == f'Team Ham: {spots_left_ham}':
                st.success(f"You can't join Ham, you're already on Team Red. To ABANDON RED HEARTLESSY re-enter your API key and select Team Red again. Then you'll be able to join Ham like the little traitor you are.")
        else:
            "something went wrong, this is probably an issue with Red's code"

# Displaying the dictionaries
st.write('Team Ham:', team_ham)
st.write('Team Red:', team_red)