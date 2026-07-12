# Module 01 — Object-Oriented Garden Systems (Code Cultivation)

**Ambiente**: Python 3.13.1 | Verificado em: 2026-07-12

## Objetivo do Módulo

Evoluir de scripts simples para OOP: classes, herança, encapsulamento, polimorfismo, static/class methods,
nested classes e pattern matching (`match/case`). O tema "digital garden ecosystem" constrói um sistema
coeso de gerenciamento de plantas, progredindo de uma única classe até uma hierarquia com estatísticas
internas.

## Conceitos-Chave

### `if __name__ == "__main__":` — O Ponto de Entrada

Quando Python executa um arquivo, `__name__` é definido como `"__main__"`. Quando importado, `__name__`
vira o nome do módulo. O guard permite que o mesmo arquivo sirva como script e módulo importável.

O subject do ex00 reintroduz esse padrão (proibido em module_00). A mudança sinaliza que agora os
exercícios podem ter código executável além de definições. O shebang (`#!/usr/bin/env python3`) também
é citado: ele instrui o kernel a usar o interpretador Python para executar o script via `chmod +x`.

### Classes e Objetos (Data Model)

`class Plant:` é um bloco executado em namespace separado pela metaclasse `type`. O corpo da classe
vira `__dict__` da classe. Métodos são funções armazenadas no `__dict__` — o **descriptor protocol**
(`__get__`) transforma funções em bound methods no acesso via instância.

`__init__` **não é o construtor**. O construtor real é `__new__` (aloca memória). `__init__` recebe a
instância já criada e configura atributos. Chamar `Plant("Rose", 25, 30)`:
1. `type.__call__(Plant, "Rose", 25, 30)`
2. `Plant.__new__(Plant, ...)` aloca a instância
3. `Plant.__init__(self, "Rose", 25, 30)` inicializa

**Bytecode real de `Plant.__init__()` (ex01)**:

```
  4           RESUME                   0
  5           LOAD_FAST                1 (name)
              LOAD_FAST                0 (self)
              STORE_ATTR               0 (name)
  6           LOAD_FAST                2 (height)
              LOAD_FAST                0 (self)
              STORE_ATTR               1 (height)
  7           LOAD_FAST                3 (age)
              LOAD_FAST                0 (self)
              STORE_ATTR               2 (age)
              RETURN_CONST             0 (None)
```

- `STORE_ATTR` com nome literal (não mangleado) — name mangling acontece na compilação e já aparece
  com o nome transformado no bytecode
- `RETURN_CONST 0 (None)` — `__init__` não tem `return` explícito, retorna `None`

**Fontes**: https://docs.python.org/3/reference/datamodel.html#object.__init__

### Atributos e Métodos

Atributos de instância são armazenados no `__dict__` da instância. Acesso a `self.height`:
1. Busca em `instance.__dict__` — se achar, retorna
2. Se não, busca no `__dict__` da classe (e sobe na MRO)
3. Se encontrado na classe com `__get__` (descriptor), chama o descriptor

**Bytecode real de `Plant.show()` (ex01)**:

```
  8           RESUME                   0
  9           LOAD_CONST               1 ('')
              LOAD_FAST                0 (self)
              LOAD_ATTR                0 (name)
              FORMAT_SIMPLE
              ...
              BUILD_STRING             4
              RETURN_VALUE
```

### Encapsulamento — Protected vs Name Mangling

Python não tem modificadores de acesso. As convenções:
- `_attr` — **protected**: sinaliza "uso interno". Acessível, mas por convenção não deve ser.
- `__attr` — **name mangling**: o compilador renomeia para `_ClassName__attr`. Existe para evitar
  conflitos em herança múltipla, não para privacidade.

`dir()` em uma instância de `Plant` com `__height` mostra `_Plant__height` — confirmado empiricamente:

```python
class Test:
    def __init__(self):
        self.__secret = 42
t = Test()
print(t._Test__secret)  # 42
```

O subject do ex04 pede **protected convention** (`_attr`), não mangling. Razão: name mangling dificulta
acesso em subclasses (`_Plant__height` vs `_Tree__height`). Código corrigido: todos os `__attr` nos
ex04–ex06 foram convertidos para `_attr`.

**Fontes**: https://docs.python.org/3/tutorial/classes.html#private-variables

### Getters / Setters e `@property`

O código usa getters/setters Java-style (`get_height()`, `set_height()`). O idioma Python é `@property`:

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

O subject introduz getters/setters primeiro para ensinar encapsulamento antes da syntactic sugar.

**Fontes**: https://docs.python.org/3/library/functions.html#property

### Herança e MRO (C3 Linearization)

Python usa **C3 linearization** para MRO. Para herança simples: `Flower → Plant → object`.
`super()` delega ao próximo na MRO. Em herança múltipla (diamante), `super()` garante que cada
classe seja chamada exatamente uma vez.

`super().__init__()` deve ser chamado para reusar a lógica do pai.

**Bytecode real de `Flower.__init__()` (ex05)**:

```
 96           RESUME                   0
104           LOAD_GLOBAL              0 (super)
              LOAD_DEREF               6 (__class__)
              LOAD_FAST                0 (self)
              LOAD_SUPER_ATTR          5 (__init__ + NULL|self)
              LOAD_FAST_LOAD_FAST     18 (name, height)
              LOAD_FAST_LOAD_FAST     52 (ages, growth)
              CALL                     4
              POP_TOP
105           LOAD_CONST               1 ('')
              LOAD_FAST                0 (self)
              STORE_ATTR               2 (_color)
 ...
```

- `LOAD_SUPER_ATTR` (3.12+) — opcode dedicado para `super()`
- A sequência `super()` + `__init__` compila para `LOAD_GLOBAL(super)` + `LOAD_DEREF(__class__)` +
  `LOAD_SUPER_ATTR` + argumentos + `CALL`
- `STORE_ATTR` usa o nome já mangleado (aqui `_color`, não `__color`)

### `super()` e Herança em Cadeia

`super()` sem argumentos equivale a `super(__class__, self)`. A variável `__class__` é inserida
pelo compilador em métodos. O objeto `super` resultante busca na MRO a partir da classe seguinte.

No código existente, `Flower.show()` (ex05) **não chama** `super().show()` — constrói a string do zero,
duplicando a formatação. Um design melhor seria:

```python
def show(self) -> str:
    return f"{super().show()}\nColor: {self._color}"
```

### `@staticmethod` vs `@classmethod` vs Método de Instância

| Decorator | Primeiro parâmetro | Acesso | Uso |
|-----------|-------------------|--------|-----|
| (nenhum) | `self` | instância | opera no estado |
| `@classmethod` | `cls` | classe | factory methods |
| `@staticmethod` | nenhum | nada | utilitária no namespace da classe |

**Bytecode real de `Plant.is_older_than_year()` (staticmethod, ex06)**:

```
 33           RESUME                   0
 34           LOAD_FAST                0 (days)
              LOAD_CONST               1 (365)
              COMPARE_OP             148 (bool(>))
              RETURN_VALUE
```

— não recebe `self` ou `cls`, apenas os argumentos explícitos.

**Bytecode real de `Plant.create_anonymous()` (classmethod, ex06)**:

```
 37           RESUME                   0
 39           LOAD_FAST                0 (cls)
              LOAD_CONST               1 ('Unknown plant')
              LOAD_CONST               2 (0.0)
              LOAD_CONST               3 (0)
              LOAD_CONST               4 (1.0)
              LOAD_CONST               0 (None)
              ...
              CALL                     5
              RETURN_VALUE
```

— `cls` é passado como primeiro argumento. Se chamado em `Flower.create_anonymous()`, `cls` = `Flower`,
e a instância criada será do tipo `Flower`.

### Nested Classes

```python
class Plant:
    class _Stats:
        def __init__(self):
            self.grow_count = 0
```

Classes aninhadas em Python **não** são inner classes (estilo Java). `_Stats` é apenas um atributo
de `Plant` — não tem acesso automático à instância externa.

`Tree._TreeStats(Plant._Stats)` estende a nested class adicionando `shade_count`. O `super()` dentro
de `_TreeStats.display()` chama `Plant._Stats.display()`.

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

`match` usa `isinstance()` internamente. `case Tree():` verifica a classe do sujeito. Ordem importa:
primeiro match ganha. A performance é similar a uma cadeia de `isinstance()` checks.

**Fontes**: https://peps.python.org/pep-0634/

## Regras e Restrições do Subject

| Regra | Motivo |
|-------|--------|
| Python 3.10+ | match/case (PEP 634), type union |
| PascalCase classes / snake_case vars | PEP 8 |
| flake8 + mypy obrigatórios | Type hints verificados |
| `super()` autorizado | Herança |
| `@staticmethod`, `@classmethod` autorizados (ex06) | Decorator syntax |
| Protected convention (`_attr`) | Mangling prejudica herança |
| `if __name__` permitido | Diferença de module_00 |

## Correlação com Exercícios Existentes

### ex00 — ft_garden_intro.py
Único exercício do repositório **sem função** — script puro com `if __name__`. Quebra o padrão.
Valores hardcoded (Rose, 25cm, 30 days). Subject menciona "variáveis simples".

### ex01 — ft_garden_data.py
`class Plant` com `__init__` + `show()`. Tem `try/except ValueError` (antecipando module_02).
Lógica interativa (`exit/add`) vai além do subject.

### ex02 — ft_plant_growth.py
Adiciona `grow()` e `age()`. Simula 7 dias com `range(7)`. Growth rate configurável.

### ex03 — ft_plant_factory.py
Construtor com parâmetros. Cria 5 plantas pré-definidas. Adiciona `total_plants` counter extra.

### ex04 — ft_garden_security.py
**Corrigido**: `__` → `_`. Getters/setters com validação de negativos via `print()` (não `raise`).

### ex05 — ft_plant_types.py
**Corrigido**: `__` → `_` na base e subclasses. `Flower.show()` **não chama** `super().show()` —
duplica lógica de formatação. `Tree.__init__` reatribui `self._stats` — sobrescreve `_Stats` com
`_TreeStats`.

### ex06 — ft_garden_analytics.py
**Corrigido**: `__` → `_` e `set_ages(64)` → `for _ in range(20)`. Implementa `Seed(Flower)`,
`_TreeStats(Plant._Stats)`, `@staticmethod`, `@classmethod`. A função `display_plant_stats` é
definida fora de classe — pattern funcional.

## Erros Comuns

1. Name mangling em subclasse: `__attr` vira `_Pai__attr`, subclasse acessa `_Filho__attr`
2. Esquecer `super().__init__()` — atributos do pai nunca criados
3. `@staticmethod` não recebe `self` nem `cls` — erro comum de assinatura
4. Nested class não tem relação com instância externa
5. `match/case` com `case _:` antes dos específicos — sempre match
6. Getters/setters sem validação — subject testa negativos

## Perguntas de Autoavaliação

- `super().__init__()` vs `Plant.__init__(self, ...)` — diferença na MRO?
- Se uma subclasse não define `__init__`, qual construtor é chamado?
- O que é o descriptor protocol? Como transforma funções em bound methods?
- `@classmethod` recebe `cls`. Como a herança afeta o valor de `cls`?
- Por que o subject pede `_attr` em vez de `__attr`?
- `_Stats` dentro de `Plant` — é possível instanciá-la de fora? A protegida?

## Fontes Consultadas

- https://docs.python.org/3/reference/datamodel.html#object.__init__
- https://docs.python.org/3/tutorial/classes.html#private-variables
- https://docs.python.org/3/library/functions.html#super
- https://docs.python.org/3/library/functions.html#classmethod
- https://docs.python.org/3/library/functions.html#staticmethod
- https://docs.python.org/3/library/functions.html#property
- https://docs.python.org/3/library/dis.html#opcode-LOAD_SUPER_ATTR
- https://docs.python.org/3/whatsnew/3.12.html
- https://docs.python.org/3/reference/compound_stmts.html#class-definitions
- https://peps.python.org/pep-0634/ (Pattern Matching)
- https://peps.python.org/pep-0484/ (Type Hints)
