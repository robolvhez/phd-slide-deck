import re

with open('slides/methods.tex', 'r') as f:
    tex = f.read()

# Extract SNIPAR frame
snipar_match = re.search(r'(% ============================================================\n% Flujo de trabajo de SNIPAR\n% ============================================================\n\\begin\{frame\}\[c, fragile\]\{Flujo de trabajo de SNIPAR\}[\s\S]*?\\end\{frame\}\n)', tex)

if snipar_match:
    snipar_block = snipar_match.group(1)
    # Remove from original location
    tex = tex.replace(snipar_block, '')
    
    # Insert before Escalamiento incremental
    target = r'(% ---- Option C: Cascading Incremental ----\n% ponytail: plain TikZ, no # args, hardcoded positions\n\\begin\{frame\}\[b\]\{Diseño experimental: Escalamiento incremental\})'
    tex = re.sub(target, snipar_block + r'\n' + r'\1', tex)
    
    with open('slides/methods.tex', 'w') as f:
        f.write(tex)
    print("Updated methods.tex")
else:
    print("Could not find SNIPAR in methods.tex")

with open('guion-examen-candidatura.md', 'r') as f:
    md = f.read()

# Extract SNIPAR from guion
snipar_guion_match = re.search(r'---\n\n## SLIDE \d+ — "Flujo de trabajo de SNIPAR \(Estimador Robusto\)"\n\n\*\*\\\[Contenido visual\\\]:\*\* Diagrama de bloques del módulo SNIPAR en color rojo \(IBD, Imputación, Estimador\)\.\n\n\*\*Guion:\*\*\n\n> Finalmente, ¿qué le hacemos a la cohorte de individuos emparentados\? Aquí utilizamos el módulo de SNIPAR\.\n> Primero, inferimos los segmentos idénticos por descendencia \(IBD\) entre hermanos\. Luego, usamos esa información para imputar los genotipos parentales faltantes\.\n> Esta imputación Mendeliana es la clave que permite a nuestro estimador robusto aislar el efecto genético directo, eliminando por completo cualquier estratificación poblacional residual\.\n\n⏱️ \*\~50 segundos\*\n\n', md)

if snipar_guion_match:
    snipar_guion_block = snipar_guion_match.group(0)
    md = md.replace(snipar_guion_block, '')
    
    # Update title in block to SLIDE 18
    snipar_guion_block_new = snipar_guion_block.replace('## SLIDE 23', '## SLIDE 18')
    
    target_md = '---\n\n## SLIDE 18 — "Diseño experimental: Escalamiento incremental"'
    md = md.replace(target_md, snipar_guion_block_new + '---\n\n## SLIDE 19 — "Diseño experimental: Escalamiento incremental"')
    
    # Now increment subsequent slides manually
    # 19 -> 20
    md = md.replace('## SLIDE 19 — "Datos de entrada: Fenotipos"', '## SLIDE 20 — "Datos de entrada: Fenotipos"')
    # 20 -> 21
    md = md.replace('## SLIDE 20 — "Selección de cohortes"', '## SLIDE 21 — "Selección de cohortes"')
    # 21 -> 22
    md = md.replace('## SLIDE 21 — "Partición de la cohorte"', '## SLIDE 22 — "Partición de la cohorte"')
    # old 23 Tamaños Efectivos stays 23, so we are synced!
    
    with open('guion-examen-candidatura.md', 'w') as f:
        f.write(md)
    print("Updated guion-examen-candidatura.md")
else:
    print("Could not find SNIPAR in guion-examen-candidatura.md")

