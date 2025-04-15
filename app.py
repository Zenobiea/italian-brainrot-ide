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
**Basic Commands:**
*   `Tralalero Tralala variable Trippi Troppi value` : Assign value (e.g., `Tralalero Tralala x Trippi Troppi 10`)
*   `Tralalero Tralala variable Trippi Troppi RANDOM_TRALALERO min max` : Assign random integer (e.g., `Tralalero Tralala cpu Trippi Troppi RANDOM_TRALALERO 1 3`)
*   `Bombardiro Crocodilo value_or_variable` : Print something (e.g., `Bombardiro Crocodilo x`)

**Control Flow:**
*   `Lirili Larila condition Gusini` : If statement
*   `Boneca Ambalabu` : Else statement
*   `Trulimero Trulicina` : End If/Else block
*   `Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur condition Bananini` : While loop
*   `Ballerina Cappucina` : End While loop block

**Operators:**
*   `Brr Brr Patapim` : `+` | `Chimpanzini Bananini` : `-` | `Bombombini Gusini` : `*` | `Capuccino Assassino` : `/`
*   `Trippi Troppi` : `==` | `La Vaca Saturno Saturnita` : `!=`
*   `Frigo Camelo` : `>` | `Bombombini Gusini Gusini` : `<`
*   `Frigo Camelo Trippi Troppi` : `>=` | `Bombombini Gusini Gusini Trippi Troppi` : `<=`

**Comments:** `#`
**Note:** Input (`U Din Din...`) is disabled.
"""


def translate_expression(expression_str):
    if KEYWORDS["U Din Din Din Din Dun Ma Din Din Din Dun"] in expression_str:
         raise ValueError("Errore Saturnita! Input ('U Din Din...') is not supported in the web version.")
    if KEYWORDS["RANDOM_TRALALERO"] in expression_str:
         raise SyntaxError("RANDOM_TRALALERO must be used directly in assignment, not within other expressions.")

    temp_expression = expression_str
    for br, py in sorted(KEYWORDS.items(), key=lambda item: len(item[0]), reverse=True):
         if py not in [":", "else:", "dedent_marker", "if", "while", "print_command", "assignment_start", "int(input())", "random_command"]:
             temp_expression = temp_expression.replace(br, py)
    return temp_expression

def transpile_to_python(brainrot_code):
    indent_level = 0
    indent_space = "    "
    lines = brainrot_code.splitlines()
    processed_lines = []
    line_number = 0

    for line in lines:
        line_number += 1
        stripped_line = line.strip()

        if stripped_line.startswith('#') or not stripped_line:
            processed_lines.append((indent_level, stripped_line))
            continue

        if stripped_line == "Trulimero Trulicina" or stripped_line == "Ballerina Cappucina":
            if indent_level == 0:
                raise IndentationError(f"Errore Crocodilo! Dedent ('{stripped_line}') without matching if/while on line {line_number}")
            indent_level -= 1
            processed_lines.append((indent_level, "# dedent marker"))
            continue

        if stripped_line == "Boneca Ambalabu":
            if indent_level == 0:
                 raise IndentationError(f"Errore Crocodilo! Else ('{stripped_line}') without matching if on line {line_number}")
            processed_lines.append((indent_level - 1, "else:"))
            continue

        processed_lines.append((indent_level, stripped_line))

        if stripped_line.startswith("Lirili Larila") or \
           stripped_line.startswith("Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur"):
            indent_level += 1

    final_python_code = []
    for level, line_content in processed_lines:
        current_indent = indent_space * level
        original_line = line_content

        if original_line == "# dedent marker": continue

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
                  raise SyntaxError(f"Invalid Lirili Larila syntax: {original_line}")

        elif processed_line.startswith("Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur"):
            while_match = re.match(r"Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur\s+(.*?)\s+Bananini", processed_line)
            if while_match:
                condition = while_match.group(1).strip()
                translated_cond = translate_expression(condition)
                processed_line = f"while {translated_cond}:"
            else:
                 raise SyntaxError(f"Invalid Tung Tung Tung syntax: {original_line}")

        elif processed_line == "else:":
            pass
        elif processed_line.startswith('#') or not processed_line:
            pass


        if processed_line and not processed_line.isspace():
             final_python_code.append(current_indent + processed_line)

    return "\n".join(final_python_code)


st.set_page_config(page_title="Italian Brainrot IDE", layout="wide")
st.title("Italian Brainrot Interpreter frfr icl im genius")
st.caption("Write your 'Tralalero Tralala' code below and watch the magic!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Brainrot Code:")
    example_code = """# Rock Paper Scissors - Brainrot Edition!
Bombardiro Crocodilo "Benvenuti al Bombardiro Sasso Carta Forbice!"

# Define choices: 1=Sasso (Rock), 2=Carta (Paper), 3=Forbice (Scissors)
Tralalero Tralala SCELTA_SASSO Trippi Troppi 1
Tralalero Tralala SCELTA_CARTA Trippi Troppi 2
Tralalero Tralala SCELTA_FORBICE Trippi Troppi 3

# --- Player's Choice (Simulated) ---
# !!! EDIT THIS LINE TO CHANGE YOUR CHOICE !!!
Tralalero Tralala scelta_giocatore Trippi Troppi SCELTA_CARTA # Change to SCELTA_SASSO or SCELTA_FORBICE
# !!! ----------------------------- !!!

Bombardiro Crocodilo "---"
Bombardiro Crocodilo "Giocatore ha scelto:"
Lirili Larila scelta_giocatore Trippi Troppi SCELTA_SASSO Gusini
    Bombardiro Crocodilo "Sasso 🗿"
Trulimero Trulicina
Lirili Larila scelta_giocatore Trippi Troppi SCELTA_CARTA Gusini
    Bombardiro Crocodilo "Carta 📄"
Trulimero Trulicina
Lirili Larila scelta_giocatore Trippi Troppi SCELTA_FORBICE Gusini
    Bombardiro Crocodilo "Forbice ✂️"
Trulimero Trulicina

# --- Computer's Choice (Random) ---
# Uses the special RANDOM_TRALALERO keyword
Tralalero Tralala scelta_computer Trippi Troppi RANDOM_TRALALERO 1 3
Bombardiro Crocodilo "Computer ha scelto:"
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


# --- Determine the Winner ---
Bombardiro Crocodilo "Risultato Tralalero:"

# Check for Tie
Lirili Larila scelta_giocatore Trippi Troppi scelta_computer Gusini
    Bombardiro Crocodilo "Pareggio! Boneca Ambalabu!"
Boneca Ambalabu # Not a tie, check win conditions

    # Player chose Rock
    Lirili Larila scelta_giocatore Trippi Troppi SCELTA_SASSO Gusini
        Lirili Larila scelta_computer Trippi Troppi SCELTA_FORBICE Gusini
            Bombardiro Crocodilo "Giocatore Vince! Sasso batte Forbice!"
        Boneca Ambalabu # Computer chose Paper
            Bombardiro Crocodilo "Computer Vince! Carta batte Sasso!"
        Trulimero Trulicina
    Trulimero Trulicina

    # Player chose Paper
    Lirili Larila scelta_giocatore Trippi Troppi SCELTA_CARTA Gusini
        Lirili Larila scelta_computer Trippi Troppi SCELTA_SASSO Gusini
            Bombardiro Crocodilo "Giocatore Vince! Carta batte Sasso!"
        Boneca Ambalabu # Computer chose Scissors
            Bombardiro Crocodilo "Computer Vince! Forbice batte Carta!"
        Trulimero Trulicina
    Trulimero Trulicina

    # Player chose Scissors
    Lirili Larila scelta_giocatore Trippi Troppi SCELTA_FORBICE Gusini
        Lirili Larila scelta_computer Trippi Troppi SCELTA_CARTA Gusini
            Bombardiro Crocodilo "Giocatore Vince! Forbice batte Carta!"
        Boneca Ambalabu # Computer chose Rock
            Bombardiro Crocodilo "Computer Vince! Sasso batte Forbice!"
        Trulimero Trulicina
    Trulimero Trulicina

Trulimero Trulicina # End of the main Else (not a tie)

Bombardiro Crocodilo "---"
Bombardiro Crocodilo "Partita Finita! Ballerina Cappucina!"
"""
    brainrot_input = st.text_area("Enter code here:", height=600, value=example_code)

    with st.expander("Show Brainrot Keyword Reference"):
        st.markdown(KEYWORD_HELP)

    run_button = st.button("Run Bombardiro! 🐊")


with col2:
    st.subheader("Execution Result:")

    if run_button and brainrot_input:
        st.markdown("---")
        try:
            python_code = transpile_to_python(brainrot_input)

            code_output = io.StringIO()
            with contextlib.redirect_stdout(code_output):
                exec(python_code, {'random': random})

            output_string = code_output.getvalue()
            if output_string:
                 st.text(output_string)
            else:
                 st.info("No output was produced.")

        except IndentationError as e:
            st.error(f"🚨 Indentation Error! 🚨\n{e}")
        except ValueError as e:
            st.error(f"🚨 Value Error! 🚨\n{e}")
        except SyntaxError as e:
             st.error(f"🚨 Syntax Error! 🚨\n{e}")
        except NameError as e:
             st.error(f"🚨 Name Error! 🚨\n{e}")
             st.info("Did you forget to assign a variable using 'Tralalero Tralala' before using it?")
        except Exception as e:
            st.error(f"🚨 Unexpected Error! 🚨\nType: {type(e).__name__}\nMessage: {e}")
            st.code(traceback.format_exc())

    elif run_button:
        st.warning("Please enter some Brainrot code before running!")

st.markdown("---")
st.markdown("Created with Ambalabu and Capuccino Assassino!")
