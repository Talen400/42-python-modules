# AGENT.md

Instruções para o agente trabalhar neste repositório (Python Modules — 42).

## Contexto do Projeto

Este repositório contém os exercícios dos Python Modules da 42 (module_00 a module_10).
Cada module possui um `en.subject.pdf` com o enunciado oficial e pastas `exXX/` com o
código já implementado (quando existente).

O objetivo do usuário é **estudar e revisar conceitos**, não gerar cola. O usuário já é
veterano na piscine — não simplifique explicações para nível iniciante, mas mantenha
**rigor técnico acima de tudo**.

## Regras Gerais (sempre válidas, qualquer tarefa)

1. **Nunca escreva soluções completas dos exercícios.** Nem em concept.md, nem em
   explicações, nem em exemplos. Exemplos ilustrativos são permitidos, mas devem usar
   nomes de variáveis/funções diferentes dos exercícios reais e não devem ser
   copiáveis diretamente como resposta.

2. **Leia o subject de verdade antes de escrever qualquer coisa sobre um module.**
   Não infira conteúdo a partir apenas dos nomes de arquivos/pastas. Se o PDF não
   puder ser lido, diga isso explicitamente em vez de inventar conteúdo genérico.

3. **Não alucine internals do Python.** Toda afirmação sobre bytecode, opcodes, ou
   comportamento interno do CPython deve ser confirmada empiricamente (rodando
   `python3 --version` e `dis.dis()` de verdade), nunca descrita de memória.

4. **Não alucine comportamento de linguagem/versão.** Afirmações sobre sintaxe,
   built-ins, PEPs, ou mudanças entre versões do Python devem ser verificadas contra
   a documentação oficial (docs.python.org), não assumidas.

5. **Marque incerteza explicitamente.** Se uma afirmação técnica não puder ser
   verificada por execução real ou documentação oficial, marque como
   `⚠️ não verificado` em vez de apresentar como fato.

6. **Correlacione com o código já implementado.** Quando houver `.py` já escrito na
   pasta do exercício, analise-o (bugs, typos, decisões de design, edge cases) e use
   isso para enriquecer a explicação — isso tem mais valor do que teoria solta.

## Fontes de Verificação (nesta ordem de prioridade)

1. Execução real no ambiente: `python3 --version`, `dis.dis()`, testes rápidos em REPL.
2. Documentação oficial:
   - https://docs.python.org/3/library/ — biblioteca padrão
   - https://docs.python.org/3/reference/ — referência da linguagem
   - https://docs.python.org/3/whatsnew/ — mudanças por versão
   - PEPs relevantes (ex: PEP 498, PEP 701, PEP 484) em https://peps.python.org/
3. Se nenhuma das duas acima for possível, marcar como não verificado.

## Ao Gerar/Revisar `concept.md`

Estrutura esperada em cada `module_XX/concept.md`:

- **Objetivo do módulo** (baseado no subject real)
- **Conceitos-chave** com profundidade técnica (sem necessidade de simplificar)
- **Regras e restrições do subject** (normas, funções proibidas, versão exigida etc.)
  e o porquê delas existirem
- **Correlação com exercícios existentes** (bugs, typos, decisões de design)
- **Erros comuns** que a moulinette costuma pegar
- **Perguntas de autoavaliação** (sem resposta)
- **Fontes consultadas** (links reais usados na verificação)

Antes de finalizar o arquivo, faça uma checagem própria: cada afirmação técnica tem
respaldo em execução real ou documentação oficial? Se não, corrija ou marque como
não verificado.

## O Que Evitar (erros já cometidos anteriormente)

- Citar opcodes que não existem mais na versão atual (ex: `SETUP_LOOP`,
  `CALL_FUNCTION` sem checar se foram removidos/unificados).
- Citar atributos/comportamentos de Python 2 como se fossem válidos em Python 3
  (ex: `sys.stdout.softspace`).
- Atribuir comportamento a uma versão específica do Python sem confirmar no
  whatsnew correspondente.
- Gerar conteúdo genérico de "curso de Python" desconectado do subject real da 42.
