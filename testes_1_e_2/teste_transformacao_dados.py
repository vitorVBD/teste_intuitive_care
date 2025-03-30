import pandas as pd
import pdfplumber
import zipfile
import os
import pickle

def load_pdf_files():
    try:
        with open("pdf_files.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("Erro: Execute primeiro o teste_web_scraping.py")
        return []
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return []

pdf_files = load_pdf_files()

def extract_table_from_pdf(pdf_file_path):
    all_tables = []

    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            
            for table in tables:
                if table and len(table) > 1:
                    if table[0] and "PROCEDIMENTO" in str(table[0][0]).upper():
                        all_tables.extend(table)

    if not all_tables:
        return pd.DataFrame()
    
    df = pd.DataFrame(all_tables[1:], columns=all_tables[0])
    return df

def process_data(df):
    if df.empty:
        return df
    
    df = df.dropna(how='all').drop_duplicates()
    
    replacements = {
        'OD': 'Seg. Odontológico',
        'AMB': 'Seg. Ambulatorial'
    }
    
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = (
                df[col]
                .replace(replacements)
                .str.strip()
                .str.upper()
            )
    
    df.fillna({'VIGÊNCIA': 'SEM DATA', 'DUT': 0}, inplace=True)
    
    df['VIGÊNCIA'] = pd.to_datetime(df['VIGÊNCIA'], errors='coerce')
    
    relevant_columns = ['PROCEDIMENTO', 'VIGÊNCIA', 'OD', 'AMB', 'GRUPO', 'SUBGRUPO']
    df = df[[c for c in relevant_columns if c in df.columns]]
    
    df.sort_values(by=['GRUPO', 'PROCEDIMENTO'], inplace=True)
    
    print(f"✅ Dados processados. Shape final: {df.shape}")
    
    return df

def save_to_csv(df, csv_file_path):
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
    print(f"Arquivo CSV salvo em: {csv_file_path}")

def create_zip_with_csv(csv_file_path, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_file_path, os.path.basename(csv_file_path))
    print(f"Arquivo ZIP criado com sucesso: {zip_filename}")

def main():
    csv_filename = "Rol_de_Procedimentos.csv"
    zip_filename = "Teste_Vitor.zip"
    csv_file_path = os.path.join(os.path.expanduser("~/Downloads"), csv_filename)

    try:
        if not pdf_files:
            print("Nenhum PDF encontrado para processar.")
            return
            
        print("Extraindo dados do PDF...")
        df = extract_table_from_pdf(pdf_files[0])
        
        print("Processando dados...")
        processed_df = process_data(df)
        
        if not processed_df.empty:
            print("Salvando arquivo CSV...")
            save_to_csv(processed_df, csv_file_path)
            
            print("Criando arquivo ZIP...")
            create_zip_with_csv(csv_file_path, zip_filename)
            
            os.remove(csv_file_path)
            
            print("Processo finalizado com sucesso!")
        else:
            print("Nenhuma tabela válida encontrada no PDF.")

    except Exception as exc:
        print(f"Um erro inesperado ocorreu: {exc}")

if __name__ == "__main__":
    main()