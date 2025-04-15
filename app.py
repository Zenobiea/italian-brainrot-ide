import streamlit as st
import re
import sys
import io
import contextlib
import traceback

KEYWORDS = {
    "Tralalero Tralala": "assignment_start",
    "Bombardiro Crocodilo": "print_command",
    "U Din Din Din Din Dun Ma Din Din Din Dun": "int(input())", #disabled for web
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
}

def translate_expression(expression_str):
    if KEYWORDS["U Din Din Din Din Dun Ma Din Din Din Dun"] in expression_str:
         raise ValueError("Errore Saturnita! Input ('U Din Din...') is not supported in the web version.")

    temp_expression = expression_str
    for br, py in sorted(KEYWORDS.items(), key=lambda item: len(item[0]), reverse=True):
         if py not in [":", "else:", "dedent_marker", "if", "while", "print_command", "assignment_start", "int(input())"]:
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
st.title("🤪 Italian Brainrot Interpreter 🤪")
st.caption("Write your 'Tralalero Tralala' code below and watch the magic!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Brainrot Code:")
    example_code = """# Example Program!
Tralalero Tralala message Trippi Troppi "Ciao Mondo Crocodilo!"
Bombardiro Crocodilo message

Tralalero Tralala x Trippi Troppi 5
Tralalero Tralala y Trippi Troppi 10
Tralalero Tralala somma Trippi Troppi x Brr Brr Patapim y

Bombardiro Crocodilo "La somma e':"
Bombardiro Crocodilo somma

# Ciclo
Tralalero Tralala i Trippi Troppi 0
Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur i Bombombini Gusini Gusini 3 Bananini
    Bombardiro Crocodilo "Giro numero:"
    Bombardiro Crocodilo i
    Tralalero Tralala i Trippi Troppi i Brr Brr Patapim 1
Ballerina Cappucina

Bombardiro Crocodilo
Bombardiro Crocodilo "Finito!"
"""
    brainrot_input = st.text_area("Enter code here:", height=400, value=example_code)
    run_button = st.button("Run Bombardiro! 🐊")

with col2:
    st.subheader("Output & Translation:")

    if run_button and brainrot_input:
        st.markdown("---")
        try:
            st.write("**Python Translation:**")
            python_code = transpile_to_python(brainrot_input)
            st.code(python_code, language='python')

            st.write("**Execution Result:**")
            code_output = io.StringIO()
            with contextlib.redirect_stdout(code_output):
                exec(python_code, {})

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
        except Exception as e:
            st.error(f"🚨 Unexpected Error! 🚨\nType: {type(e).__name__}\nMessage: {e}")
            st.code(traceback.format_exc())

    elif run_button:
        st.warning("Please enter some Brainrot code before running!")

st.markdown("---")
st.markdown("Created with Ambalabu and Capuccino Assassino!")
    elif run_button:
        st.warning("Please enter some Brainrot code before running!")

st.markdown("---")
st.markdown("Created with Ambalabu and Capuccino Assassino!") 
