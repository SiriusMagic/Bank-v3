import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Lock, ArrowDownToLine, Building2, Users, Send, TrendingUp, TrendingDown, Shield, Trophy, ChevronRight } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import TransferToCardDialog from '../components/TransferToCardDialog';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const navigate = useNavigate();
  const [vault, setVault] = useState(null);
  const [cards, setCards] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [pointsBalance, setPointsBalance] = useState(null);
  const [insurancePolicy, setInsurancePolicy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [transferDialogOpen, setTransferDialogOpen] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [vaultRes, cardsRes, transRes, pointsRes, insuranceRes] = await Promise.all([
        axios.get(`${API}/vault`),
        axios.get(`${API}/cards`),
        axios.get(`${API}/vault/transactions?limit=5`),
        axios.get(`${API}/missions/balance`),
        axios.get(`${API}/insurance/policy`)
      ]);
      setVault(vaultRes.data);
      setCards(cardsRes.data);
      setTransactions(transRes.data);
      setPointsBalance(pointsRes.data);
      setInsurancePolicy(insuranceRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTransferSuccess = async () => {
    await fetchData();
    setTransferDialogOpen(false);
  };

  // Calculate metrics
  const ingresos = transactions.filter(t => t.transaction_type === 'deposit').reduce((sum, t) => sum + t.amount, 0);
  const egresos = transactions.filter(t => t.transaction_type === 'transfer_to_card').reduce((sum, t) => sum + t.amount, 0);

  // Mock flow data
  const flowData = [
    { date: 'Lun', ingresos: 500, egresos: 200 },
    { date: 'Mar', ingresos: 300, egresos: 450 },
    { date: 'Mié', ingresos: 800, egresos: 300 },
    { date: 'Jue', ingresos: 400, egresos: 600 },
    { date: 'Vie', ingresos: 900, egresos: 400 },
    { date: 'Sáb', ingresos: 600, egresos: 350 },
    { date: 'Dom', ingresos: 200, egresos: 150 }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-muted-foreground">Cargando...</p>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6 space-y-6" data-testid="home-page">
      {/* Welcome Header */}
      <div>
        <h1 className="text-2xl md:text-3xl font-bold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          ¡Hola, Bienvenido!
        </h1>
        <p className="text-sm text-muted-foreground mt-1">
          Tu centro de control financiero
        </p>
      </div>

      {/* Main Vault Module */}
      <Card className="p-6 md:p-8 bg-gradient-to-br from-[#0284C7] to-[#0369A1] text-white relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white rounded-full transform translate-x-32 -translate-y-32"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-white rounded-full transform -translate-x-24 translate-y-24"></div>
        </div>

        <div className="relative space-y-6">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Lock size={24} />
                <p className="text-sm opacity-90">Bóveda Segura</p>
              </div>
              <h2 className="text-xl md:text-2xl font-bold mb-1" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {vault?.name || 'Mi Bóveda'}
              </h2>
            </div>
            <Badge className="bg-white/20 text-white border-0 hover:bg-white/30">
              Protegida
            </Badge>
          </div>

          <div>
            <p className="text-sm opacity-90 mb-2">Saldo Principal</p>
            <div className="text-4xl md:text-5xl font-bold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              ${vault?.balance.toLocaleString('es-ES', { minimumFractionDigits: 2 })}
            </div>
          </div>

          <Button
            onClick={() => setTransferDialogOpen(true)}
            className="w-full md:w-auto bg-white text-[#0284C7] hover:bg-gray-100 font-semibold h-12 px-8"
          >
            <ArrowDownToLine size={20} className="mr-2" />
            Transferir a Tarjetas
          </Button>
        </div>
      </Card>

      {/* Quick Transactions */}
      <div>
        <h2 className="text-lg font-semibold mb-3" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          Transacciones Rápidas
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <Button variant="outline" className="h-20 flex-col gap-2 hover:border-[#00CED1] hover:bg-[#00CED1]/5">
            <Building2 size={24} className="text-[#00CED1]" />
            <span className="text-xs">Recarga Banco del Barrio</span>
          </Button>
          <Button variant="outline" className="h-20 flex-col gap-2 hover:border-[#E91E63] hover:bg-[#E91E63]/5">
            <Users size={24} className="text-[#E91E63]" />
            <span className="text-xs">Pedir a Contactos</span>
          </Button>
          <Button variant="outline" className="h-20 flex-col gap-2 hover:border-[#FFD700] hover:bg-[#FFD700]/5">
            <Send size={24} className="text-[#FFD700]" />
            <span className="text-xs">Transferir a Cuentas Externas</span>
          </Button>
        </div>
      </div>

      {/* Metrics and Flow Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Ingresos */}
        <Card className="p-4">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Ingresos Totales</p>
              <p className="text-2xl font-bold text-green-600" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                ${ingresos.toFixed(2)}
              </p>
              <p className="text-xs text-muted-foreground mt-1">Este mes</p>
            </div>
            <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
              <TrendingUp size={24} className="text-green-600" />
            </div>
          </div>
        </Card>

        {/* Egresos */}
        <Card className="p-4">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Egresos Totales</p>
              <p className="text-2xl font-bold text-red-600" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                ${egresos.toFixed(2)}
              </p>
              <p className="text-xs text-muted-foreground mt-1">Este mes</p>
            </div>
            <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
              <TrendingDown size={24} className="text-red-600" />
            </div>
          </div>
        </Card>

        {/* Net */}
        <Card className="p-4">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Balance Neto</p>
              <p className={`text-2xl font-bold ${(ingresos - egresos) >= 0 ? 'text-green-600' : 'text-red-600'}`} style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                ${(ingresos - egresos).toFixed(2)}
              </p>
              <p className="text-xs text-muted-foreground mt-1">Este mes</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Flow Chart */}
      <Card className="p-4 md:p-6">
        <h3 className="text-base md:text-lg font-semibold mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          Flujo de Dinero (Semana)
        </h3>
        <div className="w-full h-64">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={flowData}>
              <defs>
                <linearGradient id="colorIngresos" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10B981" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#10B981" stopOpacity={0.1} />
                </linearGradient>
                <linearGradient id="colorEgresos" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#EF4444" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#EF4444" stopOpacity={0.1} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis dataKey="date" tick={{ fill: '#4B5563', fontSize: 12 }} />
              <YAxis tick={{ fill: '#4B5563', fontSize: 12 }} tickFormatter={(value) => `$${value}`} />
              <Tooltip />
              <Area type="monotone" dataKey="ingresos" stroke="#10B981" fillOpacity={1} fill="url(#colorIngresos)" />
              <Area type="monotone" dataKey="egresos" stroke="#EF4444" fillOpacity={1} fill="url(#colorEgresos)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Recent Transactions */}
      {transactions.length > 0 && (
        <Card className="p-4 md:p-6">
          <h3 className="text-base md:text-lg font-semibold mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Historial Rápido
          </h3>
          <div className="space-y-3">
            {transactions.map((trans, index) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                <div>
                  <p className="font-medium text-sm">{trans.description}</p>
                  <p className="text-xs text-muted-foreground">
                    {new Date(trans.date).toLocaleDateString('es-ES', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
                <p className={`font-semibold text-sm ${
                  trans.transaction_type === 'deposit' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {trans.transaction_type === 'deposit' ? '+' : '-'}${Math.abs(trans.amount).toFixed(2)}
                </p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Promotion Modules */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Insurance Widget */}
        <Card 
          className="p-4 md:p-6 cursor-pointer hover:shadow-lg transition-all group"
          onClick={() => navigate('/seguros')}
        >
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-full bg-[#00CED1]/10 flex items-center justify-center flex-shrink-0 group-hover:bg-[#00CED1] transition-colors">
              <Shield size={24} className="text-[#00CED1] group-hover:text-white transition-colors" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-base mb-1">Seguros</h3>
              {insurancePolicy ? (
                <p className="text-sm text-muted-foreground">
                  Estás Cubierto. <strong>{insurancePolicy.plan_name}</strong> activo.
                </p>
              ) : (
                <p className="text-sm text-muted-foreground">
                  Tu Bóveda necesita un Paracaídas de Emergencia. ¡Cúbrete con el Plan Único!
                </p>
              )}
            </div>
            <ChevronRight size={20} className="text-muted-foreground" />
          </div>
        </Card>

        {/* Missions Widget */}
        <Card 
          className="p-4 md:p-6 cursor-pointer hover:shadow-lg transition-all group"
          onClick={() => navigate('/misiones')}
        >
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-full bg-[#FFD700]/10 flex items-center justify-center flex-shrink-0 group-hover:bg-[#FFD700] transition-colors">
              <Trophy size={24} className="text-[#FFD700] group-hover:text-white transition-colors" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-base mb-1">Misiones</h3>
              <p className="text-sm text-muted-foreground">
                Llevas <strong>{pointsBalance?.total_points || 0} Puntos</strong>. ¡Canjea por efectivo o descuentos!
              </p>
            </div>
            <ChevronRight size={20} className="text-muted-foreground" />
          </div>
        </Card>
      </div>

      {/* Transfer Dialog */}
      <TransferToCardDialog
        open={transferDialogOpen}
        onClose={() => setTransferDialogOpen(false)}
        vault={vault}
        cards={cards}
        onSuccess={handleTransferSuccess}
      />
    </div>
  );
};

export default Home;