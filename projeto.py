import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados do arquivo CSV
df = pd.read_csv('tiktok_dataset_100.csv')

# Título da página
st.title("Dashboard de Métricas do TikTok")

# Inicializar a sessão para armazenar os perfis seguidos
if 'followed_profiles' not in st.session_state:
    st.session_state['followed_profiles'] = []

# Inicializar a sessão para armazenar os criadores filtrados
if 'filtered_creators' not in st.session_state:
    st.session_state['filtered_creators'] = None

# Configuração de estilo e tema, incluindo animação no botão
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
    }
    
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #45a049;
    }

    .stButton>button:active {
        background-color: #2E7D32;
    }
    
    .profile-container {
        width: 300px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        margin-left: 50px;
    }

    .profile-picture {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid #4CAF50;
        object-fit: cover;
    }

    h1 {
        font-size: 20px;
        margin: 10px 0;
    }

    p.bio {
        color: gray;
        font-size: 14px;
        margin-bottom: 20px;
    }

    .stats {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }

    .stats div {
        text-align: center;
    }

    .stats div h2 {
        margin: 0;
        font-size: 18px;
        color: #333;
    }

    .stats div p {
        margin: 0;
        color: gray;
        font-size: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para exibir os perfis com botão "Seguir" ou "Deixar de Seguir"
def display_creators_with_button(filtered_df):
    for i, row in filtered_df.iterrows():
        perfil_id = row['User ID']
        followers = row['Followers']
        avg_view = row['AVG View']
        nicho = row['Nicho']
        
        # Layout do perfil adaptado do arquivo HTML
        st.markdown(f"""
            <div class="profile-container">
                <img src="https://via.placeholder.com/100" class="profile-picture" alt="Foto de perfil">
                <h1>{perfil_id}</h1>
                <p class="bio">Criador de conteúdo sobre {nicho}.</p>
                <div class="stats">
                    <div>
                        <h2>{avg_view}</h2>
                        <p>Visualizações</p>
                    </div>
                    <div>
                        <h2>{followers}</h2>
                        <p>Seguidores</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Botões de "Seguir" ou "Deixar de Seguir"
        if perfil_id in st.session_state['followed_profiles']:
            if st.button(f"Deixar de seguir {perfil_id}", key=f"unfollow_{perfil_id}"):
                st.session_state['followed_profiles'].remove(perfil_id)
        else:
            if st.button(f"Seguir {perfil_id}", key=f"follow_{perfil_id}"):
                st.session_state['followed_profiles'].append(perfil_id)
                st.success(f"Seguindo {perfil_id}!")

# Opções do menu
menu = ['Home', 'Melhores Criadores', 'Cadastrar Requisitos']
choice = st.sidebar.selectbox("Menu", menu)

# Exibir lista de perfis seguidos na barra lateral, abaixo do menu
st.sidebar.subheader("Perfis Seguidos")
if st.session_state['followed_profiles']:
    for perfil in st.session_state['followed_profiles']:
        st.sidebar.write(perfil)
else:
    st.sidebar.write("Nenhum perfil seguido.")

# Home - Exibe a lista de criadores com o botão "Seguir" ou "Deixar de Seguir"
if choice == 'Home':
    st.subheader("Lista de Criadores de Conteúdo")
    display_creators_with_button(df)

# Página "Melhores Criadores"
elif choice == 'Melhores Criadores':
    st.subheader("Melhores Criadores para a Campanha")
    
    # Selecionar o nicho para filtrar
    selected_niche = st.selectbox('Selecione o Nicho', df['Nicho'].unique())
    
    # Filtrar os dados com base no nicho selecionado
    filtered_df = df[df['Nicho'] == selected_niche]
    filtered_df = filtered_df.sort_values(by='AVG View', ascending=False).head(10)
    
    if not filtered_df.empty:
        # Gráfico de barras com os melhores criadores
        fig = px.bar(filtered_df, x='User ID', y='AVG View', title=f"Top Criadores no Nicho {selected_niche}")
        st.plotly_chart(fig)
    else:
        st.write("Nenhum criador encontrado para este nicho.")

# Página "Cadastrar Requisitos" - Exibe perfis com o botão de "Seguir" ou "Deixar de Seguir"
elif choice == 'Cadastrar Requisitos':
    st.subheader("Cadastrar Requisitos para Criadores de Conteúdo")
    
    # Selecionar o nicho
    selected_niche = st.selectbox('Selecione o Nicho', df['Nicho'].unique())
    
    # Entradas para requisitos
    min_followers = st.number_input("Quantidade mínima de seguidores", min_value=0, value=1000)
    min_avg_views = st.number_input("Média mínima de visualizações", min_value=0, value=5000)
    
    # Botão de buscar criadores
    if st.button('Buscar Criadores'):
        # Filtrar criadores com base nos requisitos
        st.session_state['filtered_creators'] = df[(df['Nicho'] == selected_niche) & 
                                                   (df['Followers'] >= min_followers) & 
                                                   (df['AVG View'] >= min_avg_views)]
        
    # Verificar se existem criadores filtrados e exibi-los com os botões
    if st.session_state['filtered_creators'] is not None:
        if not st.session_state['filtered_creators'].empty:
            st.subheader("Criadores Filtrados")
            display_creators_with_button(st.session_state['filtered_creators'])
        else:
            st.write("Nenhum criador encontrado com os requisitos fornecidos.")
