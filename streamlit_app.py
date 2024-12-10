# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie !.
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe , max_selections  = 5  )

# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()



if ingredients_list:

    ingredients_string =''


    for fruit_chosen in ingredients_list:
       
        ingredients_string += fruit_chosen +' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen, 'is', search_on, '.')        
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        try:
            fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
            if fruityvice_response.status_code == 200:
                # Parse JSON response
                fruityvice_data = fruityvice_response.json()
                fv_df = pd.DataFrame([fruityvice_data])  # Convert the single JSON object to a DataFrame
                st.dataframe(fv_df, use_container_width=True)
            else:
                st.error(f"Error fetching data for {fruit_chosen}: {fruityvice_response.status_code}")
                st.write(f"Response: {fruityvice_response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch data for {fruit_chosen}: {e}")

    # st.write(ingredients_string)    

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    



