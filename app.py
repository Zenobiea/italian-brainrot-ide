import streamlit as st
import re
import sys
import io
import contextlib
import traceback
import random

KEYWORDS = {
    "Tralalero Tralala": "assignment_start",
    "Bombardiro Crocodilo": "print_command",
    "U Din Din Din Din Dun Ma Din Din Din Dun": "int(input())",
    "Lirili Larila": "if",
    "Gusini": ":",
    "Boneca Ambalabu": "else:",
    "Trulimero Trulicina": "dedent_marker",
    "Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur": "while",
    "Bananini": ":",
    "Ballerina Cappucina": "dedent_marker",
    "Frigo Camelo Trippi Troppi": ">=",
    "Bombombini Gusini Gusini Trippi Troppi": "<=",
    "Bombombini Gusini Gusini": "<",
    "Frigo Camelo": ">",
    "Trippi Troppi": "==",
    "La Vaca Saturno Saturnita": "!=",
    "Brr Brr Patapim": "+",
    "Chimpanzini Bananini": "-",
    "Bombombini Gusini": "*",
    "Capuccino Assassino": "/",
    "RANDOM_TRALALERO": "random_command"
}

KEYWORD_HELP = """
**Basics ong:**
*   `Tralalero Tralala var Trippi Troppi val` : Assign val 2 var (e.g., `Tralalero Tralala x Trippi Troppi 10`)
*   `Tralalero Tralala var Trippi Troppi RANDOM_TRALALERO min max` : Assign random int (e.g., `Tralalero Tralala cpu Trippi Troppi RANDOM_TRALALERO 1 3`)
*   `Bombardiro Crocodilo val_or_var` : Print stuff (e.g., `Bombardiro Crocodilo x`)

**Control Flow fr:**
*   `Lirili Larila condition Gusini` : If statement
*   `Boneca Ambalabu` : Else statement
*   `Trulimero Trulicina` : End If/Else block
*   `Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur condition Bananini` : While loop
*   `Ballerina Cappucina` : End While loop block

**Operators icl:**
*   `Brr Brr Patapim` : `+` | `Chimpanzini Bananini` : `-` | `Bombombini Gusini` : `*` | `Capuccino Assassino` : `/`
*   `Trippi Troppi` : `==` | `La Vaca Saturno Saturnita` : `!=`
*   `Frigo Camelo` : `>` | `Bombombini Gusini Gusini` : `<`
*   `Frigo Camelo Trippi Troppi` : `>=` | `Bombombini Gusini Gusini Trippi Troppi` : `<=`

**Comments:** `#` ignored lol
**Note:** Input (`U Din Din...`) disabled 4 web. Player choice comes from UI buttons now.
"""


def translate_expression(expression_str):
    if KEYWORDS["U Din Din Din Din Dun Ma Din Din Din Dun"] in expression_str:
         raise ValueError("OMG Error! Input ('U Din Din...') disabled 4 web.")
    if KEYWORDS["RANDOM_TRALALERO"] in expression_str:
         raise SyntaxError("RANDOM_TRALALERO gotta be used in assignment directly, not inside stuff.")

    temp_expression = expression_str
    for br, py in sorted(KEYWORDS.items(), key=lambda item: len(item[0]), reverse=True):
         if py not in [":", "else:", "dedent_marker", "if", "while", "print_command", "assignment_start", "int(input())", "random_command"]:
             temp_expression = temp_expression.replace(br, py)
    return temp_expression

def transpile_to_python(brainrot_code):
    indent_level = 0
    indent_space = "    "
    lines = brainrot_code.splitlines()
    processed_lines_with_levels = []
    line_number = 0

    for line in lines:
        line_number += 1
        stripped_line = line.strip()
        current_line_level = indent_level

        if stripped_line.startswith('#') or not stripped_line:
            processed_lines_with_levels.append((current_line_level, stripped_line))
            continue

        if stripped_line == "Trulimero Trulicina" or stripped_line == "Ballerina Cappucina":
            if indent_level == 0:
                raise IndentationError(f"OMG Indent Error! Dedent ('{stripped_line}') no match on line {line_number}")
            indent_level -= 1
            current_line_level = indent_level
            processed_lines_with_levels.append((current_line_level, "# dedent marker"))
            continue

        if stripped_line == "Boneca Ambalabu":
            if indent_level == 0:
                 raise IndentationError(f"OMG Indent Error! Else ('{stripped_line}') no match on line {line_number}")
            current_line_level = indent_level - 1
            processed_lines_with_levels.append((current_line_level, "else:"))
            continue

        processed_lines_with_levels.append((current_line_level, stripped_line))

        if stripped_line.startswith("Lirili Larila") or \
           stripped_line.startswith("Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur"):
            indent_level += 1


    final_python_code = []
    for level, line_content in processed_lines_with_levels:
        if line_content == "# dedent marker": continue

        current_indent = indent_space * level
        original_line = line_content
        processed_line = original_line.strip()

        assign_match = re.match(r"Tralalero Tralala\s+(\w+)\s+Trippi Troppi\s+(.*)", processed_line)
        if assign_match:
            var_name = assign_match.group(1)
            expression = assign_match.group(2).strip()
            random_match = re.match(r"RANDOM_TRALALERO\s+(\S+)\s+(\S+)", expression)
            if random_match:
                 min_val_str = random_match.group(1)
                 max_val_str = random_match.group(2)
                 min_val_translated = translate_expression(min_val_str)
                 max_val_translated = translate_expression(max_val_str)
                 processed_line = f"{var_name} = random.randint({min_val_translated}, {max_val_translated})"
            else:
                 translated_expr = translate_expression(expression)
                 processed_line = f"{var_name} = {translated_expr}"

        elif processed_line.startswith("Bombardiro Crocodilo"):
            print_match = re.match(r"Bombardiro Crocodilo(?:\s+(.*))?", processed_line)
            if print_match:
                expression = print_match.group(1)
                if expression:
                    translated_expr = translate_expression(expression.strip())
                    processed_line = f"print({translated_expr})"
                else:
                    processed_line = "print()"
            else:
                 processed_line = "print()"

        elif processed_line.startswith("Lirili Larila"):
             if_match = re.match(r"Lirili Larila\s+(.*?)\s+Gusini", processed_line)
             if if_match:
                 condition = if_match.group(1).strip()
                 translated_cond = translate_expression(condition)
                 processed_line = f"if {translated_cond}:"
             else:
                  raise SyntaxError(f"Bruh, ur Lirili Larila syntax kinda sus: {original_line}")

        elif processed_line.startswith("Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur"):
            while_match = re.match(r"Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur\s+(.*?)\s+Bananini", processed_line)
            if while_match:
                condition = while_match.group(1).strip()
                translated_cond = translate_expression(condition)
                processed_line = f"while {translated_cond}:"
            else:
                 raise SyntaxError(f"Bruh, ur Tung Tung Tung syntax kinda sus: {original_line}")

        elif processed_line == "else:":
            pass
        elif processed_line.startswith('#') or not processed_line:
            pass


        if processed_line or (original_line.startswith('#')):
             final_python_code.append(current_indent + processed_line)
        elif original_line and not original_line.strip():
             final_python_code.append("")


    return "\n".join(final_python_code)


st.set_page_config(page_title="Italian Brainrot IDE", layout="wide")
st.title("Italian Brainrot Interpreter frfr icl im genius ikr </3")
st.caption("Drop ur 'Tralalero Tralala' code below & peep the magic ong cuhhh")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ur Brainrot Code:")
    example_code = """# RPS - Brainrot Edition! fr fr
Bombardiro Crocodilo "Ayo! Welcome 2 Bombardiro Sasso Carta Forbice!"

# Define choices: 1=Sasso (Rock), 2=Carta (Paper), 3=Forbice (Scissors)
Tralalero Tralala SCELTA_SASSO Trippi Troppi 1
Tralalero Tralala SCELTA_CARTA Trippi Troppi 2
Tralalero Tralala SCELTA_FORBICE Trippi Troppi 3

# Player's Choice now comes from the UI buttons!
# The variable _player_choice_from_ui holds the value (1, 2, or 3)
Tralalero Tralala scelta_giocatore Trippi Troppi _player_choice_from_ui

Bombardiro Crocodilo "---"
Bombardiro Crocodilo "U chose:"
Lirili Larila scelta_giocatore Trippi Troppi SCELTA_SASSO Gusini
    Bombardiro Crocodilo "Sasso 🗿"
Trulimero Trulicina
Lirili Larila scelta_giocatore Trippi Troppi SCELTA_CARTA Gusini
    Bombardiro Crocodilo "Carta 📄"
Trulimero Trulicina
Lirili Larila scelta_giocatore Trippi Troppi SCELTA_FORBICE Gusini
    Bombardiro Crocodilo "Forbice ✂️"
Trulimero Trulicina

# Computer's Choice (Random)
Tralalero Tralala scelta_computer Trippi Troppi RANDOM_TRALALERO 1 3
Bombardiro Crocodilo "CPU chose:"
Lirili Larila scelta_computer Trippi Troppi SCELTA_SASSO Gusini
    Bombardiro Crocodilo "Sasso 🗿"
Trulimero Trulicina
Lirili Larila scelta_computer Trippi Troppi SCELTA_CARTA Gusini
    Bombardiro Crocodilo "Carta 📄"
Trulimero Trulicina
Lirili Larila scelta_computer Trippi Troppi SCELTA_FORBICE Gusini
    Bombardiro Crocodilo "Forbice ✂️"
Trulimero Trulicina
Bombardiro Crocodilo "---"


# Determine the Winner ong
Bombardiro Crocodilo "Result icl:"

# Check for Tie
Lirili Larila scelta_giocatore Trippi Troppi scelta_computer Gusini
    Bombardiro Crocodilo "Issa tie! Boneca Ambalabu!"
Boneca Ambalabu

    # Player chose Rock
    Lirili Larila scelta_giocatore Trippi Troppi SCELTA_SASSO Gusini
        Lirili Larila scelta_computer Trippi Troppi SCELTA_FORBICE Gusini
            Bombardiro Crocodilo "Player wins! Sasso beats Forbice!"
        Boneca Ambalabu
            Bombardiro Crocodilo "CPU wins! Carta beats Sasso!"
        Trulimero Trulicina
    Trulimero Trulicina

    # Player chose Paper
    Lirili Larila scelta_giocatore Trippi Troppi SCELTA_CARTA Gusini
        Lirili Larila scelta_computer Trippi Troppi SCELTA_SASSO Gusini
            Bombardiro Crocodilo "Player wins! Carta beats Sasso!"
        Boneca Ambalabu
            Bombardiro Crocodilo "CPU wins! Forbice beats Carta!"
        Trulimero Trulicina
    Trulimero Trulicina

    # Player chose Scissors
    Lirili Larila scelta_giocatore Trippi Troppi SCELTA_FORBICE Gusini
        Lirili Larila scelta_computer Trippi Troppi SCELTA_CARTA Gusini
            Bombardiro Crocodilo "Player wins! Forbice beats Carta!"
        Boneca Ambalabu
            Bombardiro Crocodilo "CPU wins! Sasso beats Forbice!"
        Trulimero Trulicina
    Trulimero Trulicina

Trulimero Trulicina

Bombardiro Crocodilo "---"
Bombardiro Crocodilo "GG! Ballerina Cappucina!"
"""
    brainrot_input = st.text_area("Code goes here:", height=450, value=example_code)

    # --- Player Choice Input ---
    st.subheader("Ur Move Player-chan:")
    player_choice_map = {"Sasso 🗿 (Rock)": 1, "Carta 📄 (Paper)": 2, "Forbice ✂️ (Scissors)": 3}
    player_choice_label = st.radio(
        "Pick ur fighter:",
        options=list(player_choice_map.keys()),
        horizontal=True,
        label_visibility="collapsed" # Hide the "Pick ur fighter" label above buttons
    )
    # Get the corresponding number (1, 2, or 3)
    player_choice_value = player_choice_map[player_choice_label]
    # --- End Player Choice Input ---


    with st.expander("Brainrot Keyword Help"):
        st.markdown(KEYWORD_HELP)

    run_button = st.button("Run Bombardiro! 🐊")


with col2:
    st.subheader("Result:")

    if run_button and brainrot_input:
        st.markdown("---")
        try:
            python_code = transpile_to_python(brainrot_input)

            code_output = io.StringIO()
            with contextlib.redirect_stdout(code_output):
                # Define the execution scope with random and the player's choice
                exec_scope = {
                    'random': random,
                    '_player_choice_from_ui': player_choice_value # Inject player choice
                }
                exec(python_code, exec_scope)

            output_string = code_output.getvalue()
            if output_string:
                 st.text(output_string)
            else:
                 st.info("No output produced fr.")

        except IndentationError as e:
            st.error(f"🚨 OMG Indent Error! 🚨\n{e}")
        except ValueError as e:
            st.error(f"🚨 OMG Value Error! 🚨\n{e}")
        except SyntaxError as e:
             st.error(f"🚨 OMG Syntax Error! 🚨\n{e}")
        except NameError as e:
             st.error(f"🚨 OMG Name Error! 🚨\n{e}")
             st.info("U forget 2 assign a var with 'Tralalero Tralala'?")
        except Exception as e:
            st.error(f"🚨 OMG Unexpected Error! 🚨\nType: {type(e).__name__}\nMessage: {e}")
            st.code(traceback.format_exc())

    elif run_button:
        st.warning("Bruh, enter some code first!")

st.markdown("---")
st.markdown("Made w Ambalabu & Capuccino Assassino lol")
