# Module 01 — Object-Oriented Garden Systems

## Objetivo do Módulo

Construir um sistema de gestão de jardim usando programação orientada a objetos. Evolui de um script simples (ex00) até uma hierarquia completa com classes aninhadas, herança múltipla indireta (via Seed → Flower → Plant), static/class methods, encapsulamento e pattern matching.

## Conceitos-Chave

### `if __name__ == "__main__":` — O Ponto de Entrada

Quando Python executa um arquivo, define `__name__` como `"__main__"`. Quando o mesmo arquivo é importado, `__name__` vira o nome do módulo. O guard `if __name__ == "__main__":` permite que o mesmo arquivo sirva como script **e** como módulo importável.

No subject, ex00 introduz esse padrão como novidade (depois de ter sido proibido no module_00). A mudança sinaliza que agora os exercícios podem ter código executável além da definição de funções.

**Bytecode**: o guard compila para LOAD_NAME + COMPARE_OP + POP_JUMP_IF_FALSE — se `__name__ != "__main__"`, pula todo o bloco.

**Shebang** (`#!/usr/bin/env python3`): o subject pergunta sobre isso na avaliação. O kernel do Linux usa o shebang para identificar o interpretador. `chmod +x` + shebang permite executar `./script.py` sem prefixar `python3`.

### Classes e Objetos (PEP 3115)

Uma classe `class Plant:` é um bloco que executa em um namespace separado (a metaclasse `type` cria o objeto classe). O `class` body vira um dicionário, que vira o `__dict__` da classe. Métodos são funções armazenadas no `__dict__` da classe — o **descriptor protocol** (`__get__`) transforma funções em bound methods no acesso via instância.

`__init__` **não é o construtor**. O construtor real é `__new__` (aloca memória). `__init__` é o inicializador — recebe a instância já criada e configura atributos. Chamar `Plant("Rose", 25, 30)`:
1. `type.__call__(Plant, "Rose", 25, 30)` é invocado
2. `Plant.__new__(Plant, ...)` aloca a instância (retorna `self`)
3. `Plant.__init__(self, "Rose", 25, 30)` inicializa

### `__init__` com Parâmetros Padrão

```python
def __init__(self, name="plant", height=0, ages=0, growth=1):
```

Parâmetros padrão são avaliados **uma vez** em tempo de definição da função — não por chamada. Para valores mutáveis (listas, dicts), isso causa compartilhamento indesejado. Aqui todos são imutáveis, então não há problema.

O código existente usa `growth` como parâmetro de `__init__` (ex02+). Plantas diferentes crescem a taxas diferentes — isso é uma boa abstração.

### Atributos de Instância

Atributos são armazenados no `__dict__` da instância (dicionário). Cada instância tem seu próprio `__dict__`. Acesso a `self.height`:
1. Busca em `instance.__dict__['height']` — se achar, retorna
2. Se não achar, busca em `type(self).__dict__['height']` (classe)
3. Se encontrado na classe e tiver `__get__` (descriptor), chama descriptor
4. Se não achar, sobe na MRO

**Slots** (PEP 412): `__slots__` substitui `__dict__` por um array de acesso O(1), economizando memória. Mas o subject não cobriu slots.

### Métodos — `self` Explícito

Diferente de C++/Java, Python exige `self` como primeiro parâmetro. `self` não é uma palavra-chave — pode ser qualquer nome (mas `self` é convenção universal).

`plant.show()` traduz para `Plant.show(plant)`. O mecanismo é o **descriptor protocol**: `Plant.__dict__['show'].__get__(plant, Plant)` retorna um bound method que insere `plant` como primeiro argumento.

### Encapsulamento — Protected Convention (`_attr`)

Python não tem modificadores de acesso (`private`, `protected`, `public`). As convenções:
- `_attr` (single underscore) — **protected**: sinaliza "internal use, not part of the public API". Acessível de fora, mas por convenção não deve ser.
- `__attr` (double underscore) — **name mangling**: o interpretador renomeia para `_ClassName__attr` em tempo de compilação. Existe para evitar conflitos em hierarquias de herança múltipla, **não para privacidade**.

O subject do ex04 diz explicitamente: **"use the protected convention (not the mangling)"**. A razão: name mangling dificulta acesso em subclasses. Se `Plant.__height` vira `_Plant__height`, `Tree` (subclasse) não consegue acessar `self.__height` (que viraria `_Tree__height`). Com `_height`, subclasses acessam diretamente.

**Código corrigido**: ex04, ex05, ex06 usavam `__height`, `__name`, `__ages`, `__growth` → convertidos para `_height`, `_name`, `_ages`, `_growth`.

Ainda assim, acessar `plant._height` funciona — a "proteção" é apenas documental.

### Getters / Setters

```python
def set_height(self, height: float) -> None:
    if height < 0:
        print(f"{self._name}: Error, height can't be negative")
        return
    self._height = height

def get_height(self) -> float:
    return self._height
```

Esse padrão (Java-style) é **não-idiomático** em Python. O idioma Python usa `@property`:

```python
@property
def height(self) -> float:
    return self._height

@height.setter
def height(self, value: float) -> None:
    if value < 0:
        raise ValueError("Height can't be negative")
    self._height = value
```

**Por que o subject ensina getters/setters em vez de `@property`?** Para introduzir o conceito de encapsulamento antes da syntactic sugar. A avaliação pode perguntar a diferença.

### Herança e MRO (C3 Linearization)

```python
class Flower(Plant):
    def __init__(self, ..., color="Red"):
        super().__init__(name, height, ages, growth)
```

Python usa **C3 linearization** (PEP 559) para determinar a Method Resolution Order. Para herança simples, é trivial: `Flower → Plant → object`. `super()` delega ao **próximo na MRO** — não ao "pai". Isso faz diferença em herança múltipla (diamante).

`super().__init__()` é chamado para reusar a lógica de inicialização da classe pai. Sem ele, atributos definidos em `Plant.__init__()` não seriam criados.

A chamada a `super().__init__()` deve estar no início de `__init__` da subclasse (para que atributos pai existam antes de a subclasse tocá-los).

### Sobrescrita de Métodos (Override)

`Flower.show()` sobrescreve `Plant.show()`. O dispatch é dinâmico — `super().show()` no código existente é incorreto porque `super()` em `Flower.show()` chamaria `Plant.show()`, não `Flower.show()`. O padrão correto:

```python
def show(self) -> str:
    base = super().show()  # chama Plant.show()
    return f"{base}\nColor: {self._color}"
```

Mas no código do ex05, `Flower.show()` **não chama `super().show()`** — constrói a string do zero. Isso duplica a lógica de formatação da base. Uma alternativa melhor seria:

```python
def show(self) -> str:
    return f"{super().show()}\nColor: {self._color}"
```

### `super()` e Herança em Cadeia

`super()` sem argumentos (Python 3+) equivale a `super(__class__, self)`. A variável `__class__` é uma referência implícita inserida pelo compilador em métodos. O objeto `super` resultante faz uma busca na MRO a partir da classe seguinte.

### Hierarquia do Código Existente

```
Plant (base)
├── Flower
│   └── Seed (ex06)
├── Tree
│   (Plant._Stats → Tree._TreeStats)
└── Vegetable
```

`Seed(Flower)` demonstra herança de segundo nível. `Seed.bloom()` chama `super().bloom()` (que executa `Flower.bloom()`) e depois adiciona seeds. Isso é um bom exemplo de **extensão de comportamento via super**.

### `@staticmethod` vs `@classmethod` vs Método de Instância

| Decorator | Primeiro parâmetro | Acesso ao quê? | Uso típico |
|-----------|-------------------|----------------|------------|
| (nenhum) | `self` | instância | opera no estado do objeto |
| `@classmethod` | `cls` | classe | factory methods alternativos |
| `@staticmethod` | nenhum | nada | função utilitária dentro do namespace da classe |

`@classmethod` recebe a classe como primeiro argumento (`cls`). Útil para **factory methods**:

```python
@classmethod
def create_anonymous(cls) -> "Plant":
    return cls(name="Unknown plant", height=0.0, ages=0, growth=1.0)
```

`create_anonymous` é herdado por subclasses. Se chamado em `Flower.create_anonymous()`, `cls` será `Flower`, e a instância criada será `Flower(name="Unknown plant"... )`.

`@staticmethod` não recebe `self` nem `cls`. É apenas uma função aninhada no namespace da classe.

### Nested Classes (Classes Internas)

```python
class Plant:
    class _Stats:
        def __init__(self):
            self.grow_count = 0
            self.age_count = 0
            self.show_count = 0
```

Classes aninhadas em Python **não são inner classes no sentido Java**. Não há relação entre a instância interna e a externa. `_Stats` é apenas um atributo de `Plant` — um objeto classe armazenado em `Plant.__dict__['_Stats']`. Não tem acesso automático a instâncias de `Plant`.

O objeto `_stats` é uma instância separada: `self._stats = self._Stats()`. Cada planta tem seu próprio contador.

`Tree._TreeStats(Plant._Stats)` estende a nested class, adicionando `shade_count`. Isso é possível porque `_Stats` é uma classe normal — herança funciona.

O subject pede encapsulamento para `_Stats` ("Encapsulation is required"), mas o código atual expõe `self._stats.grow_count` diretamente de dentro dos métodos de `Plant`. O encapsulamento é nominal (prefixed `_`, indicando "não mexa").

### `match` / `case` (Structural Pattern Matching, PEP 634–636)

```python
match plant:
    case Tree():
        plant.produce_shade()
    case Flower():
        plant.bloom()
    case _:
        pass
```

Introduzido no Python 3.10. O `match` testa a **classe** do sujeito usando `isinstance()` internamente. `case Tree():` funciona com a classe, não requer argumentos. Se houvesse atributos para extrair:

```python
case Flower(_, _, color=color):
    # color extraído do atributo
```

**Performance**: `match` compila para uma série de `isinstance()` checks, similar a `if isinstance(...)`. Não há otimização de salto computado como `switch` em C.

O código existente usa `match` com classes personalizadas (`Tree`, `Flower`). Note que a ordem dos `case` importa: primeiro match ganha. `case _:` é o wildcard (default).

## Regras e Restrições do Subject

| Regra | Motivo |
|-------|--------|
| Python 3.10+ | match/case exige 3.10 |
| PascalCase (classes), snake_case (vars/funções) | PEP 8 |
| flake8 + mypy obrigatórios | Verificação rigorosa de tipos e estilo |
| `super()` autorizado (ex05+) | Necessário para herança |
| `@staticmethod`, `@classmethod` autorizados (ex06) | Sintaxe de decorator |
| Protected convention (`_attr`) | Name mangling prejudica herança |
| `if __name__` permitido | Diferença de module_00 |
| Sem validação para novos atributos (ex05) | Simplifica foco em herança |

## Correlação com Exercícios Existentes

### ex00 — ft_garden_intro.py
O único exercício do repositório que **não** define função alguma — é um script puro com `if __name__`. Isso quebra o padrão dos outros módulos onde sempre há `def`. A moulinette pode estranhar. O subject mostra exemplo com variáveis, mas o código atual é hardcoded.

### ex01 — ft_garden_data.py
Define `class Plant` com `__init__` e `show()`. Usa `try/except ValueError` (antecipando module_02). A lógica de interação (`while input("exit/add")`) vai além do subject — que só pede "create and display at least 3 plants".

### ex02 — ft_plant_growth.py
Adiciona `grow()` e `age()` modificando estado. O loop simula 7 dias com `range(7)`. O growth rate (`self.growth`) é configurável por planta — diferente do subject que deixa "implementation up to you".

### ex03 — ft_plant_factory.py
Construtor populado com parâmetros. Cria 5 plantas pré-definidas. Adiciona `total_plants` counter que não está no subject. A interface interativa (exit/add) é idêntica ao ex01/ex02 — padrão copiado entre exercícios.

### ex04 — ft_garden_security.py
**Corrigido**: `__` → `_` (protected convention). Getters/setters com validação de negativos. O subject pede "print error messages from the class when invalid values are provided" — implementado com `print()` em vez de `raise`. Isso é consistente com a filosofia do módulo (ainda sem exceções).

### ex05 — ft_plant_types.py
**Corrigido**: `__` → `_` na base e subclasses. `Flower.show()` **não chama** `super().show()` — duplica a lógica de formatação. `Tree.__init__` reatribui `self._stats` depois de `super().__init__()` — isso sobrescreve o `_Stats` de `Plant` com `_TreeStats`. Funciona, mas poderia ser feito de forma mais elegante com `super().__init__` aceitando a classe de stats.

### ex06 — ft_garden_analytics.py
**Corrigido**: `__` → `_` e loop de 20 iterações em vez de `set_ages(64)`. Implementa `Seed(Flower)`, `_TreeStats(Plant._Stats)`, `@staticmethod is_older_than_year`, `@classmethod create_anonymous`. A função `display_plant_stats` é definida fora de classe — pattern funcional para operações transversais. O subject pede que `Seed.show()` melhore o Flower.show() atual — o código faz isso com `super().show()`.

## Erros Comuns

1. **Name mangling em subclasse**: `self.__attr` na classe pai vira `_Pai__attr`; subclasse que tenta `self.__attr` acessa `_Filho__attr`
2. **Esquecer `super().__init__()`**: atributos do pai nunca criados
3. **`super()` fora de método**: funciona, mas o argumento implícito `__class__` não está disponível
4. **Confundir `@staticmethod` com `@classmethod`**: `@staticmethod` não recebe `cls` — não pode acessar outros métodos de classe
5. **Nested class é apenas namespace**: não tem relação automática com a instância externa
6. **`match/case` com classes sem atributos**: `case Plant():` sempre match (qualquer planta)
7. **Getters/setters sem validação**: subject testa valores negativos

## Perguntas de Autoavaliação

- `super().__init__()` vs `Plant.__init__(self, ...)` — qual a diferença na MRO?
- Se uma subclasse **não** define `__init__`, qual construtor é chamado?
- O que é o descriptor protocol e como ele transforma funções em bound methods?
- `@classmethod` recebe `cls`. Como isso afeta herança?
- Por que o subject proíbe name mangling mas permite protected convention?
- Qual a diferença entre `staticmethod` e uma função definida fora da classe?
- `match` vs `isinstance()` — qual é mais rápido? Quando usar cada um?
- `_Stats` é acessível como `Plant._Stats`. É possível instanciá-la de fora? A protegida?
