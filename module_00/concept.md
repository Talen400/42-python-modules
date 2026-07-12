# Module 00 — Python Fundamentals (Growing Code)

## Objetivo do Módulo

Introduzir a sintaxe fundamental do Python: expressões, variáveis, funções, controle de fluxo e type hints. O tema "community garden" é um veículo para exercitar entrada/saída, conversão de tipos, condicionais, loops, recursão e anotações de tipo — tudo sem `if __name__`, sem classes, sem módulos.

## Conceitos-Chave

### Funções em CPython

Uma função `def` é compilada para um objeto `PyFunctionObject` contendo um `PyCodeObject` (bytecode, constantes, nomes). O `CALL` no bytecode (CALL_FUNCTION / CALL_PRECISE) empilha um novo frame na thread state. Cada frame tem seu próprio namespace local (`f_locals`). A relação entre `def` e `return` é:

```python
def f(x):     # cria PyFunctionObject em tempo de definição
    return x  # LOAD_FAST x; RETURN_VALUE (pop 1, push ao caller)
```

No subject, exige-se **apenas funções** (ex0–ex6) e **proíbe-se** `if __name__ == "__main__":`. A razão é pedagógica: isolar a unidade lógica (função) do script. A moulinette importa o arquivo e chama a função diretamente. Se houver código solto no módulo (top-level), ele executa no `import`, causando side effects.

### `print()` — Internals

`print()` é uma função built-in em C (`builtin_print_impl`). Ela:
1. Chama `sys.stdout.write()` para cada argumento, com `sys.stdout.softspace` para espaçamento
2. Adiciona `end` (default `\n`) no final
3. `flush` força `fflush()` no buffer do stdout (line-buffered por padrão em terminais)

Edge case: `print()` com múltiplos args separa por `sep` (default `' '`). O subject usa `print()` com concatenação via f-string, evitando essa separação.

### `input()` — Leitura do stdin

`input(prompt)` chama `PyOS_Readline()` que usa GNU readline (se disponível) ou gets padrão. Escreve o prompt em stderr (não stdout!), lê até `\n`, remove o newline e retorna uma `str`. O prompt só aparece se stdin for um TTY.

Nunca usar `input()` em código de produção real — não há controle sobre encoding, buffer, ou EOF sem exceção. O subject usa `input()` como ferramenta de aprendizado, mas a moulinette testa as funções injetando valores via redirecionamento de stdin.

### Conversão de Tipos — `int()`

`int(x)` aceita `str`, `float`, `bytes`, `bytearray`, ou qualquer objeto com `__int__()`. Para strings, faz parsing de dígitos decimais com sinal opcional. Rejeita espaços internos, pontos flutuantes, hex. Em Python 3.13, `int("0b1010", 2)` e bases customizadas continuam válidas.

O subject não exige validação de entrada (undefined behavior para negativos ou inválidos). A moulinette pode testar com entradas válidas apenas, mas nos módulos seguintes (module_02) isso vira requisito.

### f-strings (PEP 498 / PEP 701)

Desde Python 3.12 (PEP 701), f-strings são reescritas para permitir:
- Aninhamento arbitrário: `f"{f"{x}"}"`
- Reuso de aspas: `f"{d["key"]}"` (antes dava SyntaxError)
- Expressões multilinha

O bytecode gerado é equivalente a `' '.join(str(expr) for expr in ...)` — cada expressão é avaliada e convertida via `__format__`.

No código existente (`ex01`), a f-string com `"""` multilinha adiciona `\n` extra e espaços da indentação literal:

```python
print(f"""
    Garden: {name}
    Status: Growing well!
    """)
```

Isso imprime um `\n` inicial, 4 espaços antes de "Garden", um `\n` antes de "Status" e `\n` final. O subject não especifica formato exato para ex01 ("mimic the output"), mas em exercícios futuros a moulinette compara caractere a caractere.

### Condicionais — `if` / `else`

Python usa `if`, `elif`, `else`. Não existem parênteses obrigatórios — `if (x > y):` funciona mas é redundante. O compilador Python ignora os `()` para expressões simples. No bytecode, geram COMPARE_OP + POP_JUMP_IF_FALSE.

**Armadilha comum (moulinette testa)**: confundir os operadores:

| Operador | Descrição | Diferença de C |
|----------|-----------|----------------|
| `>` / `<` | comparação | igual |
| `==` | igualdade | igual (C usa `=`) |
| `!=` | diferença | igual (C usa `!=`) |
| `and` / `or` | lógicos | C usa `&&` / `\|\|` |
| `not` | negação | C usa `!` |
| `is` | identidade | compara endereço (id) |

### Loops — `while`

`while condition:` compila para:
```
SETUP_LOOP
>> FOR_ITER / POP_JUMP_IF_FALSE
   BODY
   JUMP_ABSOLUTE (topo)
>> (exit)
```

O `while` não tem contador embutido. Para iterações numeradas, usa-se `for` + `range()`. O subject só autoriza `range()` a partir do ex06.

### Recursão em CPython

CPython **não otimiza** tail recursion. Cada chamada recursiva empilha um novo frame no C stack e no Py frame stack. O limite padrão é `sys.getrecursionlimit()` = 1000. Para entradas grandes, a recursão estoura stack (RecursionError). A versão iterativa evita esse problema.

O subject pede ambos os enfoques (ex06) justamente para comparar. A versão recursiva no código usa **default sentinel** (`days: int | None = None`) — padrão idiomático para recursão com parâmetro opcional em Python. Alternativas: wrapper function, inner function (`def inner(...)` dentro de `ft_count_harvest_recursive`).

### Type Hints (PEP 484)

Introduzidos no Python 3.5, são **ignorados em runtime** pelo interpretador. O tipo é armazenado em `__annotations__` da função. A verificação é feita por ferramentas externas (mypy, pyright, pyre). No subject, são obrigatórios apenas no ex07.

O código usa:
```python
def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
```

`-> None` explicita que a função não retorna valor. O mypy valida que todas as ramificações atingem return — e `print()` retorna `None`, então `return` sem valor também é `None`.

### Métodos de String — `str.capitalize()`

`.capitalize()` retorna a string com primeiro caractere maiúsculo (via `Py_UNICODE_TO_TITLE`) e o resto minúsculo. Diferenças importantes:
- `"ß".capitalize()` → `"Ss"` em Python 3.13 (correção Unicode)
- `"résumé".capitalize()` → `"Résumé"` (preserva acentos)
- `"hello world".capitalize()` → `"Hello world"` (só primeira letra)
- `"hello world".title()` → `"Hello World"` (cada palavra)

## Regras e Restrições do Subject

| Regra | Motivo |
|-------|--------|
| Python 3.10+ | Módulo usa match/case em module_01, type union syntax `X \| Y` |
| flake8 | Padrão 42: garantir estilo consistente (E9, F, W, E501) |
| Sem `if __name__` (ex0–6) | Arquivo deve ser "importável" sem side effects |
| Type hints obrigatórios (ex07) | Pré-requisito para mypy |
| `int()` sem validação | undefined behavior — simplifica exercícios introdutórios |
| Apenas funções, sem main | Moulinette chama função diretamente |
| Sem `range()` antes do ex06 | Evita loop for; força while/recursão |

## Correlação com Exercícios Existentes

### ex00 — ft_hello_garden.py
Função mais simples possível sem parâmetros. `print()` com string literal. Sem type hint (opcional). Sem retorno (`None` implícito).

### ex01 — ft_garden_name.py
Usa `input()` e f-string com bloco `"""` multilinha. **Observação técnica**: a indentação do bloco f-string (espaços antes de `Garden:` e `Status:`) aparece na saída. Isso pode ser pego pela moulinette em comparação exata.

### ex02 — ft_plot_area.py
**Bug corrigido**: variável "lenght" → `length`. O typo sobrevive em Python (dinâmico), mas é semanticamente incorreto. Operação: `int()` duas vezes, multiplicação direta dentro da f-string.

### ex03 — ft_harvest_total.py
**Bug corrigido**: "Dau" → "Day" (typo no prompt). Três entradas e soma. O subject mostra "Day 1 harvest:", "Day 2 harvest:", "Day 3 harvest:" — o prompt correto é essencial.

### ex04 — ft_plant_age.py
Condicional simples `if (age > 60)`. Os parênteses são desnecessários em Python. Poderia ser `if age > 60:`.

### ex05 — ft_water_reminder.py
**Bug corrigido**: `"PLants"` → `"Plants"`. Condicional com `> 2` (estritamente maior). Notar que > 2 significa ≥ 3 dias desde a última rega. Se o subject testar o limite exato (2), cai no else — "Plants are fine".

### ex06 — Iterativo vs Recursivo

**Iterativo** (`ft_count_harvest_iterative.py`): usa `while` decrementando. Imprime dias decrescentes, enquanto o subject espera crescentes (Day 1, Day 2...). **Problema**: o código imprime `5, 4, 3, 2, 1, Harvest time!` mas o subject mostra `Day 1, Day 2, ..., Day 5`. A assinatura `while (days):` (parênteses) também é redundante.

**Recursivo** (`ft_count_harvest_recursive.py`): assinatura `(day: int = 1, days: int | None = None)`. Usa união `int | None` (Python 3.10+). O sentinel `None` é necessário porque default mutável não é problema aqui, mas o padrão evita confusão com o argumento `day`.

### ex07 — ft_seed_inventory.py
**Bug corrigido**: `"Unknow"` → `"Unknown"`. 
Primeiro exercício com type hints obrigatórios. Usa `str.capitalize()` e `if unit not in ["packets", "grams", "area"]` — verificação de lista vs conjunto. A diferença de performance é irrelevante para 3 itens, mas `in set` é O(1) vs O(n) da lista.

O `return` sem valor interrompe a função para branches de erro — padrão "early return".

## Erros Comuns

1. **Confundir `print()` com `return`**: a função do subject deve **imprimir** o resultado, não retorná-lo
2. **Usar `while` imprimindo ordem decrescente**: o subject espera `Day 1, Day 2...` (crescente)
3. **f-string multilinha com indentação**: espaços extras na saída são literais
4. **Typos em prompts**: "lenght", "Dau", "Unknow", "PLants" — a moulinette compara exatamente
5. **NameError por variável não definida**: Python não declara variáveis; `lenght` vira `length` em um lugar mas não em outro
6. **RecursionError**: para `days > 1000`, a recursão estoura stack
7. **Type hints opcionais ignorados**: mypy não roda sem configuração — mas o subject exige
8. **`__name__` solto fora de função**: moulinette importa e executa tudo

## Perguntas de Autoavaliação

- Por que o subject proíbe `if __name__ == "__main__":` nos primeiros 7 exercícios?
- O que acontece se `int()` receber uma string vazia? E `"3.14"`?
- `print(f"{x}")` vs `print(x)` — o bytecode gerado é diferente? Qual a diferença de performance?
- Por que CPython não otimiza tail recursion?
- `"hello".capitalize()` vs `"hello".title()` vs `"hello".upper()` — qual usar para nomes próprios como "tomato"?
- O que `str.capitalize()` faz com strings começando com números?
- Se o ex06 recursivo receber `days=0`, o que acontece com o sentinel pattern?
