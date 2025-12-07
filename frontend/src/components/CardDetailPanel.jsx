import React from 'react';
import { Card } from './ui/card.jsx';
import { Button } from './ui/button.jsx';
import { Switch } from './ui/switch.jsx';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './ui/tabs.jsx';
import { FileText, RefreshCcw, FolderOpen, ChevronRight } from 'lucide-react';

export const CardDetailPanel = ({ card, onFreezeToggle }) => {
  return (
    <Card className="p-4 md:p-6 bg-white rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.06)]">
      <div className="flex items-center justify-between">
        <h2 className="text-base md:text-lg font-semibold">{card?.nombre || 'Tarjeta'}</h2>
        <div className="flex items-center gap-3">
          <span className="text-sm">Congelar tarjeta</span>
          <Switch
            data-testid="congelar-tarjeta-switch"
            checked={!!card?.congelada}
            onCheckedChange={onFreezeToggle}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
        <Button data-testid="datos-tarjeta-button" variant="secondary" className="justify-start gap-2"><FileText size={18}/> Datos de tarjeta</Button>
        <Button data-testid="movimientos-button" variant="secondary" className="justify-start gap-2"><RefreshCcw size={18}/> Movimientos</Button>
        <Button data-testid="documentos-tarjeta-button" variant="secondary" className="justify-start gap-2"><FolderOpen size={18}/> Documentos de tarjeta</Button>
        <Button data-testid="ver-mas-button" variant="ghost" className="justify-start gap-2">Ver más <ChevronRight size={18}/></Button>
      </div>

      <Tabs defaultValue="hoy" className="mt-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger data-testid="historial-tab-hoy" value="hoy">Hoy</TabsTrigger>
          <TabsTrigger data-testid="historial-tab-semana" value="semana">Semana</TabsTrigger>
          <TabsTrigger data-testid="historial-tab-personaliza" value="personaliza">Personaliza</TabsTrigger>
        </TabsList>
        <TabsContent value="hoy" data-testid="historial-content-hoy">
          <div data-testid="grafico-hoy" className="h-[240px]"/>
        </TabsContent>
        <TabsContent value="semana" data-testid="historial-content-semana">
          <div data-testid="grafico-semana" className="h-[240px]"/>
        </TabsContent>
        <TabsContent value="personaliza" data-testid="historial-content-personaliza">
          <div className="mt-4">Seleccione un rango de fechas</div>
        </TabsContent>
      </Tabs>
    </Card>
  );
};
