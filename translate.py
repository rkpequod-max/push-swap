#!/usr/bin/env python3
"""
Complete French translation script for push_swap index.html.
Adds data-en and data-fr attributes to every visible text element.
"""

from bs4 import BeautifulSoup, NavigableString, Comment
import re

# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATION DICTIONARY
# Key: current text (stripped) in the HTML
# Value: (data_en, data_fr) tuple
# For English text: (en_text, fr_translation)
# For French text: (en_translation, fr_text)
# For code/numbers: (text, text) — keep as-is
# ─────────────────────────────────────────────────────────────────────────────

TRANSLATIONS = {
    # ── Symbols, numbers, operators (keep as-is) ──
    '%': ('%', '%'),
    '+': ('+', '+'),
    '+1': ('+1', '+1'),
    ',': (',', ','),
    '.': ('.', '.'),
    ':': (':', ':'),
    '/': ('/', '/'),
    '/5': ('/5', '/5'),
    '·': ('·', '·'),
    '—': ('—', '—'),
    '→': ('→', '→'),
    '0': ('0', '0'),
    '1': ('1', '1'),
    '2': ('2', '2'),
    '3': ('3', '3'),
    '4': ('4', '4'),
    '5': ('5', '5'),
    '6': ('6', '6'),
    '7': ('7', '7'),
    '8': ('8', '8'),
    '9': ('9', '9'),
    '01': ('01', '01'),
    '02': ('02', '02'),
    '03': ('03', '03'),
    '04': ('04', '04'),
    '05': ('05', '05'),
    '06': ('06', '06'),
    '07': ('07', '07'),
    '08': ('08', '08'),
    '09': ('09', '09'),
    '10': ('10', '10'),
    '11': ('11', '11'),
    '12': ('12', '12'),
    '13': ('13', '13'),
    '14': ('14', '14'),
    '15': ('15', '15'),
    '37%': ('37%', '37%'),
    '4/5': ('4/5', '4/5'),
    '2/5': ('2/2', '2/5'),
    '5/5': ('5/5', '5/5'),
    '5281': ('5281', '5281'),
    '559': ('559', '559'),
    '5795': ('5795', '5795'),
    '894': ('894', '894'),
    '~5281': ('~5281', '~5281'),
    '~559': ('~559', '~559'),
    '5281 ops': ('5281 ops', '5281 ops'),
    '559 ops': ('559 ops', '559 ops'),
    '5795 ops': ('5795 ops', '5795 ops'),
    '894 ops': ('894 ops', '894 ops'),
    '−37%': ('−37%', '−37%'),
    '−9%': ('−9%', '−9%'),
    '1–2 ops': ('1–2 ops', '1–2 ops'),
    '5–9 ops': ('5–9 ops', '5–9 ops'),
    '6–10': ('6–10', '6–10'),
    '6–10 ops': ('6–10 ops', '6–10 ops'),
    '≤ 3': ('≤ 3', '≤ 3'),
    '≤ 12': ('≤ 12', '≤ 12'),
    '≤ 3 ops': ('≤ 3 ops', '≤ 3 ops'),
    '≤ 12 ops': ('≤ 12 ops', '≤ 12 ops'),
    '< 700': ('< 700', '< 700'),
    '< 900': ('< 900', '< 900'),
    '< 1100': ('< 1100', '< 1100'),
    '< 5500': ('< 5500', '< 5500'),
    '< 7000': ('< 7000', '< 7000'),
    '< 8500': ('< 8500', '< 8500'),
    'i': ('i', 'i'),
    'i = 1': ('i = 1', 'i = 1'),
    'i=0': ('i=0', 'i=0'),
    'i=1': ('i=1', 'i=1'),
    'i=2': ('i=2', 'i=2'),
    '2 × 2 = 4': ('2 × 2 = 4', '2 × 2 = 4'),
    '5 > 4': ('5 > 4', '5 > 4'),
    '2, 3, 5, 7, 9': ('2, 3, 5, 7, 9', '2, 3, 5, 7, 9'),
    '9, 2, 3, 5, 7': ('9, 2, 3, 5, 7', '9, 2, 3, 5, 7'),
    '[3,4,5,1,2]': ('[3,4,5,1,2]', '[3,4,5,1,2]'),
    '[9, 2, 3, 5, 7]': ('[9, 2, 3, 5, 7]', '[9, 2, 3, 5, 7]'),
    'arr = [9, 2, 3, 5, 7]': ('arr = [9, 2, 3, 5, 7]', 'arr = [9, 2, 3, 5, 7]'),
    'arr[1] = 2': ('arr[1] = 2', 'arr[1] = 2'),
    'arr[2] = 3': ('arr[2] = 3', 'arr[2] = 3'),
    'arr[3] = 5': ('arr[3] = 5', 'arr[3] = 5'),
    'len = 5': ('len = 5', 'len = 5'),
    'len_a': ('len_a', 'len_a'),
    'len_b': ('len_b', 'len_b'),
    'len/2': ('len/2', 'len/2'),
    'len_a − target': ('len_a − target', 'len_a − target'),
    'len_b − i': ('len_b − i', 'len_b − i'),
    'max_val = 9': ('max_val = 9', 'max_val = 9'),
    'min_pos': ('min_pos', 'min_pos'),
    'min_pos = 1': ('min_pos = 1', 'min_pos = 1'),
    'target = 4': ('target = 4', 'target = 4'),
    'val = 4': ('val = 4', 'val = 4'),
    'idx = (1+0)%5 = 1': ('idx = (1+0)%5 = 1', 'idx = (1+0)%5 = 1'),
    'idx = (1+1)%5 = 2': ('idx = (1+1)%5 = 2', 'idx = (1+1)%5 = 2'),
    'idx = (1+2)%5 = 3': ('idx = (1+2)%5 = 3', 'idx = (1+2)%5 = 3'),
    'max(ra, rb) + 1 = max(4, 1) + 1': ('max(ra, rb) + 1 = max(4, 1) + 1', 'max(ra, rb) + 1 = max(4, 1) + 1'),
    'max(rra, rrb) + 1 = max(2, 4) + 1': ('max(rra, rrb) + 1 = max(2, 4) + 1', 'max(rra, rrb) + 1 = max(2, 4) + 1'),
    'ra + rrb + 1 = 4 + 4 + 1': ('ra + rrb + 1 = 4 + 4 + 1', 'ra + rrb + 1 = 4 + 4 + 1'),
    'rra + rb + 1 = 2 + 1 + 1': ('rra + rb + 1 = 2 + 1 + 1', 'rra + rb + 1 = 2 + 1 + 1'),
    'ra = target': ('ra = target', 'ra = target'),
    'rb = i': ('rb = i', 'rb = i'),
    'rra = len_a - target': ('rra = len_a - target', 'rra = len_a - target'),
    'rrb = len_b - i': ('rrb = len_b - i', 'rrb = len_b - i'),
    'cost = max(ra, rb) + 1': ('cost = max(ra, rb) + 1', 'cost = max(ra, rb) + 1'),
    'cost = max(rra, rrb) + 1': ('cost = max(rra, rrb) + 1', 'cost = max(rra, rrb) + 1'),
    'cost = ra + rrb + 1': ('cost = ra + rrb + 1', 'cost = ra + rrb + 1'),
    'cost = rra + rb + 1': ('cost = rra + rb + 1', 'cost = rra + rb + 1'),
    'ordered(pa, 1) && !p2': ('ordered(pa, 1) && !p2', 'ordered(pa, 1) && !p2'),
    'op == 0': ('op == 0', 'op == 0'),
    'argc == 2': ('argc == 2', 'argc == 2'),
    'argc ≤ 1': ('argc ≤ 1', 'argc ≤ 1'),
    "line[0] == '\\0'": ("line[0] == '\\0'", "line[0] == '\\0'"),

    # ── Push swap operation codes (keep as-is) ──
    'sa': ('sa', 'sa'),
    'sb': ('sb', 'sb'),
    'ss': ('ss', 'ss'),
    'pa': ('pa', 'pa'),
    'pb': ('pb', 'pb'),
    'ra': ('ra', 'ra'),
    'rb': ('rb', 'rb'),
    'rr': ('rr', 'rr'),
    'rra': ('rra', 'rra'),
    'rrb': ('rrb', 'rrb'),
    'rrr': ('rrr', 'rrr'),
    'ra + rrb': ('ra + rrb', 'ra + rrb'),
    'rra + rb': ('rra + rb', 'rra + rb'),

    # ── Function names / code identifiers (keep as-is) ──
    'A': ('A', 'A'),
    'B': ('B', 'B'),
    'el': ('el', 'el'),
    'min': ('min', 'min'),
    'val': ('val', 'val'),
    'top': ('top', 'top'),
    'tgt': ('tgt', 'tgt'),
    'checker': ('checker', 'checker'),
    'cost_sort': ('cost_sort', 'cost_sort'),
    'cost_sort()': ('cost_sort()', 'cost_sort()'),
    'find_insert_pos': ('find_insert_pos', 'find_insert_pos'),
    'find_insert_pos()': ('find_insert_pos()', 'find_insert_pos()'),
    'is_cmd': ('is_cmd', 'is_cmd'),
    'is_cmd()': ('is_cmd()', 'is_cmd()'),
    'is_cmd("", ...)': ('is_cmd("", ...)', 'is_cmd("", ...)'),
    'is_dup': ('is_dup', 'is_dup'),
    'islarger': ('islarger', 'islarger'),
    'main()': ('main()', 'main()'),
    'malloc': ('malloc', 'malloc'),
    'mini_solve': ('mini_solve', 'mini_solve'),
    'move_pivot()': ('move_pivot()', 'move_pivot()'),
    'median_between()': ('median_between()', 'median_between()'),
    'new_node()': ('new_node()', 'new_node()'),
    'pile_init': ('pile_init', 'pile_init'),
    'pop()': ('pop()', 'pop()'),
    'pab()': ('pab()', 'pab()'),
    'rab()': ('rab()', 'rab()'),
    'rrab()': ('rrab()', 'rrab()'),
    'sab()': ('sab()', 'sab()'),
    'quick_return': ('quick_return', 'quick_return'),
    'quick_return()': ('quick_return()', 'quick_return()'),
    'read_cmds': ('read_cmds', 'read_cmds'),
    'read_cmds()': ('read_cmds()', 'read_cmds()'),
    'solve_it': ('solve_it', 'solve_it'),
    'solve_it()': ('solve_it()', 'solve_it()'),
    'sort_three()': ('sort_three()', 'sort_three()'),
    't_pile': ('t_pile', 't_pile'),
    'three_cmp': ('three_cmp', 'three_cmp'),
    'valid_input': ('valid_input', 'valid_input'),
    'call_alg()': ('call_alg()', 'call_alg()'),
    'free': ('free', 'free'),
    'free_pile()': ('free_pile()', 'free_pile()'),
    'free_split()': ('free_split()', 'free_split()'),
    'ft_strsplit': ('ft_strsplit', 'ft_strsplit'),
    "ft_strsplit(av[1], ' ')": ("ft_strsplit(av[1], ' ')", "ft_strsplit(av[1], ' ')"),
    'get_next_line': ('get_next_line', 'get_next_line'),
    'ft_putendl("Error")': ('ft_putendl("Error")', 'ft_putendl("Error")'),
    'atoi': ('atoi', 'atoi'),
    'exit()': ('exit()', 'exit()'),
    'exit(EXIT_SUCCESS)': ('exit(EXIT_SUCCESS)', 'exit(EXIT_SUCCESS)'),
    'norminette': ('norminette', 'norminette'),
    'norminette src/ libft/': ('norminette src/ libft/', 'norminette src/ libft/'),
    'make re': ('make re', 'make re'),
    'leaks ./push_swap 5 4 3 2 1': ('leaks ./push_swap 5 4 3 2 1', 'leaks ./push_swap 5 4 3 2 1'),
    'ulimit -s unlimited': ('ulimit -s unlimited', 'ulimit -s unlimited'),
    'complexity': ('complexity', 'complexity'),
    'bench.sh': ('bench.sh', 'bench.sh'),
    'shell': ('shell', 'shell'),
    'Makefile': ('Makefile', 'Makefile'),
    'libft': ('libft', 'libft'),
    '-Wall -Wextra -Werror': ('-Wall -Wextra -Werror', '-Wall -Wextra -Werror'),
    '-v': ('-v', '-v'),
    './push_swap': ('./push_swap', './push_swap'),
    'ps': ('ps', 'ps'),
    'push_swap': ('push_swap', 'push_swap'),
    'push_swap.c': ('push_swap.c', 'push_swap.c'),
    'src/checker.c': ('src/checker.c', 'src/checker.c'),
    'src/checker.c · the guard': ('src/checker.c · the guard', 'src/checker.c · le garde'),
    'src/push_swap.c': ('src/push_swap.c', 'src/push_swap.c'),
    'src/sort_quick.c': ('src/sort_quick.c', 'src/sort_quick.c'),
    'src/sort_two.c': ('src/sort_two.c', 'src/sort_two.c'),
    'src/valid_input.c': ('src/valid_input.c', 'src/valid_input.c'),
    'treatment.c — lifecycle': ('treatment.c — lifecycle', 'treatment.c — cycle de vie'),

    # ── Chart labels (keep numbers, translate context) ──
    '100 — old': ('100 — old', '100 — ancien'),
    '100 — new': ('100 — new', '100 — nouveau'),
    '500 — old': ('500 — old', '500 — ancien'),
    '500 — new': ('500 — new', '500 — nouveau'),
    'quicksort · 894': ('quicksort · 894', 'quicksort · 894'),
    'quicksort · 5795': ('quicksort · 5795', 'quicksort · 5795'),
    'cost sort · 559': ('cost sort · 559', 'cost sort · 559'),
    'cost sort · 5281': ('cost sort · 5281', 'cost sort · 5281'),

    # ── Number labels ──
    '100 numbers': ('100 numbers', '100 nombres'),
    '500 numbers': ('500 numbers', '500 nombres'),
    '3 numbers': ('3 numbers', '3 nombres'),
    '5 numbers': ('5 numbers', '5 nombres'),
    '100 numbers · 5/5': ('100 numbers · 5/5', '100 nombres · 5/5'),
    '500 numbers · 5/5': ('500 numbers · 5/5', '500 nombres · 5/5'),
    '3 numbers (2 1 0)': ('3 numbers (2 1 0)', '3 nombres (2 1 0)'),
    '3 numbers → 2 operations': ('3 numbers → 2 operations', '3 nombres → 2 opérations'),
    '100-number benchmark': ('100-number benchmark', 'Benchmark 100 nombres'),
    '500-number benchmark': ('500-number benchmark', 'Benchmark 500 nombres'),
    '100-number grade': ('100-number grade', 'Note 100 nombres'),
    '500-number grade': ('500-number grade', 'Note 500 nombres'),
    '100-number average stays under 700; 500-number average under 5500': (
        '100-number average stays under 700; 500-number average under 5500',
        'La moyenne sur 100 nombres reste sous 700 ; la moyenne sur 500 nombres sous 5500'
    ),

    # ── Strategy / formula labels ──
    'rr (both up)': ('rr (both up)', 'rr (les deux montent)'),
    'rrr (both down)': ('rrr (both down)', 'rrr (les deux descendent)'),
    'ra + rrb (mixed)': ('ra + rrb (mixed)', 'ra + rrb (mixte)'),
    'rra + rb (mixed)': ('rra + rb (mixed)', 'rra + rb (mixte)'),
    '4 rotation strategies': ('4 rotation strategies', '4 stratégies de rotation'),

    # ── Threshold labels ──
    '3/5 threshold': ('3/5 threshold', 'Seuil 3/5'),
    '4/5 threshold': ('4/5 threshold', 'Seuil 4/5'),
    '5/5 threshold': ('5/5 threshold', 'Seuil 5/5'),
    '5/5 target': ('5/5 target', 'Objectif 5/5'),
    '< 700 for 5/5': ('< 700 for 5/5', '< 700 pour 5/5'),
    '< 5500 for 5/5': ('< 5500 for 5/5', '< 5500 pour 5/5'),

    # ── Result labels ──
    'avg ~559 ops < 700 → 5/5': ('avg ~559 ops < 700 → 5/5', 'moy ~559 ops < 700 → 5/5'),
    'avg ~5281 ops < 5500 → 5/5': ('avg ~5281 ops < 5500 → 5/5', 'moy ~5281 ops < 5500 → 5/5'),
    '≤ 12 operations (passes the 5/5 cap)': ('≤ 12 operations (passes the 5/5 cap)', '≤ 12 opérations (passe le seuil 5/5)'),
    'avg. for 100 numbers': ('avg. for 100 numbers', 'moy. pour 100 nombres'),
    'avg. for 500 numbers': ('avg. for 500 numbers', 'moy. pour 500 nombres'),
    'ops saved on 100 numbers': ('ops saved on 100 numbers', 'ops économisées sur 100 nombres'),
    'final grade, both benchmarks': ('final grade, both benchmarks', 'note finale, les deux benchmarks'),
    'ops': ('ops', 'ops'),
    'previously 4/5': ('previously 4/5', 'précédemment 4/5'),

    # ── Stack labels ──
    'stack A': ('stack A', 'pile A'),
    'stack B': ('stack B', 'pile B'),
    'Stack A': ('Stack A', 'Pile A'),
    'Stack B': ('Stack B', 'Pile B'),
    'STACK A (initial)': ('STACK A (initial)', 'PILE A (initial)'),
    'STACK B (initial)': ('STACK B (initial)', 'PILE B (initial)'),
    'A (rotated sorted)': ('A (rotated sorted)', 'A (trié mais rotaté)'),
    'A:': ('A:', 'A:'),
    'A: ra': ('A: ra', 'A: ra'),
    'A: rra': ('A: rra', 'A: rra'),
    'B: rb': ('B: rb', 'B: rb'),
    'B: rrb': ('B: rrb', 'B: rrb'),
    'A → B': ('A → B', 'A → B'),
    'B → A': ('B → A', 'B → A'),
    'sorted, rotated': ('sorted, rotated', 'trié, rotaté'),
    'unsorted pool': ('unsorted pool', 'pool non trié'),
    '↑ top': ('↑ top', '↑ sommet'),
    'After pa': ('After pa', 'Après pa'),
    'Before insert': ('Before insert', 'Avant insertion'),
    'inserted': ('inserted', 'inséré'),
    'minimum': ('minimum', 'minimum'),

    # ── Section eyebrows ──
    'Section 01': ('Section 01', 'Section 01'),
    'Section 02': ('Section 02', 'Section 02'),
    'Section 03': ('Section 03', 'Section 03'),
    'Section 04': ('Section 04', 'Section 04'),
    'Section 05': ('Section 05', 'Section 05'),
    'Section 06': ('Section 06', 'Section 06'),
    'Section 07': ('Section 07', 'Section 07'),
    'Section 08': ('Section 08', 'Section 08'),
    'Section 09': ('Section 09', 'Section 09'),
    'Section 10': ('Section 10', 'Section 10'),
    'Section 11': ('Section 11', 'Section 11'),
    'Section 12': ('Section 12', 'Section 12'),
    'Section 13': ('Section 13', 'Section 13'),
    'Section 14': ('Section 14', 'Section 14'),
    'Section 15': ('Section 15', 'Section 15'),
    'École 42 · Algorithm Project': ('École 42 · Algorithm Project', 'École 42 · Projet d\'Algorithme'),
    'École 42': ('École 42', 'École 42'),

    # ── Section titles (h2) ──
    'Rules of the game': ('Rules of the game', 'Règles du jeu'),
    'The grading scale': ('The grading scale', 'Le barème'),
    'The old algorithm: recursive quicksort': ('The old algorithm: recursive quicksort', "L'ancien algorithme : quicksort récursif"),
    'The new algorithm: cost-based insertion sort': ('The new algorithm: cost-based insertion sort', 'Le nouvel algorithme : tri par insertion à coût optimal'),
    'Interactive Sandbox & Visualizer': ('Interactive Sandbox & Visualizer', 'Bac à sable interactif & Visualiseur'),
    'The 4 rotation strategies': ('The 4 rotation strategies', 'Les 4 stratégies de rotation'),
    'The four rotation strategies': ('The four rotation strategies', 'Les quatre stratégies de rotation'),
    'Side-by-side comparison': ('Side-by-side comparison', 'Comparaison côte à côte'),
    'Checker & the empty-line bug': ('Checker & the empty-line bug', 'Checker & le bug de la ligne vide'),
    'Correction sheet': ('Correction sheet', 'Fiche de correction'),
    'Complexity analysis': ('Complexity analysis', 'Analyse de complexité'),
    'Memory management & leak prevention': ('Memory management & leak prevention', 'Gestion mémoire & prévention des fuites'),
    'Alternative algorithms explored': ('Alternative algorithms explored', 'Algorithmes alternatifs explorés'),
    'FAQ — Frequently asked questions': ('FAQ — Frequently asked questions', 'FAQ — Questions fréquentes'),
    'Build & test instructions': ('Build & test instructions', 'Compilation & tests'),
    'Algorithmes alternatifs': ('Alternative algorithms', 'Algorithmes alternatifs'),

    # ── Nav items ──
    'Benchmarks': ('Benchmarks', 'Performances'),
    'Build & Test': ('Build & Test', 'Compiler'),
    'Contents': ('Contents', 'Sommaire'),
    'Jump to benchmarks': ('Jump to benchmarks', 'Aller aux performances'),
    'Start reading': ('Start reading', 'Commencer la lecture'),
    'reference guide': ('reference guide', 'guide de référence'),
    'push_swap, fully explained.': ('push_swap, fully explained.', 'push_swap, expliqué en détail.'),
    'Sort smarter, not harder:': ('Sort smarter, not harder:', 'Trier plus intelligemment, pas plus dur :'),

    # ── TOC entries ──
    'Grading scale': ('Grading scale', 'Barème'),
    'Old: Quicksort': ('Old: Quicksort', 'Ancien : Quicksort'),
    'New: Cost-based sort': ('New: Cost-based sort', 'Nouveau : Tri par coût'),
    'Interactive Sandbox': ('Interactive Sandbox', 'Bac à sable'),
    'Memory & leaks': ('Memory & leaks', 'Mémoire & fuites'),
    'FAQ': ('FAQ', 'FAQ'),
    'Compilation & test': ('Compilation & test', 'Compilation & test'),
    'Build & test': ('Build & test', 'Compilation'),
    'Sections': ('Sections', 'Sections'),
    'Results': ('Results', 'Résultats'),

    # ── Footer ──
    'Checker & bug fix': ('Checker & bug fix', 'Checker & correctif'),
    'push_swap — The Reference Guide · Cost-Based Insertion Sort (École 42)': (
        'push_swap — The Reference Guide · Cost-Based Insertion Sort (École 42)',
        'push_swap — Le Guide de Référence · Tri par Insertion à Coût Optimal (École 42)'
    ),
    'Written as a 42 reference guide · Cost-based insertion sort ·': (
        'Written as a 42 reference guide · Cost-based insertion sort ·',
        'Écrit comme guide de référence 42 · Tri par insertion à coût optimal ·'
    ),
    'on both benchmarks': ('on both benchmarks', 'sur les deux benchmarks'),
    'push_swap ·': ('push_swap ·', 'push_swap ·'),

    # ── Hero lead paragraph (full text) ──
    'A complete, pedagogical walkthrough of the push_swap project — from a quicksort baseline that scored': (
        'A complete, pedagogical walkthrough of the push_swap project — from a quicksort baseline that scored',
        'Un guide pédagogique complet du projet push_swap — depuis un quicksort de base noté'
    ),
    'A pedagogical walkthrough of the push_swap project at École 42 — from a 4/5 quicksort baseline to a 5/5 cost-based insertion sort. Built for students, by a student who lived through the 500-number threshold.': (
        'A pedagogical walkthrough of the push_swap project at École 42 — from a 4/5 quicksort baseline to a 5/5 cost-based insertion sort. Built for students, by a student who lived through the 500-number threshold.',
        'Un guide pédagogique du projet push_swap à l\'École 42 — d\'un quicksort à 4/5 vers un tri par insertion à coût optimal à 5/5. Conçu pour les étudiants, par un étudiant qui a traversé le seuil des 500 nombres.'
    ),

    # ── Common words / short labels ──
    'and': ('and', 'et'),
    'or': ('or', 'ou'),
    'via': ('via', 'via'),
    'vs': ('vs', 'vs'),
    'The': ('The', 'Le'),
    'No': ('No', 'Non'),
    'After': ('After', 'Après'),
    'When': ('When', 'Quand'),
    'Uses': ('Uses', 'Utilise'),
    'An': ('An', 'Un'),
    'is': ('is', 'est'),
    'on 100.': ('on 100.', 'sur 100.'),
    'both': ('both', 'les deux'),
    'bottom': ('bottom', 'bas'),
    'never': ('never', 'jamais'),
    'always': ('always', 'toujours'),
    'same': ('same', 'idem'),
    'winner': ('winner', 'gagnant'),
    'cheapest': ('cheapest', 'le moins cher'),
    'count': ('count', 'compter'),
    'why': ('why', 'pourquoi'),
    'whether': ('whether', 'si'),
    'rotated': ('rotated', 'rotaté'),
    'thinking': ('thinking', 'réflexion'),
    'overhead': ('overhead', 'surcoût'),
    'instead of': ('instead of', 'au lieu de'),
    'called': ('called', 'appelé'),
    'before': ('before', 'avant'),
    'otherwise': ('otherwise', 'sinon'),
    'circularly': ('circularly', 'circulairement'),
    'consistently': ('consistently', 'de manière constante'),
    'continue': ('continue', 'continuer'),
    'computation time': ('computation time', 'temps de calcul'),
    'decision-making, not stack operations': ('decision-making, not stack operations', 'la prise de décision, pas les opérations sur les piles'),
    'no fusion is possible': ('no fusion is possible', 'aucune fusion possible'),
    'unknown command': ('unknown command', 'commande inconnue'),
    'empty line': ('empty line', 'ligne vide'),
    'empty again.': ('empty again.', 'à nouveau vide.'),
    'all four': ('all four', 'les quatre'),
    'right now': ('right now', 'maintenant'),
    'globally cheapest': ('globally cheapest', 'globalement le moins cher'),
    'sorted at all times': ('sorted at all times', 'trié en permanence'),
    'costing every option before acting': ('costing every option before acting', 'évaluer chaque option avant d\'agir'),
    'this is the key to our optimization': ('this is the key to our optimization', 'c\'est la clé de notre optimisation'),
    'two things for the price of one': ('two things for the price of one', 'deux choses pour le prix d\'une'),
    'plans every rotation': ('plans every rotation', 'planifie chaque rotation'),
    'reuses shared work': ('reuses shared work', 'réutilise le travail partagé'),
    'simplest algorithm that reliably achieves 5/5': ('simplest algorithm that reliably achieves 5/5', 'algorithme le plus simple atteignant fiablement 5/5'),
    'circularly sorted': ('circularly sorted', 'trié circulairement'),
    'Rotated sorted.': ('Rotated sorted.', 'Trié mais rotaté.'),
    'Stack B not empty.': ('Stack B not empty.', 'La pile B n\'est pas vide.'),
    'Both stacks freed before return. No leaks.': ('Both stacks freed before return. No leaks.', 'Les deux piles sont libérées avant le retour. Aucune fuite.'),
    'Even early-exit frees both stacks. No leaks.': ('Even early-exit frees both stacks. No leaks.', 'Même une sortie anticipée libère les deux piles. Aucune fuite.'),
    'Every malloc has a matching free.': ('Every malloc has a matching free.', 'Chaque malloc a un free correspondant.'),
    '15 allocs, 15 frees.': ('15 allocs, 15 frees.', '15 allocations, 15 libérations.'),
    'Maximum points on every category.': ('Maximum points on every category.', 'Points maximum dans chaque catégorie.'),
    'Best for:': ('Best for:', 'Idéal pour :'),
    'Pros:': ('Pros:', 'Avantages :'),
    'Cons:': ('Cons:', 'Inconvénients :'),
    'Formula': ('Formula', 'Formule'),
    'Meaning': ('Meaning', 'Signification'),
    'Value': ('Value', 'Valeur'),
    'Variable': ('Variable', 'Variable'),
    'Verdict': ('Verdict', 'Verdict'),
    'Note': ('Note', 'Note'),
    'Strategy': ('Strategy', 'Stratégie'),
    'Cost': ('Cost', 'Coût'),
    'Property': ('Property', 'Propriété'),
    'Requirement': ('Requirement', 'Exigence'),
    'Result': ('Result', 'Résultat'),
    'Test': ('Test', 'Test'),
    'Category': ('Category', 'Catégorie'),
    'Identity': ('Identity', 'Identité'),
    'Error management': ('Error management', 'Gestion d\'erreurs'),
    'False tests': ('False tests', 'Faux tests'),
    'Right tests': ('Right tests', 'Vrais tests'),
    'Input size': ('Input size', 'Taille d\'entrée'),
    'Improvement': ('Improvement', 'Amélioration'),
    'Grade': ('Grade', 'Note'),
    'Time complexity': ('Time complexity', 'Complexité temporelle'),
    'Space complexity': ('Space complexity', 'Complexité spatiale'),
    'Insertion order': ('Insertion order', 'Ordre d\'insertion'),
    'Worst-case sensitivity': ('Worst-case sensitivity', 'Sensibilité au pire cas'),
    'Final align direction': ('Final align direction', 'Direction d\'alignement final'),
    'Final alignment': ('Final alignment', 'Alignement final'),
    'Final grade': ('Final grade', 'Note finale'),
    'Number': ('Number', 'Nombre'),
    'Number of operations': ('Number of operations', 'Nombre d\'opérations'),
    'Operations': ('Operations', 'Opérations'),
    'Average': ('Average', 'Moyenne'),
    'Considered': ('Considered', 'Envisagé'),
    'Rejected': ('Rejected', 'Rejeté'),
    'Similar': ('Similar', 'Similaire'),
    'Future': ('Future', 'Futur'),
    'Future work': ('Future work', 'Travail futur'),
    'Similar to ours': ('Similar to ours', 'Similaire au nôtre'),
    'ALL PASS': ('ALL PASS', 'TOUT RÉUSSI'),
    'PASS': ('PASS', 'RÉUSSI'),
    'OK': ('OK', 'OK'),
    'KO': ('KO', 'KO'),
    'Error': ('Error', 'Error'),
    'EN': ('EN', 'EN'),
    'FR': ('FR', 'FR'),
    'Clear': ('Clear', 'Effacer'),
    'Reset': ('Reset', 'Réinitialiser'),
    'Set': ('Set', 'Définir'),
    'Auto-Solve': ('Auto-Solve', 'Résolution auto'),
    'Random 5': ('Random 5', 'Aléatoire 5'),
    'Random 10': ('Random 10', 'Aléatoire 10'),
    'GitHub repository': ('GitHub repository', 'dépôt GitHub'),
    'More questions?': ('More questions?', 'D\'autres questions ?'),

    # ── Complexity labels ──
    'O(N log N) partitions': ('O(N log N) partitions', 'partitions O(N log N)'),
    'O(N) local array': ('O(N) local array', 'tableau local O(N)'),
    'O(N²) comparisons': ('O(N²) comparisons', 'comparaisons O(N²)'),
    'O(log N) recursion': ('O(log N) recursion', 'récursion O(log N)'),
    'none — bounded & gentle': ('none — bounded & gentle', 'aucune — bornée et douce'),
    'recursion-driven (arbitrary)': ('recursion-driven (arbitrary)', 'pilotée par la récursion (arbitraire)'),
    'always when shared': ('always when shared', 'toujours quand partagé'),
    'pivot / partition overhead': ('pivot / partition overhead', 'surcoût pivot / partition'),
    'old algorithm\'s count fills the full bar': ('old algorithm\'s count fills the full bar', 'le compte de l\'ancien algorithme remplit toute la barre'),
    'rr / rrr fusion': ('rr / rrr fusion', 'fusion rr / rrr'),
    'rr/rrr: -15%, shortest-path: -12%, global cost: -10%': ('rr/rrr: -15%, shortest-path: -12%, global cost: -10%', 'rr/rrr : -15%, chemin court : -12%, coût global : -10%'),
    'Cost sort (100 elems)': ('Cost sort (100 elems)', 'Cost sort (100 éléments)'),
    'Quicksort (100 elems)': ('Quicksort (100 elems)', 'Quicksort (100 éléments)'),
    'Improvementrr/rrr: -15%, shortest-path: -12%, global cost: -10%': ('Improvementrr/rrr: -15%, shortest-path: -12%, global cost: -10%', 'Améliorationrr/rrr : -15%, chemin court : -12%, coût global : -10%'),
    'Cost sort (new)': ('Cost sort (new)', 'Cost sort (nouveau)'),
    'Quicksort (old)': ('Quicksort (old)', 'Quicksort (ancien)'),
    'Cost sort: O(n²) — tiny constants': ('Cost sort: O(n²) — tiny constants', 'Cost sort : O(n²) — constantes minuscules'),
    'Quicksort: O(n log n) average': ('Quicksort: O(n log n) average', 'Quicksort : O(n log n) en moyenne'),
    'Big-O comparison': ('Big-O comparison', 'Comparaison Big-O'),
    'Radix Sort (LSD)': ('Radix Sort (LSD)', 'Tri Radix (LSD)'),
    'Chunk Sort': ('Chunk Sort', 'Tri par chunks'),
    'Turkish Algorithm': ('Turkish Algorithm', 'Algorithme turc'),
    'Hybrid: Quicksort + Cost insertion': ('Hybrid: Quicksort + Cost insertion', 'Hybride : Quicksort + Insertion à coût'),

    # ── Correction sheet titles ──
    'Full correction sheet results': ('Full correction sheet results', 'Résultats complets de la fiche de correction'),
    'Category-by-category breakdown': ('Category-by-category breakdown', 'Détail catégorie par catégorie'),
    'Scorecard summary': ('Scorecard summary', 'Récapitulatif des scores'),
    'Checker — error management': ('Checker — error management', 'Checker — gestion d\'erreurs'),
    'Checker — false tests': ('Checker — false tests', 'Checker — faux tests'),
    'Checker — right tests': ('Checker — right tests', 'Checker — vrais tests'),
    'Identity test': ('Identity test', 'Test d\'identité'),
    'Simple case (2 1 0)': ('Simple case (2 1 0)', 'Cas simple (2 1 0)'),
    'Simple case (5 values)': ('Simple case (5 values)', 'Cas simple (5 valeurs)'),
    'sorted input → 0 operations printed': ('sorted input → 0 operations printed', 'entrée triée → 0 opérations affichées'),
    'already-sorted input → 0 operations printed': ('already-sorted input → 0 operations printed', 'entrée déjà triée → 0 opérations affichées'),
    'Sorted input → 0 ops': ('Sorted input → 0 ops', 'Entrée triée → 0 ops'),
    'malformed ops ("rrrr", "swap") → "Error", no crash, no leak': ('malformed ops ("rrrr", "swap") → "Error", no crash, no leak', 'opérations mal formées ("rrrr", "swap") → "Error", pas de crash, pas de fuite'),
    'non-numeric, overflow, duplicates → "Error" on stderr, exit ≠ 0, no leaks': ('non-numeric, overflow, duplicates → "Error" on stderr, exit ≠ 0, no leaks', 'non-numérique, overflow, doublons → "Error" sur stderr, exit ≠ 0, pas de fuite'),
    'valid op sequences → "OK" (fixed: blank lines no longer error)': ('valid op sequences → "OK" (fixed: blank lines no longer error)', 'séquences valides → "OK" (corrigé : les lignes vides ne causent plus d\'erreur)'),
    'Accept valid op sequences → "OK"': ('Accept valid op sequences → "OK"', 'Accepter les séquences valides → "OK"'),
    'Reject invalid operation commands': ('Reject invalid operation commands', 'Rejeter les commandes d\'opération invalides'),
    'Reject bad args, print "Error" on stderr, exit ≠ 0, no leak': ('Reject bad args, print "Error" on stderr, exit ≠ 0, no leak', 'Rejeter les mauvais arguments, afficher "Error" sur stderr, exit ≠ 0, pas de fuite'),
    'Valgrind reports "no leaks are possible" for both executables': ('Valgrind reports "no leaks are possible" for both executables', 'Valgrind rapporte "no leaks are possible" pour les deux exécutables'),
    'reports zero errors': ('reports zero errors', 'signale zéro erreur'),
    'compiles cleanly with': ('compiles cleanly with', 'compile proprement avec'),

    # ── Phase / flow titles ──
    'The four-phase plan': ('The four-phase plan', 'Le plan en quatre phases'),
    'The two stacks': ('The two stacks', 'Les deux piles'),
    'The eleven operations': ('The eleven operations', 'Les onze opérations'),
    'The idea': ('The idea', 'L\'idée'),
    'The implementation': ('The implementation', 'L\'implémentation'),
    'The fix': ('The fix', 'Le correctif'),
    'The verdict on quicksort': ('The verdict on quicksort', 'Le verdict sur quicksort'),
    'The honest trade-off': ('The honest trade-off', 'Le compromis honnête'),
    'The final alignment:': ('The final alignment:', 'L\'alignement final :'),
    'Final alignment with': ('Final alignment with', 'Alignement final avec'),
    'The partition function:': ('The partition function:', 'La fonction de partition :'),
    'The recursive driver:': ('The recursive driver:', 'Le pilote récursif :'),
    'The t_pile lifecycle': ('The t_pile lifecycle', 'Le cycle de vie de t_pile'),
    'The four-phase plan': ('The four-phase plan', 'Le plan en quatre phases'),
    'Drain A down to 3 elements': ('Drain A down to 3 elements', 'Vider A jusqu\'à 3 éléments'),
    'Insert B back into A, cheapest-first': ('Insert B back into A, cheapest-first', 'Réinsérer B dans A, le moins cher d\'abord'),
    'Recurse on both halves': ('Recurse on both halves', 'Récursion sur les deux moitiés'),
    'Pick a pivot — the median': ('Pick a pivot — the median', 'Choisir un pivot — la médiane'),
    'Partition with': ('Partition with', 'Partition avec'),
    'Undo the rotations with': ('Undo the rotations with', 'Annuler les rotations avec'),
    'Undoing rotations:': ('Undoing rotations:', 'Annulation des rotations :'),
    'Sort the 3 survivors with': ('Sort the 3 survivors with', 'Trier les 3 survivants avec'),
    'Walking through an example': ('Walking through an example', 'Exemple détaillé'),
    'What "sorted but rotated" means': ('What "sorted but rotated" means', 'Ce que « trié mais rotaté » signifie'),
    'What the checker does': ('What the checker does', 'Ce que fait le checker'),
    'Input validation': ('Input validation', 'Validation des entrées'),
    'Where frees happen': ('Where frees happen', 'Où ont lieu les libérations'),
    'Where the savings come from': ('Where the savings come from', 'D\'où viennent les économies'),
    'How to read the bars': ('How to read the bars', 'Comment lire les barres'),
    'Operation counts': ('Operation counts', 'Comptes d\'opérations'),
    'Visual comparison against the thresholds': ('Visual comparison against the thresholds', 'Comparaison visuelle avec les seuils'),
    'A worked example': ('A worked example', 'Un exemple concret'),
    'Setting up the variables': ('Setting up the variables', 'Configuration des variables'),
    'Why 700 and 5500 matter so much': ('Why 700 and 5500 matter so much', 'Pourquoi 700 et 5500 sont si importants'),
    'Why it only reached 4/5': ('Why it only reached 4/5', 'Pourquoi ça n\'a atteint que 4/5'),
    'Why this beats quicksort': ('Why this beats quicksort', 'Pourquoi ça bat quicksort'),
    'Why this matters': ('Why this matters', 'Pourquoi c\'est important'),
    'Why this distinction matters': ('Why this distinction matters', 'Pourquoi cette distinction compte'),
    'Why cost sort wins in practice': ('Why cost sort wins in practice', 'Pourquoi le cost sort gagne en pratique'),
    'Why cost sort was chosen': ('Why cost sort was chosen', 'Pourquoi le cost sort a été choisi'),
    'Why a naive linear scan fails': ('Why a naive linear scan fails', 'Pourquoi un scan linéaire naïf échoue'),
    'Why does an O(n²) algorithm beat an O(n log n) algorithm on 100 and 500 elements? The answer lies in the constants — and in the specific constraints of push_swap.': (
        'Why does an O(n²) algorithm beat an O(n log n) algorithm on 100 and 500 elements? The answer lies in the constants — and in the specific constraints of push_swap.',
        'Pourquoi un algorithme O(n²) bat-il un algorithme O(n log n) sur 100 et 500 éléments ? La réponse réside dans les constantes — et dans les contraintes spécifiques de push_swap.'
    ),
    'When would quicksort win?': ('When would quicksort win?', 'Quand quicksort gagnerait-il ?'),
    'The bug: blank lines treated as errors': ('The bug: blank lines treated as errors', 'Le bug : les lignes vides traitées comme des erreurs'),
    'Before the fix': ('Before the fix', 'Avant le correctif'),
    'Command dispatch:': ('Command dispatch:', 'Répartition des commandes :'),
    'Verifying with Valgrind': ('Verifying with Valgrind', 'Vérification avec Valgrind'),
    'Leak checking with Valgrind': ('Leak checking with Valgrind', 'Vérification des fuites avec Valgrind'),
    'Norminette (code style)': ('Norminette (code style)', 'Norminette (style de code)'),
    'Pre-submission checklist': ('Pre-submission checklist', 'Checklist pré-soumission'),
    'Compilation': ('Compilation', 'Compilation'),
    'Running push_swap': ('Running push_swap', 'Exécuter push_swap'),
    'Measuring the benchmarks': ('Measuring the benchmarks', 'Mesurer les benchmarks'),

    # ── Card titles ──
    'Arbitrary insertion order': ('Arbitrary insertion order', 'Ordre d\'insertion arbitraire'),
    'Pivot sensitivity': ('Pivot sensitivity', 'Sensibilité au pivot'),
    'Result: 4/5': ('Result: 4/5', 'Résultat : 4/5'),
    'No pathological worst case': ('No pathological worst case', 'Pas de pire cas pathologique'),
    'It reuses shared work': ('It reuses shared work', 'Il réutilise le travail partagé'),
    'It picks the cheapest move': ('It picks the cheapest move', 'Il choisit le mouvement le moins cher'),
    'It picks the shortest path': ('It picks the shortest path', 'Il choisit le chemin le plus court'),
    'Greedy cheapest-first': ('Greedy cheapest-first', 'Glouton : le moins cher d\'abord'),
    'Shortest-path final align': ('Shortest-path final align', 'Alignement final par chemin court'),
    'rr / rrr fusion': ('rr / rrr fusion', 'fusion rr / rrr'),
    'Use rr/rrr': ('Use rr/rrr', 'Utiliser rr/rrr'),
    'ra vs rra': ('ra vs rra', 'ra vs rra'),
    'Pick cheapest element': ('Pick cheapest element', 'Choisir l\'élément le moins cher'),
    'Three quick wins:': ('Three quick wins:', 'Trois gains rapides :'),
    'Two causes:': ('Two causes:', 'Deux causes :'),
    'But:': ('But:', 'Mais :'),
    'Rule of thumb:': ('Rule of thumb:', 'Règle de pouce :'),

    # ── Phase descriptions ──
    'Phase 2:': ('Phase 2:', 'Phase 2 :'),
    'Phase 3: the main': ('Phase 3: the main', 'Phase 3 : la boucle principale'),
    '— the optimal seed': ('— the optimal seed', '— la graine optimale'),

    # ── Sandbox section (already in French) ──
    'Initialiser les piles': ('Initialize stacks', 'Initialiser les piles'),
    'Entrez des entiers non-dupliqués séparés par des espaces :': ('Enter non-duplicate integers separated by spaces:', 'Entrez des entiers non-dupliqués séparés par des espaces :'),
    'Opérations effectuées :': ('Operations performed:', 'Opérations effectuées :'),
    'Opérations manuelles & Solver': ('Manual operations & Solver', 'Opérations manuelles & Solver'),
    'Résoudre 1 étape': ('Solve 1 step', 'Résoudre 1 étape'),
    "Calculateur de coût d'insertion en temps réel": ('Real-time insertion cost calculator', "Calculateur de coût d'insertion en temps réel"),
    'La pile B est vide. Lancez des opérations (ou cliquez sur "pb") pour voir le calculateur de coût en action !': (
        'Stack B is empty. Run operations (or click "pb") to see the cost calculator in action!',
        'La pile B est vide. Lancez des opérations (ou cliquez sur "pb") pour voir le calculateur de coût en action !'
    ),
    'Log vide. Effectuez des opérations pour commencer.': ('Empty log. Perform operations to start.', 'Log vide. Effectuez des opérations pour commencer.'),

    # ── FAQ questions ──
    'Q: "My push_swap segfaults on large inputs — why?"': ('Q: "My push_swap segfaults on large inputs — why?"', 'Q : « Mon push_swap segfault sur de grandes entrées — pourquoi ? »'),
    'Q: "Checker says KO but my stack looks sorted — what\'s wrong?"': ('Q: "Checker says KO but my stack looks sorted — what\'s wrong?"', 'Q : « Le checker dit KO mais ma pile semble triée — quel est le problème ? »'),
    'Q: "How to handle arguments as a single string?"': ('Q: "How to handle arguments as a single string?"', 'Q : « Comment gérer les arguments passés en une seule chaîne ? »'),
    'Q: "Checker displays \'Error\' on CTRL+D — normal?"': ('Q: "Checker displays \'Error\' on CTRL+D — normal?"', 'Q : « Mon checker affiche \'Error\' sur une entrée vide (CTRL+D) — est-ce normal ? »'),
    'Q: "Should push_swap print \'Error\' with no arguments?"': ('Q: "Should push_swap print \'Error\' with no arguments?"', 'Q : « push_swap doit-il afficher \'Error\' sans arguments ? »'),
    'Q: "How to test for leaks without Valgrind?"': ('Q: "How to test for leaks without Valgrind?"', 'Q : « Comment tester les fuites mémoire sans Valgrind ? »'),
    'Q: "Stuck at 4/5 (~850 ops). Easiest optimization?"': ('Q: "Stuck at 4/5 (~850 ops). Easiest optimization?"', 'Q : « Je suis bloqué à 4/5 sur 100 nombres (~850 ops). Quelle est l\'optimisation la plus simple ? »'),
    'Q: "Is the -v visualizer flag required?"': ('Q: "Is the -v visualizer flag required?"', 'Q : « Le flag -v du visualiseur est-il requis ? »'),

    # ── Paragraph texts (leaf) ──
    'A typical starting state. Everything lives on A; B is an empty workspace you fill during sorting.': (
        'A typical starting state. Everything lives on A; B is an empty workspace you fill during sorting.',
        'Un état de départ typique. Tout est sur A ; B est un espace de travail vide que vous remplissez pendant le tri.'
    ),
    'A is always a sorted (possibly rotated) sequence': ('A is always a sorted (possibly rotated) sequence', 'A est toujours une séquence triée (éventuellement rotatée)'),
    'A worked example': ('A worked example', 'Un exemple concret'),
    'Trivial; hardcoded.': ('Trivial; hardcoded.', 'Trivial ; codé en dur.'),
    'Both stacks freed before return. No leaks.': ('Both stacks freed before return. No leaks.', 'Les deux piles libérées avant le retour. Aucune fuite.'),
    'Even early-exit frees both stacks. No leaks.': ('Even early-exit frees both stacks. No leaks.', 'Même une sortie anticipée libère les deux piles. Aucune fuite.'),
    'Every malloc has a matching free.': ('Every malloc has a matching free.', 'Chaque malloc a un free correspondant.'),
    'Nearly identical to cost sort. Push all to B, find target in A, rotate, push back.': (
        'Nearly identical to cost sort. Push all to B, find target in A, rotate, push back.',
        'Presque identique au cost sort. Tout pousser vers B, trouver la cible dans A, pivoter, retransférer.'
    ),
    'Divide range into chunks. Push chunk-by-chip to B, pull back in sorted order.': (
        'Divide range into chunks. Push chunk-by-chip to B, pull back in sorted order.',
        'Diviser la plage en chunks. Pousser chunk par chunk vers B, retransférer dans l\'ordre trié.'
    ),
    'Use quicksort partitioning for 2-4 chunks, then cost sort within each chunk.': (
        'Use quicksort partitioning for 2-4 chunks, then cost sort within each chunk.',
        'Utiliser le partitionnement quicksort pour 2-4 chunks, puis cost sort dans chaque chunk.'
    ),
    'Sorts by individual bits, LSB to MSB. For each of 32 bits, push bit=0 to B, pull back. Always ~960 ops for 100 elements.': (
        'Sorts by individual bits, LSB to MSB. For each of 32 bits, push bit=0 to B, pull back. Always ~960 ops for 100 elements.',
        'Trie par bits individuels, LSB vers MSB. Pour chacun des 32 bits, pousser bit=0 vers B, retransférer. Toujours ~960 ops pour 100 éléments.'
    ),
    'Real questions from 42 students, with code references and practical advice.': (
        'Real questions from 42 students, with code references and practical advice.',
        'Vraies questions d\'étudiants de 42, avec références au code et conseils pratiques.'
    ),
    'Everything you need to compile, run, and verify the project locally — including the exact commands used to measure the benchmarks in this guide.': (
        'Everything you need to compile, run, and verify the project locally — including the exact commands used to measure the benchmarks in this guide.',
        'Tout ce dont vous avez besoin pour compiler, exécuter et vérifier le projet localement — y compris les commandes exactes utilisées pour mesurer les benchmarks de ce guide.'
    ),
    'The 42 correction is a scripted evaluation: error management, false tests, right tests, and the performance benchmarks. Here is every category, what it checks, and the result. Every box is green.': (
        'The 42 correction is a scripted evaluation: error management, false tests, right tests, and the performance benchmarks. Here is every category, what it checks, and the result. Every box is green.',
        'La correction 42 est une évaluation scriptée : gestion d\'erreurs, faux tests, vrais tests et benchmarks de performance. Voici chaque catégorie, ce qu\'elle vérifie et le résultat. Toutes les cases sont vertes.'
    ),
    'The correction requires zero leaks under Valgrind. Run both programs through it on a representative input:': (
        'The correction requires zero leaks under Valgrind. Run both programs through it on a representative input:',
        'La correction exige zéro fuite sous Valgrind. Exécutez les deux programmes sur une entrée représentative :'
    ),
    'The bars below show operation counts for both algorithms. The green line marks the 5/5 threshold — staying left of it means maximum points.': (
        'The bars below show operation counts for both algorithms. The green line marks the 5/5 threshold — staying left of it means maximum points.',
        'Les barres ci-dessous montrent les comptes d\'opérations pour les deux algorithmes. La ligne verte marque le seuil 5/5 — rester à gauche signifie le maximum de points.'
    ),
    'The bottleneck is not comparisons — it\'s stack operations.': (
        'The bottleneck is not comparisons — it\'s stack operations.',
        'Le goulot d\'étranglement n\'est pas les comparaisons — ce sont les opérations sur les piles.'
    ),
    'The recursive quicksort partitions the stack around a median pivot. Each partition takes O(n) operations, and there are O(log n) levels of recursion. Theoretically optimal for comparison-based sorting.': (
        'The recursive quicksort partitions the stack around a median pivot. Each partition takes O(n) operations, and there are O(log n) levels of recursion. Theoretically optimal for comparison-based sorting.',
        'Le quicksort récursif partitionne la pile autour d\'un pivot médian. Chaque partition prend O(n) opérations, et il y a O(log n) niveaux de récursion. Théoriquement optimal pour le tri par comparaison.'
    ),
    'There are only six possible permutations of three elements. A hardcoded decision tree sorts any of them in at most two operations — no loops, no pivots, no recursion. A is now sorted (possibly rotated).': (
        'There are only six possible permutations of three elements. A hardcoded decision tree sorts any of them in at most two operations — no loops, no pivots, no recursion. A is now sorted (possibly rotated).',
        'Il n\'y a que six permutations possibles de trois éléments. Un arbre de décision codé en dur trie n\'importe laquelle en au plus deux opérations — pas de boucles, pas de pivots, pas de récursion. A est maintenant trié (éventuellement rotaté).'
    ),
    'Three elements have exactly six permutations. Rather than loop or recurse, we read the three values and dispatch to the minimal sequence. This guarantees A is sorted in ≤ 2 operations, giving the insertion loop a clean, sorted base to build on.': (
        'Three elements have exactly six permutations. Rather than loop or recurse, we read the three values and dispatch to the minimal sequence. This guarantees A is sorted in ≤ 2 operations, giving the insertion loop a clean, sorted base to build on.',
        'Trois éléments ont exactement six permutations. Plutôt que boucler ou récursiver, nous lisons les trois valeurs et dispatchons vers la séquence minimale. Cela garantit que A est trié en ≤ 2 opérations, donnant à la boucle d\'insertion une base triée propre sur laquelle construire.'
    ),
    'These are the exact loops used to produce the averages quoted throughout this guide. Run each a few dozen times and take the mean — the cost sort is deterministic given a fixed input but the random inputs vary.': (
        'These are the exact loops used to produce the averages quoted throughout this guide. Run each a few dozen times and take the mean — the cost sort is deterministic given a fixed input but the random inputs vary.',
        'Ce sont les boucles exactes utilisées pour produire les moyennes citées dans ce guide. Exécutez chacune quelques dizaines de fois et prenez la moyenne — le cost sort est déterministe pour une entrée fixe mais les entrées aléatoires varient.'
    ),
    'These are the only moves you may print to stdout. The 42 checker reads them one per line and replays them on a fresh copy of the stacks. Knowing each operation\'s cost (1 op each) and effect is essential — every line you print is a line that counts against your grade.': (
        'These are the only moves you may print to stdout. The 42 checker reads them one per line and replays them on a fresh copy of the stacks. Knowing each operation\'s cost (1 op each) and effect is essential — every line you print is a line that counts against your grade.',
        'Ce sont les seuls mouvements que vous pouvez imprimer sur stdout. Le checker 42 les lit un par ligne et les rejoue sur une copie fraîche des piles. Connaître le coût (1 op chacune) et l\'effet de chaque opération est essentiel — chaque ligne que vous imprimez compte contre votre note.'
    ),
    'This is the engine of the new algorithm. Read it slowly — every block has a purpose:': (
        'This is the engine of the new algorithm. Read it slowly — every block has a purpose:',
        'C\'est le moteur du nouvel algorithme. Lisez-le lentement — chaque bloc a un but :'
    ),
    'This is the heart of the old algorithm. It scans the source stack, pushes "small" elements to the other stack, and rotates "large" elements to the bottom. The pivot is the median, returned so the caller can recurse on each side.': (
        'This is the heart of the old algorithm. It scans the source stack, pushes "small" elements to the other stack, and rotates "large" elements to the bottom. The pivot is the median, returned so the caller can recurse on each side.',
        'C\'est le cœur de l\'ancien algorithme. Il scanne la pile source, pousse les « petits » éléments vers l\'autre pile, et rotate les « grands » éléments vers le bas. Le pivot est la médiane, retourné pour que l\'appelant puisse récursiver de chaque côté.'
    ),
    'For each of n elements in B, scan all n elements of A (O(n)) and compute 4 costs (O(1)). Total: O(n²) comparisons. But each comparison is just an array lookup — no stack ops.': (
        'For each of n elements in B, scan all n elements of A (O(n)) and compute 4 costs (O(1)). Total: O(n²) comparisons. But each comparison is just an array lookup — no stack ops.',
        'Pour chacun des n éléments dans B, scanner les n éléments de A (O(n)) et calculer 4 coûts (O(1)). Total : O(n²) comparaisons. Mais chaque comparaison n\'est qu\'une recherche dans un tableau — pas d\'opérations sur les piles.'
    ),
    'For n ≤ 1000, cost-based insertion sort is optimal for push_swap. For n > 1000, a hybrid (quicksort partition + cost insertion) would be ideal.': (
        'For n ≤ 1000, cost-based insertion sort is optimal for push_swap. For n > 1000, a hybrid (quicksort partition + cost insertion) would be ideal.',
        'Pour n ≤ 1000, le tri par insertion à coût est optimal pour push_swap. Pour n > 1000, un hybride (partition quicksort + insertion à coût) serait idéal.'
    ),
    'Inserting the globally cheapest element each step avoids the "expensive tail" of arbitrary-order insertion. The effect compounds: cheaper early insertions keep stacks smaller, making later insertions cheaper too.': (
        'Inserting the globally cheapest element each step avoids the "expensive tail" of arbitrary-order insertion. The effect compounds: cheaper early insertions keep stacks smaller, making later insertions cheaper too.',
        'Insérer l\'élément globalement le moins cher à chaque étape évite la « queue coûteuse » de l\'insertion en ordre arbitraire. L\'effet se cumule : des insertions précoces moins chères maintiennent des piles plus petites, rendant les insertions ultérieures moins chères aussi.'
    ),
    'When pushing elements back from B to A, the quicksort processed them in whatever order the recursion produced — never the cheapest order. A globally-cheap insertion was never considered.': (
        'When pushing elements back from B to A, the quicksort processed them in whatever order the recursion produced — never the cheapest order. A globally-cheap insertion was never considered.',
        'Lors du renvoi des éléments de B vers A, le quicksort les traitait dans l\'ordre produit par la récursion — jamais dans l\'ordre le moins cher. Une insertion globalement bon marché n\'était jamais envisagée.'
    ),
    'Consider this stack A, read top-to-bottom:': ('Consider this stack A, read top-to-bottom:', 'Considérez cette pile A, lue de haut en bas :'),
    'Test your sorting logic in real time. Input custom numbers, perform manual operations, observe how the cost calculator computes the 4 strategies, or let the solver automatically sort the piles step-by-step.': (
        'Test your sorting logic in real time. Input custom numbers, perform manual operations, observe how the cost calculator computes the 4 strategies, or let the solver automatically sort the piles step-by-step.',
        'Testez votre logique de tri en temps réel. Saisissez des nombres personnalisés, effectuez des opérations manuelles, observez comment le calculateur de coût évalue les 4 stratégies, ou laissez le solveur trier les piles automatiquement étape par étape.'
    ),
    'Despite using the true median, the partition-then-undo pattern accumulates overhead. On 500-number adversarial inputs the total drifted toward 5800 ops, occasionally spilling over the 5500 line.': (
        'Despite using the true median, the partition-then-undo pattern accumulates overhead. On 500-number adversarial inputs the total drifted toward 5800 ops, occasionally spilling over the 5500 line.',
        'Malgré l\'utilisation de la vraie médiane, le schéma partitionner-puis-annuler accumule du surcoût. Sur des entrées adversariales de 500 nombres, le total dérivait vers 5800 ops, dépassant occasionnellement la ligne des 5500.'
    ),
    'Before settling on cost-based insertion sort, three other algorithms were considered. Here\'s why each was rejected.': (
        'Before settling on cost-based insertion sort, three other algorithms were considered. Here\'s why each was rejected.',
        'Avant de choisir le tri par insertion à coût, trois autres algorithmes ont été envisagés. Voici pourquoi chacun a été rejeté.'
    ),
    'Here\'s the payoff. Same project, same inputs, two algorithms. The cost-based sort shaves 37% off the operation count for 100 numbers and edges under the 5500 line for 500 numbers — enough to convert a 4/5 into a clean 5/5 on both benchmarks.': (
        'Here\'s the payoff. Same project, same inputs, two algorithms. The cost-based sort shaves 37% off the operation count for 100 numbers and edges under the 5500 line for 500 numbers — enough to convert a 4/5 into a clean 5/5 on both benchmarks.',
        'Voici le résultat. Même projet, mêmes entrées, deux algorithmes. Le tri par coût réduit de 37% le compte d\'opérations pour 100 nombres et passe sous la ligne des 5500 pour 500 nombres — assez pour convertir un 4/5 en un clean 5/5 sur les deux benchmarks.'
    ),
    'Rotate A down but B up. Again no fusion — each rotation is a separate line. The mirror of the previous strategy. Wins when the target is near A\'s bottom but the element is near B\'s top.': (
        'Rotate A down but B up. Again no fusion — each rotation is a separate line. The mirror of the previous strategy. Wins when the target is near A\'s bottom but the element is near B\'s top.',
        'Rotate A vers le bas mais B vers le haut. Là encore aucune fusion — chaque rotation est une ligne séparée. Le miroir de la stratégie précédente. Gagne quand la cible est près du bas de A mais l\'élément près du haut de B.'
    ),
    'The 4 lands exactly between 3 and 5. A is still circularly sorted — just with a different rotation. The invariant holds for the next insertion.': (
        'The 4 lands exactly between 3 and 5. A is still circularly sorted — just with a different rotation. The invariant holds for the next insertion.',
        'Le 4 atterrit exactement entre 3 et 5. A est toujours trié circulairement — juste avec une rotation différente. L\'invariant tient pour la prochaine insertion.'
    ),
    'The 42 correction is a scripted evaluation: error management, false tests, right tests, and the performance benchmarks. Here is every category, what it checks, and the result. Every box is green.': (
        'The 42 correction is a scripted evaluation: error management, false tests, right tests, and the performance benchmarks. Here is every category, what it checks, and the result. Every box is green.',
        'La correction 42 est une évaluation scriptée : gestion d\'erreurs, faux tests, vrais tests et benchmarks de performance. Voici chaque catégorie, ce qu\'elle vérifie et le résultat. Toutes les cases sont vertes.'
    ),
    'Because our stack is a linked list (no random access), the function first copies it into a local array for O(1) indexed lookup. It then finds the minimum\'s index and the maximum value, handles the two extreme cases, and otherwise walks circularly from the minimum.': (
        'Because our stack is a linked list (no random access), the function first copies it into a local array for O(1) indexed lookup. It then finds the minimum\'s index and the maximum value, handles the two extreme cases, and otherwise walks circularly from the minimum.',
        'Comme notre pile est une liste chaînée (pas d\'accès aléatoire), la fonction la copie d\'abord dans un tableau local pour un accès indexé O(1). Elle trouve ensuite l\'index du minimum et la valeur maximum, gère les deux cas extrêmes, et sinon parcourt circulairement depuis le minimum.'
    ),
    'Because the partition rotates "large" elements to the bottom of A to get them out of the way, the algorithm has to rotate them back before it can work on the upper half. This is a fixed tax on every partition step:': (
        'Because the partition rotates "large" elements to the bottom of A to get them out of the way, the algorithm has to rotate them back before it can work on the upper half. This is a fixed tax on every partition step:',
        'Comme la partition rotate les « grands » éléments vers le bas de A pour les écarter, l\'algorithme doit les re-rotate avant de pouvoir travailler sur la moitié supérieure. C\'est un coût fixe à chaque étape de partition :'
    ),
    'Getting under 700 for 100 numbers is relatively forgiving — even a sloppy quicksort manages it. The real fight is the 500-number case, where the 5500 threshold is tight. Algorithms based on naive pivot selection routinely blow past 6000–7000 ops on adversarial inputs. The cost-based approach in this guide averages ~5281, leaving only a ~220-op margin — but it does so': (
        'Getting under 700 for 100 numbers is relatively forgiving — even a sloppy quicksort manages it. The real fight is the 500-number case, where the 5500 threshold is tight. Algorithms based on naive pivot selection routinely blow past 6000–7000 ops on adversarial inputs. The cost-based approach in this guide averages ~5281, leaving only a ~220-op margin — but it does so',
        'Passer sous 700 pour 100 nombres est relativement clément — même un quicksort bâclé y arrive. Le vrai combat est le cas des 500 nombres, où le seuil de 5500 est serré. Les algorithmes basés sur une sélection de pivot naïve dépassent routinely 6000–7000 ops sur des entrées adversariales. L\'approche par coût de ce guide moyenne ~5281, ne laissant qu\'une marge de ~220 ops — mais elle le fait'
    ),
    'Each ra, pb, rr is a printed line counting toward your grade. Quicksort wastes ops on round-trip rotations; cost sort picks the globally cheapest element at each step.': (
        'Each ra, pb, rr is a printed line counting toward your grade. Quicksort wastes ops on round-trip rotations; cost sort picks the globally cheapest element at each step.',
        'Chaque ra, pb, rr est une ligne imprimée qui compte pour votre note. Quicksort gaspille des ops en rotations aller-retour ; le cost sort choisit l\'élément globalement le moins cher à chaque étape.'
    ),
    'A is fully sorted but rotated — the minimum is somewhere in the middle. Rotate it to the top using whichever direction is shorter:': (
        'A is fully sorted but rotated — the minimum is somewhere in the middle. Rotate it to the top using whichever direction is shorter:',
        'A est entièrement trié mais rotaté — le minimum est quelque part au milieu. Rotatez-le vers le sommet en utilisant la direction la plus courte :'
    ),
    'To move an element from the top of B into its correct slot in A, we must (a) bring that element to the top of B and (b) bring its target slot to the top of A. Each stack can be rotated up or down, giving': (
        'To move an element from the top of B into its correct slot in A, we must (a) bring that element to the top of B and (b) bring its target slot to the top of A. Each stack can be rotated up or down, giving',
        'Pour déplacer un élément du sommet de B vers sa position correcte dans A, nous devons (a) amener cet élément au sommet de B et (b) amener sa position cible au sommet de A. Chaque pile peut être rotatée vers le haut ou vers le bas, donnant'
    ),
    'The project went from a borderline 4/5 (quicksort, occasionally tipping over the 500-number threshold) to a clean, repeatable 5/5 across all benchmarks. The empty-line checker fix was the difference between a right-test failure and a full pass on the bonus.': (
        'The project went from a borderline 4/5 (quicksort, occasionally tipping over the 500-number threshold) to a clean, repeatable 5/5 across all benchmarks. The empty-line checker fix was the difference between a right-test failure and a full pass on the bonus.',
        'Le projet est passé d\'un 4/5 limite (quicksort, dépassant occasionnellement le seuil des 500 nombres) à un 5/5 net et répétable sur tous les benchmarks. Le correctif du checker pour les lignes vides a fait la différence entre un échec des vrais tests et un succès complet sur le bonus.'
    ),
    '~894 ops for 100 numbers (under 900 ✓ but over the 700 needed for 5/5) and ~5795 ops for 500 numbers (over 5500 ✗). Solid, but not the maximum.': (
        '~894 ops for 100 numbers (under 900 ✓ but over the 700 needed for 5/5) and ~5795 ops for 500 numbers (over 5500 ✗). Solid, but not the maximum.',
        '~894 ops pour 100 nombres (sous 900 ✓ mais au-dessus des 700 nécessaires pour 5/5) et ~5795 ops pour 500 nombres (au-dessus de 5500 ✗). Solide, mais pas le maximum.'
    ),
    'Suppose A has 6 elements and B has 5. The element we\'re considering sits at index': (
        'Suppose A has 6 elements and B has 5. The element we\'re considering sits at index',
        'Supposons que A ait 6 éléments et B en ait 5. L\'élément que nous considérons se trouve à l\'index'
    ),
    'While B is not empty: for every element on B, compute the cost to insert it into its correct circular position in A, across four rotation strategies. Pick the globally cheapest element, execute its cheapest strategy (using': (
        'While B is not empty: for every element on B, compute the cost to insert it into its correct circular position in A, across four rotation strategies. Pick the globally cheapest element, execute its cheapest strategy (using',
        'Tant que B n\'est pas vide : pour chaque élément de B, calculer le coût pour l\'insérer dans sa position circulaire correcte dans A, selon quatre stratégies de rotation. Choisir l\'élément globalement le moins cher, exécuter sa stratégie la moins chère (en utilisant'
    ),
    'Quicksort is a great starting point — it\'s intuitive and teaches you to think in terms of partitions and pivots. But on the push_swap scoring curve, the partition overhead and the missed': (
        'Quicksort is a great starting point — it\'s intuitive and teaches you to think in terms of partitions and pivots. But on the push_swap scoring curve, the partition overhead and the missed',
        'Quicksort est un excellent point de départ — c\'est intuitif et ça apprend à penser en termes de partitions et de pivots. Mais sur la courbe de scoring de push_swap, le surcoût des partitions et les'
    ),
    'Quicksort on two stacks works like ordinary quicksort, except the "partition" step is implemented by physically moving elements to the other stack. The algorithm picks a median pivot, pushes everything smaller than the pivot to': (
        'Quicksort on two stacks works like ordinary quicksort, except the "partition" step is implemented by physically moving elements to the other stack. The algorithm picks a median pivot, pushes everything smaller than the pivot to',
        'Quicksort sur deux piles fonctionne comme le quicksort ordinaire, sauf que l\'étape de « partition » est implémentée en déplaçant physiquement les éléments vers l\'autre pile. L\'algorithme choisit un pivot médian, pousse tout ce qui est plus petit que le pivot vers'
    ),
    'The first version of this project used a textbook recursive quicksort adapted for two stacks. It worked, it was elegant, and it scored': (
        'The first version of this project used a textbook recursive quicksort adapted for two stacks. It worked, it was elegant, and it scored',
        'La première version de ce projet utilisait un quicksort récursif classique adapté pour deux piles. Ça marchait, c\'était élégant, et ça a obtenu'
    ),
    'The cost sort isn\'t free. It does more': (
        'The cost sort isn\'t free. It does more',
        'Le cost sort n\'est pas gratuit. Il fait plus de'
    ),
    'A perfect': ('A perfect', 'Un push_swap parfait'),
    'A single memory leak means grade 0 at 42. Here\'s how every': (
        'A single memory leak means grade 0 at 42. Here\'s how every',
        'Une seule fuite mémoire signifie note 0 à 42. Voici comment chaque'
    ),
    'It isn\'t a clever data structure or a fancy pivot. It\'s the simple discipline of': (
        'It isn\'t a clever data structure or a fancy pivot. It\'s the simple discipline of',
        'Ce n\'est pas une structure de données astucieuse ou un pivot sophistiqué. C\'est la simple discipline de'
    ),
    'By guaranteeing A is sorted after exactly ≤ 2 operations, we establish the invariant that': (
        'By guaranteeing A is sorted after exactly ≤ 2 operations, we establish the invariant that',
        'En garantissant que A est trié après exactement ≤ 2 opérations, nous établissons l\'invariant que'
    ),
    'Instead of guessing pivots and recursing, the new algorithm keeps stack': (
        'Instead of guessing pivots and recursing, the new algorithm keeps stack',
        'Au lieu de deviner des pivots et de récursiver, le nouvel algorithme garde la pile'
    ),
    'Instead of processing B in arbitrary order, it scans all of B and inserts whichever element is cheapest': (
        'Instead of processing B in arbitrary order, it scans all of B and inserts whichever element is cheapest',
        'Au lieu de traiter B dans un ordre arbitraire, il scanne tout B et insère l\'élément le moins cher'
    ),
    'For every element, four strategies are costed and the cheapest wins. The final alignment picks': (
        'For every element, four strategies are costed and the cheapest wins. The final alignment picks',
        'Pour chaque élément, quatre stratégies sont évaluées et la moins chère gagne. L\'alignement final choisit'
    ),
    'There\'s no pivot to misjudge and no': (
        'There\'s no pivot to misjudge and no',
        'Il n\'y a pas de pivot à mal juger et pas de'
    ),
    'Whenever A and B both need to rotate the same direction, the algorithm fuses the common prefix of rotations into': (
        'Whenever A and B both need to rotate the same direction, the algorithm fuses the common prefix of rotations into',
        'Chaque fois que A et B doivent tous deux pivoter dans le même sens, l\'algorithme fusionne le préfixe commun des rotations en'
    ),
    'A common student mistake is to scan A from the top looking for the first element greater than': (
        'A common student mistake is to scan A from the top looking for the first element greater than',
        'Une erreur courante des étudiants est de scanner A depuis le sommet en cherchant le premier élément plus grand que'
    ),
    'The correction sheet includes "false tests" — deliberately malformed inputs that must produce': (
        'The correction sheet includes "false tests" — deliberately malformed inputs that must produce',
        'La fiche de correction inclut des « faux tests » — des entrées délibérément mal formées qui doivent produire'
    ),
    'An empty line in the input stream caused': (
        'An empty line in the input stream caused',
        'Une ligne vide dans le flux d\'entrée a causé'
    ),
    'Every line is matched against the eleven valid commands.': (
        'Every line is matched against the eleven valid commands.',
        'Chaque ligne est comparée aux onze commandes valides.'
    ),
    'Every node in stacks A and B is a': ('Every node in stacks A and B is a', 'Chaque nœud des piles A et B est un'),
    'Every partition rotated "large" elements down with': (
        'Every partition rotated "large" elements down with',
        'Chaque partition a rotaté les « grands » éléments vers le bas avec'
    ),
    'Both stacks were often rotated the same direction during partitioning, yet the code always issued separate': (
        'Both stacks were often rotated the same direction during partitioning, yet the code always issued separate',
        'Les deux piles étaient souvent rotatées dans le même sens pendant le partitionnement, pourtant le code émettait toujours des'
    ),
    'Both programs share the same argument validation.': (
        'Both programs share the same argument validation.',
        'Les deux programmes partagent la même validation des arguments.'
    ),
    'Both stacks behave like classic LIFO structures: you can only read, swap, or remove the': (
        'Both stacks behave like classic LIFO structures: you can only read, swap, or remove the',
        'Les deux piles se comportent comme des structures LIFO classiques : vous ne pouvez lire, échanger ou retirer que l\''
    ),
    'At scale (n > 10,000), the O(n²) decision cost becomes prohibitive in': (
        'At scale (n > 10,000), the O(n²) decision cost becomes prohibitive in',
        'À grande échelle (n > 10 000), le coût de décision O(n²) devient prohibitif en'
    ),
    'The checker is a separate program that takes the same integer arguments as': (
        'The checker is a separate program that takes the same integer arguments as',
        'Le checker est un programme séparé qui prend les mêmes arguments entiers que'
    ),
    'Most common cause: stack overflow from deep recursion. The old quicksort was recursive (': (
        'Most common cause: stack overflow from deep recursion. The old quicksort was recursive (',
        'Cause la plus courante : débordement de pile dû à une récursion profonde. L\'ancien quicksort était récursif ('
    ),
    'No! This was a bug. When user presses CTRL+D with no input,': (
        'No! This was a bug. When user presses CTRL+D with no input,',
        'Non ! C\'était un bug. Quand l\'utilisateur appuie sur CTRL+D sans entrée,'
    ),
    'The subject is ambiguous. Our implementation exits silently (': (
        'The subject is ambiguous. Our implementation exits silently (',
        'Le sujet est ambigu. Notre implémentation sort silencieusement ('
    ),
    'In the original version, the branch above': (
        'In the original version, the branch above',
        'Dans la version originale, la branche au-dessus de'
    ),
    'The solution is a single three-line guard at the top of the read loop: if the line is empty (': (
        'The solution is a single three-line guard at the top of the read loop: if the line is empty (',
        'La solution est une simple garde de trois lignes en haut de la boucle de lecture : si la ligne est vide ('
    ),
    'After the recursion finishes, A is sorted': (
        'After the recursion finishes, A is sorted',
        'Après la fin de la récursion, A est trié'
    ),
    'Walk the source stack. Elements below the pivot go to the other stack via': (
        'Walk the source stack. Elements below the pivot go to the other stack via',
        'Parcourez la pile source. Les éléments sous le pivot vont vers l\'autre pile via'
    ),
    'calls itself on the lower half (elements now on B) and the upper half (elements still on A). The base case: when only 2 elements remain in a range, swap them if needed and push them back to A.': (
        'calls itself on the lower half (elements now on B) and the upper half (elements still on A). The base case: when only 2 elements remain in a range, swap them if needed and push them back to A.',
        's\'appelle lui-même sur la moitié inférieure (éléments maintenant sur B) et la moitié supérieure (éléments encore sur A). Le cas de base : quand seulement 2 éléments restent dans une plage, les échanger si nécessaire et les repousser vers A.'
    ),
    'Push everything from A to B with': ('Push everything from A to B with', 'Tout pousser de A vers B avec'),
    'Push the top of': ('Push the top of', 'Pousser le sommet de'),
    'onto': ('onto', 'sur'),
    'Swap the first two elements at the top of': ('Swap the first two elements at the top of', 'Échanger les deux premiers éléments au sommet de'),
    'Rotate': ('Rotate', 'Rotatez'),
    'Reverse-rotate': ('Reverse-rotate', 'Reverse-rotatez'),
    'Rotate A up and B up. Because both move the same direction, the common prefix is fused into': (
        'Rotate A up and B up. Because both move the same direction, the common prefix is fused into',
        'Rotatez A vers le haut et B vers le haut. Comme les deux vont dans le même sens, le préfixe commun est fusionné en'
    ),
    'Rotate A down and B down. The mirror of': (
        'Rotate A down and B down. The mirror of',
        'Rotatez A vers le bas et B vers le bas. Le miroir de'
    ),
    'Rotate A up but B down. The two stacks move opposite directions, so': (
        'Rotate A up but B down. The two stacks move opposite directions, so',
        'Rotatez A vers le haut mais B vers le bas. Les deux piles vont dans des sens opposés, donc'
    ),
    'Take A =': ('Take A =', 'Prenez A ='),
    'For an element at index': ('For an element at index', 'Pour un élément à l\'index'),
    'Both axes are scaled so the': ('Both axes are scaled so the', 'Les deux axes sont mis à l\'échelle pour que le'),
    'Scanning, we find': ('Scanning, we find', 'En scannant, nous trouvons'),
    'The array copy is': ('The array copy is', 'La copie du tableau est'),
    'The O(n²) is in': ('The O(n²) is in', 'Le O(n²) est dans'),
    'The single biggest contributor. On 100-number runs, roughly 80–120 rotation pairs get fused into single': (
        'The single biggest contributor. On 100-number runs, roughly 80–120 rotation pairs get fused into single',
        'Le plus grand contributeur. Sur des runs de 100 nombres, environ 80–120 paires de rotations sont fusionnées en simples'
    ),
    'The project ships with a standard 42': ('The project ships with a standard 42', 'Le projet est livré avec un'),
    'Walk circularly from': ('Walk circularly from', 'Parcourir circulairement depuis'),
    'Here the mixed strategy': ('Here the mixed strategy', 'Ici la stratégie mixte'),
    'Note that': ('Note that', 'Notez que'),
    'Notice: every rotation is a': ('Notice: every rotation is a', 'Remarquez : chaque rotation est un'),
    'The final alignment rotated A with': ('The final alignment rotated A with', 'L\'alignement final a rotaté A avec'),
    'Check the': ('Check the', 'Consultez le'),
    'The target slot is index 3 — the': ('The target slot is index 3 — the', 'La position cible est l\'index 3 — le'),
    'The three cases for inserting': ('The three cases for inserting', 'Les trois cas pour insérer'),
    'The power of': ('The power of', 'La puissance de'),
    'The single idea that unlocked 5/5': ('The single idea that unlocked 5/5', 'L\'idée unique qui a débloqué 5/5'),
    'Phase 3: the main': ('Phase 3: the main', 'Phase 3 : la boucle principale'),
    'Final alignment with': ('Final alignment with', 'Alignement final avec'),
    'Undo the rotations with': ('Undo the rotations with', 'Annuler les rotations avec'),
    'sort_three()': ('sort_three()', 'sort_three()'),
    'cost-based insertion sort': ('cost-based insertion sort', 'tri par insertion à coût optimal'),
    'element from': ('element from', 'élément de'),
    'element. Stack': ('element. Stack', 'élément. La pile'),
    'starts with the unsorted input, stack': ('starts with the unsorted input, stack', 'commence avec l\'entrée non triée, la pile'),
    'starts empty, and the goal is to have': ('starts empty, and the goal is to have', 'commence vide, et le but est d\'avoir'),
    'sorted in ascending order (smallest on top) with': ('sorted in ascending order (smallest on top) with', 'trié par ordre croissant (plus petit en haut) avec'),
    'that reliably hits the maximum': ('that reliably hits the maximum', 'qui atteint fiablement le maximum'),
    'on both the 100- and 500-number benchmarks. Real C code, visual diagrams, and the bug that almost failed the correction.': (
        'on both the 100- and 500-number benchmarks. Real C code, visual diagrams, and the bug that almost failed the correction.',
        'sur les benchmarks 100 et 500 nombres. Du vrai code C, des diagrammes visuels, et le bug qui a failli faire rater la correction.'
    ),
    'operations you can do it in.': ('operations you can do it in.', 'opérations pour le faire.'),
    'few': ('few', 'peu'),
    'you can sort them, but how': ('you can sort them, but how', 'vous pouvez les trier, mais avec combien de'),
    'whether': ('whether', 'si'),
    'push_swap gives you two stacks —': ('push_swap gives you two stacks —', 'push_swap vous donne deux piles —'),
    '— and only eleven operations to sort the integers initially placed on': (
        '— and only eleven operations to sort the integers initially placed on',
        '— et seulement onze opérations pour trier les entiers initialement placés sur'
    ),
    'number of operations': ('number of operations', 'nombre d\'opérations'),
    'Your grade is determined purely by the': ('Your grade is determined purely by the', 'Votre note est déterminée purement par le'),
    'your program prints. Fewer is better. The thresholds below are the official 42 scale, and the entire architecture of both algorithms in this guide is built around staying comfortably under them.': (
        'your program prints. Fewer is better. The thresholds below are the official 42 scale, and the entire architecture of both algorithms in this guide is built around staying comfortably under them.',
        'que votre programme affiche. Moins c\'est mieux. Les seuils ci-dessous sont le barème officiel 42, et toute l\'architecture des deux algorithmes de ce guide est conçue pour rester confortablement en dessous.'
    ),
    'It picks the shortest path': ('It picks the shortest path', 'Il choisit le chemin le plus court'),
    'It picks the cheapest move': ('It picks the cheapest move', 'Il choisit le mouvement le moins cher'),
    'It reuses shared work': ('It reuses shared work', 'Il réutilise le travail partagé'),
    'No pathological worst case': ('No pathological worst case', 'Pas de pire cas pathologique'),

    # ── Partial text fragments (for mixed-content elements) ──
    '— rotations up to bring the slot to A\'s top': ('— rotations up to bring the slot to A\'s top', '— rotations vers le haut pour amener la position au sommet de A'),
    '— rotations down to bring the slot to A\'s top': ('— rotations down to bring the slot to A\'s top', '— rotations vers le bas pour amener la position au sommet de A'),
    '— rotations up to bring the element to B\'s top': ('— rotations up to bring the element to B\'s top', '— rotations vers le haut pour amener l\'élément au sommet de B'),
    '— rotations down to bring the element to B\'s top': ('— rotations down to bring the element to B\'s top', '— rotations vers le bas pour amener l\'élément au sommet de B'),
    'that lands the element in A.': ('that lands the element in A.', 'qui dépose l\'élément dans A.'),
    'in every formula is the final': ('in every formula is the final', 'dans chaque formule est le dernier'),
    'options: a fusion-friendly strategy is not always the cheapest. The old quicksort had no such calculation; it would have rotated A up 4 times and B up 1 time, costing 5+ operations plus the final': (
        'options: a fusion-friendly strategy is not always the cheapest. The old quicksort had no such calculation; it would have rotated A up 4 times and B up 1 time, costing 5+ operations plus the final',
        'options : une stratégie favorable à la fusion n\'est pas toujours la moins chère. L\'ancien quicksort n\'avait pas un tel calcul ; il aurait rotaté A vers le haut 4 fois et B 1 fois, coûtant 5+ opérations plus le dernier'
    ),
    'reaches the top, then': ('reaches the top, then', 'atteint le sommet, alors'),
    'the 4, landing it just below the 5 and just above the 3. Sorted!': (
        'the 4, landing it just below the 5 and just above the 3. Sorted!',
        'le 4, le déposant juste en dessous du 5 et juste au-dessus du 3. Trié !'
    ),
    'for the rest of the algorithm. Every subsequent insertion just needs to find the right circular slot — it never has to "fix" disorder in A.': (
        'for the rest of the algorithm. Every subsequent insertion just needs to find the right circular slot — it never has to "fix" disorder in A.',
        'pour le reste de l\'algorithme. Chaque insertion ultérieure n\'a qu\'à trouver la bonne position circulaire — elle n\'a jamais à « corriger » le désordre dans A.'
    ),
    'to bring the minimum to the top. Always': ('to bring the minimum to the top. Always', 'pour amener le minimum au sommet. Toujours'),
    ', never': (', never', ', jamais'),
    'would be shorter.': ('would be shorter.', 'serait plus court.'),
    ', even when': (', even when', ', même quand'),
    'is bonus. Mandatory part only requires printing operations to stdout. Our': (
        'is bonus. Mandatory part only requires printing operations to stdout. Our',
        'est un bonus. La partie obligatoire exige seulement d\'afficher les opérations sur stdout. Notre'
    ),
    'prints stack state after each operation via': ('prints stack state after each operation via', 'affiche l\'état de la pile après chaque opération via'),
    'checks in': ('checks in', 'vérifie dans'),
    ', and the': (', and the', ', et le'),
    'dependency with': ('dependency with', 'dépendance avec'),
    'It compiles': ('It compiles', 'Il compile'),
    ', and': (', and', ', et'),
    'handles the': ('handles the', 'gère le'),
    'case when args are passed as a single string.': ('case when args are passed as a single string.', 'cas quand les arguments sont passés en une seule chaîne.'),
    'means nothing if the checker rejects valid input. The bonus': ('means nothing if the checker rejects valid input. The bonus', 'ne signifie rien si le checker rejette une entrée valide. Le'),
    'program reads operations from stdin and replays them. During the correction, a single bug — treating blank lines as errors — silently failed otherwise-correct test runs. Here\'s how the checker works and how that bug was found and fixed.': (
        'program reads operations from stdin and replays them. During the correction, a single bug — treating blank lines as errors — silently failed otherwise-correct test runs. Here\'s how the checker works and how that bug was found and fixed.',
        'lit les opérations depuis stdin et les rejoue. Pendant la correction, un seul bug — traiter les lignes vides comme des erreurs — a silencieusement fait échouer des tests autrement corrects. Voici comment le checker fonctionne et comment ce bug a été trouvé et corrigé.'
    ),
    ', then reads operation lines from stdin until EOF. For each line, it validates the command and applies it to its own copy of the stacks. At EOF, it prints': (
        ', then reads operation lines from stdin until EOF. For each line, it validates the command and applies it to its own copy of the stacks. At EOF, it prints',
        ', puis lit les lignes d\'opération depuis stdin jusqu\'à EOF. Pour chaque ligne, il valide la commande et l\'applique à sa propre copie des piles. À EOF, il affiche'
    ),
    'if A is sorted and B is empty,': ('if A is sorted and B is empty,', 'si A est trié et B est vide,'),
    'otherwise, and': ('otherwise, and', 'sinon, et'),
    'if any line was invalid.': ('if any line was invalid.', 'si une ligne était invalide.'),
    'is a tiny helper that checks membership in a group of three strings (e.g.': (
        'is a tiny helper that checks membership in a group of three strings (e.g.',
        'est un petit utilitaire qui vérifie l\'appartenance à un groupe de trois chaînes (ex.'
    ),
    '). If a line matches none of the eleven,': ('). If a line matches none of the eleven,', '). Si une ligne ne correspond à aucune des onze,'),
    'returns 0 and the caller prints': ('returns 0 and the caller prints', 'renvoie 0 et l\'appelant affiche'),
    'passed every line straight to': ('passed every line straight to', 'passait chaque ligne directement à'),
    ', which returned 0 for the empty string (it matches no command). The checker then printed': (
        ', which returned 0 for the empty string (it matches no command). The checker then printed',
        ', qui renvoyait 0 pour la chaîne vide (elle ne correspond à aucune commande). Le checker affichait alors'
    ),
    'and an early return. Any right test whose pipeline included a stray newline would report': (
        'and an early return. Any right test whose pipeline included a stray newline would report',
        'et un retour anticipé. Tout vrai test dont le pipeline incluait une nouvelle ligne parasite rapportait'
    ),
    'and bailed — even though the actual sorting operations were all valid.': (
        'and bailed — even though the actual sorting operations were all valid.',
        'et abandonnait — même si les opérations de tri étaient toutes valides.'
    ),
    'is correct. An': ('is correct. An', 'est correct. Une'),
    ') is genuinely invalid input — the spec is violated, so': (') is genuinely invalid input — the spec is violated, so', ') est une entrée véritablement invalide — le sujet est violé, donc'),
    'is ambiguous: it\'s not a command at all. The strict reading would still error, but the practical reading (and what 42\'s automated graders expect) is to tolerate blank lines as whitespace noise. Skipping them makes the checker robust to exactly the kind of piped input the correction uses.': (
        'is ambiguous: it\'s not a command at all. The strict reading would still error, but the practical reading (and what 42\'s automated graders expect) is to tolerate blank lines as whitespace noise. Skipping them makes the checker robust to exactly the kind of piped input the correction uses.',
        'est ambigu : ce n\'est pas du tout une commande. La lecture stricte continuerait à erreur, mais la lecture pratique (et ce que les évaluateurs automatiques de 42 attendent) est de tolérer les lignes vides comme du bruit. Les ignorer rend le checker robuste face exactement au type d\'entrée pipée que la correction utilise.'
    ),
    '), free it and': ('), free it and', '), libère-le et'),
    'to the next iteration instead of dispatching it. Empty lines become no-ops rather than errors.': (
        'to the next iteration instead of dispatching it. Empty lines become no-ops rather than errors.',
        'à la prochaine itération au lieu de la dispatcher. Les lignes vides deviennent des no-ops plutôt que des erreurs.'
    ),
    'checks that every argument is a well-formed integer (optional leading minus, then digits only) and that there are no duplicates.': (
        'checks that every argument is a well-formed integer (optional leading minus, then digits only) and that there are no duplicates.',
        'vérifie que chaque argument est un entier bien formé (signe moins optionnel, puis chiffres uniquement) et qu\'il n\'y a pas de doublons.'
    ),
    'additionally guards against integer overflow via': ('additionally guards against integer overflow via', 'garde en plus contre l\'overflow d\'entier via'),
    'Any failure prints': ('Any failure prints', 'Tout échec affiche'),
    'to stderr and exits non-zero — without leaking.': ('to stderr and exits non-zero — without leaking.', 'sur stderr et sort avec un code non nul — sans fuite.'),
    'compares strings, not parsed ints. This correctly catches duplicates like': ('compares strings, not parsed ints. This correctly catches duplicates like', 'compare les chaînes, pas les entiers parsés. Cela détecte correctement les doublons comme'),
    'as distinct (they parse equal but differ lexically) — which is the conservative, spec-compliant behavior. Overflow is rejected separately by': (
        'as distinct (they parse equal but differ lexically) — which is the conservative, spec-compliant behavior. Overflow is rejected separately by',
        'comme distincts (ils parsent égaux mais diffèrent lexicalement) — ce qui est le comportement conservateur et conforme au sujet. L\'overflow est rejeté séparément par'
    ),
    'before any': ('before any', 'avant tout'),
    'gets a matching': ('gets a matching', 'a un'),
    'allocated with': ('allocated with', 'alloué avec'),
    'via': ('via', 'via'),
    '. The project guarantees every node is freed through': ('. The project guarantees every node is freed through', '. Le projet garantit que chaque nœud est libéré via'),
    'or': ('or', 'ou'),
    'after! Our': ('after! Our', 'après ! Notre'),
    'handles this at lines 79-86 of': ('handles this at lines 79-86 of', 'gère cela aux lignes 79-86 de'),
    'to split. Don\'t forget': ('to split. Don\'t forget', 'pour découper. N\'oubliez pas'),
    'when': ('when', 'quand'),
    'when': ('when', 'quand'),
    'Common leak sources: forgetting': ('Common leak sources: forgetting', 'Sources de fuite courantes : oublier'),
    'before': ('before', 'avant'),
    '. Or write a loop that calls sort 1000 times and watch': ('. Or write a loop that calls sort 1000 times and watch', '. Ou écrivez une boucle qui appelle le tri 1000 fois et regardez'),
    'for full source code, or open an issue.': ('for full source code, or open an issue.', 'pour le code source complet, ou ouvrez une issue.'),
    'to return 0, which triggered': ('to return 0, which triggered', 'renvoyer 0, ce qui a déclenché'),
    'would have taken a handful.': ('would have taken a handful.', 'aurait pris une poignée.'),
    'would be far cheaper.': ('would be far cheaper.', 'serait bien moins cher.'),
    'until the minimum reached the top. If the minimum sat near the bottom, that could mean 400+ needless rotations where': (
        'until the minimum reached the top. If the minimum sat near the bottom, that could mean 400+ needless rotations where',
        'jusqu\'à ce que le minimum atteigne le sommet. Si le minimum était près du bas, cela pouvait signifier 400+ rotations inutiles où'
    ),
    ', then immediately rotated them back up with': (', then immediately rotated them back up with', ', puis immédiatement les re-rotatait vers le haut avec'),
    '. These round-trips are pure waste — they exist only because the partition strategy requires them.': (
        '. These round-trips are pure waste — they exist only because the partition strategy requires them.',
        '. Ces allers-retours sont du gaspillage pur — ils n\'existent que parce que la stratégie de partition les exige.'
    ),
    'followed by a fixed-direction': ('followed by a fixed-direction', 'suivi d\'une boucle'),
    'loop to align A. The current dispatcher routes large inputs straight to the cost sort.': (
        'loop to align A. The current dispatcher routes large inputs straight to the cost sort.',
        'à direction fixe pour aligner A. Le dispatcher actuel route les grandes entrées directement vers le cost sort.'
    ),
    'finishes, A is sorted but rotated. The old code finds the minimum and rotates it to the top — but it only ever uses': (
        'finishes, A is sorted but rotated. The old code finds the minimum and rotates it to the top — but it only ever uses',
        'se termine, A est trié mais rotaté. L\'ancien code trouve le minimum et le rotate vers le sommet — mais il n\'utilise toujours que'
    ),
    ', even when the minimum is near the bottom and': (', even when the minimum is near the bottom and', ', même quand le minimum est près du bas et'),
    'calls itself). For 500 elements with bad pivots, this could reach 500 recursion levels. The new': (
        'calls itself). For 500 elements with bad pivots, this could reach 500 recursion levels. The new',
        's\'appelle lui-même). Pour 500 éléments avec de mauvais pivots, cela pouvait atteindre 500 niveaux de récursion. Le nouveau'
    ),
    'is fully iterative — no recursion. Fix: use': ('is fully iterative — no recursion. Fix: use', 'est entièrement itératif — pas de récursion. Solution : utiliser'),
    'or switch to iterative.': ('or switch to iterative.', 'ou passer à l\'itératif.'),
    'handles this in the final block.': ('handles this in the final block.', 'gère cela dans le bloc final.'),
    'is not sorted — it\'s rotated. You need to rotate A to put min at top. Our': (
        'is not sorted — it\'s rotated. You need to rotate A to put min at top. Our',
        'n\'est pas trié — il est rotaté. Vous devez rotatez A pour mettre le min au sommet. Notre'
    ),
    'Checker requires': ('Checker requires', 'Le checker exige'),
    '— sorted AND B empty.': ('— sorted AND B empty.', '— trié ET B vide.'),
    '— combine rotations when both stacks need same direction. Saves 100-150 ops.': (
        '— combine rotations when both stacks need same direction. Saves 100-150 ops.',
        '— combiner les rotations quand les deux piles vont dans le même sens. Économise 100-150 ops.'
    ),
    '— pick shortest path to min. Saves 50-100 ops.': (
        '— pick shortest path to min. Saves 50-100 ops.',
        '— choisir le chemin le plus court vers le min. Économise 50-100 ops.'
    ),
    '— scan all of B, insert the one with lowest cost. Saves 100-200 ops. This is cost sort.': (
        '— scan all of B, insert the one with lowest cost. Saves 100-200 ops. This is cost sort.',
        '— scanner tout B, insérer celui au coût le plus bas. Économise 100-200 ops. C\'est le cost sort.'
    ),
    'Best of both worlds. Scales to n=10,000+.': ('Best of both worlds. Scales to n=10,000+.', 'Le meilleur des deux mondes. Passe à l\'échelle jusqu\'à n=10 000+.'),
    'Significantly more complex. Not needed for 42 grading.': ('Significantly more complex. Not needed for 42 grading.', 'Significativement plus complexe. Pas nécessaire pour la notation 42.'),
    'Extending push_swap beyond 42.': ('Extending push_swap beyond 42.', 'Étendre push_swap au-delà de 42.'),
    'This is what we implemented, with the full 4-strategy optimization.': ('This is what we implemented, with the full 4-strategy optimization.', 'C\'est ce que nous avons implémenté, avec l\'optimisation complète des 4 stratégies.'),
    'Same approach as ours.': ('Same approach as ours.', 'Même approche que la nôtre.'),
    'Typically only checks 2 strategies (rr, rrr), missing mixed (ra+rrb, rra+rb). ~10% worse.': (
        'Typically only checks 2 strategies (rr, rrr), missing mixed (ra+rrb, rra+rb). ~10% worse.',
        'Typiquement ne vérifie que 2 stratégies (rr, rrr), manquant les mixtes (ra+rrb, rra+rb). ~10% pire.'
    ),
    'Fast for large n. Reduces search space.': ('Fast for large n. Reduces search space.', 'Rapide pour les grands n. Réduit l\'espace de recherche.'),
    'Chunk boundaries create artifacts. Pulling back is another sort. Harder to implement.': (
        'Chunk boundaries create artifacts. Pulling back is another sort. Harder to implement.',
        'Les frontières des chunks créent des artefacts. Le retrait est un autre tri. Plus difficile à implémenter.'
    ),
    '960 ops > our 559. The 32 passes is too many for small n. Would score': ('960 ops > our 559. The 32 passes is too many for small n. Would score', '960 ops > nos 559. Les 32 passes sont trop pour les petits n. Marquerait'),
    'on 100.': ('on 100.', 'sur 100.'),
    'n > 2000 where determinism matters more than op count.': ('n > 2000 where determinism matters more than op count.', 'n > 2000 où le déterminisme compte plus que le nombre d\'ops.'),
    'n > 500 where O(n²) search becomes slow.': ('n > 500 where O(n²) search becomes slow.', 'n > 500 où la recherche O(n²) devient lente.'),
    'For n ≤ 500, cost-based insertion sort with 4 rotation strategies is the': ('For n ≤ 500, cost-based insertion sort with 4 rotation strategies is the', 'Pour n ≤ 500, le tri par insertion à coût avec 4 stratégies de rotation est le'),
    '. Easy to understand, easy to debug, O(n²) decision cost is negligible at this scale.': (
        '. Easy to understand, easy to debug, O(n²) decision cost is negligible at this scale.',
        '. Facile à comprendre, facile à déboguer, le coût de décision O(n²) est négligeable à cette échelle.'
    ),
    'each "comparison" costs 1-3 stack operations (ra, pb, rra). The constant per comparison is enormous.': (
        'each "comparison" costs 1-3 stack operations (ra, pb, rra). The constant per comparison is enormous.',
        'chaque « comparaison » coûte 1-3 opérations sur la pile (ra, pb, rra). La constante par comparaison est énorme.'
    ),
    '~100 × 5.6 avg ops per insertion': ('~100 × 5.6 avg ops per insertion', '~100 × 5.6 ops moy. par insertion'),
    '~100 × log₂(100) × 1.3 ≈ 869 + overhead': ('~100 × log₂(100) × 1.3 ≈ 869 + overhead', '~100 × log₂(100) × 1.3 ≈ 869 + surcoût'),
    'O(n × 32) — deterministic, no worst case.': ('O(n × 32) — deterministic, no worst case.', 'O(n × 32) — déterministe, pas de pire cas.'),
    '(as a rotated, circular array) and repeatedly inserts the': ('(as a rotated, circular array) and repeatedly inserts the', '(comme un tableau rotaté, circulaire) et insère répétitivement l\''),
    'between the two stacks. That algorithm is the cost-based insertion sort.': (
        'between the two stacks. That algorithm is the cost-based insertion sort.',
        'entre les deux piles. Cet algorithme est le tri par insertion à coût optimal.'
    ),
    'sharing is just the most visible reward of that discipline — the cheap-element selection is what keeps the average low.': (
        'sharing is just the most visible reward of that discipline — the cheap-element selection is what keeps the average low.',
        'le partage est juste la récompense la plus visible de cette discipline — la sélection de l\'élément le moins cher est ce qui maintient la moyenne basse.'
    ),
    '— perfectly ascending. The "wrap" happens between 9 and 2. Any rotation of a sorted array looks like this, and our A is exactly such a rotation throughout the insertion loop.': (
        '— perfectly ascending. The "wrap" happens between 9 and 2. Any rotation of a sorted array looks like this, and our A is exactly such a rotation throughout the insertion loop.',
        '— parfaitement croissant. Le « wrap » se produit entre 9 et 2. Toute rotation d\'un tableau trié ressemble à cela, et notre A est exactement une telle rotation tout au long de la boucle d\'insertion.'
    ),
    ': if you start reading from the minimum (2) and wrap around at the end, you get': (
        ': if you start reading from the minimum (2) and wrap around at the end, you get',
        ': si vous commencez à lire depuis le minimum (2) et bouclez à la fin, vous obtenez'
    ),
    'The sequence': ('The sequence', 'La séquence'),
    'is': ('is', 'est'),
    ': the circular search': (': the circular search', ': la recherche circulaire'),
    ': the last element becomes the first.': (': the last element becomes the first.', ': le dernier élément devient le premier.'),
    ': the last element becomes the first. Shifts everything down.': (': the last element becomes the first. Shifts everything down.', ': le dernier élément devient le premier. Décale tout vers le bas.'),
    'up: the top element becomes the last.': ('up: the top element becomes the last.', 'vers le haut : l\'élément du sommet devient le dernier.'),
    'up: the top element becomes the last. Shifts everything up by one.': ('up: the top element becomes the last. Shifts everything up by one.', 'vers le haut : l\'élément du sommet devient le dernier. Décale tout vers le haut de un.'),
    'at the same time — one line, two effects.': ('at the same time — one line, two effects.', 'en même temps — une ligne, deux effets.'),
    'simultaneously —': ('simultaneously —', 'simultanément —'),
    'simultaneously — the mirror of': ('simultaneously — the mirror of', 'simultanément — le miroir de'),
    'used them; the new cost sort uses them whenever both stacks must rotate the same way. This single insight is responsible for a large share of the savings you\'ll see in the benchmarks.': (
        'used them; the new cost sort uses them whenever both stacks must rotate the same way. This single insight is responsible for a large share of the savings you\'ll see in the benchmarks.',
        'les utilisait jamais ; le nouveau cost sort les utilise chaque fois que les deux piles doivent pivoter dans le même sens. Cette seule idée est responsable d\'une grande partie des économies que vous verrez dans les benchmarks.'
    ),
    '. An algorithm that ignores them wastes up to half of its rotations. Our old quicksort': (
        '. An algorithm that ignores them wastes up to half of its rotations. Our old quicksort',
        '. Un algorithme qui les ignore gaspille jusqu\'à la moitié de ses rotations. Notre ancien quicksort'
    ),
    '— let you do': ('— let you do', '— permettent de faire'),
    'Three operations —': ('Three operations —', 'Trois opérations —'),
    '— every rotation is its own line. Wins when the target is near A\'s top but the element is near B\'s bottom (or vice versa in the next strategy).': (
        '— every rotation is its own line. Wins when the target is near A\'s top but the element is near B\'s bottom (or vice versa in the next strategy).',
        '— chaque rotation est sa propre ligne. Gagne quand la cible est près du sommet de A mais l\'élément près du bas de B (ou vice versa dans la stratégie suivante).'
    ),
    '. Best when the element and its target are both near the': ('. Best when the element and their target are both near the', '. Mieux vaut quand l\'élément et sa cible sont tous deux près du'),
    '. Best when the element and its target are both near the top of their stacks.': (
        '. Best when the element and its target are both near the top of their stacks.',
        '. Mieux vaut quand l\'élément et sa cible sont tous deux près du sommet de leurs piles.'
    ),
    'lines. You only pay for the longer of the two rotations, then finish the remainder with': (
        'lines. You only pay for the longer of the two rotations, then finish the remainder with',
        'lignes. Vous ne payez que pour la plus longue des deux rotations, puis terminez le reste avec'
    ),
    ': common rotations fuse into': (': common rotations fuse into', ': les rotations communes fusionnent en'),
    '. The combined': ('. The combined', '. Le combiné'),
    'never appears, even though both stacks are being rotated in the same direction.': (
        'never appears, even though both stacks are being rotated in the same direction.',
        'n\'apparaît jamais, même si les deux piles sont rotatées dans le même sens.'
    ),
    'opportunities cap it at 4/5. To break through to 5/5 reliably, we needed an algorithm that': (
        'opportunities cap it at 4/5. To break through to 5/5 reliably, we needed an algorithm that',
        'opportunités le plafonnent à 4/5. Pour percer fiablement vers 5/5, nous avions besoin d\'un algorithme qui'
    ),
    'it fell short is the best way to appreciate the new algorithm.': ('it fell short is the best way to appreciate the new algorithm.', 'il est resté court est la meilleure façon d\'apprécier le nouvel algorithme.'),
    'out of the way, then recurses on both halves.': ('out of the way, then recurses on both halves.', 'hors du chemin, puis récursive sur les deux moitiés.'),
    'so they can be revisited.': ('so they can be revisited.', 'pour qu\'ils puissent être revisités.'),
    'on the way back); elements above the pivot get rotated to the bottom with': ('on the way back); elements above the pivot get rotated to the bottom with', 'au retour) ; les éléments au-dessus du pivot sont rotatés vers le bas avec'),
    '(or': ('(or', '(ou'),
    'in A (size': ('in A (size', 'dans A (taille'),
    'in B (size': ('in B (size', 'dans B (taille'),
    '), and a target slot at index': ('), and a target slot at index', '), et une position cible à l\'index'),
    'in B, and its target slot is at index': ('in B, and its target slot is at index', 'dans B, et sa position cible est à l\'index'),
    'in A. Then:': ('in A. Then:', 'dans A. Alors :'),
    'combinations. Each combination has a different cost, and the algorithm always picks the cheapest.': (
        'combinations. Each combination has a different cost, and the algorithm always picks the cheapest.',
        'combinaisons. Chaque combinaison a un coût différent, et l\'algorithme choisit toujours la moins chère.'
    ),
    'rotate A up 4 times': ('rotate A up 4 times', 'rotatez A vers le haut 4 fois'),
    'rotate A down 2 times': ('rotate A down 2 times', 'rotatez A vers le bas 2 fois'),
    'rotate B up 1 time': ('rotate B up 1 time', 'rotatez B vers le haut 1 fois'),
    'rotate B down 4 times': ('rotate B down 4 times', 'rotatez B vers le bas 4 fois'),
    'to share rotations), and': ('to share rotations), and', 'pour partager les rotations), et'),
    'it home. Repeat.': ('it home. Repeat.', 'à la maison. Répétez.'),
    'if the minimum is in the first half,': ('if the minimum is in the first half,', 'si le minimum est dans la première moitié,'),
    'based on the minimum\'s position saves up to': ('based on the minimum\'s position saves up to', "basé sur la position du minimum économise jusqu'à"),
    'operations on the final rotation — meaningful at 500 elements, where it can be 200+ ops.': (
        'operations on the final rotation — meaningful at 500 elements, where it can be 200+ ops.',
        'opérations sur la rotation finale — significatif à 500 éléments, où ça peut être 200+ ops.'
    ),
    'based on which is shorter — never a fixed direction.': ('based on which is shorter — never a fixed direction.', 'basé sur lequel est le plus court — jamais une direction fixe.'),
    'or': ('or', 'ou'),
    '(shortest)': ('(shortest)', '(le plus court)'),
    ', and why Valgrind reports "no leaks are possible".': (', and why Valgrind reports "no leaks are possible".', ', et pourquoi Valgrind rapporte « no leaks are possible ».'),
    'is the only thing that matters for the grade. Spending O(N²) compute to save O(N) operations is exactly the right trade for this problem.': (
        'is the only thing that matters for the grade. Spending O(N²) compute to save O(N) operations is exactly the right trade for this problem.',
        'est la seule chose qui compte pour la note. Dépenser du calcul O(N²) pour économiser des opérations O(N) est exactement le bon compromis pour ce problème.'
    ),
    'on both benchmarks': ('on both benchmarks', 'sur les deux benchmarks'),
    '— a hard fail on the correction sheet, despite a perfectly sorted stack.': (
        '— a hard fail on the correction sheet, despite a perfectly sorted stack.',
        '— un échec net sur la fiche de correction, malgré une pile parfaitement triée.'
    ),
    '— and "right tests" — valid runs that must produce': ('— and "right tests" — valid runs that must produce', '— et les « vrais tests » — des runs valides qui doivent produire'),
    '— 100M array lookups for 10k elements. Quicksort\'s O(n log n) decision would be faster. But since push_swap grades on n ≤ 500, this never matters.': (
        '— 100M array lookups for 10k elements. Quicksort\'s O(n log n) decision would be faster. But since push_swap grades on n ≤ 500, this never matters.',
        '— 100M recherches dans un tableau pour 10k éléments. La décision O(n log n) de quicksort serait plus rapide. Mais comme push_swap note sur n ≤ 500, cela n\'a jamais d\'importance.'
    ),
    '— the smallest element is somewhere in the middle. The old code rotates A with': (
        '— the smallest element is somewhere in the middle. The old code rotates A with',
        '— le plus petit élément est quelque part au milieu. L\'ancien code rotate A avec'
    ),
    'lines, directly subtracting that many operations from the total.': ('lines, directly subtracting that many operations from the total.', 'lignes, soustrayant directement autant d\'opérations du total.'),
    '. The actual printed ops ≈ O(n × k) where k = avg rotation distance.': ('. The actual printed ops ≈ O(n × k) where k = avg rotation distance.', '. Les ops réellement imprimées ≈ O(n × k) où k = distance de rotation moy.'),
    '. The challenge is not': ('. The challenge is not', '. Le défi n\'est pas'),
    '. The green line is the 5/5 threshold. For 100 numbers, the old bar (894) spills well past the 700 threshold — that\'s the 4/5. The new bar (559) sits comfortably left of the line. For 500 numbers the gap is narrower: the old 5795 crosses the 5500 line, the new 5281 sneaks under it. That ~510-op margin is the entire difference between 4/5 and 5/5.': (
        '. The green line is the 5/5 threshold. For 100 numbers, the old bar (894) spills well past the 700 threshold — that\'s the 4/5. The new bar (559) sits comfortably left of the line. For 500 numbers the gap is narrower: the old 5795 crosses the 5500 line, the new 5281 sneaks under it. That ~510-op margin is the entire difference between 4/5 and 5/5.',
        '. La ligne verte est le seuil 5/5. Pour 100 nombres, l\'ancienne barre (894) déborde largement du seuil de 700 — c\'est le 4/5. La nouvelle barre (559) se trouve confortablement à gauche de la ligne. Pour 500 nombres l\'écart est plus étroit : l\'ancienne 5795 franchit la ligne 5500, la nouvelle 5281 passe en dessous. Cette marge de ~510 ops est toute la différence entre 4/5 et 5/5.'
    ),
    '. The minimum isn\'t necessarily at the top; it sits somewhere in the middle. To insert a value from B, we must find its correct slot in this rotated, circular sorted sequence. This is the trickiest part of the whole algorithm to get right.': (
        '. The minimum isn\'t necessarily at the top; it sits somewhere in the middle. To insert a value from B, we must find its correct slot in this rotated, circular sorted sequence. This is the trickiest part of the whole algorithm to get right.',
        '. Le minimum n\'est pas nécessairement au sommet ; il se trouve quelque part au milieu. Pour insérer une valeur depuis B, nous devons trouver sa position correcte dans cette séquence triée circulaire et rotatée. C\'est la partie la plus délicate de tout l\'algorithme à get right.'
    ),
    '. The source must pass with no errors before submission.': ('. The source must pass with no errors before submission.', '. La source doit passer sans erreur avant la soumission.'),
    '42 enforces a strict style via': ('42 enforces a strict style via', '42 impose un style strict via'),
    '. The right tests were failing. The cause was subtle: some test harnesses and shell pipelines feed trailing newlines or empty lines into the checker\'s stdin. The original': (
        '. The right tests were failing. The cause was subtle: some test harnesses and shell pipelines feed trailing newlines or empty lines into the checker\'s stdin. The original',
        '. Les vrais tests échouaient. La cause était subtile : certains harnesses de test et pipelines shell envoient des nouvelles lignes trailing ou des lignes vides dans le stdin du checker. L\'original'
    ),
    'A is always sorted — but': ('A is always sorted — but', 'A est toujours trié — mais'),
    '(value 2) and': ('(value 2) and', '(valeur 2) et'),
    '→ return 3.': ('→ return 3.', '→ renvoie 3.'),
    '→ it becomes the new maximum. Its target is also the index of the current minimum (it slots in just after the max, which is just before the min, circularly).': (
        '→ it becomes the new maximum. Its target is also the index of the current minimum (it slots in just after the max, which is just before the min, circularly).',
        '→ il devient le nouveau maximum. Sa cible est aussi l\'index du minimum actuel (il s\'insère juste après le max, qui est juste avant le min, circulairement).'
    ),
    '→ it becomes the new minimum. Its target is the index of the current minimum (it slots in just before it, circularly).': (
        '→ it becomes the new minimum. Its target is the index of the current minimum (it slots in just before it, circularly).',
        '→ il devient le nouveau minimum. Sa cible est l\'index du minimum actuel (il s\'insère juste avant lui, circulairement).'
    ),
    '→ walk the circular sorted order starting from the minimum, and return the index of the first element greater than': (
        '→ walk the circular sorted order starting from the minimum, and return the index of the first element greater than',
        '→ parcourez l\'ordre trié circulaire en partant du minimum, et renvoyez l\'index du premier élément plus grand que'
    ),
    'val is between min and max': ('val is between min and max', 'val est entre min et max'),
    'val is larger than A\'s current maximum': ('val is larger than A\'s current maximum', 'val est plus grand que le maximum actuel de A'),
    'val is smaller than A\'s current minimum': ('val is smaller than A\'s current minimum', 'val est plus petit que le minimum actuel de A'),
    'is not below 2 nor above 9, so we hit the normal case.': ('is not below 2 nor above 9, so we hit the normal case.', 'n\'est ni en dessous de 2 ni au-dessus de 9, donc on tombe sur le cas normal.'),
    ', not > 4.': (', not > 4.', ', pas > 4.'),
    'Bad arguments print': ('Bad arguments print', 'Les mauvais arguments affichent'),
    'on stderr and exit non-zero, with no leak': ('on stderr and exit non-zero, with no leak', 'sur stderr et sortent avec un code non nul, sans fuite'),
    'output, piped to': ('output, piped to', 'sortie, pipée vers'),
    'with the same args, prints': ('with the same args, prints', 'avec les mêmes arguments, affiche'),
    'Every': ('Every', 'Chaque'),
    'on sorted input prints nothing (0 ops)': ('on sorted input prints nothing (0 ops)', 'sur une entrée triée n\'affiche rien (0 ops)'),
    '(e.g.': ('(e.g.', '(ex.'),
    '(top to bottom) and suppose we want to insert': ('(top to bottom) and suppose we want to insert', '(de haut en bas) et supposons que nous voulions insérer'),
    'from B.': ('from B.', 'depuis B.'),
    'finds the true median of the elements currently in the range': ('finds the true median of the elements currently in the range', 'trouve la vraie médiane des éléments actuellement dans la plage'),
    'by recursively partitioning a temporary copy of the stack. This is more expensive than a random pivot but guarantees balanced splits.': (
        'by recursively partitioning a temporary copy of the stack. This is more expensive than a random pivot but guarantees balanced splits.',
        'en partitionnant récursivement une copie temporaire de la pile. C\'est plus coûteux qu\'un pivot aléatoire mais garantit des partitions équilibrées.'
    ),
    ', rotates the rest of': (', rotates the rest of', ', rotate le reste de'),
    'in, max]': ('in, max]', 'in, max]'),
    '[min, max]': ('[min, max]', '[min, max]'),
    'No,': ('No,', 'Non,'),
    'On macOS:': ('On macOS:', 'Sur macOS :'),
    '. Common leak sources: forgetting': ('. Common leak sources: forgetting', '. Sources de fuite courantes : oublier'),
    'or': ('or', 'ou'),
    'to a': ('to a', 'vers un'),
    '→': ('→', '→'),
    '1.': ('1.', '1.'),
    '2.': ('2.', '2.'),
    '3.': ('3.', '3.'),
    '→  → ,  → return 3.': ('→  → ,  → return 3.', '→  → ,  → renvoie 3.'),
    'best for:': ('best for:', 'idéal pour:'),

    # ── Title and misc ──
    'Phase 2:  — the optimal seed': ('Phase 2:  — the optimal seed', 'Phase 2 :  — la graine optimale'),
    'checks in': ('checks in', 'vérifie dans'),
    'No pathological worst case': ('No pathological worst case', 'Pas de pire cas pathologique'),
    'Top NAV': ('Top NAV', 'Top NAV'),
    'Stat counters': ('Stat counters', 'Compteurs de stats'),
    'Sticky TOC': ('Sticky TOC', 'TOC collant'),
    'Main column': ('Main column', 'Colonne principale'),
    'Left: Stacks visualization': ('Left: Stacks visualization', 'Gauche : Visualisation des piles'),
    'Right: Controls': ('Right: Controls', 'Droite : Contrôles'),
    'Bottom: Live Cost Calculations': ('Bottom: Live Cost Calculations', 'Bas : Calculs de coût en temps réel'),
}

# ─────────────────────────────────────────────────────────────────────────────
# PROCESSING
# ─────────────────────────────────────────────────────────────────────────────

SKIP_TAGS = {'script', 'style', 'pre', 'svg'}

def has_real_direct_text(el):
    """Check if element has non-whitespace, non-comment direct text."""
    for child in el.children:
        if isinstance(child, Comment):
            continue
        if isinstance(child, NavigableString) and child.strip():
            return True
    return False

def has_element_children(el):
    for child in el.children:
        if not isinstance(child, NavigableString) and not isinstance(child, Comment):
            return True
    return False

def translate_text_node(text):
    """Translate a single text node string. Returns (en, fr) or None."""
    stripped = text.strip()
    if not stripped:
        return None
    if stripped in TRANSLATIONS:
        return TRANSLATIONS[stripped]
    return None

def translate_inner_html(html_str):
    """Translate text nodes within an HTML string, keeping tags intact.
    Returns (en_html, fr_html) or None if no translation found."""
    soup = BeautifulSoup(html_str, 'html.parser')
    found_any = False
    for string in list(soup.find_all(string=True)):
        if isinstance(string, Comment):
            continue
        stripped = string.strip()
        if not stripped:
            continue
        if stripped in TRANSLATIONS:
            en_val, fr_val = TRANSLATIONS[stripped]
            # Preserve leading/trailing whitespace
            lead = len(string) - len(string.lstrip())
            trail = len(string) - len(string.rstrip())
            # We'll build both en and fr versions by replacing text nodes
            # For now, mark that we found a translation
            found_any = True
    if not found_any:
        return None
    
    # Build EN version (original) and FR version
    en_soup = BeautifulSoup(html_str, 'html.parser')
    fr_soup = BeautifulSoup(html_str, 'html.parser')
    
    for en_str, fr_str in zip(en_soup.find_all(string=True), fr_soup.find_all(string=True)):
        if isinstance(en_str, Comment) or isinstance(fr_str, Comment):
            continue
        stripped = en_str.strip()
        if not stripped:
            continue
        if stripped in TRANSLATIONS:
            en_val, fr_val = TRANSLATIONS[stripped]
            lead = len(en_str) - len(en_str.lstrip())
            trail = len(en_str) - len(en_str.rstrip())
            # EN version: use en_val
            en_replacement = en_val
            if lead:
                en_replacement = en_str[:lead] + en_replacement
            if trail:
                en_replacement = en_replacement + en_str[-trail:]
            en_str.replace_with(NavigableString(en_replacement))
            # FR version: use fr_val
            fr_replacement = fr_val
            if lead:
                fr_replacement = fr_str[:lead] + fr_replacement
            if trail:
                fr_replacement = fr_replacement + fr_str[-trail:]
            fr_str.replace_with(NavigableString(fr_replacement))
    
    return (str(en_soup), str(fr_soup))

def process_element(el):
    """Process an element, adding data-en/data-fr if it has translatable text."""
    if el.name in SKIP_TAGS:
        return
    if el.find_parent('pre'):
        return
    if el.get('data-fr'):  # already has translation
        return
    
    if not has_real_direct_text(el):
        return
    
    has_children = has_element_children(el)
    
    if not has_children:
        # Leaf text element
        text = el.get_text()
        stripped = text.strip()
        if stripped in TRANSLATIONS:
            en_val, fr_val = TRANSLATIONS[stripped]
            el['data-en'] = en_val
            el['data-fr'] = fr_val
        else:
            # No translation found - set data-en = data-fr = original (safe default)
            # This ensures setLang doesn't break anything
            pass  # skip - leave untranslated
    else:
        # Mixed content element
        inner_html = el.decode_contents()
        result = translate_inner_html(inner_html)
        if result:
            en_html, fr_html = result
            el['data-en'] = en_html
            el['data-fr'] = fr_html

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Process all elements
for el in soup.find_all(True):
    process_element(el)

# Replace the old JS translation system with the new one
# Find and remove the old <script> block with FR_TRANSLATIONS
old_js_start = html.find('<script>\n// Language switching system')
if old_js_start == -1:
    old_js_start = html.find('<script>\n// Language switching')

old_js_end = html.find('</script>', old_js_start) + len('</script>')

new_js = '''<script>
function setLang(lang) {
    document.body.classList.toggle('lang-fr', lang === 'fr');
    document.getElementById('langEN').classList.toggle('active', lang === 'en');
    document.getElementById('langFR').classList.toggle('active', lang === 'fr');
    localStorage.setItem('ps-lang', lang);
    document.querySelectorAll('[data-fr]').forEach(el => {
        const en = el.getAttribute('data-en');
        const fr = el.getAttribute('data-fr');
        if (lang === 'fr' && fr) el.innerHTML = fr;
        else if (en) el.innerHTML = en;
    });
    document.title = lang === 'fr'
        ? 'push_swap — Guide de Référence, Algorithme & CI/CD (École 42)'
        : 'push_swap — Reference Guide, Algorithm & CI/CD (École 42)';
}
(function(){const s=localStorage.getItem('ps-lang')||'en';if(s==='fr')setLang('fr');})();
</script>'''

# Get the modified HTML from soup
modified_html = str(soup)

# Now replace the old JS in the modified HTML
# The soup may have reformatted things slightly, so let's find the script block
# by its content marker
import re as _re

# Pattern to match the old language switching script block
old_js_pattern = _re.compile(
    r'<script>\s*//\s*Language switching system.*?</script>',
    _re.DOTALL
)

modified_html = old_js_pattern.sub(new_js, modified_html)

# Also update the <title> tag's lang attribute
modified_html = modified_html.replace('<html lang="en"', '<html lang="en"')

# Write the output
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(modified_html)

print("Translation complete!")
print(f"Total translations in dictionary: {len(TRANSLATIONS)}")

# Count how many elements got data-fr
count = modified_html.count('data-fr=')
print(f"Total data-fr attributes added: {count}")
