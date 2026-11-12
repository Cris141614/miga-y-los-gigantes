# Instrucciones para Claude: Miga y los Gigantes

## La bóveda es la fuente de verdad
- Todo el contenido del proyecto (historia, personajes, mecánicas, niveles, decisiones, tareas, canal) vive en `docs/`, la bóveda de Obsidian. No se guarda contenido en otro lugar.
- Antes de responder, diseñar o programar algo del juego o del canal, consultar la bóveda. Si la bóveda y lo que recuerdas no coinciden, manda la bóveda.

## Cómo consultar (grafo de conocimiento)
1. Empezar en `docs/00-Inicio.md`: es el nodo central del grafo.
2. Seguir los enlaces `[[Nota]]` a las notas relacionadas. `[[Nota]]` es el archivo `Nota.md` en cualquier subcarpeta de `docs/`.
3. Para ver quién enlaza a una nota (backlinks): `grep -rn "\[\[Nota" docs --include=*.md`.
4. Los embeds `![[archivo.png]]` apuntan a archivos de `docs/Referencias/`.
5. Leer las notas enlazadas que afecten la respuesta, no solo la primera.

## Cómo guardar
- Una nota por tema. Si ya existe, editarla; no duplicar.
- Toda nota nueva va en su carpeta, enlaza al menos a una nota existente y se enlaza desde su nota padre o desde `00-Inicio`. Una nota sin enlaces queda huérfana en el grafo.
- Las decisiones se escriben en la nota del tema con fecha (AAAA-MM-DD).
- Tareas en `Produccion/Tareas.md`. Assets nuevos en `Produccion/Inventario.md`.
- Nombres de archivos, scripts y ramas según `Produccion/Convenciones.md`.

## Git y GitHub
- Nunca ejecutar comandos que cambien git o GitHub (add, commit, push, branch, merge, gh...). Solo revisar el estado (status, log, diff) y darle al usuario los comandos para que él los ejecute.
- Ramas y mensajes de commit: ver `Produccion/Convenciones.md`.

## Estructura
Ver `README.md`. El proyecto de Unity está en `juego/` (Unity 6000.5, URP); los scripts propios van en `juego/Assets/_Proyecto/Scripts/`.
