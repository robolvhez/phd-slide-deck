import sys

with open('guion-examen-candidatura.md', 'r') as f:
    md = f.read()

# The SNIPAR block to extract
snipar_block = """---

## SLIDE 23 — "Flujo de trabajo de SNIPAR (Estimador Robusto)"

**\\[Contenido visual\\]:** Diagrama de bloques del módulo SNIPAR en color rojo (IBD, Imputación, Estimador).

**Guion:**

> Finalmente, ¿qué le hacemos a la cohorte de individuos emparentados? Aquí utilizamos el módulo de SNIPAR.
> Primero, inferimos los segmentos idénticos por descendencia (IBD) entre hermanos. Luego, usamos esa información para imputar los genotipos parentales faltantes.
> Esta imputación Mendeliana es la clave que permite a nuestro estimador robusto aislar el efecto genético directo, eliminando por completo cualquier estratificación poblacional residual.

⏱️ *\\~50 segundos*

"""

if snipar_block not in md:
    print("Could not find SNIPAR block")
    sys.exit(1)

# Remove the block from its current location
md = md.replace(snipar_block, "")

# The text to insert before
target = """---

## SLIDE 18 — "Diseño experimental: Escalamiento incremental\""""

if target not in md:
    print("Could not find target SLIDE 18")
    sys.exit(1)

# Modify SNIPAR title to SLIDE 18
snipar_block_renamed = snipar_block.replace("SLIDE 23", "SLIDE 18")

# Modify target to SLIDE 19
target_renamed = target.replace("SLIDE 18", "SLIDE 19")

# Insert
md = md.replace(target, snipar_block_renamed + target_renamed)

# Renumber subsequent slides up to 22
md = md.replace('## SLIDE 19 — "Datos de entrada: Fenotipos"', '## SLIDE 20 — "Datos de entrada: Fenotipos"')
md = md.replace('## SLIDE 20 — "Selección de cohortes"', '## SLIDE 21 — "Selección de cohortes"')
md = md.replace('## SLIDE 21 — "Partición de la cohorte"', '## SLIDE 22 — "Partición de la cohorte"')

with open('guion-examen-candidatura.md', 'w') as f:
    f.write(md)

print("guion updated successfully")
