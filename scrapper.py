import asyncio
from pyppeteer import launch
import csv

def save_to_csv(lista):
    # Abre un archivo para escribir
    with open('empresas_espana.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Escribe la cabecera
        writer.writerow(['Empresa'])

        # Escribe cada nombre de empresa
        for nombre_empresa in lista:
            writer.writerow([nombre_empresa])

    print("Archivo 'empresas_espana.csv' creado con éxito.")


async def extract_company_names():
    browser = await launch(headless=True)
    page = await browser.newPage()

    # Navega a la página
    await page.goto('https://ecatalogue.firabarcelona.com/AlimentariaHostelco/home?filter=ONLY_EXHIBITORS&lang=es_ES')
    print("entrando a la página")

    # Espera a que se cargue el contenido dinámico inicial
    print("comanzando 4 seg para cargar la página")
    await asyncio.sleep(4)
    print("tiempo! 4 seg")
    print(' ')

    vuelta = 1
    while True:
        print('---')
        print('VUELTA {}'.format(vuelta))
        see_more_button = await page.querySelector('.see_more_button')
        if see_more_button:
            print('boton "See More" encontrado')
            await see_more_button.click()
            print('boton clickeado!')
            print("comenzando 4 seg para cargar nuevas empresas")
            await asyncio.sleep(4)
            print("tiempo! 4 seg. Nuevo contenido en la página")
            vuelta += 1
        else:
            print('No hay más botónes')
            break
    
    # Ahora, extraemos los nombres de las empresas
    print('buscando las empresas con la class asignada')
    company_names = await page.evaluate('''() => {
        let names = [];
        let elements = document.querySelectorAll('.list_parent_item.list .data_block_title.pointer.appColorOnHover');
        for (let element of elements) {
            names.push(element.textContent.trim());
        }
        return names;
    }''')

    await browser.close()
    print('browser cerrado')
    print(' ')
    print('empresas encontradas : {}'.format(len(company_names)))
    return company_names


# Ejecuta la función
names = asyncio.get_event_loop().run_until_complete(extract_company_names())

# for name in names:
#     print(name)

save_to_csv(names)