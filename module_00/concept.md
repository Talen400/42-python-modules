# Module 00 — Python Fundamentals (Growing Code)

**Ambiente**: Python 3.13.1 | Verificado em: 2026-07-12

## Objetivo do Módulo

Introduzir sintaxe fundamental do Python: expressões, variáveis, funções, controle de fluxo e type hints.
Tema "community garden" para exercitar entrada/saída, conversão de tipos, condicionais, loops, recursão
e anotações de tipo. Proibido usar `if __name__`, classes ou módulos nos primeiros 7 exercícios.

## Conceitos-Chave

### Funções

Uma função `def` é compilada para um objeto função contendo um code object (`__code__`) com o bytecode,
constantes e nomes. Quando chamada, um novo frame é empilhado na thread state.

Bytecode real de `ft_hello_garden()` (ex00):

```
  1           RESUME                   0
  2           LOAD_GLOBAL              1 (print + NULL)
              LOAD_CONST               1 ('Hello, Garden Community!')
              CALL                     1
              POP_TOP
              RETURN_CONST             0 (None)
```

**Opcodes importantes**:
- `CALL` (não `CALL_FUNCTION`!) — opcode único de chamada desde Python 3.11
- `RETURN_CONST` — otimização 3.13+ para retornar constantes (vs `LOAD_CONST` + `RETURN_VALUE`)
- `RESUME` — gerencia pontos de suspensão para generators/coroutines (3.11+)

O subject exige **apenas funções** (ex0–ex6) e proíbe `if __name__`. A moulinette importa o arquivo
e chama a função diretamente. Código solto no módulo executa no `import`, causando side effects.

### `print()` — Internals

`print()` é implementada em C (`builtin_print_impl`). Ela:
1. Escreve cada argumento via `sys.stdout.write()`, separando com `sep` (default `' '`)
2. Adiciona `end` (default `'\n'`) no final
3. `flush=True` força `fflush()` no buffer

O espaçamento entre argumentos é gerenciado internamente pela implementação C — **não** usa
`sys.stdout.softspace` (atributo removido do Python 3). A documentação oficial confirma que `print()`
chama `sys.stdout.write()` para cada argumento.

**Fontes**: https://docs.python.org/3/library/functions.html#print

### `input()` — Leitura do stdin

`input(prompt)` escreve o prompt em **stderr** (não stdout!), lê até `\n`, remove o newline e retorna
`str`. O prompt só aparece se stdin for TTY. A implementação usa `PyOS_Readline()` que chama GNU readline
quando disponível.

**Fontes**: https://docs.python.org/3/library/functions.html#input

### Conversão de Tipos — `int()`

`int(x)` aceita `str`, `float`, `bytes` ou objetos com `__int__()`. Para strings, parseia dígitos
decimais com sinal opcional. Rejeita espaços, floats (ex: `"3.14"`), hex sem base explícita.

O subject não exige validação (undefined behavior para entradas inválidas). A moulinette pode testar
com entradas válidas — a validação vira requisito em module_02.

### f-strings (PEP 498 / PEP 701)

Desde Python 3.12 (PEP 701), f-strings permitem aninhamento arbitrário e reuso de aspas.

Bytecode real de `ft_garden_name()` (ex01):

```
  2           LOAD_GLOBAL              1 (input + NULL)
              LOAD_CONST               1 ('Enter garden name: ')
              CALL                     1
              STORE_FAST               0 (name)
  3           LOAD_GLOBAL              3 (print + NULL)
              LOAD_CONST               2 ('\n    Garden: ')
  4           LOAD_FAST                0 (name)
              FORMAT_SIMPLE
              LOAD_CONST               3 ('\n    Status: Growing well!\n    ')
  3           BUILD_STRING             3
              CALL                     1
              POP_TOP
              RETURN_CONST             0 (None)
```

O `BUILD_STRING` concatena as partes da f-string. `FORMAT_SIMPLE` chama `str()` / `__format__` na
expressão interpolada. A indentação do bloco `"""` (espaços e newlines) é **literal** na string final.

### Condicionais — `if` / `else`

Bytecode real de `ft_plant_age()` (ex04):

```
  2           LOAD_GLOBAL              1 (int + NULL)
              LOAD_GLOBAL              3 (input + NULL)
              LOAD_CONST               1 ('Enter plant age in days: ')
              CALL                     2
              STORE_FAST               0 (age)
  3           LOAD_FAST                0 (age)
              LOAD_CONST               2 (60)
              COMPARE_OP             148 (bool(>))
              POP_JUMP_IF_FALSE       12 (to L1)
  4           LOAD_GLOBAL              5 (print + NULL)
              LOAD_CONST               3 ('Plant is ready to harvest!')
              CALL                     1
              POP_TOP
              RETURN_CONST             0 (None)
  6   L1:     LOAD_GLOBAL              5 (print + NULL)
              LOAD_CONST               4 ('Plant needs more time to grow')
              CALL                     1
              POP_TOP
              RETURN_CONST             0 (None)
```

`COMPARE_OP` com argumento `148` inclui o bit `bool` (bit 4 = 16) desde Python 3.13, forçando
conversão a bool — a comparação agora sempre produz `True`/`False`. `POP_JUMP_IF_FALSE` pula
para o `else` se a condição for falsa.

### Loops — `while`

O `while` em Python 3.13 compila sem `SETUP_LOOP` (removido no 3.8). Exemplo genérico:

```
 13           LOAD_FAST_LOAD_FAST     16 (x, n)
              COMPARE_OP              18 (bool(<))
              POP_JUMP_IF_FALSE       12 (to L2)
 14   L1:     LOAD_FAST                1 (x)
              LOAD_CONST               2 (1)
              BINARY_OP               13 (+=)
              STORE_FAST               1 (x)
 13           LOAD_FAST_LOAD_FAST     16 (x, n)
              COMPARE_OP              18 (bool(<))
              POP_JUMP_IF_FALSE        2 (to L2)
              JUMP_BACKWARD           12 (to L1)
 15   L2:     ...
```

- `POP_JUMP_IF_FALSE` + `JUMP_BACKWARD` substituem `SETUP_LOOP`
- `JUMP_BACKWARD` (3.11+) verifica interrupts (Ctrl+C)
- `BINARY_OP` com oparg `13` corresponde a `+=` (operador in-place)

**Fontes**: https://docs.python.org/3/library/dis.html#opcode-JUMP_BACKWARD

### Recursão em CPython

CPython **não otimiza** tail recursion. Cada chamada recursiva empilha um frame no C stack e no
Py frame stack. O limite padrão: `sys.getrecursionlimit()` = 1000 (confirmado).

Bytecode real de `ft_count_harvest_recursive()` (ex06):

```
  1           RESUME                   0
  2           LOAD_FAST                1 (days)
              POP_JUMP_IF_NOT_NONE    20 (to L1)
  3           LOAD_GLOBAL              1 (int + NULL)
              LOAD_GLOBAL              3 (input + NULL)
              ...
  4   L1:     LOAD_FAST_LOAD_FAST      1 (day, days)
              COMPARE_OP             148 (bool(>))
              POP_JUMP_IF_FALSE       12 (to L2)
  5           LOAD_GLOBAL              5 (print + NULL)
              LOAD_CONST               2 ('Harvest time!')
              ...
  7   L2:     LOAD_GLOBAL              5 (print + NULL)
              ...
  8           LOAD_GLOBAL              7 (ft_count_harvest_recursive + NULL)
              LOAD_FAST                0 (day)
              LOAD_CONST               4 (1)
              BINARY_OP                0 (+)
              LOAD_FAST                1 (days)
              CALL                     2
              POP_TOP
              RETURN_CONST             0 (None)
```

O sentinel pattern (`days: int | None = None`) é o padrão idiomático. A chamada recursiva
aparece como `CALL` — sem tail call optimization.

**Fontes**: https://docs.python.org/3/library/sys.html#sys.getrecursionlimit

### Type Hints (PEP 484)

Type hints são armazenados em `__annotations__` da função e **ignorados em runtime**. A verificação
é feita por mypy/pyright.

```python
def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
```

`-> None` indica que a função não retorna valor. O código usa `str.capitalize()` que retorna o
primeiro caractere em maiúsculo e o resto em minúsculo — confirmado: `"ß".capitalize()` → `"Ss"`.

**Fontes**: https://docs.python.org/3/library/stdtypes.html#str.capitalize

## Regras e Restrições do Subject

| Regra | Motivo |
|-------|--------|
| Python 3.10+ | Type union `X \| Y`, match/case (preparação) |
| flake8 | Padrão 42: E9, F, W, E501 |
| Sem `if __name__` (ex0–6) | Arquivo deve ser importável sem side effects |
| Type hints obrigatórios (ex07) | Pré-requisito para mypy |
| Sem `range()` antes do ex06 | Força while/recursão |
| `int()` sem validação | Undefined behavior — simplifica introdutórios |

## Correlação com Exercícios Existentes

### ex00 — ft_hello_garden.py
Função mais simples: `print()` com string literal. Sem type hint (opcional). Retorno `None` implícito.

### ex01 — ft_garden_name.py
`input()` + f-string com `"""`. A indentação do bloco (espaços e `\n`) aparece literal na saída —
pode ser pego pela moulinette em comparação exata.

### ex02 — ft_plot_area.py
**Bug corrigido**: `lenght` → `length`. Operação: `int()` + multiplicação dentro da f-string.
Uso de variáveis `length` e `width` sem validação de tipo.

### ex03 — ft_harvest_total.py
**Bug corrigido**: `"Dau"` → `"Day"`. Três entradas somadas diretamente.

### ex04 — ft_plant_age.py
Condicional `if age > 60` (parênteses desnecessários). `COMPARE_OP` com coerção a bool.

### ex05 — ft_water_reminder.py
**Bug corrigido**: `"PLants"` → `"Plants"`. Condicional `> 2` (strict). Valor exato 2 cai no else.

### ex06 — ft_count_harvest_iterative.py / recursive.py
**Problema**: iterativo imprime ordem **decrescente** (5, 4, 3...) enquanto o subject espera
ordem **crescente** (Day 1, Day 2...). Recursivo está correto com sentinel pattern.

### ex07 — ft_seed_inventory.py
**Bug corrigido**: `"Unknow"` → `"Unknown"`. Primeiro com type hints obrigatórios.
`if unit not in ["packets", "grams", "area"]` — verifica lista (O(n) para 3 itens).

## Erros Comuns

1. Confundir `print()` com `return`
2. `while` imprimindo ordem decrescente vs crescente
3. f-string multilinha com indentação — espaços extras são literais
4. Typos em prompts: `lenght`, `Dau`, `Unknow`, `PLants`
5. RecursionError para `days > 1000`
6. `__name__` solto fora de função — moulinette importa e executa

## Perguntas de Autoavaliação

- Por que o subject proíbe `if __name__ == "__main__":` nos ex0–6?
- O que acontece se `int()` receber uma string vazia? E `3.14`?
- `print(f"{x}")` vs `print(x)` — o bytecode gerado é diferente?
- Por que CPython não otimiza tail recursion? O que acontece com o C stack?
- `"hello".capitalize()` vs `"hello".title()` — qual a diferença para strings com maiúsculas no meio?
- `"hello world".capitalize()` → qual o resultado exato?

## Fontes Consultadas

- https://docs.python.org/3/library/functions.html#print
- https://docs.python.org/3/library/functions.html#input
- https://docs.python.org/3/library/functions.html#int
- https://docs.python.org/3/library/stdtypes.html#str.capitalize
- https://docs.python.org/3/library/dis.html
- https://docs.python.org/3/library/sys.html#sys.getrecursionlimit
- https://docs.python.org/3/reference/executionmodel.html
- https://docs.python.org/3/whatsnew/3.13.html
- https://peps.python.org/pep-0484/ (Type Hints)
- https://peps.python.org/pep-0498/ (f-strings)
- https://peps.python.org/pep-0701/ (f-strings aninhadas)
