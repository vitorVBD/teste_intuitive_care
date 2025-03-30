from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import zipfile
import os
import time

def setup_download_directory():
    project_root = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(project_root, "downloaded_pdfs")
    os.makedirs(download_dir, exist_ok=True)
    return download_dir

def configure_chrome_options(download_dir):
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("detach", True)
    return chrome_options

def initialize_browser(chrome_options):
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    return browser

def handle_cookie_consent(browser):
    browser.get('https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos')
    browser.find_element('xpath', '/html/body/div[5]/div/div/div/div/div[2]/button[2]').click()

def download_pdf_files(browser, download_dir):
    pdf_links = browser.find_elements('xpath', '//*[@id="cfec435d-6921-461f-b85a-b425bc3cb4a5"]/div/ol/li/a')
    pdf_files = []
    exclude_link_xpath = '//*[@id="cfec435d-6921-461f-b85a-b425bc3cb4a5"]/div/ol/li[1]/a[2]'

    for link in pdf_links:
        if link.get_attribute('href') != browser.find_element('xpath', exclude_link_xpath).get_attribute('href'):
            try:
                actions = ActionChains(browser)
                actions.key_down(Keys.ALT).click(link).key_up(Keys.ALT).perform()
                time.sleep(5)
            except Exception as exc:
                print(f"Erro ao baixar o arquivo: {exc}")

            files = os.listdir(download_dir)
            most_recent_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_dir, x)))
            pdf_files.append(os.path.join(download_dir, most_recent_file))
    
    return pdf_files

def create_zip_archive(download_dir, pdf_files):
    zip_path = os.path.join(download_dir, "PDFs_baixados.zip")
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for pdf in pdf_files:
                zipf.write(pdf, os.path.basename(pdf))
    except zipfile.BadZipFile as e:
        print(f"Erro ao criar o arquivo zip: {str(e)}")
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {str(e)}")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {str(e)}")
    else:
        print(f"Arquivo zip criado em: {zip_path}")

def main():
    download_dir = setup_download_directory()
    chrome_options = configure_chrome_options(download_dir)
    browser = initialize_browser(chrome_options)
    
    handle_cookie_consent(browser)
    pdf_files = download_pdf_files(browser, download_dir)
    browser.quit()
    
    create_zip_archive(download_dir, pdf_files)

    with open("pdf_files.pkl", "wb") as f:
        import pickle
        pickle.dump(pdf_files, f)

if __name__ == "__main__":
    main()
    