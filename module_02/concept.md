# Module 02 — Error Handling

**Ambiente**: Python 3.13.1 | Verificado em: 2026-07-12

---

## Objetivo do Módulo

Ensinar tratamento de exceções: capturar erros com `try/except`, lançar com `raise`, criar
exceções customizadas e garantir limpeza com `finally`. Tema "agricultural data pipeline":
sensores IoT, validação de dados, resiliência.

---

## Conceitos-Chave

### `try/except` — Capturando Erros

**TL;DR**: `try:` tenta executar um bloco. Se der erro, `except:` captura e trata.
`except ValueError:` captura só esse tipo de erro. `except:` (sem tipo) captura **tudo**,
incluindo Ctrl+C — evite.

<details>
<summary><strong>🔍 Aprofundando: bytecode em 3.13 (sem SETUP_FINALLY), ExceptionTable</strong></summary>

> ✅ Python 3.13 não usa mais `SETUP_FINALLY` ou `END_FINALLY` — sistema de exceção
> reescrito no 3.11.
>
> Bytecode real de `try/except` básico:
>
> ```
>   6           RESUME                   0
>   7           NOP
>   8   L1:     LOAD_GLOBAL              1 (int + NULL)
>               LOAD_CONST               1 ('abc')
>               CALL                     1
>               STORE_FAST               0 (x)
>  11   L2:     RETURN_CONST             3 ('ok')
>   --   L3:     PUSH_EXC_INFO
>   9           LOAD_GLOBAL              2 (ValueError)
>               CHECK_EXC_MATCH
>               POP_JUMP_IF_FALSE        3 (to L5)
>               POP_TOP
>  10   L4:     POP_EXCEPT
>               RETURN_CONST             2 ('error')
>   9   L5:     RERAISE                  0
>   --   L6:     COPY                     3
>               POP_EXCEPT
>               RERAISE                  1
> ExceptionTable:
>   L1 to L2 -> L3 [0]
>   L3 to L4 -> L6 [1] lasti
>   L5 to L6 -> L6 [1] lasti
> ```
>
> Opcodes de exceção em 3.13:
>
> | Opcode | Função |
> |--------|--------|
> | `PUSH_EXC_INFO` | Salva a exceção corrente na pilha |
> | `CHECK_EXC_MATCH` | Testa se a exceção corresponde ao tipo do `except` |
> | `POP_EXCEPT` | Remove o handler de exceção da pilha |
> | `RERAISE` | Relança a exceção atual |
> | `COPY` | Copia item da pilha (para preservar exceção) |
>
> A `ExceptionTable` mapeia intervalos de bytecode para handlers. O número entre colchetes
> é a profundidade do bloco `try`.
>
> https://docs.python.org/3/library/dis.html

</details>

### Hierarquia de Exceções

**TL;DR**: `except ValueError:` antes de `except Exception:` — a ordem importa, o primeiro
match ganha. `except Exception:` captura erros comuns. `except:` captura tudo (má prática).

<details>
<summary><strong>🔍 Aprofundando: BaseException vs Exception, CHECK_EXC_MATCH</strong></summary>

> `except Exception:` captura todas as exceções que herdam de `Exception` — **não** captura
> `KeyboardInterrupt`, `SystemExit` ou `GeneratorExit` (herdam de `BaseException` diretamente).
>
> `except:` (sem tipo) captura **tudo**, inclusive `BaseException` — engole Ctrl+C.
>
> Bytecode de `except (ValueError, TypeError) as e`:
>
> ```
> PUSH_EXC_INFO
> LOAD_GLOBAL (ValueError)
> CHECK_EXC_MATCH
> POP_JUMP_IF_FALSE (próximo except)
> ...
> ```
>
> `CHECK_EXC_MATCH` testa STACK[-2] contra STACK[-1], pop e push bool.
>
> https://docs.python.org/3/library/exceptions.html

</details>

### `raise` — Lançando Exceções

**TL;DR**: `raise ValueError("mensagem")` para de executar e sobe o erro. Dentro de um
`except`, `raise` (sem argumento) relança o mesmo erro com o traceback original.

<details>
<summary><strong>🔍 Aprofundando: RAISE_VARARGS, raise vs raise e, __cause__</strong></summary>

> Bytecode de `raise_demo()`:
>
> ```
>  47           RESUME                   0
>  48           LOAD_FAST                0 (v)
>               LOAD_CONST               1 (0)
>               COMPARE_OP              18 (bool(<))
>               POP_JUMP_IF_FALSE       11 (to L1)
>  49           LOAD_GLOBAL              1 (ValueError + NULL)
>               LOAD_CONST               2 ('negativo')
>               CALL                     1
>               RAISE_VARARGS            1
>  50   L1:     LOAD_FAST                0 (v)
>               RETURN_VALUE
> ```
>
> ✅ `RAISE_VARARGS 1` — levanta a exceção no topo da pilha.
>
> **`raise` vs `raise e`**:
> - `raise` (dentro de `except`) — relança exceção ativa preservando o traceback original
> - `raise e` — cria novo traceback a partir do frame atual (perde o original)
>
> `raise ... from` (PEP 3134) encadeia exceções via `__cause__`.
> https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement

</details>

### `try/except/else/finally`

**TL;DR**: `else:` executa se **nenhuma** exceção ocorreu no `try`. `finally:` executa
**sempre** — depois do `try`, do `except`, mesmo se tiver `return` ou exceção não tratada.

<details>
<summary><strong>🔍 Aprofundando: bytecode com finally duplicado, finally engolindo exceção</strong></summary>

> Bytecode real de `try/except/else/finally`:
>
> ```
>  32           RESUME                   0
>  33           NOP
>  34   L1:     LOAD_CONST               1 (42)
>               STORE_FAST               0 (x)
>  38   L2:     NOP
>  40           LOAD_CONST               2 (1)
>               STORE_FAST               1 (y)
>               RETURN_CONST             3 ('ok')
>   --   L3:     PUSH_EXC_INFO
>  35           LOAD_GLOBAL              0 (ValueError)
>               CHECK_EXC_MATCH
>               POP_JUMP_IF_FALSE        5 (to L6)
>               POP_TOP
>  36   L4:     POP_EXCEPT
>  40   L5:     LOAD_CONST               2 (1)
>               STORE_FAST               1 (y)
>               RETURN_CONST             4 ('err')
>  35   L6:     RERAISE                  0
>   --   L7:     COPY                     3
>               POP_EXCEPT
>               RERAISE                  1
>        L8:     PUSH_EXC_INFO
>  40           LOAD_CONST               2 (1)
>               STORE_FAST               1 (y)
>               RERAISE                  0
> ```
>
> O código do `finally` aparece **duplicado** no bytecode: uma cópia pro caminho sem exceção
> (após `L2`) e outra pro caminho com exceção (`L8`). Isso garante que sempre execute.
>
> **Caso extremo**: se `finally` contém `return`, ele sobrepõe a exceção pendente — exceção
> **engolida**.
>
> https://docs.python.org/3/reference/compound_stmts.html#the-try-statement

</details>

### Custom Exceptions

**TL;DR**: Crie suas próprias exceções fazendo uma classe que herda de `Exception`.
`class GardenError(Exception): pass`. Depois `raise GardenError()`. Dá pra adicionar
atributos extras.

<details>
<summary><strong>🔍 Aprofundando: hierarquia semântica, mensagem default via super</strong></summary>

> Herança de exceções segue a MRO: `except GardenError:` captura `PlantError` e `WaterError`.
> A mensagem default é passada via `super().__init__()`.
>
> ```python
> class GardenError(Exception):
>     def __init__(self, message="Unknown garden error"):
>         self.message = message
>         super().__init__(self.message)
>
> class PlantError(GardenError):
>     pass
> ```
>
> Exceções customizadas permitem código mais expressivo, hierarquia semântica,
> e atributos extras (`self.sensor_id`, `self.plant_name`).

</details>

### Tabela de Exceções do Subject

| Exceção | Quando ocorre no exercício |
|---------|---------------------------|
| `ValueError` | `int("abc")`, validação de range |
| `ZeroDivisionError` | Divisão por zero |
| `FileNotFoundError` | `open("inexistente")` |
| `TypeError` | `"abc" + 123` |
| Custom (`GardenError`, etc.) | Ex03–04: exceções semânticas |

---

## Regras e Restrições do Subject

| Regra | Motivo |
|-------|--------|
| `try/except` obrigatório em todos | Foco em tratamento de erro |
| `TypeError` com `mypy` | mypy acusa linha intencionalmente quebrada |
| Custom exceptions herdam de `Exception` | Hierarquia padrão |
| `finally` para cleanup | Pré-requisito para context managers (module_04) |

---

## Correlação com Exercícios

### ex00 — Agricultural Data Validation
`input_temperature()` com `try/except ValueError` básico. Testa "25" (ok) e "abc" (erro).

### ex01 — Raise Exception
Adiciona `raise` para range 0–40. `input_temperature()` retorna `int` ou `raise ValueError`.

### ex02 — Different Types of Problems
`garden_operations(n)` com 4 exceções em um único `try/except` com tupla:
```python
except (ValueError, ZeroDivisionError, FileNotFoundError, TypeError) as e:
```
Subject proíbe usar `type()` — usa `str(e)`.

### ex03 — Custom Error Types
Hierarquia: `GardenError → PlantError`, `GardenError → WaterError`.
Mensagem default no `__init__`.

### ex04 — Finally Block
`water_plant()` valida capitalização. `try/except/finally` com `return` dentro do `except`.

---

## Erros Comuns

1. `except:` (sem tipo) captura `KeyboardInterrupt` — impede Ctrl+C
2. `return` dentro de `finally` — engole exceção pendente
3. Ordem errada de `except` — `except Exception:` antes de `except ValueError:` sempre captura
4. `raise e` em vez de `raise` — perde traceback original dentro de except
5. Custom exception sem `super().__init__()` — mensagem não propagada

---

## Perguntas de Autoavaliação

- `except ValueError:` vs `except ValueError as e:` — diferença de acesso?
- O que acontece se `finally` levanta exceção diferente da original?
- Por que `except:` (sem tipo) é má prática?
- `raise` vs `raise e` — por que o primeiro preserva o traceback?
- `else` no `try/except` — quando exatamente executa?

---

## Fontes Consultadas

- https://docs.python.org/3/reference/compound_stmts.html#the-try-statement
- https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement
- https://docs.python.org/3/library/exceptions.html
- https://docs.python.org/3/library/dis.html
- https://docs.python.org/3/whatsnew/3.11.html (exception handling rewrite)
- https://docs.python.org/3/whatsnew/3.13.html
- https://docs.python.org/3/tutorial/errors.html
- https://peps.python.org/pep-3134/ (Exception Chaining)
