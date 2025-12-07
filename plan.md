# Plan — Sistema de Tarjetas tipo “aira”

## 1) Objetivos
- Corregir el problema: al pulsar una tarjeta, se despliega el mismo menú/historial para todas. Cada tarjeta debe mostrar su propio historial, acciones e indicadores.
- Respetar el estilo visual de la imagen (tema amarillo/turquesa) y la estructura: sidebar, tarjetas, historial, acciones, toggle “Congelar tarjeta”, cashback.
- Implementar FE (React) + BE (FastAPI) + DB (MongoDB). Todas las rutas del backend bajo `/api` y uso estricto de variables de entorno.

## 2) Enfoque por Fases

### Fase 1 — POC del Núcleo (¿Se requiere?)
- Decisión: NO se requiere POC separado. El núcleo es manejo de estado/UI (nivel bajo, sin integraciones externas). Se avanza directo a la app con pruebas incrementales.

### Fase 2 — Desarrollo de la Aplicación (principal)
Implementación completa y pruebas end-to-end.

## 3) Arquitectura y Modelado
- Colecciones MongoDB:
  - cards: { _id, type: [debit|credit|virtual], holderName, brand: “VISA”, balance, frozen: bool, last4, expMonth, expYear, colorTheme, cashback (number) }
  - transactions: { _id, cardId, date, amount, category, description }
  - documents: { _id, cardId, name, url }
- Relaciones: 1 tarjeta → N movimientos, N documentos.

## 4) Backend (FastAPI)
- Endpoints (prefijo `/api`):
  - GET `/api/cards` → lista de tarjetas (datos resumidos + estado frozen + cashback)
  - GET `/api/cards/{card_id}` → detalle (datos de tarjeta)
  - GET `/api/cards/{card_id}/transactions?range=hoy|semana` → movimientos filtrados
  - GET `/api/cards/{card_id}/documents` → documentos
  - PATCH `/api/cards/{card_id}/freeze` body: { frozen: bool } → congelar/descongelar
  - GET `/api/cards/{card_id}/history` → serie temporal para el gráfico (por tarjeta)
- Utilidades: helper `serialize_doc` que convierta ObjectId/fechas a JSON.
- Semilla de datos: endpoint temporal `/api/dev/seed` para crear 3 tarjetas (principal, crédito, desechable) y sus movimientos; retirar en producción.
- Conexión: `MONGO_URL` desde entorno. Servidor en `0.0.0.0:8001`.

## 5) Frontend (React)
- Layout:
  - Sidebar amarillo con las entradas mostradas (solo visual, no navega a secciones complejas todavía).
  - Panel principal con: tarjeta destacada, sección “Historial” (gráfico), fila de acciones (Datos, Movimientos, Documentos, Ver más), toggle Congelar, bloque de Cashback, listado de demás tarjetas (crédito, desechable).
- Estado clave (evita el bug actual):
  - `selectedCardId` en un estado de alto nivel (Context/State en App). Las vistas de historial/acciones leen SIEMPRE este id.
  - Cada componente de tarjeta dispara `setSelectedCardId(card._id)` al click; las demás tarjetas NO se expanden ni comparten menú.
- Datos por tarjeta (fetch on select):
  - Al seleccionar tarjeta: fetch paralelo de `/cards/{id}`, `/history`, `/transactions?range=...`, `/documents`, `/cashback`.
  - Los componentes muestran solo datos vinculados al `selectedCardId`.
- Interacciones:
  - Botones de acción con modales/drawers minimalistas:
    - Datos de tarjeta: número enmascarado, vencimiento, titular.
    - Movimientos: lista paginada/sencilla por tarjeta.
    - Documentos: listado con links simulados.
    - Ver más: menú placeholder (sin lógica extra por ahora).
  - Toggle “Congelar tarjeta”: PATCH al endpoint; reflejar estado inmediato por tarjeta.
  - Historial: gráfico de línea (Recharts) alimentado por `/history` de la tarjeta seleccionada. Tabs “Hoy/Semana” afectan el dataset.
- Estilo:
  - Tema amarillo/turquesa según imagen. shadcn/ui para botones, cards y modales. Sin fondos transparentes.
- Accesibilidad/QA:
  - data-testid en elementos clave: `card-item`, `card-item-{id}`, `card-menu`, `history-chart`, `btn-datos`, `btn-movimientos`, `btn-documentos`, `btn-ver-mas`, `toggle-freeze`, `cashback-value`.

## 6) Historias de Usuario (Fase 2)
1. Al hacer click en una tarjeta específica, solo esa tarjeta muestra su historial y menú; las demás permanecen sin cambios.
2. Quiero alternar “Congelar tarjeta” y que el estado persista por tarjeta y no afecte a otras.
3. Al cambiar entre Hoy/Semana, el gráfico se actualiza con datos de la tarjeta seleccionada.
4. Necesito ver los Movimientos de la tarjeta activa sin que se mezclen con los de otras.
5. Quiero abrir “Datos de tarjeta” y ver número enmascarado y vencimiento de la tarjeta activa.
6. Deseo ver el valor de cashback asociado únicamente a la tarjeta elegida.

## 7) Pasos de Implementación
- Backend:
  1) Definir modelos y conexión MongoDB.
  2) Implementar serialización segura (ObjectId/fecha).
  3) Endpoints listados (incluye `/history` y `freeze`).
  4) Semillado `/api/dev/seed` con 3 tarjetas y movimientos.
- Frontend:
  5) Layout y tema (sidebar + panel principal).
  6) Estado `selectedCardId` y CardList con `onClick` → select.
  7) Gráfico con Recharts y tabs Hoy/Semana.
  8) Acciones (modales) y toggle freeze por tarjeta.
  9) Mostrar cashback por tarjeta.
- Integración:
  10) Usar `process.env.REACT_APP_BACKEND_URL` + `/api` en todas las llamadas.

## 8) Pruebas y Validación
- Lint FE/BE, luego pruebas E2E con testing agent:
  - Selección de tarjeta cambia exclusivamente el contenido del panel.
  - Toggle `Congelar` afecta solo a esa tarjeta y persiste tras recarga.
  - Movimientos e Historial cargan datasets distintos para tarjetas distintas.
  - data-testid presentes y accesibles.
  - Sin errores de pantalla roja; logs limpios.

## 9) Acciones Siguientes (Next Actions)
1. ✅ Confirmación de este plan (diseño como imagen) - COMPLETADO
2. ✅ Implementación directa de Fase 2 (sin POC separado), solicitando diseño detallado al `design_agent` al iniciar FE - COMPLETADO
3. ✅ Crear semilla y endpoints; luego UI completa - COMPLETADO
4. ✅ Ejecutar testing agent y corregir cualquier hallazgo - COMPLETADO

## STATUS: FASE 2 COMPLETADA ✅
- Backend implementado con todos los endpoints funcionando
- Frontend implementado con selección independiente de tarjetas
- Testing completado al 100% (32/32 tests backend + UI completo)
- Bug crítico corregido (parámetro range → range_type)
- PROBLEMA ORIGINAL RESUELTO: Cada tarjeta ahora muestra su propio contenido único

## 10) Criterios de Éxito
- Cada tarjeta controla su propio menú/historial/estado (sin “mirroring”).
- Estados (freeze/cashback) persistentes por tarjeta en MongoDB.
- UI fiel al estilo amarillo/turquesa y sin fondos transparentes.
- API con prefijo `/api`, uso estricto de variables de entorno, servidor en `0.0.0.0:8001`.
- Todas las historias de usuario verificadas por el testing agent y sin fallas abiertas.
