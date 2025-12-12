# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie:cup_with_straw:")
st.write(
  """Choose the Fruits you like in your Smoothie
  """
)



from snowflake.snowpark.functions import col
cnx =  st.connection("Snowflake")
session =  cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

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

    st.write(s)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + s + """','"""+name+"""')"""
    

    # st.write(my_insert_stmt)

    time_to_insert  =  st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(name+'! Your Smoothie is ordered!', icon="✅")
