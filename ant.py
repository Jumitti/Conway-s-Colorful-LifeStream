import streamlit as st
import numpy as np
import time

# Directions pour Langton's Ant (N, E, S, W)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def update_ant_position(grid, ant_positions, ant_directions):
    # Récupère les états actuels des cases où se trouvent les fourmis
    current_states = [grid[pos] for pos in ant_positions]

    # Inverse les états des cases
    for i, pos in enumerate(ant_positions):
        grid[pos] = (current_states[i] + 1) % 4

    # Détermine les nouvelles directions en fonction des états actuels des cases
    for i, state in enumerate(current_states):
        if state == 0:  # Case blanche
            ant_directions[i] = (ant_directions[i] + 1) % 4  # Tourne à droite
        elif state == 1:  # Ant 1 (noir)
            ant_directions[i] = (ant_directions[i] - 1) % 4  # Tourne à gauche
        elif state == 2:  # Ant 2 (rouge)
            ant_directions[i] = (ant_directions[i] + 1) % 4  # Tourne à droite
        elif state == 3:  # Ant 3 (bleu)
            ant_directions[i] = (ant_directions[i] - 1) % 4  # Tourne à gauche

    # Déplace chaque fourmi dans sa nouvelle direction
    for i, pos in enumerate(ant_positions):
        ant_positions[i] = (pos[0] + directions[ant_directions[i]][0], pos[1] + directions[ant_directions[i]][1])

    # Gestion des bords de la grille (grille infinie)
    for i, pos in enumerate(ant_positions):
        ant_positions[i] = (pos[0] % grid.shape[0], pos[1] % grid.shape[1])

    return grid, ant_positions, ant_directions


def draw_grid_with_ants(grid, ant_positions):
    display_grid = np.full(grid.shape, "⬜", dtype='<U2')
    display_grid[grid == 1] = "⬛"
    display_grid[grid == 2] = "🟥"
    display_grid[grid == 3] = "🟦"

    # Place chaque fourmi sur la grille avec une icône spécifique
    for i, pos in enumerate(ant_positions):
        if i == 0:
            display_grid[pos] = "🐜"  # Ant 1
        elif i == 1:
            display_grid[pos] = "🐞"  # Ant 2
        elif i == 2:
            display_grid[pos] = "🦋"  # Ant 3

    grid_str = "\n".join(["".join(row) for row in display_grid])
    st.text(grid_str)


# Interface Streamlit
st.title("Langton's Ant Simulation with Multiple Insects")
st.sidebar.header("Paramètres de la simulation")

# Taille de la grille
grid_size = st.sidebar.slider("Taille de la grille", min_value=10, max_value=100, value=50)

# Sélection des insectes à inclure
include_ant1 = st.sidebar.checkbox("Inclure Ant 1 (noir)", True)
include_ant2 = st.sidebar.checkbox("Inclure Ant 2 (rouge)", False)
include_ant3 = st.sidebar.checkbox("Inclure Ant 3 (bleu)", False)

# Initialisation de la grille avec les fourmis sélectionnées au centre
if 'grid' not in st.session_state:
    grid = np.zeros((grid_size, grid_size), dtype=int)

    ant_positions = []
    ant_directions = []

    if include_ant1:
        ant_positions.append((grid_size // 2, grid_size // 2))
        ant_directions.append(0)  # Direction initiale (Nord)
    if include_ant2:
        ant_positions.append((grid_size // 2, grid_size // 2))
        ant_directions.append(1)  # Direction initiale (Est)
    if include_ant3:
        ant_positions.append((grid_size // 2, grid_size // 2))
        ant_directions.append(2)  # Direction initiale (Sud)
else:
    grid = st.session_state.grid
    ant_positions = st.session_state.ant_positions
    ant_directions = st.session_state.ant_directions

st.session_state.grid = grid
st.session_state.ant_positions = ant_positions
st.session_state.ant_directions = ant_directions

if st.sidebar.button("Reset grille"):
    grid = np.zeros((grid_size, grid_size), dtype=int)
    ant_positions = []
    ant_directions = []

    if include_ant1:
        ant_positions.append((grid_size // 2, grid_size // 2))
        ant_directions.append(0)  # Direction initiale (Nord)
    if include_ant2:
        ant_positions.append((grid_size // 2, grid_size // 2))
        ant_directions.append(1)  # Direction initiale (Est)
    if include_ant3:
        ant_positions.append((grid_size // 2, grid_size // 2))
        ant_directions.append(2)  # Direction initiale (Sud)

    st.session_state.grid = grid
    st.session_state.ant_positions = ant_positions
    st.session_state.ant_directions = ant_directions

st.sidebar.divider()

# Ajout d'un toggle pour l'exécution automatique
auto_run = st.sidebar.checkbox("Exécution automatique", False)

if auto_run:
    st.session_state.grid, st.session_state.ant_positions, st.session_state.ant_directions = update_ant_position(
        st.session_state.grid, st.session_state.ant_positions, st.session_state.ant_directions
    )
    draw_grid_with_ants(st.session_state.grid, st.session_state.ant_positions)
    time.sleep(0.1)  # Délai entre chaque étape pour visualisation
    st.rerun()

# Bouton pour avancer d'une étape manuellement
if not auto_run and st.sidebar.button("Étape suivante"):
    st.session_state.grid, st.session_state.ant_positions, st.session_state.ant_directions = update_ant_position(
        st.session_state.grid, st.session_state.ant_positions, st.session_state.ant_directions
    )
    draw_grid_with_ants(st.session_state.grid, st.session_state.ant_positions)
