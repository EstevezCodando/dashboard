import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def gerar_intervalos_operadores(df, data_atual=None):
    """
    Gera intervalos (data_inicio, data_fim, num_operadores)
    a partir de um DataFrame com colunas:
      - data (yyyy-mm-dd)
      - evento (Entrada ou Saida)
      - usuario
    Se data_atual for None, usa a data máxima encontrada no df ou a data do dia.
    """

    # 1) Garante que a coluna 'data' seja datetime (no formato date, sem horas)
    df['data'] = pd.to_datetime(df['data']).dt.date
    
    # 2) Marca evento como +1 para 'Entrada' e -1 para 'Saida'
    df['delta'] = df['evento'].apply(lambda x: 1 if x.lower() == 'entrada' else -1)

    # 3) Agrupa por (data, usuário), somando deltas, caso exista mais de um registro 
    # de entrada/saída do mesmo usuário na mesma data (não usual, mas previne inconsistências).
    eventos_por_data = (
        df.groupby(['data', 'usuario'], as_index=False)
          .agg({'delta': 'sum'})
    )

    # 4) Agrupa os dados por data, criando uma lista de (usuario, delta) para cada data.
    eventos_agrupados = (
        eventos_por_data.groupby('data')
                        .apply(lambda g: list(zip(g['usuario'], g['delta'])))
                        .reset_index(name='mudancas')
                        .sort_values('data')
                        .reset_index(drop=True)
    )
    
    # 5) Define a data_final. Se não for informada, pega o máximo entre a última data de evento
    # e a data do dia de hoje.
    if data_atual is None:
        data_final = max(eventos_agrupados['data'].max(), datetime.now().date())
    else:
        data_final = pd.to_datetime(data_atual).date()
    
    # 6) Percorre a sequência de datas de eventos, gerando intervalos. 
    #    Mantemos um conjunto de operadores ativos para saber quantos operadores estão ativos 
    #    em determinado intervalo.
    usuarios_ativos = set()
    intervalos = []
    
    # Lista ordenada das datas de evento
    datas_eventos = eventos_agrupados['data'].tolist()
    
    # Data inicial para o primeiro intervalo (a primeira data do CSV)
    data_inicial = datas_eventos[0]

    # Índice para percorrer as datas de evento
    idx_evento = 0
    
    # Enquanto houver eventos a processar...
    while idx_evento < len(datas_eventos):
        dia_evento = datas_eventos[idx_evento]
        
        # Se existe um "pulo" de data_inicial para dia_evento > data_inicial,
        # criamos um intervalo [data_inicial, dia_evento - 1]
        # pois no dia do evento a composição de operadores muda.
        if dia_evento > data_inicial:
            dia_fim = dia_evento - timedelta(days=1)
            if dia_fim >= data_inicial:
                intervalos.append({
                    'data_inicio': data_inicial,
                    'data_fim': dia_fim,
                    'num_operadores': len(usuarios_ativos)
                })
        
        # Pega as mudanças de operadores nesse dia_evento
        mudancas_do_dia = eventos_agrupados.loc[
            eventos_agrupados['data'] == dia_evento,
            'mudancas'
        ].values[0]
        
        # Primeiro removemos quem saiu (Saida = -1)
        saidas = [u for (u, d) in mudancas_do_dia if d < 0]
        for user in saidas:
            if user in usuarios_ativos:
                usuarios_ativos.remove(user)
        
        # Em seguida, adicionamos quem entrou (Entrada = +1)
        entradas = [u for (u, d) in mudancas_do_dia if d > 0]
        for user in entradas:
            usuarios_ativos.add(user)
        
        # Atualiza data_inicial para esse dia_evento
        data_inicial = dia_evento
        idx_evento += 1
    
    # Após processar todos os eventos, criamos o último intervalo 
    # [data_inicial, data_final] (se ainda estiver no intervalo de interesse).
    if data_inicial <= data_final:
        intervalos.append({
            'data_inicio': data_inicial,
            'data_fim': data_final,
            'num_operadores': len(usuarios_ativos)
        })
    
    # Converte intervalos para DataFrame
    df_intervalos = pd.DataFrame(intervalos)
    return df_intervalos


def gerar_dataframe_atividades(df_intervals):
    """
    df_intervals: DataFrame com colunas
        data_inicio, data_fim, num_operadores (todas date ou string)
    Retorna um DataFrame com
        date, atividades_dia, expected_cumulative
    """
    rows = []
    
    for _, row in df_intervals.iterrows():
        start = row['data_inicio']
        end   = row['data_fim']
        num_op = row['num_operadores']
        
        # Se estiverem como string, converte para date:
        if isinstance(start, str):
            start = datetime.strptime(start, '%Y-%m-%d').date()
        if isinstance(end, str):
            end   = datetime.strptime(end, '%Y-%m-%d').date()
        
        # Gera um registro para cada dia no intervalo
        current_day = start
        while current_day <= end:
            rows.append({
                'date': current_day,
                'atividades_dia': num_op
            })
            current_day += timedelta(days=1)
    
    df = pd.DataFrame(rows)
    df.sort_values('date', inplace=True)
    df['expected_cumulative'] = df['atividades_dia'].cumsum()
    return df

def plotar_grafico_atividades(df):
    """
    Plota o gráfico de atividades acumuladas esperadas ao longo do tempo.
    - df deve conter as colunas 'date' e 'expected_cumulative'.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['expected_cumulative'], marker='o')
    
    plt.title('Atividades Concluídas Esperadas ao Longo dos Dias')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Atividades (acumulada)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Caminho do CSV com os eventos de entrada/saída de operadores
    csv_path = r'C:\DevDash\Operadores_evento.csv'
    df = pd.read_csv(csv_path, encoding='utf-8')
    
    df_result = gerar_intervalos_operadores(df, data_atual='2025-01-27')
    df_atividades = gerar_dataframe_atividades(df_result)
    plotar_grafico_atividades(df_atividades)