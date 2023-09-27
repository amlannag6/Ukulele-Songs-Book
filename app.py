import streamlit as st
import os
import base64
import webbrowser
from streamlit.components.v1 import html

# Streamlit app
st.title("Ukulele-Song-Book By AMLAN")

# Function to organize and store uploaded PDFs in the "songs" folder
def organize_and_store_pdfs(uploaded_files):
    song_dir = "songs"  # Specify the folder name
    os.makedirs(song_dir, exist_ok=True)
    stored_files = []

    for uploaded_file in uploaded_files:
        file_path = os.path.join(song_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        stored_files.append(file_path)

    # Add code to include PDFs from the "songs" folder
    stored_files.extend([os.path.join("songs", file) for file in os.listdir("songs") if file.endswith(".pdf")])

    return stored_files

# Function to display PDF content using base64 encoding
def display_pdf(pdf_path, auto_scroll=False):
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    # Embed the PDF viewer using HTML
    if auto_scroll:
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
            'width="100%" height="850px" style="scroll-behavior: smooth;"></iframe>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
            'width="100%" height="850px"></iframe>',
            unsafe_allow_html=True,
        )

# Function to open a YouTube Music link in the browser
def open_youtube_music(song_name):
    search_query = f"{song_name} ukulele cover"  # Modify this as needed
    url = f"https://music.youtube.com/search?q={search_query}"
    webbrowser.open(url)

# Define the folder where your PDFs are stored
pdf_folder = "songs"

# List all PDF files in the folder
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Main content section
st.sidebar.header("Song Selection Options:")
search_query = st.sidebar.text_input("Search by name:")

# Create an alphabetically organized list of available songs
alphabetical_songs = {}
for file_path in pdf_files:
    first_letter = file_path[0].upper() if file_path and file_path[0].isalpha() else '#'
    if first_letter not in alphabetical_songs:
        alphabetical_songs[first_letter] = []
    alphabetical_songs[first_letter].append((file_path, os.path.join(pdf_folder, file_path)))

# Sort the songs alphabetically
sorted_alphabetical_songs = sorted(alphabetical_songs.items())

# Create a sidebar section for the list of available songs
st.sidebar.subheader("Available Songs")

# Create a dropdown for selecting a letter
selected_letter = st.sidebar.selectbox("Select a letter:", ["All"] + [letter for letter, _ in sorted_alphabetical_songs])

# Display songs starting with the selected letter
if selected_letter == "All":
    for letter, songs in sorted_alphabetical_songs:
        st.sidebar.subheader(f"Songs Starting with '{letter}'")
        for file_path, pdf_path in songs:
            # Change the link to display the selected PDF when clicked
            if st.sidebar.button(file_path):
                st.subheader(f"Currently Viewing: {file_path}")
                pdf_path = os.path.join(pdf_folder, file_path)
                display_pdf(pdf_path, auto_scroll=True)
                # Add a YouTube Music button to open the song in YouTube Music
                if st.button(f"Listen to '{file_path}' on YouTube Music"):
                    open_youtube_music(file_path)
else:
    selected_songs = alphabetical_songs.get(selected_letter, [])
    st.sidebar.subheader(f"Songs Starting with '{selected_letter}'")
    for file_path, pdf_path in selected_songs:
        # Change the link to display the selected PDF when clicked
        if st.sidebar.button(file_path):
            st.subheader(f"Currently Viewing: {file_path}")
            pdf_path = os.path.join(pdf_folder, file_path)
            display_pdf(pdf_path, auto_scroll=True)
            # Add a YouTube Music button to open the song in YouTube Music
            if st.button(f"Listen to '{file_path}' on YouTube Music"):
                open_youtube_music(file_path)

# Create a sidebar section for Admin functions
st.sidebar.subheader("Admin Section")

# Create a password input field
password_input = st.sidebar.text_input("Enter Password:", type="password")

# Define the correct password
correct_password = "1999"

if password_input == correct_password:
    # Display the Admin functions if the password is correct
    st.sidebar.subheader("Admin Functions")

    # Upload PDF Songs
    uploaded_files = st.sidebar.file_uploader("Upload PDF Songs (Limit 200MB per file • PDF)", type=["pdf"], accept_multiple_files=True)
    stored_files = []  # Initialize the list here

    if uploaded_files:
        st.sidebar.subheader("Uploaded PDF Songs:")
        stored_files = organize_and_store_pdfs(uploaded_files)
        for file_path in stored_files:
            st.sidebar.write(file_path)

    # Fetch PDFs from Website
    if st.sidebar.button("Fetch PDFs from Website"):
        st.sidebar.text("Downloading PDFs from the website...")
        # Add code to fetch PDFs here

        # Provide a message indicating that the download has finished
        st.sidebar.text("PDFs downloaded successfully!")

else:
    # Display a message if the password is incorrect
    st.sidebar.warning("Incorrect password. Please enter the correct password to access Admin functions.")

# Run the Streamlit app
if __name__ == "__main__":
    st.sidebar.text("Amlan's Personal Song-Book")