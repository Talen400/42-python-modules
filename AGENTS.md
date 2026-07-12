# AGENT.md

Instruções para o agente trabalhar neste repositório (Python Modules — 42).

## Contexto do Projeto

Este repositório contém os exercícios dos Python Modules da 42 (module_00 a module_10).
Cada module possui um subject com o enunciado oficial e pastas `exXX/` com o
código já implementado (quando existente).

O objetivo do usuário é **estudar e revisar conceitos**, não gerar cola. O usuário já é
veterano na piscine, mas **este repositório é público e será lido por outras pessoas**,
incluindo iniciantes que podem chegar via busca (ex: "42 python module 00 concept").

Por isso, os `concept.md` devem servir **dois públicos ao mesmo tempo**:
- Quem quer só entender o conceito rapidamente (iniciante, primeira leitura)
- Quem quer profundidade técnica real (avançado, curioso, revisão)

Isso é resolvido com estrutura em camadas (ver seção "Ao Gerar/Revisar concept.md"),
não com simplificação — **rigor técnico continua acima de tudo**, apenas organizado
de forma que não intimide quem está começando.

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

6. **Correlacione com o código já implementado, mas sem expor bugs/typos pessoais.**
   Quando houver `.py` já escrito na pasta do exercício, use-o pra mostrar **qual
   conceito é aplicado onde** (ex: "este exercício usa recursão com sentinel
   pattern"). NÃO narre erros de digitação, bugs corrigidos, ou strings exatas
   esperadas pela moulinette (ex: não escreva "bug corrigido: X → Y"). Isso não
   ensina o conceito, expõe erros pessoais desnecessariamente num repo público, e
   pode revelar a saída exata esperada pelo exercício.

7. **Escreva em camadas.** Todo conceito deve ter uma explicação simples e direta
   primeiro (o que é, pra que serve, sem jargão desnecessário), e só depois o
   aprofundamento técnico (bytecode, internals, edge cases). Ver formato exato na
   seção "Ao Gerar/Revisar concept.md".

8. **Sinalize o nível de confiança com moderação — não em toda frase.** Use a legenda:
   - `✅` — confirmado por execução real (`dis.dis()`, teste em REPL, etc.)
   - `📚` — confirmado pela documentação oficial
   - `⚠️` — não verificado
   Aplique isso **apenas** em afirmações que sejam: (a) sobre bytecode/internals
   específicos de versão, ou (b) genuinamente arriscadas de estarem erradas. Não
   marque toda frase do texto — a maioria do conteúdo (explicações conceituais,
   TL;DRs, descrições de sintaxe básica) não precisa de badge nenhum. Se mais da
   metade das linhas de uma seção têm um emoji, é sinal de uso excessivo — remova.

9. **Nada de emoji decorativo fora da legenda de confiança — com uma única exceção.**
   Sem `🐍`, `🎯`, etc. em títulos, subtítulos ou texto corrido. As únicas exceções:
   - A legenda `✅ / 📚 / ⚠️`, usada com moderação conforme a regra 8.
   - O emoji fixo `🔍` no `<summary>` do bloco de aprofundamento (ver seção
     "Ao Gerar/Revisar concept.md"), sempre em negrito: `**🔍 Aprofundando: ...**`.
     Esse é o único emoji que se repete estruturalmente — não varie ("🔬", "🧠",
     etc.), sempre `🔍`.
   Fora dessas duas exceções, texto técnico deve parecer uma referência séria, não
   um post de rede social.

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

- **Cabeçalho de ambiente**: versão do Python usada e data da verificação
  (ex: `Ambiente: Python 3.13.1 | Verificado em: AAAA-MM-DD`)
- **Objetivo do módulo** (baseado no subject real, em linguagem direta)
- **Conceitos-chave**, cada um em duas camadas:
  1. **TL;DR** (1–3 frases, sem jargão): o que é e pra que serve. Deve fazer sentido
     pra alguém que nunca ouviu falar do conceito.
  2. **Aprofundamento** dentro de um bloco colapsável do GitHub, pra não intimidar
     quem só quer o essencial. O conteúdo interno deve ficar em **blockquote**
     (prefixo `>` em cada linha) — isso faz o GitHub renderizar com barra lateral e
     recuo, deixando claro visualmente que aquele bloco é diferente do TL;DR mesmo
     depois de expandido:
     ```markdown
     <details>
     <summary><strong>🔍 Aprofundando: bytecode, internals, edge cases</strong></summary>

     > (conteúdo técnico denso aqui — bytecode real via dis.dis(), trade-offs,
     > referências a PEPs, etc. Cada linha do aprofundamento começa com `>`,
     > incluindo linhas em branco entre parágrafos e blocos de código.)
     >
     > ```
     > RESUME 0
     > LOAD_GLOBAL ...
     > ```

     </details>
     ```
     Blocos de código dentro do blockquote também levam `>` antes dos ``` ``` ```
     de abertura/fechamento, senão o recuo quebra no meio.
- **Regras e restrições do subject** (normas, funções proibidas, versão exigida etc.)
  e o porquê delas existirem — explicado de forma que iniciante entenda a motivação,
  não só a regra
- **Correlação com exercícios existentes**: qual conceito cada exercício exercita e
  por quê — sem citar bugs, typos ou strings exatas do seu código
- **Erros comuns** que a moulinette costuma pegar, descritos de forma **genérica**
  (ex: "confundir `print()` com `return`", "esquecer que `while` decrescente não é
  o mesmo que crescente") — nunca citando o erro específico que você cometeu
- **Perguntas de autoavaliação** (sem resposta)
- **Fontes consultadas** (links reais usados na verificação)

Use a legenda de confiança (`✅` / `📚` / `⚠️`) com moderação, conforme a regra 8 —
apenas onde ela realmente ajuda o leitor a calibrar confiança, não em toda linha.

Antes de finalizar o arquivo, faça uma checagem própria: cada afirmação técnica tem
respaldo em execução real ou documentação oficial? Se não, corrija ou marque como
não verificado. Além disso: um iniciante conseguiria ler só os TL;DRs (ignorando os
`<details>`) e sair com entendimento correto do módulo?

## Estrutura do Repositório (nível raiz)

Como o repositório é público, mantenha também:

- **`README.md`** na raiz explicando: o que é a 42 e a piscine de Python (breve),
  o que são os `concept.md` (material de estudo complementar, não solução), como
  navegar (ler o subject do módulo primeiro, depois o `concept.md`), e um
  aviso claro de que o conteúdo não substitui fazer os exercícios sozinho.
- **`GLOSSARY.md`** na raiz com termos que se repetem entre módulos (ex: bytecode,
  frame, moulinette, norma, type hint, PEP). Isso evita reexplicar o básico em todo
  `concept.md` — cada um pode linkar pro glossário na primeira menção do termo.

## O Que Evitar (erros já cometidos anteriormente)

- Citar opcodes que não existem mais na versão atual (ex: `SETUP_LOOP`,
  `CALL_FUNCTION` sem checar se foram removidos/unificados).
- Citar atributos/comportamentos de Python 2 como se fossem válidos em Python 3
  (ex: `sys.stdout.softspace`).
- Atribuir comportamento a uma versão específica do Python sem confirmar no
  whatsnew correspondente.
- Gerar conteúdo genérico de "curso de Python" desconectado do subject real da 42.
- Narrar bugs, typos ou erros específicos do código do usuário (ex: "bug corrigido:
  lenght → length"). Isso não ensina conceito, expõe erro pessoal num repo público,
  e pode revelar a saída exata que a moulinette espera.
