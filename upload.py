from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import psycopg2

def authenticate_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

def connect_to_postgresql():
    conn = psycopg2.connect(
        dbname='Nome do seu banco de dados',
        user='Usuario',
        password='Sua senha',
        host='Seu host'
    )
    cursor = conn.cursor()
    return conn, cursor

def list_image_links(drive, folder_id):
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    image_data = [{'title': file['title'], 'link': file['alternateLink']} for file in file_list if file['mimeType'].startswith('image/')]
    return image_data
 
def insert_links_into_postgresql(cursor, tabela_imagens, image_data):
    for data in image_data:
        cursor.execute(f"INSERT INTO {tabela_imagens} (titulo, url_da_foto) VALUES ('{data['title']}', '{data['link']}')")

if __name__ == "__main__": 
    google_drive_folder_id = '1TTaWSQfuKBuzgtnGF_heL1JieT_nAi8x' # Exemplo de id da pasta do Google Drive
    tabela_imagens = "fotos"
 
    drive = authenticate_google_drive()
 
    conn, cursor = connect_to_postgresql()
 
    image_links = list_image_links(drive, google_drive_folder_id) 
    print(image_links)
 
    insert_links_into_postgresql(cursor, tabela_imagens, image_links)
    print("Migração Concluída! :)")
 
    conn.commit()
    conn.close()
