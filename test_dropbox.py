
import streamlit as st
import os
import io
import dropbox

# Initialize Streamlit page
st.set_page_config(page_title='🦜🔗 Ask the Doc App')
st.title('🦜🔗 Ask the Doc App')

# Dropbox access token
DROPBOX_ACCESS_TOKEN = 'sl.Bm8jxBX__OKwEG2QstJGBtVictWyU7KfbbnpdelGyPW0BGIS2CTV3avy_38DaFjuhkK3ZbuCwBRP0BBOwEwVnKPy0qkdmkt0iWCC6xPZY9QlmYaAJTYwsdhdja2aZsqy0JcBuYlRnTPoyhbt3Ag4vxc'  # Replace with your actual access token

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Function to list files in the "test-llm" folder with extensions .pdf and .txt
def list_dropbox_files(folder_path):
    files = []
    try:
        for entry in dbx.files_list_folder(folder_path).entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                if entry.name.lower().endswith(('.pdf', '.txt','.docx')):
                    files.append(entry)
        return files
    except Exception as e:
        st.error(f"Failed to list files in Dropbox: {str(e)}")
        return []

# List files in the "test-llm" folder
dropbox_folder_path = '/test-llm'
files_in_dropbox = list_dropbox_files(dropbox_folder_path)

# Function to download files from Dropbox and store them as variables
def download_and_store_files(files):
    file_data = {}  # Dictionary to store file data

    for file_metadata in files:
        try:
            file_path = file_metadata.path_display
            _, response = dbx.files_download(file_path)
            file_content = response.content
            file_data[file_metadata.name] = file_content
        except Exception as e:
            st.error(f"Failed to download file '{file_metadata.name}' from Dropbox: {str(e)}")

    return file_data

# Function to upload a file to Dropbox
def upload_file_to_dropbox(file, folder_path):
    try:
        # Specify the path and file name in Dropbox
        dropbox_path = f"{folder_path}/{file.name}"

        # Read the file
        file_content = file.read()

        # Upload the file to Dropbox
        dbx.files_upload(file_content, dropbox_path)

        return True
    except Exception as e:
        st.error(f"Failed to upload file '{file.name}' to Dropbox: {str(e)}")
        return False

# Display the list of downloaded file names with delete options
selected_files = st.multiselect("Select files to delete", [file.name for file in files_in_dropbox])
if st.button("Delete Selected Files"):
    for file_name in selected_files:
        file_path = os.path.join(dropbox_folder_path, file_name)
        try:
            dbx.files_delete_v2(file_path)
            st.success(f"File '{file_name}' deleted successfully.")
        except Exception as e:
            st.error(f"Failed to delete file '{file_name}' from Dropbox: {str(e)}")

# Display the list of downloaded file names
st.write(f"Downloaded files from Dropbox:")
for file_name in files_in_dropbox:
    st.write(file_name.name)

# Now you can access the file contents using the downloaded_files dictionary
# For example, to access the content of a file named 'example.pdf':
# content = downloaded_files['example.pdf']

# Upload file button
uploaded_file = st.file_uploader("Upload a new file to Dropbox", type=['pdf', 'txt','docx'])
if uploaded_file is not None:
    if upload_file_to_dropbox(uploaded_file, dropbox_folder_path):
        st.success(f"File '{uploaded_file.name}' uploaded to Dropbox successfully.")
