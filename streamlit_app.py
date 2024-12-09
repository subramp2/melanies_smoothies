# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie !.
    """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)


#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)
#st.write("You favorite fruit is:", option)



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe)

if ingredients_list:
 #   st.write(ingredients_list)
 #   st.text(ingredients_list)
    
    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        
    st.write(ingredients_string)    

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
