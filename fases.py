import streamlit as st
from datetime import datetime, date, timedelta, timezone
import calendar

# --- Constantes e Funções de Cálculo Lunar ---
# Duração do mês sinódico (novilúnio a novilúnio)
LUNAR_CYCLE_DAYS = 29.530588853
# Data de referência: Lua Nova de 6 de Janeiro de 2000, 18:14 UTC
REFERENCE_NEW_MOON_UTC = datetime(2000, 1, 6, 18, 14, 0, tzinfo=timezone.utc)

# Nomes das fases da lua e emojis correspondentes em Português
MOON_PHASE_EMOJIS = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
MOON_PHASE_NAMES_PT = [
    "Lua Nova", "Crescente Iluminante", "Quarto Crescente", "Gibosa Crescente",
    "Lua Cheia", "Gibosa Minguante", "Quarto Minguante", "Minguante Iluminante"
]

# Nomes dos dias da semana e meses em Português
DAY_NAMES_PT = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
MONTH_NAMES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

def calculate_moon_phase(target_date: date):
    """
    Calcula a fase da lua para uma data específica.
    Retorna um dicionário com o nome da fase e o emoji.
    """
    # Converte o objeto date para datetime à meia-noite UTC para consistência
    target_datetime_utc = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=timezone.utc)

    # Calcula a diferença em segundos entre a data alvo e a data de referência da Lua Nova
    diff_seconds = (target_datetime_utc - REFERENCE_NEW_MOON_UTC).total_seconds()
    # Converte a diferença para dias
    diff_days = diff_seconds / (24 * 60 * 60)

    # Calcula a "idade" da lua no ciclo atual (quantos dias desde a última Lua Nova)
    moon_age = diff_days % LUNAR_CYCLE_DAYS
    # Garante que a idade seja positiva
    if moon_age < 0:
        moon_age += LUNAR_CYCLE_DAYS

    # Determina o índice da fase (0-7)
    phase_index = int(moon_age / (LUNAR_CYCLE_DAYS / 8))
    phase_index = phase_index % 8 # Garante que o índice esteja dentro do array (0-7)

    return {
        "name": MOON_PHASE_NAMES_PT[phase_index],
        "emoji": MOON_PHASE_EMOJIS[phase_index],
    }

# --- Interface do Streamlit ---
st.set_page_config(page_title="Calendário Lunar", layout="wide", initial_sidebar_state="expanded")

st.title("🌔 Calendário Lunar Interativo 🌕")
st.markdown("Selecione um mês e ano na barra lateral para visualizar o calendário lunar correspondente.")

# --- Seleção de Data na Sidebar ---
st.sidebar.header("🗓️ Selecione o Período")
current_time = datetime.now()
current_year = current_time.year
current_month_num = current_time.month

# Usamos listas separadas para garantir a ordem correta e mapeamento
available_years = list(range(current_year - 50, current_year + 51)) # Intervalo de 100 anos

# Seleção do ano
selected_year = st.sidebar.selectbox(
    "Ano",
    options=available_years,
    index=available_years.index(current_year) # Define o ano atual como padrão
)

# Seleção do mês
selected_month_name = st.sidebar.selectbox(
    "Mês",
    options=MONTH_NAMES_PT,
    index=current_month_num - 1 # current_month_num é 1-indexado
)
selected_month_num = MONTH_NAMES_PT.index(selected_month_name) + 1

st.header(f"{selected_month_name} de {selected_year}", anchor=False)

# --- Geração e Exibição do Calendário ---
# O calendário do Python começa a semana na Segunda-feira por padrão
cal = calendar.Calendar()
# monthdatescalendar retorna uma lista de semanas, onde cada semana é uma lista de objetos datetime.date
# Isso é útil pois já temos o objeto data completo para cada dia.
month_days_with_dates = cal.monthdatescalendar(selected_year, selected_month_num)

# Cabeçalho dos dias da semana
cols_header = st.columns(7)
for i, day_name in enumerate(DAY_NAMES_PT):
    cols_header[i].markdown(f"<p style='text-align:center; font-weight:bold; color: #FFC107;'>{day_name}</p>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top:0; margin-bottom:10px;'>", unsafe_allow_html=True)


# Dias do calendário
today = date.today()

for week in month_days_with_dates:
    cols_days = st.columns(7)
    for i, day_date_obj in enumerate(week):
        with cols_days[i]:
            # Verifica se o dia pertence ao mês selecionado
            is_current_month = (day_date_obj.month == selected_month_num)
            
            day_display_number = day_date_obj.day
            moon_info = calculate_moon_phase(day_date_obj) if is_current_month else {"name": "", "emoji": ""}

            # Estilização do dia
            text_color = "#FFFFFF"
            day_font_weight = "normal"
            cell_opacity = "1"
            
            if not is_current_month:
                text_color = "#FFFFFF" # Cinza para dias de outros meses
                cell_opacity = "0.6"
            
            is_today = (day_date_obj == today and is_current_month)
            border_style = "2px solid #FF0000" if is_today else "1px solid #4A4A4A"
            background_color = "rgba(255, 193, 7, 0.1)" if is_today else "rgba(46, 46, 46, 0.3)" # Fundo sutil para hoje

            st.markdown(
                f"""
                <div style="
                    min-height: 110px;
                    padding: 8px;
                    border-radius: 8px;
                    border: {border_style};
                    background-color: {background_color};
                    margin-bottom: 8px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: space-between;
                    opacity: {cell_opacity};
                ">
                    <div style="font-size: 1.1em; font-weight: {'bold' if is_today else day_font_weight}; color: {'#000000' if is_today else text_color};">
                        {day_display_number}
                    </div>
                    <div style="font-size: 2.2em; margin: 5px 0;" title="{moon_info['name'] if is_current_month else ''}">
                        {moon_info['emoji'] if is_current_month else '&nbsp;'}
                    </div>
                    <div style="font-size: 0.7em; text-align: center; color: #000000; min-height: 2.2em; line-height: 1.1em;">
                        {moon_info['name'] if is_current_month else '&nbsp;'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Rodapé ---
st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido com Python e Streamlit.")
st.sidebar.markdown("Fases da lua são aproximadas.")

st.markdown("---")
st.caption("As fases da lua são calculadas com base no ciclo sinódico médio. A data de referência para o cálculo é 6 de Janeiro de 2000, 18:14 UTC.")
st.caption("CopyRigth Multiverso Digital 2024. Todos os direitos reservados.")
st.markdown("Para mais informações, visite [Multiverso Digital](https://multiversodigital.com.br).")
st.markdown("Para sugestões e melhorias, entre em contato conosco através do nosso [e-mail](mailto:abreu@multiversodigital.com.br)")


