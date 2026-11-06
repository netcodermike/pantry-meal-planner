"""Offline pantry inventory and recipe matching, with a Tkinter interface."""
import json
from pathlib import Path
import tempfile
import os

DEFAULT_RECIPES = [
    {'name': 'Tomato pasta', 'ingredients': ['pasta', 'tomato', 'olive oil']},
    {'name': 'Bean rice bowl', 'ingredients': ['rice', 'beans', 'onion']},
    {'name': 'Garden omelette', 'ingredients': ['egg', 'spinach', 'cheese']},
    {'name': 'Apple oats', 'ingredients': ['oats', 'apple', 'milk']},
    {'name': 'Chickpea salad', 'ingredients': ['chickpea', 'tomato', 'cucumber']},
]

def normalize(value):
    return value.strip().casefold()

def rank_recipes(pantry, recipes):
    available = {normalize(x) for x in pantry}
    ranked = []
    for recipe in recipes:
        ingredients = {normalize(x) for x in recipe['ingredients']}
        missing = sorted(ingredients - available)
        ranked.append((recipe['name'], missing, len(ingredients & available)))
    return sorted(ranked, key=lambda row: (len(row[1]), -row[2], row[0]))

def validate(data):
    if not isinstance(data, dict) or not isinstance(data.get('pantry'), list) or not isinstance(data.get('recipes'), list):
        raise ValueError('Expected pantry and recipes lists')
    if not all(isinstance(x, str) and normalize(x) for x in data['pantry']):
        raise ValueError('Pantry entries must be nonempty text')
    for r in data['recipes']:
        if not isinstance(r, dict) or not isinstance(r.get('name'), str) or not r['name'].strip() or not isinstance(r.get('ingredients'), list) or not r['ingredients'] or not all(isinstance(i, str) and normalize(i) for i in r['ingredients']):
            raise ValueError('Each recipe needs a name and a nonempty ingredients list')
    return data

def save(path, data):
    validate(data)
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)

def launch(path):
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, simpledialog
    path = Path(path)
    data = validate(json.loads(path.read_text(encoding='utf-8'))) if path.exists() else {'pantry': [], 'recipes': DEFAULT_RECIPES}
    root = tk.Tk(); root.title('Pantry Meal Planner'); root.geometry('860x600')
    main = ttk.Frame(root, padding=20); main.pack(fill='both', expand=True)
    ttk.Label(main, text='What can you cook?', font=('Segoe UI', 24)).pack(anchor='w')
    ttk.Label(main, text='Add ingredients you have. Select meals to collect a shopping list.').pack(anchor='w', pady=10)
    row = ttk.Frame(main); row.pack(fill='x')
    ingredient = ttk.Entry(row); ingredient.pack(side='left', fill='x', expand=True)
    pantry_list = tk.Listbox(main, height=5); pantry_list.pack(fill='x', pady=10)
    meals = tk.Listbox(main, selectmode='extended', exportselection=False); meals.pack(fill='both', expand=True)
    ranked = []
    def refresh():
        nonlocal ranked
        pantry_list.delete(0, 'end')
        for item in sorted(data['pantry']): pantry_list.insert('end', item)
        ranked = rank_recipes(data['pantry'], data['recipes']); meals.delete(0, 'end')
        for name, missing, hits in ranked:
            meals.insert('end', f'{name} — '+('ready to cook' if not missing else 'need: '+', '.join(missing)))
    def persist():
        try: save(path, data); refresh()
        except (OSError, ValueError) as e: messagebox.showerror('Save failed', str(e))
    def add():
        value = normalize(ingredient.get())
        if value and value not in data['pantry']: data['pantry'].append(value); persist()
        ingredient.delete(0, 'end')
    def remove():
        selected = [pantry_list.get(i) for i in pantry_list.curselection()]
        data['pantry'] = [x for x in data['pantry'] if x not in selected]; persist()
    def recipe():
        name = simpledialog.askstring('New recipe', 'Recipe name:', parent=root)
        if not name or not name.strip(): return
        raw = simpledialog.askstring('Ingredients', 'Comma-separated ingredients:', parent=root)
        if not raw: return
        values = sorted({normalize(x) for x in raw.split(',') if normalize(x)})
        if values: data['recipes'].append({'name': name.strip(), 'ingredients': values}); persist()
    def shopping():
        selected = meals.curselection()
        if not selected: messagebox.showinfo('Choose meals', 'Select one or more meals first.'); return
        items = sorted({item for i in selected for item in ranked[i][1]})
        destination = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text', '*.txt')])
        if destination:
            try: Path(destination).write_text('\n'.join(items)+'\n', encoding='utf-8')
            except OSError as e: messagebox.showerror('Export failed', str(e))
    ttk.Button(row, text='Add ingredient', command=add).pack(side='right')
    controls = ttk.Frame(main); controls.pack(fill='x', pady=12)
    for label, command in [('Remove selected ingredient', remove), ('Add recipe', recipe), ('Export shopping list', shopping)]:
        ttk.Button(controls, text=label, command=command).pack(side='left', padx=4)
    ingredient.bind('<Return>', lambda e: add()); refresh(); root.mainloop()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', default='pantry.json'); args = parser.parse_args()
    try: launch(args.store)
    except (OSError, ValueError, json.JSONDecodeError) as e: parser.exit(1, f'Cannot open pantry: {e}\n')
