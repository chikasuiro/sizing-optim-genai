import os
import re
from .ai_class import GeometryParams

freecad_python_path = os.environ.get('FREECAD_PYTHON_PATH',
                                     'C:/Program Files/FreeCAD 1.0/bin/python.exe')
freecad_macro = __file__.replace('common/simulate.py', 'data/freecad_macro.py') \
    .replace('common\\simulate.py', 'data\\freecad_macro.py')

def rewrite_macro(params: GeometryParams) -> None:
    with open(freecad_macro, 'r', encoding='utf-8') as f:
        macro_content = f.read()

    param_str = f'params = {params.model_dump_json(indent=4)}'
    if 'params =' in macro_content:
        macro_content = re.sub(r'params = \{.*?\}', param_str, macro_content, flags=re.DOTALL)
    else:
        macro_content = param_str + '\n' + macro_content

    with open('./freecad_macro.py', 'w', encoding='utf-8') as f:
        f.write(macro_content)
    return None

def run_simulation(params: GeometryParams) -> dict:
    rewrite_macro(params)
    os.system(f'"{freecad_python_path}" ./freecad_macro.py')
    with open('volume.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        volume = float(lines[0].strip())
    with open('0.log', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        line_global_sms_node = lines[-15].strip()
        max_stress = float(line_global_sms_node.split()[1])
    return {'max_stress': max_stress, 'volume': volume}

def calculate_score(simulation_result: dict) -> float:
    max_stress = simulation_result['max_stress']
    volume = simulation_result['volume']
    score = -1 * max_stress - 0.01 * volume
    return score
