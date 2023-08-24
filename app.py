# IMPORTANDO BIBLIOTECAS DE TERCEIROS
from suds.client import Client
from tqdm import tqdm
import requests as r



# CONSTANTES
URL_SISTEMA: str = "seu_site.com"
URL_SOAP: str = "http://{}/sistema/webservices/geturlimage.php?wsdl".format(URL_SISTEMA)
TABELA: str = "tabela"
UNIDADE: str = "banco_de_dados"



# FUNÇÃO PARA REALIZAR O DOWNLOAD DO ARQUIVO
class BaixarArquivo:
    def __init__(self, url: str, img_key: str, table: str, unidade: str) -> None:
    
        # PARÂMETROS PARA MONTAGEM DA URL
        self.__img_key: str = img_key
        self.__table: str = table
        self.__unidade: str = unidade
        
        # INSTANCIANDO CLIENT
        client = Client(url)
        
        # MONTANDO URL
        self.__url_de_requisicao: str = client.service.geturlimage(self.__img_key, self.__table, self.__unidade)
        
        # REALIZANDO O DOWNLOAD
        self.__arquivo_tmp = r.get(self.__url_de_requisicao, stream=True)
        
    # MÉTODO PARA SALVAR O ARQUIVO EM UM CAMINHO ESPECÍFICADO
    def salva_arquivo(self, caminho_para_salvar: str) -> None:
    
        # GRAVRANDO O ARQUIVO BAIXADO NA MÁQUINA
        if self.__arquivo_tmp.status_code == 200:
            with open(caminho_para_salvar, 'wb') as arquivo:
                arquivo.write(self.__arquivo_tmp.content)
                    
            

def tratar_caracteres_indevidos(texto):
    texto = texto\
    .replace("\\","")\
    .replace("/","")\
    .replace("|","")\
    .replace("<","")\
    .replace(">","")\
    .replace("*","")\
    .replace(":","")\
    .replace("'","")\
    .replace("?","")\
    .replace('"',"")
    
    return texto
    
    
# APLICAÇÃO ######################################################################################
pasta_de_trabalho: str = input("\nINFORME A PASTA DE TRABALHO: ")
print("\n")

# ABRINDO TXT COM OS NOMES DOS ARQUIVOS
with open(pasta_de_trabalho + "\\lista_de_arquivos.txt", "r", encoding="utf-8") as lista_de_arquivos:
    
    # CONTANDO TOTAL DE ARQUIVOS A SEREM BAIXADOS PARA MONTAR BARRA DE PROGRESSO
    total_de_arquivos: int = sum(1 for arquivo in lista_de_arquivos)
    lista_de_arquivos.seek(0)
    
    for arquivo in tqdm(lista_de_arquivos, total = total_de_arquivos, desc = "PROGRESSO: "):
        
        reg_imagens_key, nome_do_arquivo = arquivo.strip().split("|@#")
        nome_do_arquivo = tratar_caracteres_indevidos(nome_do_arquivo)
        caminho_completo: str = "{}\\Files\\{}".format(pasta_de_trabalho, nome_do_arquivo)
        
        try:
            arquivo_tmp = BaixarArquivo(URL_SOAP, reg_imagens_key, TABELA, UNIDADE)
            arquivo_tmp.salva_arquivo(caminho_completo)
            
            with open(pasta_de_trabalho + "\\Log\\LOG_DE_SUCESSO.txt", "a", encoding="utf-8") as log_de_sucesso:
                log_de_sucesso.write("Sucesso ao baixar o arquivo '{}', caminho do arquivo: '{}'.\n".format(reg_imagens_key, caminho_completo))
            
        except Exception as erro_nao_tratado:
            with open(pasta_de_trabalho + "\\Log\\LOG_ERRO_NAO_TRATADO.txt", "a", encoding="utf-8") as log_erro_nao_tratado:
                log_erro_nao_tratado.write("Erro ao baixar o arquivo '{}'. | {}\n".format(reg_imagens_key, erro_nao_tratado))
