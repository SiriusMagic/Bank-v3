{
  "meta": {
    "product_name": "Aira - Gestión de Tarjetas Bancarias",
    "app_type": "Fintech dashboard (React + FastAPI + MongoDB)",
    "audience": "Usuarios bancarios que administran múltiples tarjetas (físicas, crédito y desechables)",
    "primary_tasks": [
      "Ver y cambiar entre tarjetas",
      "Consultar saldo y cashback",
      "Congelar/descongelar tarjeta",
      "Ver movimientos e histórico",
      "Acceder a datos/documentos de tarjeta"
    ],
    "success_actions": [
      "Cambio de tarjeta fluido (sin pérdida de contexto)",
      "Historial claro con filtros (Hoy / Semana / Personaliza)",
      "Estados de tarjeta evidentes (activa/congelada)",
      "Acciones principales visibles y accesibles"
    ],
    "brand_attributes": ["confiable", "profesional", "ágil", "claro", "moderno"]
  },

  "typography": {
    "fonts": {
      "heading": "Space Grotesk, ui-sans-serif, system-ui",
      "body": "Karla, Inter, ui-sans-serif, system-ui",
      "numeric": "Space Grotesk, ui-monospace, SFMono-Regular"
    },
    "import_instructions": "Use Google Fonts: <link href=\"https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Karla:wght@400;500;600;700&display=swap\" rel=\"stylesheet\">",
    "scale": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl tracking-tight",
      "h2": "text-base md:text-lg font-semibold tracking-tight",
      "h3": "text-base font-semibold",
      "body": "text-sm md:text-base leading-relaxed",
      "small": "text-xs leading-snug"
    },
    "usage": {
      "headings": "Usar Space Grotesk para secciones, totales y saldos; controlar anchura de línea (max-w-prose)",
      "body": "Usar Karla para texto corrido y elementos de interfaz"
    }
  },

  "color_system": {
    "note": "NO usar fondos transparentes. Fondos de secciones y tarjetas deben ser sólidos; gradientes permitidos en tarjetas y secciones decorativas bajo la regla de <=20% viewport.",
    "semantics": {
      "sidebar_yellow": "#FFD700",
      "card_turquoise": "#00CED1",
      "card_turquoise_600": "#00B3B5",
      "card_turquoise_50": "#E5FCFD",
      "accent_teal": "#0F766E",
      "mint": "#B8FFF1",
      "ink": "#111827",
      "ink_muted": "#4B5563",
      "surface": "#F7F8FA",
      "surface_alt": "#FFFFFF",
      "border": "#E5E7EB",
      "success": "#0E9F6E",
      "warning": "#F59E0B",
      "danger": "#DC2626",
      "info": "#0284C7"
    },
    "hsl_tokens_overrides_for_index.css": {
      "--background": "210 20% 98%",
      "--foreground": "220 17% 10%",
      "--card": "0 0% 100%",
      "--card-foreground": "220 17% 10%",
      "--primary": "182 100% 41%", 
      "--primary-foreground": "0 0% 100%",
      "--secondary": "51 100% 50%", 
      "--secondary-foreground": "220 17% 10%",
      "--accent": "186 83% 85%", 
      "--accent-foreground": "220 17% 10%",
      "--muted": "220 14% 96%",
      "--muted-foreground": "220 10% 46%",
      "--destructive": "0 72% 50%",
      "--destructive-foreground": "0 0% 100%",
      "--border": "220 13% 91%",
      "--ring": "182 100% 41%",
      "--radius": "0.75rem",
      "--chart-1": "182 100% 41%",
      "--chart-2": "51 100% 50%",
      "--chart-3": "188 60% 35%",
      "--chart-4": "204 94% 94%",
      "--chart-5": "14 91% 60%"
    },
    "gradients": {
      "allowed_examples": [
        {
          "name": "card-cyan-mint",
          "css": "bg-[linear-gradient(135deg,_#00CED1_0%,_#8EEAD5_60%,_#E5FCFD_100%)]"
        },
        {
          "name": "header-mist",
          "css": "bg-[linear-gradient(90deg,_#FFFFFF_0%,_#F2FBFF_50%,_#FFFFFF_100%)]"
        },
        {
          "name": "accent-teal-wash",
          "css": "bg-[linear-gradient(180deg,_#E6FFFA_0%,_#FFFFFF_100%)]"
        }
      ],
      "prohibited": [
        "gradientes morados/rosas saturados",
        "azul-oscuro a morado",
        "rojo a rosa",
        "múltiples capas en el mismo viewport"
      ],
      "enforcement": "Si un área degradada supera el 20% del viewport o afecta la legibilidad, usa color sólido de la paleta"
    },
    "elevation": {
      "shadow_card": "shadow-[0_10px_30px_rgba(0,0,0,0.06)]",
      "shadow_popover": "shadow-[0_6px_20px_rgba(0,0,0,0.10)]",
      "ring_selected": "ring-2 ring-offset-2 ring-[color:var(--ring)] ring-offset-white"
    },
    "radii": {
      "sm": "0.375rem",
      "md": "0.75rem",
      "lg": "1rem",
      "xl": "1.25rem"
    }
  },

  "layout_and_grid": {
    "container": "mx-auto max-w-[1280px] px-4 md:px-6",
    "shell": {
      "mobile_first": true,
      "grid": "grid grid-cols-1 lg:grid-cols-[260px_1fr] min-h-screen",
      "sidebar": "bg-[#FFD700] text-[#111827] border-r border-[#E5E7EB]",
      "content": "bg-[color:hsl(var(--background))]"
    },
    "header": {
      "classes": "flex items-center justify-between py-4 sticky top-0 bg-white border-b border-[#E5E7EB] z-30",
      "search": "hidden md:flex w-full max-w-sm"
    },
    "cards_scroller": "flex gap-4 overflow-x-auto snap-x snap-mandatory pb-2",
    "content_split": "grid grid-cols-1 xl:grid-cols-3 gap-6",
    "history_area": "xl:col-span-2"
  },

  "navigation": {
    "sidebar_structure": [
      {"icon": "CreditCard", "label": "Tarjetas", "route": "/", "data-testid": "nav-tarjetas-link"},
      {"icon": "Activity", "label": "Movimientos", "route": "/movimientos", "data-testid": "nav-movimientos-link"},
      {"icon": "FileText", "label": "Documentos", "route": "/documentos", "data-testid": "nav-documentos-link"},
      {"icon": "Shield", "label": "Seguridad", "route": "/seguridad", "data-testid": "nav-seguridad-link"},
      {"icon": "Settings", "label": "Ajustes", "route": "/ajustes", "data-testid": "nav-ajustes-link"}
    ],
    "active_styles": "bg-black/5 rounded-md"
  },

  "components": {
    "reuse": "Usar componentes shadcn en ./components/ui/*.jsx; no usar HTML nativo para dropdown, calendar, toast, etc.",
    "core": [
      {"name": "Button", "path": "./components/ui/button.jsx"},
      {"name": "Card", "path": "./components/ui/card.jsx"},
      {"name": "Tabs", "path": "./components/ui/tabs.jsx"},
      {"name": "Switch", "path": "./components/ui/switch.jsx"},
      {"name": "Badge", "path": "./components/ui/badge.jsx"},
      {"name": "Select", "path": "./components/ui/select.jsx"},
      {"name": "Tooltip", "path": "./components/ui/tooltip.jsx"},
      {"name": "Popover", "path": "./components/ui/popover.jsx"},
      {"name": "Calendar", "path": "./components/ui/calendar.jsx"},
      {"name": "Sheet", "path": "./components/ui/sheet.jsx"},
      {"name": "Table", "path": "./components/ui/table.jsx"},
      {"name": "Toaster", "path": "./components/ui/sonner.jsx"}
    ],
    "new_jsx_scaffolds": [
      {
        "file": "/app/frontend/src/components/CardItem.jsx",
        "snippet": "import React from 'react';\nimport { Card } from './ui/card.jsx';\nimport { Badge } from './ui/badge.jsx';\nimport { Visa } from 'lucide-react';\n\nexport const CardItem = ({ selected, onClick, card }) => {\n  return (\n    <button\n      type=\"button\"\n      onClick={onClick}\n      data-testid=\"card-item-button\"\n      className={[\n        'snap-start min-w-[280px] text-left',\n        selected ? 'ring-2 ring-[color:hsl(var(--ring))] ring-offset-2 ring-offset-white' : 'ring-0'\n      ].join(' ')}\n    >\n      <Card className=\"relative overflow-hidden p-4 rounded-xl bg-white shadow-[0_10px_30px_rgba(0,0,0,0.06)]\">\n        <div className=\"absolute inset-0 pointer-events-none bg-[linear-gradient(135deg,_#00CED1_0%,_#8EEAD5_60%,_#E5FCFD_100%)] opacity-90\"/>\n        <div className=\"relative flex flex-col gap-3 text-[#0b3b3a]\">\n          <div className=\"flex items-center justify-between\">\n            <span className=\"font-medium\">{card.nombre}</span>\n            <Visa size={24} aria-hidden\"true\" />\n          </div>\n          <div className=\"text-2xl font-semibold\">${'{'}card.saldo{'}'}</div>\n          <div className=\"flex items-center gap-2\">\n            <Badge className=\"bg-white/80 text-[#0b3b3a]\">{card.tipo}</Badge>\n            {card.congelada && <Badge className=\"bg-black/20 text-[#0b3b3a]\">Congelada</Badge>}\n          </div>\n        </div>\n      </Card>\n    </button>\n  );\n};"
      },
      {
        "file": "/app/frontend/src/components/CardDetailPanel.jsx",
        "snippet": "import React from 'react';\nimport { Card } from './ui/card.jsx';\nimport { Button } from './ui/button.jsx';\nimport { Switch } from './ui/switch.jsx';\nimport { Tabs, TabsList, TabsTrigger, TabsContent } from './ui/tabs.jsx';\nimport { FileText, RefreshCcw, FolderOpen, ChevronRight } from 'lucide-react';\n\nexport const CardDetailPanel = ({ card, onFreezeToggle }) => {\n  return (\n    <Card className=\"p-4 md:p-6 bg-white rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.06)]\">\n      <div className=\"flex items-center justify-between\">\n        <h2 className=\"text-base md:text-lg font-semibold\">{card.nombre}</h2>\n        <div className=\"flex items-center gap-3\">\n          <span className=\"text-sm\">Congelar tarjeta</span>\n          <Switch\n            data-testid=\"congelar-tarjeta-switch\"\n            checked={card.congelada}\n            onCheckedChange={onFreezeToggle}\n          />\n        </div>\n      </div>\n\n      <div className=\"grid grid-cols-2 md:grid-cols-4 gap-3 mt-4\">\n        <Button data-testid=\"datos-tarjeta-button\" variant=\"secondary\" className=\"justify-start gap-2\"><FileText size={18}/> Datos de tarjeta</Button>\n        <Button data-testid=\"movimientos-button\" variant=\"secondary\" className=\"justify-start gap-2\"><RefreshCcw size={18}/> Movimientos</Button>\n        <Button data-testid=\"documentos-tarjeta-button\" variant=\"secondary\" className=\"justify-start gap-2\"><FolderOpen size={18}/> Documentos de tarjeta</Button>\n        <Button data-testid=\"ver-mas-button\" variant=\"ghost\" className=\"justify-start gap-2\">Ver más <ChevronRight size={18}/></Button>\n      </div>\n\n      <Tabs defaultValue=\"hoy\" className=\"mt-6\">\n        <TabsList className=\"grid w-full grid-cols-3\">\n          <TabsTrigger data-testid=\"historial-tab-hoy\" value=\"hoy\">Hoy</TabsTrigger>\n          <TabsTrigger data-testid=\"historial-tab-semana\" value=\"semana\">Semana</TabsTrigger>\n          <TabsTrigger data-testid=\"historial-tab-personaliza\" value=\"personaliza\">Personaliza</TabsTrigger>\n        </TabsList>\n        <TabsContent value=\"hoy\" data-testid=\"historial-content-hoy\">\n          {/* Recharts placeholder container with data-testid */}\n          <div data-testid=\"grafico-hoy\" className=\"h-[240px]\"/>\n        </TabsContent>\n        <TabsContent value=\"semana\" data-testid=\"historial-content-semana\">\n          <div data-testid=\"grafico-semana\" className=\"h-[240px]\"/>\n        </TabsContent>\n        <TabsContent value=\"personaliza\" data-testid=\"historial-content-personaliza\">\n          {/* Usar Calendar de shadcn para rango de fechas */}\n          <div className=\"mt-4\">Seleccione un rango de fechas</div>\n        </TabsContent>\n      </Tabs>\n    </Card>\n  );\n};"
      }
    ]
  },

  "buttons_and_icons": {
    "family": "Professional / Corporate",
    "shape": "rounded-md (8-12px)",
    "variants": {
      "primary": "bg-[color:hsl(var(--primary))] text-white hover:bg-[#00B3B5] focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[color:hsl(var(--ring))]",
      "secondary": "bg-[color:hsl(var(--muted))] text-[color:hsl(var(--foreground))] hover:bg-[#EAECEE]",
      "ghost": "bg-transparent text-[color:hsl(var(--foreground))] hover:bg-black/5"
    },
    "sizes": {
      "sm": "h-9 px-3",
      "md": "h-10 px-4",
      "lg": "h-12 px-5"
    },
    "icons": "Usar lucide-react. No usar emojis."
  },

  
  "states_and_interactions": {
    "hover": {
      "card": "translate-y-[-2px] shadow-[0_14px_40px_rgba(0,0,0,0.10)] transition-transform duration-200 ease-out",
      "nav": "bg-black/5",
      "button": "brightness-95"
    },
    "active": {
      "card": "translate-y-0",
      "nav": "bg-black/10"
    },
    "selected_card": "ring-2 ring-offset-2 ring-[color:hsl(var(--ring))]",
    "disabled": "opacity-50 pointer-events-none",
    "focus": "outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[color:hsl(var(--ring))]"
  },

  "motion": {
    "lib": "framer-motion",
    "install": "npm i framer-motion",
    "principles": [
      "No usar transition: all; transiciona solo propiedades necesarias",
      "Duraciones 150–250ms, curvas ease-out/ease-in-out",
      "Entrada sutil: fade + slide 8–12px"
    ],
    "examples": {
      "card_switch": "<motion.div initial={{opacity:0,y:8}} animate={{opacity:1,y:0}} transition={{duration:0.2}} />",
      "hover_raise": "whileHover={{y:-2}} whileTap={{y:0}}"
    }
  },

  "history_chart": {
    "lib": "Recharts",
    "install": "npm i recharts",
    "palette": ["#00CED1", "#FFD700", "#0F766E", "#8EEAD5"],
    "scaffold": "import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';\n\nexport const HistoryChart = ({ data, testid }) => (\n  <div className=\"h-[240px]\" data-testid={testid}>\n    <ResponsiveContainer width=\"100%\" height=\"100%\">\n      <AreaChart data={data}>\n        <defs>\n          <linearGradient id=\"c1\" x1=\"0\" y1=\"0\" x2=\"0\" y2=\"1\">\n            <stop offset=\"0%\" stopColor=\"#00CED1\" stopOpacity=\"0.5\"/>\n            <stop offset=\"100%\" stopColor=\"#00CED1\" stopOpacity=\"0\"/>\n          </linearGradient>\n        </defs>\n        <XAxis dataKey=\"x\" tick={{fontSize:12}} />\n        <YAxis tick={{fontSize:12}} />\n        <Tooltip wrapperStyle={{outline:'none'}} />\n        <Area type=\"monotone\" dataKey=\"y\" stroke=\"#00B3B5\" fill=\"url(#c1)\" strokeWidth={2} />\n      </AreaChart>\n    </ResponsiveContainer>\n  </div>\n);"
  },

  "pages_and_structure": {
    "shell_jsx": "<div className=\"grid grid-cols-1 lg:grid-cols-[260px_1fr] min-h-screen\">\n  <aside className=\"bg-[#FFD700] border-r border-[#E5E7EB] p-4\">/* nav items */</aside>\n  <main className=\"bg-[color:hsl(var(--background))]\">\n    <header className=\"flex items-center justify-between py-4 px-4 md:px-6 border-b bg-white\">Aira</header>\n    <section className=\"container mx-auto max-w-[1280px] px-4 md:px-6 py-6\">\n      <div className=\"flex gap-4 overflow-x-auto snap-x snap-mandatory pb-2\">/* CardItem list */</div>\n      <div className=\"grid grid-cols-1 xl:grid-cols-3 gap-6 mt-6\">\n        <div className=\"xl:col-span-2\">/* History + chart */</div>\n        <div>/* Side widgets (cashback, límites) */</div>\n      </div>\n    </section>\n  </main>\n</div>",
    "spanish_labels": {
      "cta": ["Datos de tarjeta", "Movimientos", "Documentos de tarjeta", "Ver más"],
      "tabs": ["Hoy", "Semana", "Personaliza"],
      "toggle": "Congelar tarjeta",
      "nav": ["Tarjetas", "Movimientos", "Documentos", "Seguridad", "Ajustes"],
      "cashback": "Cashback acumulado"
    }
  },

  "spacing": {
    "rule": "Usa 2–3x más espacio de lo que parece necesario. Evita densidad excesiva.",
    "scale": [4, 8, 12, 16, 20, 24, 32, 40, 48, 64]
  },

  "accessibility": {
    "contrast": "Asegurar AA mínimo (texto #111827 sobre #FFD700 y sobre blanco).",
    "focus": "Siempre visible (ring-2 + ring-offset-2).",
    "keyboard": "Navegación por Tab para acciones, tabs y tarjetas.",
    "language": "Texto de interfaz en español por defecto."
  },

  "data_testid_convention": {
    "rule": "kebab-case que describe el rol. Incluir en todos los elementos interactivos y de información clave.",
    "examples": [
      "data-testid=\"nav-tarjetas-link\"",
      "data-testid=\"card-item-button\"",
      "data-testid=\"congelar-tarjeta-switch\"",
      "data-testid=\"historial-tab-hoy\"",
      "data-testid=\"grafico-semana\"",
      "data-testid=\"saldo-actual-text\""
    ]
  },

  "micro_interactions": {
    "buttons": {
      "hover": "opacity-95 transition-opacity duration-150",
      "press": "scale-[0.98] transition-transform duration-150"
    },
    "cards": {
      "hover": "translate-y-[-2px] transition-transform duration-200",
      "select": "ring-2 ring-offset-2 ring-[color:hsl(var(--ring))]"
    },
    "scroll": {
      "cards_scroller": "snap-x snap-mandatory with momentum scrolling"
    }
  },

  "card_variations": {
    "main": {
      "bg": "card-cyan-mint gradient",
      "content": "Saldo grande, nombre titular, logo VISA",
      "state_selected": "ring + shadow elevación"
    },
    "credit": {
      "bg": "mismo gradiente + etiqueta 'Crédito'",
      "content": "Límite disponible y deuda",
      "example_balance": "$2,500.50"
    },
    "disposable": {
      "bg": "degradado más claro",
      "content": "Monto disponible",
      "example_balance": "$80.00"
    }
  },

  "no_transparency_rule": "No usar backgrounds transparentes. Emplear sólidos (blanco, surface, amarillo) o gradientes suaves en tarjetas y secciones decorativas.",

  "images_and_textures": {
    "usage": "Aplicar sutil textura/noise únicamente como decoración en headers o banners (<=20% del viewport). No en áreas de lectura.",
    "image_tokens": ["bg-[url('https://images.unsplash.com/photo-1613624193079-bbfce3671d2a?q=85&auto=format&fit=crop&w=1200')]", "bg-[url('https://images.unsplash.com/photo-1642182584235-be600dfef913?q=85&auto=format&fit=crop&w=1200')]", "bg-[url('https://images.unsplash.com/photo-1518640467707-6811f4a6ab73?q=85&auto=format&fit=crop&w=1200')]"]
  },

  "libraries": {
    "icons": {
      "name": "lucide-react",
      "install": "npm i lucide-react",
      "usage": "import { CreditCard } from 'lucide-react'"
    },
    "charts": {
      "name": "recharts",
      "install": "npm i recharts"
    },
    "toasts": {
      "name": "sonner",
      "path": "./components/ui/sonner.jsx",
      "usage": "import { Toaster, toast } from './components/ui/sonner.jsx'"
    }
  },

  "component_path": {
    "button": "./components/ui/button.jsx",
    "card": "./components/ui/card.jsx",
    "tabs": "./components/ui/tabs.jsx",
    "switch": "./components/ui/switch.jsx",
    "calendar": "./components/ui/calendar.jsx",
    "table": "./components/ui/table.jsx",
    "select": "./components/ui/select.jsx",
    "tooltip": "./components/ui/tooltip.jsx",
    "popover": "./components/ui/popover.jsx",
    "sheet": "./components/ui/sheet.jsx",
    "sonner": "./components/ui/sonner.jsx"
  },

  "image_urls": [
    {
      "category": "decorative-bg",
      "description": "Teal abstract texture (suave)",
      "url": "https://images.unsplash.com/photo-1613624193079-bbfce3671d2a?crop=entropy&cs=srgb&fm=jpg&q=85"
    },
    {
      "category": "decorative-bg",
      "description": "Burbujas cyan difusas",
      "url": "https://images.unsplash.com/photo-1642182584235-be600dfef913?crop=entropy&cs=srgb&fm=jpg&q=85"
    },
    {
      "category": "decorative-bg",
      "description": "Pinceladas teal sobre blanco",
      "url": "https://images.unsplash.com/photo-1518640467707-6811f4a6ab73?crop=entropy&cs=srgb&fm=jpg&q=85"
    }
  ],

  "instructions_to_main_agent": [
    "1) Sustituye tokens en src/index.css con hsl_tokens_overrides_for_index.css (mantén estructura @layer base).",
    "2) Implementa el layout_and_grid.shell. Sidebar fijo amarillo con menú e iconos lucide.",
    "3) Crea componentes CardItem.jsx y CardDetailPanel.jsx con los snippets. Incluye data-testid en TODOS los elementos interactivos.",
    "4) Añade framer-motion para transiciones de entrada y cambio de tarjeta (card_switch).",
    "5) Integra Recharts con el scaffold HistoryChart para tabs Hoy/Semana/Personaliza.",
    "6) Usa Tabs y Calendar de shadcn en la pestaña Personaliza para rango de fechas.",
    "7) Asegura estados de interacción: hover, focus-visible, selected (ring-2).",
    "8) Respeta la RESTRICCIÓN DE GRADIENTES. No apliques gradiente a áreas de lectura ni al sidebar.",
    "9) No uses fondos transparentes. Cards y secciones con sólidos/gradientes suaves únicamente.",
    "10) Usa sonner para toasts (operaciones de congelar/descongelar, errores de red).",
    "11) Internacionalización inicial en español (labels proporcionados).",
    "12) Todos los botones, vínculos, inputs, tabs, menús y mensajes clave deben tener data-testid (kebab-case)."
  ],

  "inspiration_references": {
    "dribbble": [
      "https://dribbble.com/tags/wallet-dashboard",
      "https://dribbble.com/tags/fintech-dashboard"
    ],
    "behance": [
      "https://www.behance.net/search/projects/banking%20dashboard%20ui?locale=en_US"
    ],
    "notes": "Tomar: sidebar contrastado, tarjetas cyan con datos prominentes, acciones con iconos y tabs para histórico. Mezclar layout limpio de dashboards con acentos vibrantes en tarjetas."
  }
}


<General UI UX Design Guidelines>  
    - You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms
    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text
   - NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json

 **GRADIENT RESTRICTION RULE**
NEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc
NEVER use dark gradients for logo, testimonial, footer etc
NEVER let gradients cover more than 20% of the viewport.
NEVER apply gradients to text-heavy content or reading areas.
NEVER use gradients on small UI elements (<100px width).
NEVER stack multiple gradient layers in the same viewport.

**ENFORCEMENT RULE:**
    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors

**How and where to use:**
   • Section backgrounds (not content backgrounds)
   • Hero section header content. Eg: dark to light to dark color
   • Decorative overlays and accent elements only
   • Hero section with 2-3 mild color
   • Gradients creation can be done for any angle say horizontal, vertical or diagonal

- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**

</Font Guidelines>

- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. 
   
- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.

- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.
   
- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly
    Eg: - if it implies playful/energetic, choose a colorful scheme
           - if it implies monochrome/minimal, choose a black–white/neutral scheme

**Component Reuse:**
	- Prioritize using pre-existing components from src/components/ui when applicable
	- Create new components that match the style and conventions of existing components when needed
	- Examine existing components to understand the project's component patterns before creating new ones

**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component

**Best Practices:**
	- Use Shadcn/UI as the primary component library for consistency and accessibility
	- Import path: ./components/[component-name]

**Export Conventions:**
	- Components MUST use named exports (export const ComponentName = ...)
	- Pages MUST use default exports (export default function PageName() {...})

**Toasts:**
  - Use `sonner` for toasts"
  - Sonner component are located in `/app/src/components/ui/sonner.tsx`

Use 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals.
</General UI UX Design Guidelines>
