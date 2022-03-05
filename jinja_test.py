from jinja2 import Template

cities = [{"id": 1, "city": "Москва"},
          {"id": 5, "city": "Тверь"},
          {"id": 7, "city": "Минск"},
          {"id": 8, "city": "Смоленск"},
          {"id": 11, "city": "Калуга"}]

link = '''<select name="cities">
{% for c in cities -%}
{% if c.id > 5 -%}
    <option value="{{c['id']}}">{{c['city']}}</option>
{% else -%}
    <option>{{ c["city"] }}</option>    
{% endif -%}
{% endfor -%}
</select>'''

tm = Template(link)
msg = tm.render(cities=cities)
print(msg)

cars = [
    {"model": "Ауди", "price": 23000},
    {"model": "Шкода", "price": 17300},
    {"model": "Вольво", "price": 43300},
    {"model": "Фольксваген", "price": 21300},
]

temp = '''
    {% macro input(name, value='', type='text', size=20) -%}
        <input type='{{ type }}' name='{{ name }}' value='{{ value|e }}' size = '{{ size }}'>  
    {%- endmacro %}
    
    <p>{{ input('username') }}
    <p>{{ input('email') }}
    <p>{{ input('password') }}
    
    
    '''
tm = Template(temp)
msg = tm.render(cs=cars)
print(msg)

