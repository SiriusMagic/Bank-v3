import React from 'react';
import { Home, CreditCard, Activity, FileText, Settings, Users, Target, Gift, DollarSign, HelpCircle } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { icon: Home, label: 'Inicio', active: false },
    { icon: Users, label: 'Cuentas', active: false },
    { icon: CreditCard, label: 'Tarjetas', active: true },
    { icon: Activity, label: 'Transfere', active: false },
    { icon: Target, label: 'Misiones', active: false },
    { icon: Target, label: 'Metas', active: false },
    { icon: Gift, label: 'Subscripct', active: false },
    { icon: DollarSign, label: 'Microprés', active: false },
    { icon: DollarSign, label: 'Ingresos y egresos', active: false },
    { icon: Users, label: 'Perfil', active: false },
    { icon: Settings, label: 'Ajustes', active: false },
    { icon: HelpCircle, label: 'Ayuda', active: false },
  ];

  return (
    <aside className="hidden lg:flex lg:flex-col w-[260px] bg-[#FFD700] border-r border-[#E5E7EB] p-4" data-testid="sidebar">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-[#111827]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>aira</h1>
      </div>
      <nav className="flex-1 space-y-1">
        {navItems.map((item, index) => (
          <button
            key={index}
            className={`w-full flex items-center gap-3 px-3 py-2.5 text-sm font-medium text-[#111827] rounded-md transition-colors ${
              item.active ? 'bg-black/5' : 'hover:bg-black/5'
            }`}
            data-testid={`nav-${item.label.toLowerCase().replace(' ', '-')}`}
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;