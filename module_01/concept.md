# Module 01 — Object-Oriented Programming

**Ambiente**: Python 3.13.1 | Verificado em: 2026-07-12

---

## Objetivo do Módulo

Você vai evoluir de funções soltas para um sistema com classes, herança, encapsulamento e
polimorfismo. Tema "digital garden ecosystem": começa com uma classe `Plant`, depois `Flower`
e `Tree` (herança), métodos especiais (`@staticmethod`, `@classmethod`), nested classes,
e `match/case` para despacho polimórfico.

---

## Conceitos-Chave

### `if __name__ == "__main__":`

**TL;DR**: Esse bloco só executa quando o arquivo é rodado diretamente (não quando importado).
Em module_00 era proibido; aqui é permitido. Serve pra ter código de teste ou demo dentro
do mesmo arquivo sem poluir quem importa.

<details>
<summary><strong>🔍 Aprofundando: `__name__`, pontos de entrada, shebang</strong></summary>

> Quando Python executa um arquivo, `__name__` é `"__main__"`. Quando importado, vira o
> nome do módulo. O guard permite que o mesmo arquivo sirva como script e módulo importável.
>
> O shebang (`#!/usr/bin/env python3`) instrui o kernel a usar o interpretador Python
> quando o script é executado via `./script.py`.

</details>

### Classes e Objetos

**TL;DR**: `class Plant:` define um tipo novo. Ela agrupa dados (atributos) e comportamentos
(métodos). `__init__` roda quando você cria uma instância: `p = Plant("Rose", 25, 30)`.
Dentro dos métodos, `self` é a própria instância.

<details>
<summary><strong>🔍 Aprofundando: metaclasse type, __new__, descriptor protocol, bytecode</strong></summary>

> O corpo da classe é executado em namespace separado pela metaclasse `type`. O resultado
> vira `__dict__` da classe.
>
> ✅ `__init__` **não é o construtor**. O construtor real é `__new__` (aloca memória).
> `__init__` recebe a instância já criada e configura atributos. Chamar `Plant("Rose", 25, 30)`:
> 1. `type.__call__(Plant, "Rose", 25, 30)`
> 2. `Plant.__new__(Plant, ...)` aloca a instância
> 3. `Plant.__init__(self, "Rose", 25, 30)` inicializa
>
> ✅ [Bytecode](../GLOSSARY.md#bytecode) real de `Plant.__init__()` (ex01) — `STORE_ATTR` com nome não mangleado
> (o name mangling já foi resolvido na compilação):
>
> ```
>   4           RESUME                   0
>   5           LOAD_FAST                1 (name)
>               LOAD_FAST                0 (self)
>               STORE_ATTR               0 (name)
>   6           LOAD_FAST                2 (height)
>               LOAD_FAST                0 (self)
>               STORE_ATTR               1 (height)
>   7           LOAD_FAST                3 (age)
>               LOAD_FAST                0 (self)
>               STORE_ATTR               2 (age)
>               RETURN_CONST             0 (None)
> ```
>
> - `STORE_ATTR` com nome literal — name mangling já transformado na compilação
> - `RETURN_CONST 0 (None)` — `__init__` não tem `return` explícito
>
> 📚 https://docs.python.org/3/reference/datamodel.html#object.__init__
>
> **Conexões:**
> - Em C: `malloc()` + `init()` vs `__new__()` + `__init__()`. Em C você aloca e inicializa separadamente; Python explicita os dois passos mas esconde o `__new__` na prática.
> - Diagrama: `Plant("Rose", 25, 30)` → `type.__call__` → `__new__` (aloca) → `__init__` (configura)

</details>

### Atributos e Métodos

**TL;DR**: `self.nome = valor` guarda um dado no objeto. `def metodo(self):` define uma
função que opera na instância. Chamar `objeto.metodo()` automaticamente passa `self`.

<details>
<summary><strong>🔍 Aprofundando: descriptor protocol, MRO lookup, bytecode LOAD_ATTR</strong></summary>

> Acesso a `self.height`:
> 1. Busca em `instance.__dict__` — se achar, retorna
> 2. Se não, busca no `__dict__` da classe (e sobe na [MRO](../GLOSSARY.md#mro))
> 3. Se encontrado na classe com `__get__` ([descriptor](../GLOSSARY.md#descriptor-protocol)), chama o descriptor
>
> Bytecode real de `Plant.show()` (ex01):
>
> ```
>   8           RESUME                   0
>   9           LOAD_CONST               1 ('')
>               LOAD_FAST                0 (self)
>               LOAD_ATTR                0 (name)
>               FORMAT_SIMPLE
>               ...
>               BUILD_STRING             4
>               RETURN_VALUE
> ```

</details>

### Encapsulamento — Protected vs Name Mangling

**TL;DR**: Python não tem `private`. Use `_attr` pra dizer "isso é interno, não mexa".
Use `__attr` só se precisar evitar conflito em herança (o Python renomeia pra
`_Classe__attr` via [name mangling](../GLOSSARY.md#name-mangling)). O subject **exige** `_attr` ([protected convention](../GLOSSARY.md#protected-convention)), não `__attr`.

<details>
<summary><strong>🔍 Aprofundando: name mangling na compilação, empírico com dir()</strong></summary>

> `dir()` em instância com `__height` mostra `_Plant__height` (confirmado em REPL):
>
> ```python
> class Test:
>     def __init__(self):
>         self.__secret = 42
> t = Test()
> print(t._Test__secret)  # 42
> ```
>
> ✅ Name mangling dificulta acesso em subclasses: `__attr` vira `_Pai__attr`, mas
> subclasse tenta `_Filho__attr`. Por isso o subject pede `_attr`.
>
> 📚 https://docs.python.org/3/tutorial/classes.html#private-variables

</details>

### Getters / Setters e `@property`

**TL;DR**: O código usa getters `get_height()` e setters `set_height()` estilo Java.
Em Python idiomático, usa-se `@property` pra mesma coisa com sintaxe mais limpa.

<details>
<summary><strong>🔍 Aprofundando: descriptor protocol de property, implementação C</strong></summary>

> `@property` é um descriptor: `property.__get__()` chama o getter,
> `property.__set__()` chama o setter.
>
> ```python
> @property
> def height(self) -> float:
>     return self._height
>
> @height.setter
> def height(self, value: float) -> None:
>     if value < 0:
>         raise ValueError("Height can't be negative")
>     self._height = value
> ```
>
> O subject introduz getters/setters primeiro para ensinar encapsulamento antes da
> syntactic sugar. 📚 https://docs.python.org/3/library/functions.html#property

</details>

### Herança e MRO

**TL;DR**: `class Flower(Plant):` faz `Flower` herdar tudo de `Plant`. `super()` chama
o método da classe pai. Se você não chamar `super().__init__()`, os atributos do pai
nunca são criados.

<details>
<summary><strong>🔍 Aprofundando: C3 linearization, LOAD_SUPER_ATTR bytecode</strong></summary>

> Python usa **C3 linearization** para MRO. Herança simples: `Flower → Plant → object`.
> `super()` delega ao próximo na MRO.
>
> ✅ Bytecode real de `Flower.__init__()` (ex05) — `LOAD_SUPER_ATTR` (3.12+) é o [opcode](../GLOSSARY.md#opcode)
> dedicado para `super()`:
>
> ```
>  96           RESUME                   0
> 104           LOAD_GLOBAL              0 (super)
>               LOAD_DEREF               6 (__class__)
>               LOAD_FAST                0 (self)
>               LOAD_SUPER_ATTR          5 (__init__ + NULL|self)
>               LOAD_FAST_LOAD_FAST     18 (name, height)
>               LOAD_FAST_LOAD_FAST     52 (ages, growth)
>               CALL                     4
>               POP_TOP
> 105           LOAD_CONST               1 ('')
>               LOAD_FAST                0 (self)
>               STORE_ATTR               2 (_color)
> ```
>
> - `LOAD_SUPER_ATTR` (3.12+) — opcode dedicado para `super()`
> - A sequência `super()` + `__init__` compila para `LOAD_GLOBAL(super)` + `LOAD_DEREF(__class__)` +
>   `LOAD_SUPER_ATTR` + argumentos + `CALL`
>
> `super()` sem argumentos equivale a `super(__class__, self)`. A variável `__class__`
> é inserida pelo compilador em métodos.
>
> ⚠️ No código existente, `Flower.show()` (ex05) **não chama** `super().show()` — constrói a
> string do zero, duplicando lógica. Design alternativo:
>
> ```python
> def show(self) -> str:
>     return f"{super().show()}\nColor: {self._color}"
> ```
>
> **Conexões:**
> - Diagrama: MRO de `Flower("Rose", 25, 30, "red")` → `Flower` → `Plant` → `object`. `super().__init__` navega do `Flower` para `Plant` na cadeia.
> - Em C: herança é composição de structs (struct Flower { struct Plant parent; ... }) vs MRO com lookup dinâmico em dicts.

</details>

### `@staticmethod` vs `@classmethod`

**TL;DR**:
- Método normal recebe `self` (instância)
- `@classmethod` recebe `cls` (classe) — útil pra factories
- `@staticmethod` não recebe nem `self` nem `cls` — é uma função normal dentro da classe

<details>
<summary><strong>🔍 Aprofundando: bytecode real de ambos, bound vs unbound</strong></summary>

> Bytecode de `Plant.is_older_than_year()` (staticmethod, ex06):
>
> ```
>  33           RESUME                   0
>  34           LOAD_FAST                0 (days)
>               LOAD_CONST               1 (365)
>               COMPARE_OP             148 (bool(>))
>               RETURN_VALUE
> ```
>
> — não recebe `self` ou `cls`, apenas argumentos explícitos.
>
> Bytecode de `Plant.create_anonymous()` (classmethod, ex06):
>
> ```
>  37           RESUME                   0
>  39           LOAD_FAST                0 (cls)
>               LOAD_CONST               1 ('Unknown plant')
>               LOAD_CONST               2 (0.0)
>               LOAD_CONST               3 (0)
>               LOAD_CONST               4 (1.0)
>               LOAD_CONST               0 (None)
>               ...
>               CALL                     5
>               RETURN_VALUE
> ```
>
> — se chamado em `Flower.create_anonymous()`, `cls` = `Flower`.
>
> 📚 https://docs.python.org/3/library/functions.html#classmethod

</details>

### Nested Classes

**TL;DR**: Uma classe dentro de outra. Em Python, **não** são inner classes como em Java —
não têm acesso automático à instância externa.

<details>
<summary><strong>🔍 Aprofundando: nested class é atributo estático, herança de nested</strong></summary>

> `_Stats` dentro de `Plant` é apenas um atributo de classe — não recebe `self` da externa.
> `Tree._TreeStats(Plant._Stats)` estende a nested class.
> `_TreeStats.display()` pode chamar `super().display()` normalmente.

</details>

### `match` / `case`

**TL;DR**: `match valor:` testa o valor contra vários padrões. `case Tree():` verifica
se é instância de `Tree`. Útil pra polimorfismo sem precisar de métodos virtuais.

<details>
<summary><strong>🔍 Aprofundando: isinstance internamente, [PEP 634](../GLOSSARY.md#pep), performance</strong></summary>

> `match` usa `isinstance()` internamente. `case Tree():` verifica a classe do sujeito.
> Ordem importa: primeiro match ganha. Performance similar a cadeia de `isinstance()`.
>
> 📚 https://peps.python.org/pep-0634/

</details>

---

## Regras e Restrições do Subject

| Regra | Por quê? |
|-------|----------|
| Python 3.10+ | match/case ([PEP 634](../GLOSSARY.md#pep)) |
| PascalCase classes / snake_case vars | PEP 8 |
| `super()` autorizado | Herança |
| `@staticmethod`, `@classmethod` autorizados | Decorator syntax |
| Protected convention (`_attr`) | Mangling prejudica herança |
| `if __name__` permitido | Diferença de module_00 |

---

## Correlação com Exercícios

### ex00 — ft_garden_intro.py
Único exercício do repositório **sem função** — script puro com `if __name__`.
Valores hardcoded (Rose, 25cm, 30 days).

### ex01 — ft_garden_data.py
`class Plant` com `__init__` + `show()`. Tem `try/except ValueError`.

### ex02 — ft_plant_growth.py
Adiciona `grow()` e `age()`. Simula 7 dias com `range(7)`.

### ex03 — ft_plant_factory.py
Construtor com parâmetros. Cria 5 plantas. Adiciona `total_plants` counter extra.

### ex04 — ft_garden_security.py
Getters/setters com validação de negativos via `print()` (não `raise`).

### ex05 — ft_plant_types.py
`Flower.show()` **não** chama `super().show()` — não usa herança para estender
a formatação. `Tree.__init__` reatribui `self._stats`, sobrescrevendo `_Stats`
com `_TreeStats`.

### ex06 — ft_garden_analytics.py
`Seed(Flower)`, `_TreeStats(Plant._Stats)`, `@staticmethod`, `@classmethod`.
Função `display_plant_stats` definida fora de classe — pattern funcional.

---

## Erros Comuns

1. Name mangling em subclasse: `__attr` vira `_Pai__attr`, subclasse acessa `_Filho__attr`
2. Esquecer `super().__init__()` — atributos do pai nunca criados
3. `@staticmethod` não recebe `self` nem `cls`
4. Nested class não tem relação com instância externa
5. `match/case` com `case _:` antes dos específicos — sempre match
6. Getters/setters sem validação — subject testa negativos

---

## Perguntas de Autoavaliação

- `super().__init__()` vs `Plant.__init__(self, ...)` — diferença na MRO?
- Se uma subclasse não define `__init__`, qual construtor é chamado?
- O que é o descriptor protocol? Como transforma funções em bound methods?
- `@classmethod` recebe `cls`. Como a herança afeta o valor de `cls`?
- Por que o subject pede `_attr` em vez de `__attr`?
- `_Stats` dentro de `Plant` — é possível instanciá-la de fora?

---

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
