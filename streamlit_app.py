import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests

st.set_page_config(page_title='Books Store', layout='wide')
st.markdown(
    """
    <style>
    #MainMenu {
        display:none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    div {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    

    
books_Asset_url ="https://github.com/iamanimesh11/intelligence_books_suggester_App/releases/download/Books.pkl/books.pkl"
popular_Asset_url ="https://github.com/iamanimesh11/intelligence_books_suggester_App/releases/download/Books.pkl/popular.pkl"
pt_asset_url="https://github.com/iamanimesh11/intelligence_books_suggester_App/releases/download/Books.pkl/pt.pkl"
similarity_Score_Asset_url="https://github.com/iamanimesh11/intelligence_books_suggester_App/releases/download/Books.pkl/similarity_scores.pkl"
# Load data
def download_asset(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Download the asset and save it with the desired filename
download_asset(books_Asset_url, 'books.pkl')
download_asset(pt_asset_url,'pt.pkl')
download_asset(similarity_Score_Asset_url,'similarity_scores.pkl')
download_asset(popular_Asset_url, 'popular.pkl')

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

def recommend(user_input):
    if not is_valid_input(user_input):
        return "Oops, not found! Try another one."
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return data

def is_valid_input(user_input):
    return user_input in pt.index

def main():

    
        
    page_options = ['Home', 'ML model']
    selected_page = st.sidebar.selectbox('Navigate to:', page_options)
    st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
    )


    st.sidebar.title('')
    # Navigation selectbox in the sidebar


    if selected_page == 'Home':
        # Stylish background
        st.title('Bestsellers Books Paradise')
        st.markdown('- Popularity based', unsafe_allow_html=True)
        st.sidebar.write('About this Page:')
        st.sidebar.write(
            'You can see the top most popular books fetched from dataset by using popularity based rating of books which are rated by atleast fixed number of users for valuability')


        st.markdown(
            """
            <style>
            body {
                background-color: #F5F5F5;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Show book list
        st.subheader('Popular Books')
        st.markdown("Made by Animesh | [Github](https://github.com/iamanimesh11) | [LinkedIn](https://www.linkedin.com/in/animesh-singh11)")

        # Custom CSS for card-like layout
        st.markdown(
            """
            <style>
            .book-item {
                background-color: black;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                overflow: hidden;
                transition: transform 0.3s;
                margin-bottom: 20px; /* Add spacing between rows */
            }
            .book-item:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2);
            }
            .book-image {
                height: 250px;
                object-fit: cover;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            .book-details {
                padding: 10px;
                text-align: center;
            }
            .book-title {
                font-size: 18px;
                font-weight: bold;
                color: #FFFFFF;
                margin-bottom: 5px;
            }
            .book-author {
                font-size: 16px;
                color: #777;
                margin-bottom: 10px;
            }
            .book-votes {
                color: #f00;
                margin-bottom: 5px;
            }
            .book-rating {
                color: #FFFF00;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Apply grid layout with 4 columns
        row = st.columns(4)

        for i in range(len(popular_df)):
            with row[i % 4]:
                # Add hover effect and card-like layout
                st.markdown(
                    f"""
                           <div class="book-item">
                               <img class="book-image" src="{popular_df['Image-URL-M'].iloc[i]}" alt="{popular_df['Book-Title'].iloc[i]}">
                               <div class="book-details">
                                   <p class="book-title">{popular_df['Book-Title'].iloc[i]}</p>
                                   <p class="book-author">Author: {popular_df['Book-Author'].iloc[i]}</p>
                                   <p class="book-votes">Votes: {popular_df['num_ratings'].iloc[i]}</p>
                                   <p class="book-rating">Rating: {popular_df['avg_ratings'].iloc[i] / 10 * 8:.1f}/5</p>
                               </div>
                           </div>
                           """,
                    unsafe_allow_html=True
                )

    elif selected_page == 'ML model':
        # Recommendation form
        st.title('Intelligence Books Suggester')
        st.markdown('-collaborative filtering based', unsafe_allow_html=True)
        st.sidebar.write('About this Page:')
        st.sidebar.write( 'Discovering your next favorite book has never been easier with our Intelligent Book Suggester.')
        st.sidebar.write( ' web app uses advanced collaborative filtering techniques to provide you with top-rated book recommendations based on your preferences with high accuracy.')


        user_input = st.selectbox('Type a book name:', [''] + list(pt.index))
        st.text("Try Books:Neverwhere,The Notebook, Icebound , A Walk to Remember,1984 ,To Kill a Mockingbird")

        if st.button("Tell me more like this.."):
            if user_input.strip() == "":
                st.warning('Please type something.')
            else:
                if not is_valid_input(user_input):
                    st.warning('Oops, not found! Please try another one.')
                else:
                    data = recommend(user_input)
                    if isinstance(data, list):
                        row = st.columns(5)
                        for i in range(len(data)):
                            with row[i % 5]:
                                st.image(data[i][2], width=150)
                                st.markdown(f"<h3 style='font-size: 16px;'>{data[i][0]}</h3>", unsafe_allow_html=True)
                                st.write(f"Author: {data[i][1]}")

    st.markdown("Made by Animesh | [Github](https://github.com/iamanimesh11) | [LinkedIn](https://www.linkedin.com/in/animesh-singh11)")

if __name__ == '__main__':
    main()
