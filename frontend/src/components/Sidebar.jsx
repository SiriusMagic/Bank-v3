import React, { useState } from 'react';
import { Home, CreditCard, Activity, FileText, Settings, Users, Target, Gift, DollarSign, HelpCircle, ChevronLeft, ChevronRight, Repeat, Wallet, TrendingUp } from 'lucide-react';
import { Button } from './ui/button';

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);

  const navItems = [
    { icon: Home, label: 'Inicio', active: false },
    { icon: Wallet, label: 'Cuentas', active: false },
    { icon: CreditCard, label: 'Tarjetas', active: true },
    { icon: Repeat, label: 'Transferencia', active: false },
    { icon: Target, label: 'Misiones', active: false },
    { icon: Target, label: 'Metas', active: false },
    { icon: Gift, label: 'Subscripción', active: false },
    { icon: DollarSign, label: 'Préstamos', active: false },
    { icon: TrendingUp, label: 'Ingresos y egresos totales', active: false },
    { icon: Users, label: 'Perfil', active: false },
    { icon: Settings, label: 'Ajustes', active: false },
    { icon: HelpCircle, label: 'Ayuda', active: false },
  ];

  const toggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  return (
    <aside 
      className={`hidden lg:flex lg:flex-col bg-[#FFD700] border-r border-[#E5E7EB] transition-all duration-300 ease-in-out ${
        collapsed ? 'w-[80px]' : 'w-[260px]'
      }`} 
      data-testid="sidebar"
    >
      <div className="p-4 flex items-center justify-between">
        {!collapsed && (
          <h1 className="text-2xl font-bold text-[#111827]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            aira
          </h1>
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleSidebar}
          className="hover:bg-black/5 text-[#111827] ml-auto"
          data-testid="sidebar-toggle"
        >
          {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </Button>
      </div>

      <nav className="flex-1 px-2 space-y-1 overflow-y-auto">
        {navItems.map((item, index) => (
          <button
            key={index}
            className={`w-full flex items-center gap-3 px-3 py-2.5 text-sm font-medium text-[#111827] rounded-md transition-colors ${
              item.active ? 'bg-black/10' : 'hover:bg-black/5'
            } ${collapsed ? 'justify-center' : ''}`}
            data-testid={`nav-${item.label.toLowerCase().replace(/\s+/g, '-')}`}
            title={collapsed ? item.label : ''}
          >
            <item.icon size={20} className="flex-shrink-0" />
            {!collapsed && <span className="truncate">{item.label}</span>}
          </button>
        ))}
      </nav>

      <div className={`p-4 border-t border-black/10 ${collapsed ? 'text-center' : ''}`}>
        <p className={`text-xs text-[#111827]/60 font-medium ${collapsed ? 'transform rotate-90 origin-center' : ''}`}>
          {collapsed ? 'v1.0' : 'Versión 1.0.0'}
        </p>
        {!collapsed && (
          <p className="text-xs text-[#111827]/40 mt-1">© 2024 Aira</p>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;