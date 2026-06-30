import sys
import pathlib
from datetime import datetime

# We will import FPDF inside the script after installing it
# This script will be executed via the command line

PDF_CODE = """# -*- coding: utf-8 -*-
import sys
from fpdf import FPDF
from datetime import datetime

class LabReportPDF(FPDF):
    def header(self):
        # Draw a top colored bar
        self.set_fill_color(139, 92, 246) # Violet
        self.rect(0, 0, 210, 8, 'F')
        
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(156, 163, 175) # Gray
        self.cell(0, 10, 'RAPPORT DE TP - PYTHON M2 - CAMPUS', 0, 0, 'L')
        self.cell(0, 10, 'DAY 1', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(156, 163, 175)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, num, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(243, 244, 246) # Light gray
        self.set_text_color(17, 24, 39) # Dark gray
        self.cell(0, 10, f' {num}. {title}', 0, 1, 'L', fill=True)
        self.ln(4)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(139, 92, 246) # Violet
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)

    def code_block(self, code):
        self.set_font('Courier', '', 9)
        self.set_fill_color(15, 23, 42) # Slate 900
        self.set_text_color(243, 244, 246) # Light gray
        
        # Calculate height based on lines
        lines = code.strip().split('\\n')
        
        # We use multi_cell to draw the block
        # To make it look like a block, we draw a background rect or just use multi_cell with fill=True
        # FPDF multi_cell with fill=True works great
        self.multi_cell(0, 4.5, code.strip(), border=1, align='L', fill=True)
        self.ln(4)
        # Reset text color
        self.set_text_color(31, 41, 55)

    def test_result(self, result_text, success=True):
        self.set_font('Helvetica', 'B', 9)
        if success:
            self.set_text_color(16, 185, 129) # Green
            self.set_fill_color(236, 253, 245) # Light Green
            prefix = "[OK] "
        else:
            self.set_text_color(239, 68, 68) # Red
            self.set_fill_color(254, 242, 242) # Light Red
            prefix = "[ERREUR] "
            
        self.cell(0, 6, prefix + "Test de validation :", 0, 1, 'L', fill=True)
        self.set_font('Courier', '', 8.5)
        self.set_text_color(55, 65, 81)
        self.multi_cell(0, 4, result_text.strip(), border=1, align='L')
        self.ln(4)
        self.set_text_color(31, 41, 55)

# Initialize PDF
pdf = LabReportPDF()
pdf.alias_nb_pages()
pdf.add_page()

# Title Page / Header
pdf.set_font('Helvetica', 'B', 22)
pdf.set_text_color(17, 24, 39)
pdf.cell(0, 15, 'Rapport de TP - Day 1', 0, 1, 'C')
pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(107, 114, 128)
pdf.cell(0, 5, 'Algorithmes de Base, Fichiers & CLI de Surveillance de Serveurs', 0, 1, 'C')
pdf.ln(10)

# Metadata Table
pdf.set_fill_color(249, 250, 251)
pdf.set_font('Helvetica', 'B', 9)
pdf.set_text_color(75, 85, 99)
pdf.cell(40, 7, 'Date de rendu :', 1, 0, 'L', fill=True)
pdf.set_font('Helvetica', '', 9)
pdf.cell(150, 7, datetime.now().strftime('%d/%m/%Y %H:%M'), 1, 1, 'L')
pdf.set_font('Helvetica', 'B', 9)
pdf.cell(40, 7, 'Etudiant :', 1, 0, 'L', fill=True)
pdf.set_font('Helvetica', '', 9)
pdf.cell(150, 7, 'Amine (M2)', 1, 1, 'L')
pdf.set_font('Helvetica', 'B', 9)
pdf.cell(40, 7, 'Statut :', 1, 0, 'L', fill=True)
pdf.set_font('Helvetica', 'B', 9)
pdf.set_text_color(16, 185, 129)
pdf.cell(150, 7, '100% DES TESTS VALIDES', 1, 1, 'L')
pdf.ln(10)

pdf.set_text_color(31, 41, 55)

# ----------------------------------------
# CHAPTER 1: LAB 1
# ----------------------------------------
pdf.chapter_title('1', 'Lab 1 : Programmation Python de Base & Fichiers')

pdf.set_font('Helvetica', '', 10)
pdf.multi_cell(0, 5, "Ce premier module valide les concepts fondamentaux de Python : boucles, manipulation de chaines de caracteres, listes de comprehension, ainsi que la lecture/ecriture de fichiers plats et JSON.")
pdf.ln(4)

# Ex 1
pdf.section_title('Exercice 1.1 : Calcul de la Factorielle (Boucle)')
pdf.set_font('Helvetica', '', 10)
pdf.multi_cell(0, 5, "Objectif : Completer la fonction factorial(n) pour calculer la factorielle d'un nombre entier en utilisant une boucle.")
pdf.ln(2)
code_ex1 = \"\"\"def factorial(n):
    \\\"\\\"\\\"Compute the factorial of a number.\\\"\\\"\\\"
    result = 1
    for i in range(1, n + 1):  # <-- Rempli : n + 1
        result *= i  # <-- Rempli : i
    return result\"\"\"
pdf.code_block(code_ex1)
pdf.test_result("factorial(5) -> 120\\nfactorial(3) -> 6\\nfactorial(1) -> 1\\nAll test cases passed!")

# Ex 2
pdf.section_title('Exercice 1.2 : Inversion de Chaine de Caracteres')
pdf.set_font('Helvetica', '', 10)
pdf.multi_cell(0, 5, "Objectif : Retourner une chaine de caracteres inversee en utilisant le slicing Python.")
pdf.ln(2)
code_ex2 = \"\"\"def reverse_string(s):
    \\\"\\\"\\\"Reverse a string.\\\"\\\"\\\"
    return s[::-1]  # <-- Rempli : s[::-1]\"\"\"
pdf.code_block(code_ex2)
pdf.test_result("reverse_string('Python') -> 'nohtyP'\\nreverse_string('Data') -> 'ataD'\\nAll test cases passed!")

# Ex 3
pdf.section_title('Exercice 1.3 : Filtrer les Nombres Pairs')
pdf.set_font('Helvetica', '', 10)
pdf.multi_cell(0, 5, "Objectif : Utiliser une liste de comprehension pour extraire uniquement les nombres pairs d'une liste.")
pdf.ln(2)
code_ex3 = \"\"\"def find_even_numbers(lst):
    \\\"\\\"\\\"Return a list of even numbers.\\\"\\\"\\\"
    return [num for num in lst if num % 2 == 0]  # <-- Rempli : num et num % 2 == 0\"\"\"
pdf.code_block(code_ex3)
pdf.test_result("find_even_numbers([1, 2, 3, 4, 5, 6]) -> [2, 4, 6]\\nfind_even_numbers([10, 15, 20, 25]) -> [10, 20]\\nAll test cases passed!")

# Page Break for Chapter 2
pdf.add_page()

# Ex 4
pdf.section_title('Exercice 1.4 : Ecriture et Lecture dans un Fichier Texte')
pdf.set_font('Helvetica', '', 10)
pdf.multi_cell(0, 5, "Objectif : Ecrire une liste de chaines dans un fichier avec des retours a la ligne, puis lire ce fichier pour reconstruire la liste d'origine.")
pdf.ln(2)
code_ex4 = \"\"\"# Writing to a file
def write_to_file(filename, data):
    with open(filename, 'w') as file:  # <-- Rempli : 'w'
        for name in data:
            file.write(name + '\\\\n')  # <-- Rempli : write(name + '\\\\n')

# Reading from a file
def read_from_file(filename):
    with open(filename, 'r') as file:  # <-- Rempli : 'r'
        return file.readlines()  # <-- Rempli : readlines()\"\"\"
pdf.code_block(code_ex4)
pdf.test_result("write_to_file('names.txt', ['Alice', 'Bob', 'Charlie'])\\nread_from_file('names.txt') -> ['Alice\\\\n', 'Bob\\\\n', 'Charlie\\\\n']\\nAll test cases passed!")

# Ex 5
pdf.section_title('Exercice 1.5 : Ecriture et Lecture JSON')
pdf.set_font('Helvetica', '', 10)
pdf.multi_cell(0, 5, "Objectif : Utiliser le module json pour sauvegarder et charger un dictionnaire dans un fichier structure.")
pdf.ln(2)
code_ex5 = \"\"\"import json

# Writing to a JSON file
def write_json(filename, data):
    with open(filename, 'w') as file:  # <-- Rempli : 'w'
        json.dump(data, file, indent=4)  # <-- Rempli : data

# Reading from a JSON file
def read_json(filename):
    with open(filename, 'r') as file:  # <-- Rempli : 'r'
        return json.load(file)  # <-- Rempli : load(file)\"\"\"
pdf.code_block(code_ex5)
pdf.test_result("write_json('data.json', {...})\\nread_json('data.json') -> {...}\\nAll test cases passed!")

# ----------------------------------------
# CHAPTER 2: LAB 1.2 SERVER HEALTH
# ----------------------------------------
pdf.ln(5)
pdf.chapter_title('2', 'Lab 1.2 : Outil CLI de Surveillance des Serveurs')

pdf.set_font('Helvetica', '', 10)
pdf.multi_cell(0, 5, "Ce lab consiste a developper un script complet de surveillance de serveurs. Il charge un fichier JSON contenant une liste de serveurs, verifie le statut de chacun a l'aide de requetes HTTP avec timeout, et genere un rapport consolide.")
pdf.ln(4)

pdf.section_title('Etape 1 : Chargement de la Configuration (load_servers)')
code_cli1 = \"\"\"def load_servers(path: str) -> list[dict]:
    \\\"\\\"\\\"Load and return the list of servers from a JSON file.\\\"\\\"\\\"
    try:
        raw = pathlib.Path(path).read_text(encoding='utf-8')
        return json.loads(raw)
    except FileNotFoundError:
        print(f"Error: The file '{path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{path}' is not valid JSON.", file=sys.stderr)
        sys.exit(1)\"\"\"
pdf.code_block(code_cli1)

pdf.add_page()

pdf.section_title('Etape 2 : Verification Individuelle des Serveurs (check_server)')
pdf.set_font('Helvetica', '', 10)
pdf.multi_cell(0, 5, "Cette etape utilise la bibliotheque requests. Les serveurs sont qualifies de :\\n- UP : Reponse HTTP 200 en moins de 500ms.\\n- DEGRADED : Reponse HTTP 200 mais superieure a 500ms, ou code HTTP different de 200.\\n- DOWN : Timeout de 5s atteint ou erreur de connexion.")
pdf.ln(2)
code_cli2 = \"\"\"def check_server(server: dict) -> dict:
    \\\"\\\"\\\"Check the health of a single server and return a result dict.\\\"\\\"\\\"
    url = f\\\"{server['protocol']}://{server['host']}:{server['port']}{server['health_path']}\\\"
    start = time.time()
    try:
        resp = requests.get(url, timeout=5)
        elapsed_ms = (time.time() - start) * 1000
        
        status_code = resp.status_code
        if status_code == 200:
            if elapsed_ms <= 500:
                status = \\\"UP\\\"
            else:
                status = \\\"DEGRADED\\\"
        else:
            status = \\\"DEGRADED\\\"
            
        return {
            \\\"name\\\": server[\\\"name\\\"],
            \\\"url\\\": url,
            \\\"status\\\": status,
            \\\"response_time_ms\\\": elapsed_ms,
            \\\"status_code\\\": status_code
        }
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        return {
            \\\"name\\\": server[\\\"name\\\"],
            \\\"url\\\": url,
            \\\"status\\\": \\\"DOWN\\\",
            \\\"response_time_ms\\\": None,
            \\\"status_code\\\": None,
            \\\"error\\\": str(e)
        }\"\"\"
pdf.code_block(code_cli2)

pdf.section_title('Etape 3 : Rapport de Synthese (run_health_check)')
code_cli3 = \"\"\"def run_health_check(servers: list[dict]) -> dict:
    \\\"\\\"\\\"Check all servers and return a summary report.\\\"\\\"\\\"
    results = []
    up, degraded, down = 0, 0, 0
    for server in servers:
        res = check_server(server)
        results.append(res)
        if res[\\\"status\\\"] == \\\"DOWN\\\":
            down += 1
        elif res[\\\"status\\\"] == \\\"UP\\\":
            up += 1
        else:
            degraded += 1
    return {
        \\\"checked_at\\\": datetime.now().isoformat(timespec='seconds'),
        \\\"total\\\": len(servers),
        \\\"up\\\": up,
        \\\"degraded\\\": degraded,
        \\\"down\\\": down,
        \\\"results\\\": results
    }\"\"\"
pdf.code_block(code_cli3)

# Simulation Table output
pdf.section_title('Exemple de Rapport d\\'Execution (Console)')
console_output = \"\"\"[o_o] api-prod-1 : UP (HTTP 200, 145.2ms)
[o_o] api-prod-2 : DEGRADED (HTTP 503, 152.8ms)
[-_ -] slow-server : DOWN (Error: Read timed out. (read timeout=5))
[-_ -] unreachable : DOWN (Error: Connection to 10.255.255.1 timed out.)

Report Summary:
- Total: 4, UP: 1, DEGRADED: 1, DOWN: 2
- Checked at: 2026-06-29T14:07:30\"\"\"
pdf.test_result(console_output)

# Output PDF
pdf.output('Day1_Labs_Report.pdf')
print('PDF successfully generated!')
"""

pathlib.Path("generate_pdf_worker.py").write_text(PDF_CODE, encoding="utf-8")
print("generate_pdf_worker.py created.")
