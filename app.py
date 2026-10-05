import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="FFKARAOKE", page_icon="🎤", layout="wide")

# Inicialização de Estados (Base de dados simulada em memória/sessão)
if "prestadores" not in st.session_state:
    st.session_state.prestadores = pd.DataFrame(columns=["Nome", "Telefone", "Pagamento", "Estado"])
if "fila_musicas" not in st.session_state:
    st.session_state.fila_musicas = []
if "clientes_qrcode" not in st.session_state:
    st.session_state.clientes_qrcode = []

st.title("🎵 FFKARAOKE - Sistema Profissional")

# Menu Lateral de Navegação por Perfis
menu = st.sidebar.selectbox("Escolha o Perfil", ["Administrador", "Prestador de Serviço", "Cliente (Via QR Code)"])

# ==========================================
# 1. PERFIL: ADMINISTRADOR
# ==========================================
if menu == "Administrador":
    st.header("Painel do Administrador (FFKARAOKE)")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Pedidos Pendentes", "Pedidos de Reforços", "Prestadores Online", "Registo Global"])
    
    with tab1:
        st.subheader("Aprovação de Novos Prestadores")
        # Simulação de dados pendentes
        nome_p = st.text_input("Nome do Prestador (Registo Direto / Teste)")
        tel_p = st.text_input("Telefone")
        pag_p = st.text_input("Comprovativo de Pagamento")
        if st.button("Enviar Pedido de Registo"):
            novo = pd.DataFrame([[nome_p, tel_p, pag_p, "Pendente"]], columns=["Nome", "Telefone", "Pagamento", "Estado"])
            st.session_state.prestadores = pd.concat([st.session_state.prestadores, novo], ignore_index=True)
            st.success("Pedido enviado com sucesso!")
            
        pendentes = st.session_state.prestadores[st.session_state.prestadores["Estado"] == "Pendente"]
        st.dataframe(pendentes)
        
        if not pendentes.empty:
            idx = st.number_input("Índice para Aprovar/Recusar", min_value=0, max_value=len(pendentes)-1, step=1)
            col_a, col_r = st.columns(2)
            if col_a.button("Aprovar"):
                real_idx = pendentes.index[idx]
                st.session_state.prestadores.at[real_idx, "Estado"] = "Aprovado"
                st.success("Prestador Aprovado!")
                st.rerun()
            if col_r.button("Recusar"):
                real_idx = pendentes.index[idx]
                st.session_state.prestadores.at[real_idx, "Estado"] = "Recusado"
                st.warning("Prestador Recusado!")
                st.rerun()

    with tab2:
        st.subheader("Pedidos de Reforço de Contrato")
        st.info("Aqui aparecerão os pedidos de renovação de contrato dos prestadores.")

    with tab3:
        st.subheader("Prestadores Online no Momento")
        aprovados = st.session_state.prestadores[st.session_state.prestadores["Estado"] == "Aprovado"]
        st.dataframe(aprovados)

    with tab4:
        st.subheader("Registo Global (Todos os Prestadores)")
        st.dataframe(st.session_state.prestadores)

# ==========================================
# 2. PERFIL: PRESTADOR DE SERVIÇO
# ==========================================
elif menu == "Prestador de Serviço":
    st.header("Painel do Prestador - FFKARAOKE")
    
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.subheader("📺 Leitor de Vídeo e Fila de Reprodução")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Exemplo de leitor
        
        st.markdown("---")
        st.markdown("### ⚙️ Controlos Profissionais")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📤 Separar Vídeo para 2ª Tela"):
                st.info("Modo de segunda tela ativado (janela flutuante/pop-up pronta para projetor).")
        with c2:
            if st.button("🎤 Remover Voz (Modo Karaoke)"):
                st.success("Frequências vocais isoladas do vídeo!")
        with c3:
            if st.button("🔍 Pesquisar Música na Internet"):
                st.text_input("Procurar link para download direto:")
        
        st.subheader("Playlist Atual (Próximos Cantores)")
        if st.session_state.fila_musicas:
            for i, musica in enumerate(st.session_state.fila_musicas):
                st.write(f"**{i+1}.** 🎵 {musica['musica']} - Cantor: **{musica['cliente']}** (Posição: {i+1})")
        else:
            st.info("Ainda não há músicas na playlist.")

    with col_r:
        st.subheader("📱 QR Code para Clientes")
        st.markdown("Mostre este código na mesa ou tela para os clientes pedirem músicas:")
        # Simulação visual de QR Code
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=FFKARAOKE_CLIENTE", width=180)
        
        st.markdown("---")
        st.subheader("Adicionar Música Manualmente")
        musica_manual = st.text_input("Nome da Música")
        cliente_manual = st.text_input("Nome do Cliente")
        if st.button("Inserir na Playlist"):
            st.session_state.fila_musicas.append({"musica": musica_manual, "cliente": cliente_manual})
            st.success("Adicionado à playlist!")
            st.rerun()

# ==========================================
# 3. PERFIL: CLIENTE (VIA QR CODE)
# ==========================================
elif menu == "Cliente (Via QR Code)":
    st.header("🎤 Bem-vindo ao FFKARAOKE")
    st.markdown("Insira os seus dados para pedir a sua música e subir ao palco!")
    
    with st.form("form_cliente"):
        nome_cliente = st.text_input("Como gostaria de ser chamado?")
        tel_cliente = st.text_input("Número de Telefone")
        selfie_cliente = st.file_uploader("Quer carregar uma selfie? (Para gerar caricatura)", type=["png", "jpg", "jpeg"])
        musica_desejada = st.text_input("Qual música quer cantar?")
        
        enviar_pedido = st.form_submit_button("Enviar Pedido de Música")
        
        if enviar_pedido and nome_cliente and musica_desejada:
            st.session_state.fila_musicas.append({"musica": musica_desejada, "cliente": nome_cliente})
            st.success(f"Pedido enviado com sucesso, {nome_cliente}!")
            
    if st.session_state.fila_musicas:
        st.markdown("---")
        st.subheader("📊 O seu Estado na Fila")
        posicao = len(st.session_state.fila_musicas)
        st.info(F"A sua posição atual na fila é: **{posicao}**. Prepare-se!")
