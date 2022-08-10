import jedi

code_path = "/home/haruan/Projects/astrologia/mapa_astral/views.py"
with open(code_path) as code_file:
    code = code_file.read()

script = jedi.Script(code, path=code_path)
names = script.get_names()

for name in names:
    print(name.goto(follow_imports=True)[0].module_path)
