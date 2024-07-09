import streamlit as st
import numpy as np
import time
import random
from utils.page_config import page_congif


def update_ant_position(grid, ant_positions, ant_directions, ant_colors):
    new_positions = []

    for i, pos in enumerate(ant_positions):
        current_state = grid[pos] if grid[pos] == ant_colors[i] or grid[pos] == 0 else 0

        grid[pos] = ant_colors[i] if current_state == 0 else 0

        if current_state == 0:
            ant_directions[i] = (ant_directions[i] + 1) % 4
        else:
            ant_directions[i] = (ant_directions[i] - 1) % 4

        new_pos = (pos[0] + directions[ant_directions[i]][0], pos[1] + directions[ant_directions[i]][1])
        new_pos = (new_pos[0] % grid.shape[0], new_pos[1] % grid.shape[1])

        new_positions.append(new_pos)

    for i, new_pos in enumerate(new_positions):
        if new_positions.count(new_pos) > 1:
            new_positions[i] = ant_positions[i]

    ant_positions = new_positions

    return grid, ant_positions, ant_directions


def count_colors(grid):
    colors = ["⬜", "⬛", "🟥", "🟧", "🟫", "🟪", "🟦", "🟨", "🟩"]

    counts = [np.count_nonzero(grid == i) for i in range(len(colors))]
    counts_text = " | ".join(f"{colors}: {count}" for colors, count in zip(colors, counts))
    st.text(counts_text)


def draw_grid_with_ants(grid, ant_positions):
    colors = ["⬛", "🟥", "🟧", "🟫", "🟪", "🟦", "🟨", "🟩"]
    bugs = ["🐜", "🐞", "🦋", "🐌", "🕷️", "🦂", "🐝", "🦗"]

    display_grid = np.full(grid.shape, "⬜", dtype='<U2')

    for i in range(1, len(colors) + 1):
        display_grid[grid == i] = colors[i - 1]

    for i, pos in enumerate(ant_positions):
        if i < len(bugs):
            display_grid[pos] = bugs[i]

    grid_str = "\n".join(["".join(row) for row in display_grid])
    st.text(grid_str)


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

page_congif()
st.sidebar.title("Langton's AntLit")
st.sidebar.divider()

st.sidebar.subheader("Settings 🛠️")

st.sidebar.markdown("**Grid size 📅**")
width_size = st.sidebar.slider("Width size ➡️", min_value=10, max_value=250, value=50, step=1)
length_size = st.sidebar.slider("Length size ⬇️", min_value=10, max_value=250, value=50, step=1)

st.sidebar.markdown("**Number of bugs 🐜**", help="Default 3")
number_bugs = st.sidebar.number_input("Number of bugs", value=3, step=1, min_value=1, max_value=8,
                                      label_visibility="collapsed")

if 'grid_ant' not in st.session_state:
    grid_ant = np.zeros((length_size, width_size), dtype=int)

    ant_positions = []
    ant_directions = []
    ant_colors = []

    for i in range(1, number_bugs + 1):
        ant_positions.append((random.randint(0, length_size - 1), random.randint(0, width_size - 1)))
        ant_directions.append(random.randint(0, 3))
        ant_colors.append(i)

else:
    grid_ant = st.session_state.grid_ant
    ant_positions = st.session_state.ant_positions
    ant_directions = st.session_state.ant_directions
    ant_colors = st.session_state.ant_colors

st.session_state.grid_ant = grid_ant
st.session_state.ant_positions = ant_positions
st.session_state.ant_directions = ant_directions
st.session_state.ant_colors = ant_colors

if st.sidebar.button("Reset grid 🔄️"):
    grid_ant = np.zeros((length_size, width_size), dtype=int)

    ant_positions = []
    ant_directions = []
    ant_colors = []

    for i in range(1, number_bugs + 1):
        ant_positions.append((random.randint(0, length_size - 1), random.randint(0, width_size - 1)))
        ant_directions.append(random.randint(0, 3))
        ant_colors.append(i)

    st.session_state.grid_ant = grid_ant
    st.session_state.ant_positions = ant_positions
    st.session_state.ant_directions = ant_directions
    st.session_state.ant_colors = ant_colors

st.sidebar.divider()
col1, col2 = st.sidebar.columns(2, gap="small")
if col1.toggle("Automatic ⏯️"):
    st.session_state.grid_ant, st.session_state.ant_positions, st.session_state.ant_directions = update_ant_position(
        st.session_state.grid_ant, st.session_state.ant_positions, st.session_state.ant_directions,
        st.session_state.ant_colors
    )
    count_colors(st.session_state.grid_ant)
    draw_grid_with_ants(st.session_state.grid_ant, st.session_state.ant_positions)
    time.sleep(0.1)
    st.rerun()

if col2.button("Next step 🦶🏽"):
    st.session_state.grid_ant, st.session_state.ant_positions, st.session_state.ant_directions = update_ant_position(
        st.session_state.grid_ant, st.session_state.ant_positions, st.session_state.ant_directions,
        st.session_state.ant_colors)

count_colors(st.session_state.grid_ant)
draw_grid_with_ants(st.session_state.grid_ant, st.session_state.ant_positions)
