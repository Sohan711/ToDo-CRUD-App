import streamlit as st

import pandas as pd 
from db_fxns import * 
import streamlit.components.v1 as stc
import plotly.express as px


# Data Viz Pkgs
import plotly.express as px 
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')

# DB fxn
from db_fxns import create_table,add_data,view_all_data,get_task,view_unique_task,edit_task_data,delete_data

About = """
Our CRUD (Create, Read, Update, Delete) application is a powerful tool designed to manage data efficiently. It provides essential functionalities to perform operations on a dataset or database:

What is CRUD?
CRUD represents the four fundamental operations for persistent storage:

Create: Add new entries or records to the dataset.

Read: Retrieve and view existing data from the dataset.

Update: Modify or edit existing data within the dataset.

Delete: Remove or eliminate data entries from the dataset.


Key Features-->
User-Friendly Interface: Our application boasts an intuitive and user-friendly design, making it accessible to users of all levels of technical expertise.
Reliable Data Management: With CRUD functionality, users can efficiently manage and manipulate data without hassle.
Security and Permissions: We prioritize data security, implementing robust measures to ensure that access and modifications are performed by authorized personnel only.
Scalability and Performance: Our application is designed to handle large datasets while maintaining optimal performance.

How to Use
Our application simplifies data management tasks:

Create: Click on the 'Create' button to add new data entries.

Read: Browse through the database using the search or navigation features to view existing data.

Update: Edit data fields by selecting the record and applying changes as needed.

Delete: Remove unwanted records by selecting them and confirming deletion.

Conclusion
Our CRUD application is a versatile tool, offering essential data management capabilities to streamline your workflow. It simplifies the process of handling data, ensuring efficiency, accuracy, and ease of use.
"""
def main():
    st.title("ToDo App")
    menu = ["Create","Read","Update","Delete","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    create_table()

    if choice == "Create":
        st.subheader("Add Items")
        col1,col2 = st.columns(2)

        with col1:
            task = st.text_area("Task to do")
        

        with col2:
            task_status = st.selectbox("Status",["ToDo","Doing","Done"])
            task_due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task,task_status,task_due_date)
            st.success("Successfully Added Task : {}".format(task))


    elif choice == "Read":
        st.subheader("View Items")
        result = view_all_data()
        # st.write(result)
        df = pd.DataFrame(result,columns=['Task','Status','Due Date'])
        with st.expander("View All Data"):
            st.dataframe(df)

        with st.expander("Task Status"):
            task_df = df['Status'].value_counts().to_frame()
            st.dataframe(task_df)

            task_df = task_df.reset_index()
            st.dataframe(task_df)

            # p1 = px.pie(task_df,names='index',values='Status')
            # st.plotly_chart(p1)


    elif choice == "Update":
        st.subheader("Edit/Update Items")
        result = view_all_data()
        df = pd.DataFrame(result,columns=['Task','Status','Due Date'])
        with st.expander("Current Data"):
            st.dataframe(df)

        list_of_task = [i[0] for i in view_unique_task()]
        selected_task = st.selectbox("Task To Edit",list_of_task)
        # st.write(list_of_task)
        selected_result = get_task(selected_task)
        # st.write(selected_result)

        if selected_result:
            task = selected_result[0][0]
            task_status = selected_result[0][1]
            task_date = selected_result[0][2]
            col1,col2 = st.columns(2)

            with col1:
                new_task = st.text_area("Update Task",task)
        

            with col2:
                new_task_status = st.selectbox(task_status,["ToDo","Doing","Done"])
                new_task_due_date = st.date_input(task_date)

            if st.button("Update Task"):
                edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_date)
                st.success("Successfully Updated Task ({}) to ->({})".format(task,new_task))

                result2 = view_all_data()
                df2 = pd.DataFrame(result2,columns=['Task','Status','Due Date'])
                with st.expander("UPDATED DATA"):
                    st.dataframe(df2)


    elif choice == "Delete":
        st.subheader("Delete")
        result = view_all_data()
        df = pd.DataFrame(result,columns=['Task','Status','Due Date'])
        with st.expander("Current Data"):
            st.dataframe(df)

        list_of_task = [i[0] for i in view_unique_task()]
        selected_task = st.selectbox("Task To Delete",list_of_task)
        st.warning("Do you want to delete {}".format(selected_task))
        if st.button("Delete Task"):
            delete_data(selected_task)
            st.success("Task has been Successfully Deleted")
        
        new_result = view_all_data()
        df2 = pd.DataFrame(new_result,columns=['Task','Status','Due Date'])
        with st.expander("Updated Data"):
            st.dataframe(df2)

    else:
        st.subheader("About")
        st.markdown(About)

if __name__ == '__main__':


    main()
