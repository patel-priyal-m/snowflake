# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
import requests
from snowflake.snowpark.functions import col
import pandas as pd


# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie:cup_with_straw:")
st.write(
  """Choose the Fruits you like in your Smoothie
  """
)



cnx =  st.connection("snowflake")
session =  cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
pd_df=   my_dataframe.to_pandas()
name = st.text_input("Name on Smoothie", "Kitty Cat")

ingredients_list = st.multiselect(
    "Choose upto 5 ingrediants:",
    my_dataframe,
    max_selections  = 5
)

if ingredients_list: 
    s = ""
    for i in ingredients_list:
        s+=i + " "
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', i,' is ', search_on, '.')
        
        st.subheader(i+" Mutrition Info" )
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)

    st.write(s)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + s + """','"""+name+"""')"""
    

    # st.write(my_insert_stmt)

    time_to_insert  =  st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(name+'! Your Smoothie is ordered!', icon="✅")


