import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Switch } from './ui/switch';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './ui/tabs';
import { FileText, RefreshCcw, FolderOpen, ChevronRight, Snowflake } from 'lucide-react';
import HistoryChart from './HistoryChart';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CardDetailPanel = ({ card, onCardUpdate }) => {
  const [historyData, setHistoryData] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [activeRange, setActiveRange] = useState('semana');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (card) {
      fetchCardData();
    }
  }, [card, activeRange]);

  const fetchCardData = async () => {
    try {
      setLoading(true);
      const [historyRes, transRes, docsRes] = await Promise.all([
        axios.get(`${API}/cards/${card.id}/history?range=${activeRange}`),
        axios.get(`${API}/cards/${card.id}/transactions?range=${activeRange}`),
        axios.get(`${API}/cards/${card.id}/documents`)
      ]);
      setHistoryData(historyRes.data);
      setTransactions(transRes.data);
      setDocuments(docsRes.data);
    } catch (error) {
      console.error('Error fetching card data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFreezeToggle = async (checked) => {
    try {
      const response = await axios.patch(`${API}/cards/${card.id}/freeze`, {
        frozen: checked
      });
      onCardUpdate(response.data);
    } catch (error) {
      console.error('Error toggling freeze:', error);
    }
  };

  if (!card) {
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground">
        Selecciona una tarjeta para ver detalles
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Main Card Display */}
      <Card className="p-6 bg-white rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.06)]">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-semibold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              {card.holder_name}
            </h2>
            <p className="text-sm text-muted-foreground">•••• {card.last4}</p>
          </div>
          <div className="flex items-center gap-3">
            <Snowflake size={18} className={card.frozen ? 'text-[#00CED1]' : 'text-muted-foreground'} />
            <span className="text-sm font-medium">Congelar tarjeta</span>
            <Switch
              data-testid="congelar-tarjeta-switch"
              checked={card.frozen}
              onCheckedChange={handleFreezeToggle}
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <Button
            data-testid="datos-tarjeta-button"
            variant="secondary"
            className="justify-start gap-2 bg-[#F7F8FA] hover:bg-[#E5E7EB]"
          >
            <FileText size={18} />
            <span className="text-xs md:text-sm">Datos de tarjeta</span>
          </Button>
          <Button
            data-testid="movimientos-button"
            variant="secondary"
            className="justify-start gap-2 bg-[#F7F8FA] hover:bg-[#E5E7EB]"
          >
            <RefreshCcw size={18} />
            <span className="text-xs md:text-sm">Movimientos</span>
          </Button>
          <Button
            data-testid="documentos-button"
            variant="secondary"
            className="justify-start gap-2 bg-[#F7F8FA] hover:bg-[#E5E7EB]"
          >
            <FolderOpen size={18} />
            <span className="text-xs md:text-sm">Documentos de tarjeta</span>
          </Button>
          <Button
            data-testid="ver-mas-button"
            variant="secondary"
            className="justify-start gap-2 bg-[#F7F8FA] hover:bg-[#E5E7EB]"
          >
            <ChevronRight size={18} />
            <span className="text-xs md:text-sm">Ver más</span>
          </Button>
        </div>
      </Card>

      {/* History Chart */}
      <Card className="p-6 bg-white rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.06)]">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Historial
          </h3>
          <Tabs value={activeRange} onValueChange={setActiveRange} className="w-auto">
            <TabsList data-testid="history-tabs">
              <TabsTrigger value="hoy" data-testid="tab-hoy">Hoy</TabsTrigger>
              <TabsTrigger value="semana" data-testid="tab-semana">Semana</TabsTrigger>
              <TabsTrigger value="personaliza" data-testid="tab-personaliza">Personaliza</TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
        <HistoryChart data={historyData} loading={loading} />
      </Card>

      {/* Cashback */}
      <Card className="p-4 bg-[#E5FCFD] rounded-xl border-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-[#0F766E]">Has obtenido en cashback</span>
            <div className="w-5 h-5 rounded-full bg-[#00CED1] flex items-center justify-center text-white text-xs">?</div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-[#0F766E]" data-testid="cashback-value">
              ${card.cashback.toFixed(2)}
            </span>
            <ChevronRight size={18} className="text-[#0F766E]" />
          </div>
        </div>
      </Card>

      {/* Recent Transactions */}
      <Card className="p-6 bg-white rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.06)]">
        <h3 className="text-lg font-semibold mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          Movimientos recientes
        </h3>
        <div className="space-y-3" data-testid="transactions-list">
          {transactions.slice(0, 5).map((transaction, index) => (
            <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
              <div>
                <div className="font-medium text-sm">{transaction.description}</div>
                <div className="text-xs text-muted-foreground">{transaction.category}</div>
              </div>
              <div className="text-right">
                <div className={`font-semibold text-sm ${transaction.amount < 0 ? 'text-red-600' : 'text-green-600'}`}>
                  ${Math.abs(transaction.amount).toFixed(2)}
                </div>
                <div className="text-xs text-muted-foreground">
                  {new Date(transaction.date).toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })}
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default CardDetailPanel;