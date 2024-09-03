# Entrega 3

## Correcciones de la Entrega 2

1. Se realizó un cambio en los `CLOSE` de los tokens, ya que algunos no cerraban correctamente.

    - Código anterior:

    ```python
    t_CLOSE_HEALTH_TOPICS = r'\<\/health-topics\>'
    ```

    - Código nuevo implementado:

    ```python
    def t_CLOSE_HEALTH_TOPICS(t):
        r'</health-topics>'
        return t
    ```

2. Se utilizó una expresión regular para el URL.

    - Código anterior:

    ```python
    def t_OPEN_PRIMARY_INSTITUTE(t):
        r'\<primary-institute url="([^"]+)"\>'
        t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
        t.value = re.sub(r'\s+', ' ', t.value).strip()
        return t
    ```

    - Código nuevo implementado:

    ```python
    def t_URL(t):
        r'url="([a-z]+\:\/\/)?(www\.)?((\w|-)+\.[^ <>]+)"'
        t.value = t.value.split('=')[1].strip('"')
        return t
    ```

3. Se separaron los atributos dentro de los tokens para obtener un mejor análsis léxico.

    - Código anterior:

    ```python
    Para esta línea del `XML`: <health-topics total="2044" date-generated="08/10/2024 02:30:32">

    def t_OPEN_HEALTH_TOPICS(t):
        r'\<health-topics total="(\d+)" date-generated="(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})"\>'
        t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
        t.value = re.sub(r'\s+', ' ', t.value).strip()
        return t
    
    t_CLOSE_HEALTH_TOPICS = r'\<\/health-topics\>'
    ```

    - Código nuevo implementado:

    ```python
    Para esta línea del `XML`: <health-topics total="2044" date-generated="08/10/2024 02:30:32">

    def t_OPEN_HEALTH_TOPICS(t):
        r'<health-topics'
        return t

    def t_TOPICS_TOTAL(t):
        r'total="(\d+)"'
        t.value = int(t.value.split('=')[1].strip('"'))
        return t

    def t_DATE_GENERATED(t):
        r'date-generated="/(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0,1,2])\/(19|20)\d{2} \d{2}:\d{2}:\d{2}"'
        t.value = t.value.split('=')[1].strip('"')
        return t

    def t_CLOSE_HEALTH_TOPICS(t):
        r'</health-topics>'
        return t
    ```

4. En el documento `XML` hay una línea con un `<p>` erróneo:

    ```python
    <p. class="">NIH: National Institute on Aging<p></p></p.></full-summary>
    ```

    Se modificó a la siguiente línea para controlar el error y no perder la información:

    ```python
    <p>NIH: National Institute on Aging</p></full-summary>
    ```

5. En vez de imprimir los tokens y su contenido en la terminal, se guardan en un `.txt` para leer los resultados con más facilidad.
