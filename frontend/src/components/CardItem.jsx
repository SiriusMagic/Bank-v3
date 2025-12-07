import React from 'react';
import { Card } from './ui/card.jsx';
import { Badge } from './ui/badge.jsx';
import { CreditCard } from 'lucide-react';

export const CardItem = ({ selected, onClick, card }) => {
  return (
    <button
      type="button"
      onClick={onClick}
      data-testid="card-item-button"
      className={[
        'snap-start min-w-[280px] text-left rounded-xl',
        selected ? 'ring-2 ring-[color:hsl(var(--ring))] ring-offset-2 ring-offset-white' : 'ring-0'
      ].join(' ')}
    >
      <Card className="relative overflow-hidden p-4 bg-white shadow-[0_10px_30px_rgba(0,0,0,0.06)] rounded-xl">
        <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(135deg,_#00CED1_0%,_#8EEAD5_60%,_#E5FCFD_100%)] opacity-90" />
        <div className="relative flex flex-col gap-3 text-[#0b3b3a]">
          <div className="flex items-center justify-between">
            <span className="font-medium">{card.nombre}</span>
            <CreditCard size={20} aria-hidden="true" />
          </div>
          <div className="text-2xl font-semibold" data-testid="saldo-actual-text">{card.saldo}</div>
          <div className="flex items-center gap-2">
            <Badge className="bg-white/80 text-[#0b3b3a]" data-testid="card-tipo-badge">{card.tipo}</Badge>
            {card.congelada && <Badge className="bg-black/20 text-[#0b3b3a]" data-testid="card-congelada-badge">Congelada</Badge>}
          </div>
        </div>
      </Card>
    </button>
  );
};
