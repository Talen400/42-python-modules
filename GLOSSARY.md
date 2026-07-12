# Glossário

Termos que aparecem nos `concept.md` e no dia a dia da 42.

## A

**annotation scope** — Escopo especial para anotações de tipo, type parameters e
type aliases (PEP 695, Python 3.12+). Comporta-se como escopo de função mas tem
acesso ao namespace da classe envolvente.

## B

**bytecode** — Instruções de baixo nível geradas pelo compilador Python a partir do
código fonte. São executadas pela VM do CPython. Podem ser inspecionadas com `dis.dis()`.
**Não há garantia de estabilidade** entre versões do Python.

## C

**compact dict** — Implementação de dicionário (PEP 509, Python 3.6+ CPython, Python 3.7+
oficial) que armazena entradas em ordem de inserção usando duas tabelas: índices para
sondagem hash + array de entries.

**comprehension** — Sintaxe concisa para construir listas (`[x for x in ...]`), dicts
(`{k: v for ...}`) e sets (`{x for x in ...}`). Em Python 3.12+ (PEP 709), são **inline** —
não compilam para code object separado e **não vazam** variável de iteração.

**context manager** — Objeto que implementa `__enter__` e `__exit__`, usado com `with`.
Garante que recursos sejam liberados mesmo com exceção. Ex: `with open(...) as f:`.

## D

**descriptor protocol** — Mecanismo pelo qual objetos com `__get__`, `__set__` ou `__delete__`
controlam acesso a atributos. Transforma funções em bound methods, permite `@property`,
`@classmethod`, `@staticmethod`.

## F

**flake8** — Linter que combina `pycodestyle` (PEP 8), `pyflakes` (erros lógicos) e `mccabe`
(complexidade). Usado na 42 para garantir estilo consistente.

**frame** — Estrutura que representa a execução de um bloco de código (função, módulo, classe).
Contém o code object, o dicionário local, o dicionário global, e o ponteiro para o frame
anterior (pilha). Acessível via `sys._getframe()`.

## G

**GIL (Global Interpreter Lock)** — Lock do CPython que serializa o acesso a objetos Python
entre threads. Impede paralelismo real para código Python puro. Em Python 3.13,
experimentalmente desligável (free-threaded mode, PEP 703).

## M

**MRO (Method Resolution Order)** — Ordem em que as classes base são pesquisadas na resolução
de métodos. Determinada pelo algoritmo C3 linearization. Acessível via `ClassName.__mro__`.

**mypy** — Type checker estático para Python. Verifica type hints sem executar o código.
Usado na 42 com flags `--disallow-untyped-defs` e `--strict`.

**moulinette** — Sistema automatizado de correção da 42. Testa os exercícios comparando
saída exata (stdout), verificando nomes de arquivos, e aplicando linters (flake8, mypy).

## N

**name mangling** — Transformação que o compilador Python aplica a atributos com `__`
(duplo underscore): `self.__attr` vira `_ClassName__attr`. Existe para evitar conflitos
em herança, não para privacidade.

**norma** — Conjunto de regras de estilo e organização que a 42 exige. Em Python: flake8 +
PEP 8 + proibições específicas do subject (ex: sem `if __name__` em module_00, type hints
obrigatórios).

## O

**opcode** — Instrução individual do bytecode Python. Ex: `CALL`, `LOAD_FAST`, `RETURN_VALUE`.
Cada opcode ocupa 2 bytes (opcode + argumento). Opcodes mudam entre versões — `SETUP_LOOP`
removido no 3.8, `CALL_FUNCTION` substituído por `CALL` no 3.11.

## P

**PEP (Python Enhancement Proposal)** — Documento de proposta de melhoria do Python.
Passa por revisão e aprovação antes de ser implementado. PEPs relevantes para este
repositório: PEP 8 (estilo), PEP 484 (type hints), PEP 498 (f-strings), PEP 634 (match/case),
PEP 701 (f-strings aninhadas), PEP 709 (inline comprehensions).

**protected convention** — Convenção de usar `_attr` para sinalizar "uso interno".
Diferente de `__attr` (name mangling), `_attr` é acessível por subclasses sem transformação
de nome. O subject de module_01 exige explicitamente protected convention em vez de mangling.

## T

**type hint (ou type annotation)** — Sintaxe para declarar tipos esperados em Python:
`def f(x: int) -> str:`. São ignoradas em runtime (mas acessíveis via `__annotations__`)
e verificadas por ferramentas externas (mypy, pyright).

**traceback** — Registro da pilha de chamadas no momento de uma exceção. Mostra a sequência
de chamadas desde o ponto onde a exceção foi levantada até o ponto onde foi capturada (ou
até o topo do programa).
