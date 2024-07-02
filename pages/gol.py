import streamlit as st
import numpy as np
import time
from utils.page_config import page_congif


def update_grid(grid):
    new_grid = grid.copy()
    color_counts = {1: 0, 2: 0, 3: 0}

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            for color in [1, 2, 3]:
                live_neighbors = np.sum(
                    grid[max(0, i - 1):min(i + 2, grid.shape[0]), max(0, j - 1):min(j + 2, grid.shape[1])] == color) - (
                                             grid[i, j] == color)

                if grid[i, j] == color:
                    if live_neighbors < birth_rules[color] - 1 or live_neighbors > birth_rules[color]:
                        new_grid[i, j] = 0
                    else:
                        color_counts[color] += 1
                elif grid[i, j] == 0 and live_neighbors == birth_rules[color]:
                    new_grid[i, j] = color
                    color_counts[color] += 1

    return new_grid, color_counts


def draw_grid(grid):
    display_grid = np.full(grid.shape, "⬜", dtype='<U2')
    display_grid[grid == 1] = "🟩"
    display_grid[grid == 2] = "🟥"
    display_grid[grid == 3] = "🟦"
    grid_str = "\n".join(["".join(row) for row in display_grid])
    st.text(grid_str)


page_congif()
st.sidebar.title("Conway's Game of LifeStream")
st.sidebar.divider()

st.sidebar.subheader("Settings 🛠️")

st.sidebar.markdown("**Grid size 📅**", help="It's a square")
grid_size = st.sidebar.slider("Grid size", min_value=10, max_value=250, value=50, label_visibility='collapsed')

col1, col2 = st.sidebar.columns(2, gap="small")
col1.markdown('**Percentage of live cells (%)**', help="Default 10% for each colors")
prop_green = col1.slider("Green cells", min_value=0, max_value=100, value=20)
prop_red = col1.slider("Red cells", min_value=0, max_value=100 - prop_green, value=20)
prop_blue = col1.slider("Blue  cells", min_value=0, max_value=100 - prop_green - prop_red, value=20)
prob_green = prop_green / 100
prob_red = prop_red / 100
prob_blue = prop_blue / 100

col2.markdown("**Rule of birth and death of cells**", help="e.g: if 3 (default). So if a living cell has strictly less than 2 or more than 3 living cells around it, then it dies. If a dead cell has 3 living cells around it, then it is born")
birth_rules_green = col2.number_input("Green cells", value=3, min_value=2, step=1, max_value=8)
birth_rules_red = col2.number_input("Red cells", value=3, min_value=2, step=1, max_value=8)
birth_rules_blue = col2.number_input("Blue cells", value=3, min_value=2, step=1, max_value=8)

if 'grid' not in st.session_state:
    st.session_state.grid = np.random.choice(
        [0, 1, 2, 3],
        size=(grid_size, grid_size),
        p=[1 - (prob_green + prob_red + prob_blue), prob_green, prob_red, prob_blue]
    )

birth_rules = {
    1: birth_rules_green,
    2: birth_rules_red,
    3: birth_rules_blue
}

color_counts = {1: np.sum(st.session_state.grid == 1), 2: np.sum(st.session_state.grid == 2),
                3: np.sum(st.session_state.grid == 3)}

if st.sidebar.button("Reset grid 🔄️"):
    st.session_state.grid = np.random.choice(
        [0, 1, 2, 3],
        size=(grid_size, grid_size),
        p=[1 - (prob_green + prob_red + prob_blue), prob_green, prob_red, prob_blue]
    )

st.sidebar.divider()
col1p, col2p = st.sidebar.columns(2, gap="small")
if col1p.toggle("Automatic ⏯️"):
    st.session_state.grid, color_counts = update_grid(st.session_state.grid)
    st.text(f"🟩: {color_counts[1]} | 🟥: {color_counts[2]} | 🟦: {color_counts[3]}")
    draw_grid(st.session_state.grid)
    time.sleep(0.1)
    st.rerun()

if col2p.button("Next step 🦶🏽"):
    st.session_state.grid, color_counts = update_grid(st.session_state.grid)
st.text(f"🟩: {color_counts[1]} | 🟥: {color_counts[2]} | 🟦: {color_counts[3]}")
draw_grid(st.session_state.grid)
