# Module 00 — Python Fundamentals

**Ambiente**: Python 3.13.1 | Verificado em: 2026-07-12

---

## Objetivo do Módulo

Você vai escrever funções simples que manipulam dados de uma horta comunitária:
pedir entradas com `input()`, converter tipos com `int()`, usar `if` para decisões,
`while` para repetições, e até recursão. No último exercício, type hints obrigatórios.

Tudo isso **sem** `if __name__` e **sem** classes — só funções puras.

---

## Conceitos-Chave

### Funções

**TL;DR**: Uma função é um bloco de código nomeado que você pode chamar de qualquer lugar.
`def` define, `return` devolve um valor. Toda função em Python retorna algo — se você
não escrever `return`, retorna `None`.

<details>
<summary><strong>🔍 Aprofundando: bytecode, frame objects, object layout</strong></summary>

> Uma função `def` compila para um code object contendo bytecode, constantes e nomes.
> Bytecode de `ft_hello_garden` (ex00):
>
> ```
>   1           RESUME                   0
>   2           LOAD_GLOBAL              1 (print + NULL)
>               LOAD_CONST               1 ('Hello, Garden Community!')
>               CALL                     1
>               POP_TOP
>               RETURN_CONST             0 (None)
> ```
>
> Opcodes reais do Python 3.13:
> - ✅ `CALL` (não `CALL_FUNCTION` — removido no 3.11)
> - ✅ `RETURN_CONST` (otimização 3.13+, vs `LOAD_CONST` + `RETURN_VALUE`)
> - ✅ `RESUME` (3.11+, gerencia suspensão para generators/coroutines)
>
> Cada chamada de função empilha um novo frame na thread state. O frame contém o code
> object, `f_locals`, `f_globals`, e o frame anterior.
>
> Documentação: https://docs.python.org/3/reference/executionmodel.html

</details>

### `print()`

**TL;DR**: `print()` escreve texto no terminal. Aceita vários argumentos separados por
espaço, e coloca uma quebra de linha (`\n`) no final. Dá pra mudar o separador com `sep`
e o final com `end`.

<details>
<summary><strong>🔍 Aprofundando: implementação C, buffering, softspace</strong></summary>

> `print()` é implementada em C (`builtin_print_impl`):
> 1. Escreve cada argumento via `sys.stdout.write()`, separando com `sep` (default `' '`)
> 2. Adiciona `end` (default `'\n'`)
> 3. `flush=True` força `fflush()` no buffer
>
> O espaçamento é gerenciado internamente pela implementação — **não** usa
> `sys.stdout.softspace` (atributo removido do Python 3, existia apenas no Python 2).
>
> Documentação: https://docs.python.org/3/library/functions.html#print

</details>

### `input()`

**TL;DR**: `input("pergunta: ")` mostra uma pergunta no terminal e espera o usuário
digitar algo. O que for digitado volta como string.

<details>
<summary><strong>🔍 Aprofundando: PyOS_Readline, stderr, EOF</strong></summary>

> ✅ `input(prompt)` escreve o prompt em **stderr** (não stdout!), lê até `\n`, remove
> o newline e retorna `str`. O prompt só aparece se stdin for TTY.
>
> A implementação usa `PyOS_Readline()` que chama GNU readline quando disponível.
>
> Documentação: https://docs.python.org/3/library/functions.html#input

</details>

### Conversão de Tipos — `int()`

**TL;DR**: `int("42")` pega uma string que parece número e vira um inteiro de verdade.
Se a string não for um número válido, dá erro.

<details>
<summary><strong>🔍 Aprofundando: parsing, erros comuns, base</strong></summary>

> `int(x)` aceita `str`, `float`, `bytes` ou objetos com `__int__()`. Para strings,
> parseia dígitos decimais com sinal opcional. Rejeita espaços, floats (`"3.14"`), hex
> sem base explícita.
>
> `int("0b1010", 2)` funciona e retorna 10 (confirmado em REPL).
>
> Documentação: https://docs.python.org/3/library/functions.html#int

</details>

### f-strings

**TL;DR**: f-strings são strings com `f"..."` que permitem enfiar expressões dentro
de chaves: `f"Olá, {nome}"`. O Python avalia a expressão e formata o resultado.

<details>
<summary><strong>🔍 Aprofundando: PEP 498, PEP 701, bytecode, multiline caveats</strong></summary>

> Desde Python 3.12 (PEP 701), f-strings permitem aninhamento arbitrário e reuso de aspas.
>
> Bytecode real de `ft_garden_name()` (ex01, f-string com `"""`):
>
> ```
>   2           LOAD_GLOBAL              1 (input + NULL)
>               LOAD_CONST               1 ('Enter garden name: ')
>               CALL                     1
>               STORE_FAST               0 (name)
>   3           LOAD_GLOBAL              3 (print + NULL)
>               LOAD_CONST               2 ('\n    Garden: ')
>   4           LOAD_FAST                0 (name)
>               FORMAT_SIMPLE
>               LOAD_CONST               3 ('\n    Status: Growing well!\n    ')
>   3           BUILD_STRING             3
>               CALL                     1
>               POP_TOP
>               RETURN_CONST             0 (None)
> ```
>
> O `BUILD_STRING` concatena as partes. `FORMAT_SIMPLE` chama `__format__` na expressão.
> ⚠️ Atenção: a indentação do bloco `"""` (espaços e `\n`) é **literal** na string final.

</details>

### Condicionais — `if` / `else`

**TL;DR**: `if condição:` executa um bloco se a condição for verdadeira. `else:` executa
outro bloco se for falsa. `elif:` encadeia condições.

<details>
<summary><strong>🔍 Aprofundando: bytecode COMPARE_OP, POP_JUMP_IF_FALSE em 3.13</strong></summary>

> Bytecode real de `ft_plant_age()` (ex04):
>
> ```
>   2           LOAD_GLOBAL              1 (int + NULL)
>               LOAD_GLOBAL              3 (input + NULL)
>               LOAD_CONST               1 ('Enter plant age in days: ')
>               CALL                     2
>               STORE_FAST               0 (age)
>   3           LOAD_FAST                0 (age)
>               LOAD_CONST               2 (60)
>               COMPARE_OP             148 (bool(>))
>               POP_JUMP_IF_FALSE       12 (to L1)
>   4           LOAD_GLOBAL              5 (print + NULL)
>               LOAD_CONST               3 ('Plant is ready to harvest!')
>               CALL                     1
>               POP_TOP
>               RETURN_CONST             0 (None)
>   6   L1:     LOAD_GLOBAL              5 (print + NULL)
>               ...
> ```
>
> ✅ `COMPARE_OP` com argumento `148` inclui o bit `bool` (bit 4 = 16) desde Python 3.13,
> forçando o resultado a `True`/`False`.
>
> Documentação: https://docs.python.org/3/reference/compound_stmts.html#the-if-statement

</details>

### Loops — `while`

**TL;DR**: `while condição:` repete um bloco enquanto a condição for verdadeira.
Tome cuidado pra não fazer um loop infinito (a condição precisa se tornar falsa em
algum momento).

<details>
<summary><strong>🔍 Aprofundando: bytecode sem SETUP_LOOP, JUMP_BACKWARD</strong></summary>

> ⚠️ O `while` em Python 3.13 compila **sem** `SETUP_LOOP` — opcode removido no Python 3.8.
> Usa `POP_JUMP_IF_FALSE` + `JUMP_BACKWARD`.
>
> Exemplo genérico:
>
> ```
>  13           LOAD_FAST_LOAD_FAST     16 (x, n)
>               COMPARE_OP              18 (bool(<))
>               POP_JUMP_IF_FALSE       12 (to L2)
>  14   L1:     LOAD_FAST                1 (x)
>               LOAD_CONST               2 (1)
>               BINARY_OP               13 (+=)
>               STORE_FAST               1 (x)
>  13           COMPARE_OP              18 (bool(<))
>               POP_JUMP_IF_FALSE        2 (to L2)
>               JUMP_BACKWARD           12 (to L1)
>  15   L2:     ...
> ```
>
> `JUMP_BACKWARD` (3.11+) verifica interrupts (Ctrl+C).
> https://docs.python.org/3/library/dis.html#opcode-JUMP_BACKWARD

</details>

### Recursão

**TL;DR**: Uma função que chama a si mesma. Útil para problemas que podem ser quebrados
em partes menores (mesmo problema). Mas CPython **não otimiza** recursão — cada chamada
empilha um novo frame, e há um limite (~1000 chamadas).

<details>
<summary><strong>🔍 Aprofundando: sem TCO, sentinel pattern, frame stack, RecursionError</strong></summary>

> ✅ CPython não otimiza tail recursion. Cada chamada recursiva empilha um frame no C stack
> e no Py frame stack.
>
> Limite padrão: `sys.getrecursionlimit()` = 1000 (confirmado em REPL).
>
> Bytecode real de `ft_count_harvest_recursive()` (ex06):
>
> ```
>   4   L1:     LOAD_FAST_LOAD_FAST      1 (day, days)
>               COMPARE_OP             148 (bool(>))
>               POP_JUMP_IF_FALSE       12 (to L2)
>   5           LOAD_GLOBAL              5 (print + NULL)
>               LOAD_CONST               2 ('Harvest time!')
>               ...
>   7   L2:     LOAD_GLOBAL              5 (print + NULL)
>               ...
>   8           LOAD_GLOBAL              7 (ft_count_harvest_recursive + NULL)
>               LOAD_FAST                0 (day)
>               LOAD_CONST               4 (1)
>               BINARY_OP                0 (+)
>               LOAD_FAST                1 (days)
>               CALL                     2
>               POP_TOP
>               RETURN_CONST             0 (None)
> ```
>
> O sentinel pattern (`days: int | None = None`) é o idiomático: evita confundir `None`
> como valor válido. Sem tail call optimization — `CALL` empilha novo frame.
>
> https://docs.python.org/3/library/sys.html#sys.getrecursionlimit

</details>

### Type Hints

**TL;DR**: Type hints são "dicas" de tipo que você escreve nos parâmetros e retorno
da função: `def f(x: int) -> str:`. O Python ignora em runtime, mas o `mypy` verifica.

<details>
<summary><strong>🔍 Aprofundando: PEP 484, __annotations__, runtime irrelevance</strong></summary>

> Introduzidos no PEP 484 (Python 3.5). Armazenados em `__annotations__` da função e
> **ignorados em runtime**. A verificação é feita por ferramentas externas (mypy, pyright).
>
> O subject torna type hints obrigatórios no ex07. Exemplo do código existente:
>
> ```python
> def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
> ```
>
> `str.capitalize()` — primeiro caractere maiúsculo, resto minúsculo.
> Confirmado: `"ß".capitalize()` → `"Ss"`, `"résumé".capitalize()` → `"Résumé"`.
>
> https://docs.python.org/3/library/stdtypes.html#str.capitalize

</details>

---

## Regras do Subject

| Regra | TL;DR | Por quê? |
|-------|-------|----------|
| Python 3.10+ | Versão mínima | Type union `X \| Y`, preparação para match/case |
| flake8 | Linter obrigatório | Padrão 42: estilo consistente |
| Sem `if __name__` (ex0–6) | Sem bloco main | Arquivo precisa ser importável sem efeito colateral |
| Type hints obrigatórios (ex07) | Anotações de tipo | mypy precisa delas pra verificar |
| Sem `range()` antes do ex06 | Sem `for` | Força usar `while` e recursão |
| `int()` sem validação | Não trate erros de entrada | Undefined behavior — simplifica exercícios |

---

## Correlação com Exercícios

### ex00 — ft_hello_garden.py
Função mais simples: `print()` com string literal. Sem type hint. Retorno `None` implícito.

### ex01 — ft_garden_name.py
`input()` + f-string com `"""`. A indentação do bloco (espaços e `\n`) aparece
literal na saída — a moulinette compara exatamente.

### ex02 — ft_plot_area.py
Operação: `int()` + multiplicação.

### ex03 — ft_harvest_total.py
Três entradas somadas diretamente.

### ex04 — ft_plant_age.py
Condicional `if age > 60` (parênteses são desnecessários em Python).

### ex05 — ft_water_reminder.py
Condicional `> 2` (strict).

### ex06 — ft_count_harvest_iterative.py / recursive.py
Iterativo: imprime ordem decrescente. Recursivo: sentinel pattern.

### ex07 — ft_seed_inventory.py
Primeiro com type hints obrigatórios.
`if unit not in ["packets", "grams", "area"]` — verifica lista (O(n) para 3 itens).

---

## Erros Comuns

- Confundir `print()` com `return` (a função deve **imprimir**, não retornar)
- `while` imprimindo ordem decrescente vs crescente
- f-string multilinha com indentação — espaços extras são literais
- RecursionError para `days > 1000`
- Código solto fora de função — moulinette importa e executa

---

## Perguntas de Autoavaliação

- Por que o subject proíbe `if __name__ == "__main__":` nos ex0–6?
- O que `int("3.14")` faz? E `int("")`?
- `print(f"{x}")` vs `print(x)` — o bytecode gerado é diferente? Qual mais rápido?
- Por que CPython não otimiza tail recursion? O que acontece no C stack?
- `"hello".capitalize()` vs `"hello".title()` — diferença pra "hello world"?
- O que acontece se a função recursiva do ex06 receber `days=0`?

---

## Fontes Consultadas

- https://docs.python.org/3/library/functions.html#print
- https://docs.python.org/3/library/functions.html#input
- https://docs.python.org/3/library/functions.html#int
- https://docs.python.org/3/library/stdtypes.html#str.capitalize
- https://docs.python.org/3/library/dis.html
- https://docs.python.org/3/library/sys.html#sys.getrecursionlimit
- https://docs.python.org/3/reference/executionmodel.html
- https://docs.python.org/3/reference/compound_stmts.html
- https://docs.python.org/3/whatsnew/3.13.html
- https://peps.python.org/pep-0484/ (Type Hints)
- https://peps.python.org/pep-0498/ (f-strings)
- https://peps.python.org/pep-0701/ (f-strings aninhadas)
