

class contatosApi:

    def contatosFilter(contatos):

        for contato in contatos:

            dic = {

                "contato_id"          : contato['id'],
                "autor"               : contato['autor']['id'],
                "autorAtualizacao_id" : contato['autorAtualizacao']['id'],
                "responsavel_id"      : contato['responsavel']['id'],
                "empresaAtual_id"     : contato['empresaAtual']['id']      if contato.get('empresaAtual') else None,
                "contatoPai_id"       : contato['contatoPai']['id']        if contato.get('contatoPai_id') else None,
                "nome"                : contato['nome'],
                "dataCriacao"         : contato['dataCriacao'],
                "dataAtualizacao"     : contato['dataAtualizacao'],
                "origem"              : contato['origem']                  if contato.get('origem') else None,
                "ativo"               : contato['ativo'],
                "empresa"             : contato['empresa'],
                "email"               : contato['email']                   if contato.get('email') else None ,
                "emailPrincipal"      : contato['emailPrincipal']          if contato.get('emailPrincipal') else None
            }

            yield dic


if __name__ == "__main__":

    import pandas as pd
    import numpy as np

    from nectra_lib import nectraApi

    url = "http://app.nectarcrm.com.br/crm/api/1/contatos/?displayLength=1"

    data = nectraApi.get(url)

    filters = contatosApi.contatosFilter(data)

    df = pd.DataFrame(filters)

    df.replace({np.nan: None},inplace=True)

    print(df.dtypes)


    