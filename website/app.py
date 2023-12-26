import streamlit as st
import pandas as pd
import pickle
import numpy as np
# Load Data
popularBooksData = pickle.load(open('popularBooks.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


def recommend(book_name):
    # index fetch
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    return data

def recommendation_page():
    st.title("Books Recommendation Engine")
    
    # Selectbox for book selection
    book_options = [''] + list(pt.index)
    book_input = st.selectbox('Enter a Book name:', book_options)

    

    if st.button('Recommend'):
        if book_input != 'Book Name':
            recommendations = recommend(book_input)
            if recommendations:
                st.write("Recommended Books:")
                for rec in recommendations:
                    st.write(f"Book-Title: {rec[0]}")
                    st.write(f"Book-Author: {rec[1]}")
                    # Display image if available
                    if rec[2]:
                        st.image(rec[2], width=250)
                    st.write("---")
            else:
                st.write("Sorry, no recommendations found for this book.")
        else:
            st.write("Please enter a book name.")
  



    



def display_top_50_books():
    st.title("Top 50 Books")

    # Load the popularBooksData
    # popularBooksData = load_data()

    # Create a DataFrame from the loaded popularBooksData
    df = pd.DataFrame(popularBooksData, columns=['Book-Title', 'Book-Author', 'Year-Of-Publication', 'num_rating', 'avg_rating', 'Image-URL-M'])

    # Display the book information
    for index, row in df.iterrows():
        st.header(row['Book-Title'])
        st.image(row['Image-URL-M'])
        
        st.write(f"Author: {row['Book-Author']}")
        st.write(f"Year of Publication: {row['Year-Of-Publication']}")
        st.write(f"Number of Ratings: {row['num_rating']}")
        st.write(f"Average Rating: {row['avg_rating']:.2f}")

        st.write("----")



def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", [ "Recommend Books", "Top 50 Books"])

    if selection == "Recommend Books":
        recommendation_page()
        
    elif selection == "Top 50 Books":
        display_top_50_books()

if __name__ == "__main__":
    main()
