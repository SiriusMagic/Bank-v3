import React, { useState } from 'react';
import { Home, CreditCard, Activity, FileText, Settings, Users, Target, Gift, DollarSign, HelpCircle, ChevronLeft, ChevronRight, Repeat, Wallet, TrendingUp, X } from 'lucide-react';
import { Button } from './ui/button';
import { Sheet, SheetContent, SheetHeader, SheetTitle } from './ui/sheet';

const Sidebar = ({ isMobileOpen, onMobileClose }) => {
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

  const SidebarContent = ({ isMobile = false }) => (
    <>
      <div className={`p-4 flex items-center ${isMobile ? 'justify-between' : 'justify-between'}`}>
        {(!collapsed || isMobile) && (
          <h1 className="text-2xl font-bold text-[#111827]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            aira
          </h1>
        )}
        {!isMobile && (
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleSidebar}
            className="hover:bg-black/5 text-[#111827] ml-auto"
            data-testid="sidebar-toggle"
          >
            {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
          </Button>
        )}
        {isMobile && (
          <Button
            variant="ghost"
            size="icon"
            onClick={onMobileClose}
            className="hover:bg-black/5 text-[#111827]"
            data-testid="mobile-menu-close"
          >
            <X size={20} />
          </Button>
        )}
      </div>

      <nav className="flex-1 px-2 space-y-0.5 overflow-y-auto">
        {navItems.map((item, index) => (
          <button
            key={index}
            onClick={isMobile ? onMobileClose : undefined}
            className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium text-[#111827] rounded-md transition-colors ${
              item.active ? 'bg-black/10' : 'hover:bg-black/5'
            } ${collapsed && !isMobile ? 'justify-center' : ''}`}
            data-testid={`nav-${item.label.toLowerCase().replace(/\s+/g, '-')}`}
            title={collapsed && !isMobile ? item.label : ''}
          >
            <item.icon size={18} className="flex-shrink-0" />
            {(!collapsed || isMobile) && <span className="truncate text-xs">{item.label}</span>}
          </button>
        ))}
      </nav>

      <div className={`px-4 py-3 border-t border-black/10 flex-shrink-0 ${collapsed && !isMobile ? 'text-center' : ''}`} data-testid="sidebar-version">
        <p className={`text-xs text-[#111827]/60 font-medium ${collapsed && !isMobile ? 'transform rotate-90 origin-center whitespace-nowrap' : ''}`}>
          {collapsed && !isMobile ? 'v1.0' : 'Versión 1.0.0'}
        </p>
        {(!collapsed || isMobile) && (
          <p className="text-xs text-[#111827]/40 mt-1">© 2024 Aira</p>
        )}
      </div>
    </>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside 
        className={`hidden lg:flex lg:flex-col bg-[#FFD700] border-r border-[#E5E7EB] transition-all duration-300 ease-in-out ${
          collapsed ? 'w-[80px]' : 'w-[260px]'
        }`} 
        data-testid="sidebar"
      >
        <SidebarContent />
      </aside>

      {/* Mobile Drawer */}
      <Sheet open={isMobileOpen} onOpenChange={onMobileClose}>
        <SheetContent side="left" className="w-[280px] p-0 bg-[#FFD700] border-r border-[#E5E7EB]">
          <div className="flex flex-col h-full" data-testid="mobile-sidebar">
            <SidebarContent isMobile={true} />
          </div>
        </SheetContent>
      </Sheet>
    </>
  );
};

export default Sidebar;