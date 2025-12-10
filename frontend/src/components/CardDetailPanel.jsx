import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from './ui/button';
import { Snowflake, Lock, Unlock, Download, Eye, EyeOff, ArrowUpRight, Trash2 } from 'lucide-react';
import { Card } from './ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { toast } from './ui/sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CardDetailPanel = ({ card, onCardUpdate, onReturnFunds, onDestroyCard }) => {
  const [history, setHistory] = useState([]);
  const [showCardNumber, setShowCardNumber] = useState(false);
  const [showCVV, setShowCVV] = useState(false);
  const [freezing, setFreezing] = useState(false);
  const [destroying, setDestroying] = useState(false);

  useEffect(() => {
    if (card?.id) {
      fetchHistory();
    }
  }, [card?.id]);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API}/cards/${card.id}/history`);
      setHistory(response.data);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handleFreeze = async () => {
    setFreezing(true);
    try {
      await axios.patch(`${API}/cards/${card.id}/freeze`, {
        frozen: !card.frozen
      });
      onCardUpdate({ ...card, frozen: !card.frozen });
      toast.success(card.frozen ? 'Tarjeta desbloqueada' : 'Tarjeta congelada');
    } catch (error) {
      console.error('Error freezing card:', error);
      toast.error('Error al actualizar el estado de la tarjeta');
    } finally {
      setFreezing(false);
    }
  };

  const handleReturnFunds = async () => {
    if (card.balance <= 0) {
      toast.error('No hay fondos para devolver');
      return;
    }
    await onReturnFunds(card.id);
  };

  const handleDestroy = async () => {
    if (destroying) return;
    
    setDestroying(true);
    setTimeout(async () => {
      await onDestroyCard(card.id);
      setDestroying(false);
    }, 800);
  };

  const chartData = history.slice(0, 7).reverse().map(item => ({
    date: new Date(item.date).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' }),
    amount: item.amount
  }));

  if (!card) {
    return null;
  }

  return (
    <div className={`space-y-4 transition-all duration-800 ${destroying ? 'animate-pulse opacity-50' : ''}`} data-testid="card-detail-panel">
      {/* Card Info Card */}
      <Card className="p-4 md:p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Detalles de Tarjeta
          </h3>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleFreeze}
              disabled={freezing}
              data-testid="freeze-card-btn"
            >
              {card.frozen ? <Unlock size={16} /> : <Lock size={16} />}
              <span className="ml-2">{card.frozen ? 'Desbloquear' : 'Congelar'}</span>
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-xs text-muted-foreground mb-1">Número de Tarjeta</p>
            <div className="flex items-center gap-2">
              <p className="font-mono text-sm">
                {showCardNumber ? `4532 ${card.last4} XXXX XXXX` : `•••• •••• •••• ${card.last4}`}
              </p>
              <Button
                variant="ghost"
                size="icon"
                className="h-6 w-6"
                onClick={() => setShowCardNumber(!showCardNumber)}
                data-testid="toggle-card-number"
              >
                {showCardNumber ? <EyeOff size={14} /> : <Eye size={14} />}
              </Button>
            </div>
          </div>

          <div>
            <p className="text-xs text-muted-foreground mb-1">CVV</p>
            <div className="flex items-center gap-2">
              <p className="font-mono text-sm">{showCVV ? '123' : '•••'}</p>
              <Button
                variant="ghost"
                size="icon"
                className="h-6 w-6"
                onClick={() => setShowCVV(!showCVV)}
                data-testid="toggle-cvv"
              >
                {showCVV ? <EyeOff size={14} /> : <Eye size={14} />}
              </Button>
            </div>
          </div>

          <div>
            <p className="text-xs text-muted-foreground mb-1">Vencimiento</p>
            <p className="font-mono text-sm">{card.exp_month}/{card.exp_year}</p>
          </div>

          <div>
            <p className="text-xs text-muted-foreground mb-1">Titular</p>
            <p className="text-sm">{card.holder_name}</p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="pt-4 border-t flex flex-col sm:flex-row gap-2">
          <Button
            variant="default"
            className="flex-1"
            onClick={handleReturnFunds}
            disabled={card.balance <= 0}
            data-testid="return-funds-btn"
          >
            <ArrowUpRight size={16} className="mr-2" />
            Enviar Fondos a Bóveda
          </Button>
          <Button
            variant="destructive"
            className="flex-1"
            onClick={handleDestroy}
            disabled={destroying || card.type === 'debit' || card.type === 'credit'}
            data-testid="destroy-card-btn"
          >
            <Trash2 size={16} className="mr-2" />
            {destroying ? 'Destruyendo...' : 'Destruir Tarjeta'}
          </Button>
        </div>
        
        {(card.type === 'debit' || card.type === 'credit') && (
          <p className="text-xs text-muted-foreground italic text-center">Las tarjetas fijas no pueden ser destruidas</p>
        )}
      </Card>

      {/* Transaction History Chart */}
      {history.length > 0 && (
        <Card className="p-4 md:p-6 space-y-4">
          <h3 className="text-lg font-semibold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Historial de Transacciones
          </h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="date" tick={{ fontSize: 12 }} stroke="#9ca3af" />
              <YAxis tick={{ fontSize: 12 }} stroke="#9ca3af" />
              <Tooltip />
              <Line type="monotone" dataKey="amount" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      )}

      {/* Transaction List */}
      {history.length > 0 && (
        <Card className="p-4 md:p-6 space-y-4">
          <h3 className="text-lg font-semibold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Últimas Transacciones
          </h3>
          <div className="space-y-2">
            {history.slice(0, 5).map((item) => (
              <div key={item.id} className="flex items-center justify-between py-2 border-b last:border-0">
                <div>
                  <p className="text-sm font-medium">{item.description}</p>
                  <p className="text-xs text-muted-foreground">{item.category}</p>
                </div>
                <div className="text-right">
                  <p className={`text-sm font-semibold ${item.amount < 0 ? 'text-red-600' : 'text-green-600'}`}>
                    ${Math.abs(item.amount).toFixed(2)}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {new Date(item.date).toLocaleDateString('es-ES')}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};

export default CardDetailPanel;