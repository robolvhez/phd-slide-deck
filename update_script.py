import re

with open('/home/rolvhdez/Documents/repositories/phd-slide-deck/guion-examen-candidatura.md', 'r') as f:
    content = f.read()

# Replace the methodology section (slides 18-21)
# 18: Incremental
# 19: Flujo completo (to be removed)
# 20: Fenotipos
# 21: Genotipos

# The new structure:
# 18: Incremental (updated text)
# 19: Fenotipos
# 20: Genotipos
# 21: Selección de cohortes
# 22: Flujo de trabajo de SNIPAR

new_methods = """## SLIDE 18 — "Diseño experimental: Escalamiento incremental"

**\\[Contenido visual\\]:** Diagrama TikZ de Gantt con 4 semestres (S1--S4) mostrando la progresión incremental del proyecto.

**Guion:**

> El diseño experimental sigue una estrategia de **escalamiento incremental** a lo largo de cuatro semestres.
>
> Es importante destacar que llegar al pipeline final **no fue un logro de la noche a la mañana**. Existió una curva de aprendizaje importante y un proceso iterativo de prueba y error. 
> 
> En el **Semestre 1**, los intentos iniciales y errores procesando el cromosoma 22 y 3 rasgos fueron fundamentales para ajustar las tuercas de los modelos.
>
> En el **Semestre 2** escalamos a datos imputados con TOPMed y establecimos la imputación mendeliana a escala genómica.
>
> En el **Semestre 3** incorporamos el GWAS poblacional e implementamos el estimador robusto.
>
> Y en el **Semestre 4** completaremos el atlas con 28 rasgos y el análisis completo. 
> Esta progresión nos permitió validar cada etapa antes de escalar a genoma completo.

⏱️ *\\~1 minuto 20 segundos*

---

## SLIDE 19 — "Datos de entrada: Fenotipos"

**\\[Contenido visual\\]:** Listas de rasgos conductuales y biomédicos procesados, con diagrama de flujo de scripts.

**Guion:**

> Pasando al flujo de los datos, comenzamos con nuestra materia prima: los fenotipos. Estandarizamos y pre-procesamos múltiples rasgos categorizados en conductuales y biomédicos, incluyendo logro educativo, índice de masa corporal, lípidos y diabetes.
> Esta curación asegura que nuestros rasgos y covariables estén homogeneizados para comparaciones justas.

⏱️ *\\~45 segundos*

---

## SLIDE 20 — "Datos de entrada: Genotipos"

**\\[Contenido visual\\]:** Detalles del control de calidad de genotipos, filtros y proceso de Phased a BGEN.

**Guion:**

> Para completar las entradas del sistema, procesamos los genotipos. Partimos de datos previamente faseados para el chip GSAv2 y la imputación con TOPMed.
> Aplicamos estrictos controles de calidad, como requerir un puntaje INFO mayor a 0.99, porque los modelos familiares son sumamente sensibles a errores de genotipado.

⏱️ *\\~45 segundos*

---

## SLIDE 21 — "Selección de cohortes"

**\\[Contenido visual\\]:** Diagrama de flujo mostrando la partición de la cohorte completa en individuos emparentados y no emparentados usando KING.

**Guion:**

> Una vez que tenemos los datos limpios, procedemos a dividirlos.
> Usando KING para inferencia de parentesco, separamos la muestra en un grupo puramente "no emparentado" para el GWAS poblacional, y otro grupo con "redes familiares" para el análisis familiar (FGWAS).
> Es fundamental que ambos grupos sean **estadísticamente independientes** para poder comparar posteriormente los estimadores de forma justa.

⏱️ *\\~45 segundos*

---

## SLIDE 22 — "Flujo de trabajo de SNIPAR (Estimador Robusto)"

**\\[Contenido visual\\]:** Diagrama de bloques del módulo SNIPAR en color rojo (IBD, Imputación, Estimador).

**Guion:**

> Finalmente, ¿qué le hacemos a la cohorte de individuos emparentados? Aquí utilizamos el módulo de SNIPAR.
> Primero, inferimos los segmentos idénticos por descendencia (IBD) entre hermanos. Luego, usamos esa información para imputar los genotipos parentales faltantes.
> Esta imputación Mendeliana es la clave que permite a nuestro estimador robusto aislar el efecto genético directo, eliminando por completo cualquier estratificación poblacional residual.

⏱️ *\\~50 segundos*

---"""

# Use regex to replace everything from "## SLIDE 18" to just before "## SLIDE 22" (which will become 23)
pattern = r"## SLIDE 18.*?(?=## SLIDE 22)"
content = re.sub(pattern, new_methods + "\n\n", content, flags=re.DOTALL)

# Now increment all slide numbers from 22 onwards by 1
# Find all "## SLIDE X" matches
def increment_slide(match):
    num = int(match.group(1))
    if num >= 22:
        return f"## SLIDE {num + 1}"
    return match.group(0)

content = re.sub(r"## SLIDE (\d+)", increment_slide, content)

with open('/home/rolvhdez/Documents/repositories/phd-slide-deck/guion-examen-candidatura.md', 'w') as f:
    f.write(content)
