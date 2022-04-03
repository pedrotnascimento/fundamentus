#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from datetime import datetime
import pandas as pd

today = datetime.today()

# dd/mm/YY
scraped_date = today
# print(scraped_date)


def extract_number_data_from(table, position):
    #print(table.select('.data .txt')[position].string.strip())
    dado:str = table.select('.data .txt')[position].string.strip().strip('%')
    try:
        dado_number_formated:str = dado.replace(".", "").replace(",", ".")
        dado_ret: float = float(dado_number_formated)
    except Exception as ex:
        dado_ret = float(dado_number_formated.replace("-","0"))

    return dado_ret
def extract_str_data_from(table, position):
    #print(table.select('.data .txt')[position].string.strip())
    dado_ret:str = table.select('.data .txt')[position].string.strip()
    

    return dado_ret


def extract_data_from_oscilacoes(tables, position):
    #print(table.select('.data .txt')[position].string.strip())
    dado:str = tables[2].select('.data .oscil font')[position].string.strip('%')
    try:
        dado_number_formated:str = dado.replace(".", "").replace(",", ".")
        dado_ret: float = float(dado_number_formated)
    except Exception as ex:
        dado_ret = float(dado_number_formated.replace("-","0"))
    return dado_ret



def get_data():

    with open("tickers.txt", "r") as fundamentus_file:
        stocks = fundamentus_file.read().split()

    stocks_info = []
    print("iniciou processo: ")
    for stock in stocks:
        try:
            # print(stock)            # print("Getting data for Stock {}".format(stock))
            stock_url = "{}detalhes.php?papel={}".format(
                "http://fundamentus.com.br/", stock)
            #stock_url = ("http://fundamentus.com.br/" + str(stock))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
            page = requests.get(stock_url, headers=headers)
            html = BeautifulSoup(page.text, 'html.parser')

            # Tabelas
            # 0 - Cotação
            tables = html.select("table.w728")

            # print(tables)
            # print ("Descrição: ", extract_data_from(tables[0], 8))
            ano_corrente = datetime.now().year
            setor = extract_str_data_from(tables[0], 6)
            stock_data = {
                'scraped_date': str(scraped_date),
                # 0
                'codigo': stock,
                'cotacao': extract_number_data_from(tables[0], 1),
                'volume_2meses': extract_number_data_from(tables[0], 9),
                'data_cotacao': str(datetime.strptime(extract_str_data_from(tables[0], 3), '%d/%m/%Y')),
                'setor': setor,
                'subsetor': extract_str_data_from(tables[0], 8),
                # 1 - Valor de mercado
                'valor_mercado': extract_number_data_from(tables[1], 0),
                'valor_firma': extract_number_data_from(tables[1], 2),
                'numero_acoes': extract_number_data_from(tables[1], 3),
                # 2 - Indicadores fundamentalistas
                'pl': extract_number_data_from(tables[2], 0),
                'lpa': extract_number_data_from(tables[2], 1),
                'pvp': extract_number_data_from(tables[2], 2),
                'vpa': extract_number_data_from(tables[2], 3),
                'pebit': extract_number_data_from(tables[2], 4),
                'marg_bruta': extract_number_data_from(tables[2], 5),
                'psr': extract_number_data_from(tables[2], 6),
                'marg_ebit': extract_number_data_from(tables[2], 7),
                'pativos': extract_number_data_from(tables[2], 8),
                'marg_liquida': extract_number_data_from(tables[2], 9),
                'p_cap_giro': extract_number_data_from(tables[2], 10),
                'ebit_ativo': extract_number_data_from(tables[2], 11),
                'p_ativ_circ_liq': extract_number_data_from(tables[2], 12),
                'roic': extract_number_data_from(tables[2], 13),
                'div_yield': extract_number_data_from(tables[2], 14),
                'roe': extract_number_data_from(tables[2], 15),
                'ev_ebitida': extract_number_data_from(tables[2], 16),
                'liquidez_corr': extract_number_data_from(tables[2], 17),
                'giro_ativos': extract_number_data_from(tables[2], 18),
                'div_br_patrim': extract_number_data_from(tables[2], 19),
                'cres_rec_5a': extract_number_data_from(tables[2], 20),
                # 3 - Balanço patrimonial
                'ativo': extract_number_data_from(tables[3], 0),
                'disponibilidades': extract_number_data_from(tables[3], 2),
                # 4 - Demonstrativo de resultados
                'receita_Liquida_12': extract_number_data_from(tables[4], 0),
                'receita_Liquida_3': extract_number_data_from(tables[4], 1),
                'ebit_12': extract_number_data_from(tables[4], 2),
                'ebit_3': extract_number_data_from(tables[4], 3),
                'lucro_liquido_12': extract_number_data_from(tables[4], 2),
                'lucro_liquido_3': extract_number_data_from(tables[4], 3),
                'dia': extract_data_from_oscilacoes(tables, 0),
                'mes': extract_data_from_oscilacoes(tables, 1),
                '30_dias': extract_data_from_oscilacoes(tables, 2),
                '12_meses': extract_data_from_oscilacoes(tables, 3),
                str(ano_corrente): extract_data_from_oscilacoes(tables, 4),
                str(ano_corrente-1): extract_data_from_oscilacoes(tables, 5),
                str(ano_corrente-2): extract_data_from_oscilacoes(tables, 6),
                str(ano_corrente-3): extract_data_from_oscilacoes(tables, 7),
                str(ano_corrente-4): extract_data_from_oscilacoes(tables, 8),
                str(ano_corrente-5): extract_data_from_oscilacoes(tables, 9)
            }
            if not  setor in ["Bancos","Intermediários Financeiros"]:
                stock_data['ativo_circulante']  = extract_number_data_from(tables[3],4)
                stock_data['div_bruta']  =  extract_number_data_from(tables[3],1)
                stock_data['div_liquida']  =  extract_number_data_from(tables[3],3)
                stock_data['patrimonio_liquido']  =  extract_number_data_from(tables[3],5)
            else:
                stock_data['ativo_circulante'] = "0"
                stock_data['div_bruta']  = "0"
                stock_data['div_liquida']  = "0"
                stock_data['patrimonio_liquido']  =  extract_number_data_from(tables[3],3)
            stocks_info.append(stock_data)

        except Exception as ex:
            print(f'Erro {stock} : {ex}')

    # print(json.dumps(stocks_info))
    data = "["
    for x in stocks_info[:-1]:
        data = data+(json.dumps(x)+",\n")
    data += f"{json.dumps(stocks_info[-1])}]"

    json_filename = 'data2.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        f.write(data)
        f.close()

    converter_para_excel = True
    if converter_para_excel:
        try:
            csv_filename = 'data2.csv'
            df = pd.read_json(json_filename,)
            df.to_csv(csv_filename, index=None)
        except Exception as ex:
            print(ex)

    print(f">>>>>>>>>>>>>>>>>>> Processamento completo: Ver {json_filename}")
    # print(data)
    # return json.dumps(stocks_info, indent=4)
    return data


def get_todays_data():
    with open('data2.json', encoding='utf-8') as json_file:
        d = []
        for x in json_file:
            print(x)
            # d = d+(json.dumps(x)+"\n")
            d.append(x)
        print(d)
        return (', '.join(d))


# if __name__ == '__main__':
