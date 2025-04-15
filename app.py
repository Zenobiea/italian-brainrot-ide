import streamlit as st
import re
import sys
import io 
import contextlib 
import traceback 




KEYWORDS = {
    # Structure & Assignment
    "Tralalero Tralala": "assignment_start",
    "Bombardiro Crocodilo": "print",
    "U Din Din Din Din Dun Ma Din Din Din Dun": "int(input())", 
    "Lirili Larila": "if",
    "Gusini": ":",
    "Boneca Ambalabu": "else:",
    "Trulimero Trulicina": "dedent_marker",
    "Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur": "while",
    "Bananini": ":",
    "Ballerina Cappucina": "dedent_marker",

    # Comparison Operators 
    "Frigo Camelo Trippi Troppi": ">=",
    "Bombombini Gusini Gusini Trippi Troppi": "<=",
    "Bombombini Gusini Gusini": "<",
    "Frigo Camelo": ">",
    "Trippi Troppi": "==",
    "La Vaca Saturno Saturnita": "!=",

    # Arithmetic Operators
    "Brr Brr Patapim": "+",
    "Chimpanzini Bananini": "-",
    "Bombombini Gusini": "*",
    "Capuccino Assassino": "/",
}

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
        processed_line = line_content

        
        if processed_line == "# dedent marker": continue

        
        
        assign_match = re.match(r"Tralalero Tralala\s+(\w+)\s+Trippi Troppi\s+(.*)", processed_line)
        if assign_match:
            var_name = assign_match.group(1)
            expression = assign_match.group(2).strip()

            
            if KEYWORDS["U Din Din Din Din Dun Ma Din Din Din Dun"] in expression:
                 
                 raise ValueError("Errore Saturnita! Input ('U Din Din...') is not supported in the web version.")
            

            
            temp_expression = expression
            
            for br, py in sorted(KEYWORDS.items(), key=lambda item: len(item[0]), reverse=True):
                 
                 if py not in [":", "else:", "dedent_marker", "if", "while", "print", "assignment_start", "int(input())"]:
                     temp_expression = temp_expression.replace(br, py)
            processed_line = f"{var_name} = {temp_expression}"
        else:
            
            processed_line = processed_line.replace("Lirili Larila", "if", 1)
            processed_line = processed_line.replace("Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur", "while", 1)
            processed_line = processed_line.replace("Bombardiro Crocodilo", "print", 1) 

            
            processed_line = processed_line.replace(" Gusini", ":", 1) 
            processed_line = processed_line.replace(" Bananini", ":", 1) 

            
            if KEYWORDS["U Din Din Din Din Dun Ma Din Din Din Dun"] in processed_line:
                 
                 raise ValueError("Errore Saturnita! Input ('U Din Din...') is not supported in the web version.")
            

            
            for br, py in sorted(KEYWORDS.items(), key=lambda item: len(item[0]), reverse=True):
                 if py not in [":", "else:", "dedent_marker", "if", "while", "print", "assignment_start", "int(input())"]:
                     processed_line = processed_line.replace(br, py)


        
        if processed_line and not processed_line.isspace():
             final_python_code.append(current_indent + processed_line)

    return "\n".join(final_python_code)



st.set_page_config(page_title="Italian Brainrot IDE", layout="wide")
st.title("Italian Brainrot Interpreter")
st.caption("Write your 'Tralalero Tralala' code below and watch the magic!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Brainrot Code:")
    
    example_code = """# Example Program!
Tralalero Tralala count Trippi Troppi 0
Tralalero Tralala limit Trippi Troppi 3

Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur count Bombombini Gusini Gusini limit Bananini
    Bombardiro Crocodilo count
    Tralalero Tralala count Trippi Troppi count Brr Brr Patapim 1
Ballerina Cappucina

Bombardiro Crocodilo "Finished! Bombardiro Crocodilo!"
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
                 st.info("No output was produced (did you use 'Bombardiro Crocodilo'?).")

        except IndentationError as e:
            
            st.error(f"🚨 Indentation Error! 🚨\n{e}")
            st.info("Check your 'Trulimero Trulicina' and 'Ballerina Cappucina' keywords match the start of your blocks ('Lirili Larila', 'Tung Tung...').")
        except ValueError as e: 
            st.error(f"🚨 Value Error! 🚨\n{e}")
        except Exception as e:
            st.error(f"🚨 Unexpected Error! 🚨\nType: {type(e).__name__}\nMessage: {e}")
            st.code(traceback.format_exc()) 

    elif run_button:
        st.warning("Please enter some Brainrot code before running!")

st.markdown("---")
st.markdown("Created with Ambalabu and Capuccino Assassino!") 