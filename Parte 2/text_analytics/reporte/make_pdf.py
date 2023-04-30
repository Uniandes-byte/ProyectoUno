from fpdf import FPDF 
from joblib import load
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def texto(pdf, sizeFont, text, aligment, font):
    pdf.set_font("Times", font, size=sizeFont)

    # Inicio
    return pdf.multi_cell(w=190, ln=1, txt=text, border=0, align=aligment)

def make_df(model):
    df_new = pd.DataFrame(model.get_params().keys(), columns=['Parameters'])
    df_new['Values'] = model.get_params().values()
    df_new = df_new.applymap(str)
    return df_new

def score_(modelo):
    sol = None
    if (modelo == 'MultinomialNB'):
        sol = '0.8334489937543372'
    elif (modelo == 'LogisticRegression'):
        sol = '0.8487161693268563'
    else:
        sol = '0.8501040943789036'
    return sol

def imagenes(modelo):
    sol = None
    if (modelo == 'MultinomialNB'):
        sol = 'static/images/multinomial.png'
    elif (modelo == 'LogisticRegression'):
        sol = 'static/images/linear_regresion.png'
    else:
        sol = 'static/images/red_neuronal.png'
    return sol

def formato_grafica(ax, titulo, ejex, ejey, leyenda=False, xlim=[None, None], ylim=[None, None]):
    plt.rcParams['axes.axisbelow'] = True

    ax.set_title(titulo, fontsize=12)
    ax.set_ylabel(ejey, fontsize=10)
    ax.set_xlabel(ejex, fontsize=10)

    plt.tick_params(direction='out', length=5, width=0.75, grid_alpha=0.3)
    plt.xticks(rotation=0)
    plt.minorticks_on()
    plt.ylim(ylim[0], ylim[1])
    plt.xlim(xlim[0], xlim[1])
    ax.grid(True)
    ax.grid(visible=True, which='major', color='grey', linestyle='-')
    ax.grid(visible=True, which='minor',
            color='lightgrey', linestyle='-', alpha=0.2)

    if leyenda == True:
        plt.legend(loc='best')

    plt.tight_layout()


def generacion_pdf(modelo_,_modelo, data_pdf, resultado):
    # variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    sizefont = 15
    font = 'B'
    # Inicio

    texto(pdf, sizefont, 'Departamento de Ingeniería de Sistemas y Computación', 'L', font)
    texto(pdf, sizefont, 'ISIS 3301  Inteligencia de Negocios', 'L', font)
    texto(pdf, sizefont, 'Proyecto Analítica de textos', 'L', font)
    texto(pdf, sizefont, '', 'L', font)
    texto(pdf, 20, 'Reporte de los datos suministrados', 'C', font)

    # Introducción
    sizefont = 12
    font = ''
    texto(pdf, sizefont, '', 'L',  font)
    texto(pdf, sizefont, 'El siguiente reporte presenta los resultados utilizando el modelo {}, el contenido de este se muestra a continuación:'.format(
        modelo_), 'J', font)
    texto(pdf, 3, '', 'L',  font)
    texto(pdf, sizefont, '      1. Información de los datos', 'L', font)
    texto(pdf, sizefont, '      2. Steps con los parámetros del pipeline', 'L', font)
    texto(pdf, sizefont, '      3. Puntuación del modelo', 'L', font)
    texto(pdf, sizefont, '      4. Gráficas representativa del modelo', 'L', font)
    texto(pdf, sizefont, '      5. Gráfica de las reseñas', 'L', font)

    # Primer item
    texto(pdf, 10, '', 'L',  font)
    texto(pdf, 14, '1. Información de los datos', 'L',  'B')
    texto(pdf, sizefont, 'Se encontraron {} Filas y {} Columnas, junto con {} idiomas, los cuales fueron {}.'.format(data_pdf['filas'], data_pdf['columnas'], len(data_pdf['idiomas']), data_pdf['idiomas']) +
          'El conjunto de datos suministrado además contenía {} nulos y {} duplicados.'.format(data_pdf['nulos'], data_pdf['duplicados']), 'J',  font)
    # Segundo item
    texto(pdf, 10, '', 'L',  font)
    texto(pdf, 14, '2. Steps pipeline', 'L',  'B')

    filename = _modelo  # Prámetro
    print(_modelo)
    model = load(filename)
    if (filename == "static/pipelines/pipeline_neuronalNetwork.joblib"):
        model = model.named_steps['kerasclassifier']
    df_new = make_df(model)
    df_new = df_new.values.tolist()
    df_new[0][0] = 'Parameters'
    df_new[0][1] = 'Values'
    pdf.set_font("Times", '', size=12)
    with pdf.table(cell_fill_color=(247, 247, 247), cell_fill_mode="ROWS", borders_layout="MINIMAL") as table:
        for data_row in df_new:
            row = table.row()
            for datum in data_row:
                row.cell(datum, style='')

    # Tercer item
    texto(pdf, 20, '', 'L',  'B')
    texto(pdf, 14, '3. Puntuación del modelo', 'L',  'B')
    texto(pdf, sizefont, 'Con los datos de entrenamiento se encontró un score de: ' +
          score_(modelo_), 'L', font)

    # Cuarto item
    texto(pdf, 20, '', 'L',  'B')
    texto(pdf, 14, '4. Gráficas representativa del modelo', 'L',  'B')

    pdf.image(imagenes(modelo_), w=190)  # Modelo

    # Cuarto item
    texto(pdf, 20, '', 'L',  'B')
    texto(pdf, 14, '5. Gráfica de las reseñas', 'L',  'B')

    df_sol = pd.read_csv(resultado)

    tipo = df_sol['Sentimiento'].value_counts().keys().tolist()
    valor = df_sol['Sentimiento'].value_counts().tolist()

    fig, ax = plt.subplots()
    ax.bar(tipo, valor)
    formato_grafica(ax, 'Clasificación de Reseñas',
                    'Clasificación', 'Cantidad')
    canvas = FigureCanvas(fig)
    canvas.draw()
    img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
    pdf.image(img,  w=pdf.epw/2, x=pdf.epw/4)  # Make the image full width
    pdf.output('static/results/reporte.pdf')