
def centrarVentana(root):
    root.update_idletasks()

    # Obtiene dimensiones de la pantalla
    anchoPantalla = root.winfo_screenwidth()
    altoPantalla = root.winfo_screenheight()

    # Obtiene dimensiones de la pantalla
    anchoVentana = root.winfo_width()
    altoVentana = root.winfo_height()

    x = (anchoPantalla / 2) - (anchoVentana / 2)
    y = (altoPantalla / 2) - (altoVentana / 2)

    root.geometry('+%d+%d' % (int(x), int(y)))