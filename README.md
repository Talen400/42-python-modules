# 42 — Python Modules

Este repositório contém os exercícios dos **Python Modules** da [42](https://42.fr/), um
currículo imersivo de engenharia de software. Cada module foca um tema de Python — de
sintaxe básica a tópicos avançados — com exercícios corrigidos por uma moulinette
automatizada e por peers.

## O que é a "Piscine" de Python?

Na 42, os módulos de Python são uma trilha de aprendizado progressivo. Você recebe um
**subject** descrevendo os exercícios e deve implementar soluções que
passem pela moulinette (testes automatizados) e pela defesa com outro aluno.

## O que são os `concept.md`?

Cada module_XX contém um `concept.md` — material de estudo complementar que **não substitui**
fazer os exercícios. Eles existem para:

- Explicar os conceitos por trás de cada exercício
- Mostrar bytecode real (`dis.dis()`) e comportamento interno do CPython
- Correlacionar teoria com o código já implementado (bugs, decisões de design)
- Apontar erros comuns que a moulinette pega

### Como usar

1. Leia o subject do módulo (entenda o que é pedido)
2. Tente fazer os exercícios
3. Consulte o `concept.md` para aprofundar conceitos ou entender por que algo não funciona
4. Use as perguntas de autoavaliação para testar seu entendimento

> ⚠️ Os `concept.md` **não contêm soluções completas**. Eles explicam conceitos e
> analisam código existente, mas não fornecem código pronto para copiar. O objetivo
> é que você entenda o suficiente para escrever suas próprias soluções.

## Estrutura

```
module_00/          # Python Fundamentals
  ex00/             # Exercícios
  ex01/
  ...
  concept.md        # Material de estudo
module_01/          # Object-Oriented Programming
  ...
module_02/          # Error Handling
module_03/          # Collections
module_04/          # File I/O
```

## Convenções dos `concept.md`

Cada conceito é apresentado em **duas camadas**:

1. **TL;DR** — explicação direta sem jargão, para leitura rápida
2. **🔬 Aprofundamento** (dentro de `<details>`) — bytecode real, internals, edge cases

Toda afirmação técnica carrega um badge de confiança:

- ✅ confirmado por execução real (`dis.dis()`, REPL)
- 📚 confirmado pela documentação oficial
- ⚠️ não verificado

## Ferramentas

```bash
# Instalar dependências
make install

# Verificar código com flake8 + mypy
make lint
```

Consulte o [Makefile](Makefile) para detalhes.
