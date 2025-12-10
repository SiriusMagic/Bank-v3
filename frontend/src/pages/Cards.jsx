import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CardItem from '../components/CardItem';
import CardDetailPanel from '../components/CardDetailPanel';
import { Button } from '../components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../components/ui/dialog';
import { Plus, CreditCard } from 'lucide-react';
import { toast } from '../components/ui/sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Cards = () => {
  const [cards, setCards] = useState([]);
  const [selectedCardId, setSelectedCardId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [selectedBrand, setSelectedBrand] = useState('VISA');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchCards();
  }, []);

  const fetchCards = async () => {
    try {
      const response = await axios.get(`${API}/cards`);
      if (response.data && response.data.length > 0) {
        setCards(response.data);
        setSelectedCardId(response.data[0].id);
      }
    } catch (error) {
      console.error('Error fetching cards:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCardSelect = (cardId) => {
    setSelectedCardId(cardId);
  };

  const handleCardUpdate = (updatedCard) => {
    setCards(cards.map(card => card.id === updatedCard.id ? updatedCard : card));
  };

  const handleCreateCard = async () => {
    setCreating(true);
    try {
      const response = await axios.post(`${API}/cards/create-disposable`, {
        brand: selectedBrand
      });
      toast.success('Tarjeta desechable creada exitosamente');
      await fetchCards();
      setShowCreateDialog(false);
    } catch (error) {
      console.error('Error creating card:', error);
      toast.error('Error al crear la tarjeta');
    } finally {
      setCreating(false);
    }
  };

  const handleReturnFunds = async (cardId) => {
    try {
      const response = await axios.post(`${API}/cards/${cardId}/return-funds`);
      toast.success(`$${response.data.amount_returned.toFixed(2)} devueltos a tu Bóveda Segura`);
      await fetchCards();
    } catch (error) {
      console.error('Error returning funds:', error);
      toast.error('Error al devolver fondos');
    }
  };

  const handleDestroyCard = async (cardId) => {
    try {
      const response = await axios.delete(`${API}/cards/${cardId}/destroy`);
      toast.success(`Tarjeta destruida. $${response.data.amount_returned.toFixed(2)} devueltos a tu Bóveda Segura`);
      await fetchCards();
      if (selectedCardId === cardId) {
        setSelectedCardId(cards.length > 1 ? cards.find(c => c.id !== cardId)?.id : null);
      }
    } catch (error) {
      console.error('Error destroying card:', error);
      toast.error('Error al destruir la tarjeta');
    }
  };

  const selectedCard = cards.find(card => card.id === selectedCardId);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-muted-foreground">Cargando tarjetas...</p>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6 space-y-4 md:space-y-6" data-testid="cards-page">
      {/* Cards Carousel */}
      <div className="space-y-3">
        <h2 className="text-base md:text-lg font-semibold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>Billeteras Operativas</h2>
        <div className="flex gap-3 md:gap-4 overflow-x-auto snap-x snap-mandatory pb-2 scrollbar-hide" data-testid="cards-list">
          {cards.map((card) => (
            <CardItem
              key={card.id}
              card={card}
              selected={card.id === selectedCardId}
              onClick={() => handleCardSelect(card.id)}
            />
          ))}
          
          {/* Create Card Module */}
          <button
            onClick={() => setShowCreateDialog(true)}
            className="flex-shrink-0 w-[280px] sm:w-[320px] h-[180px] snap-center rounded-xl border-2 border-dashed border-gray-300 hover:border-gray-400 hover:bg-gray-50 transition-all flex flex-col items-center justify-center gap-2 group"
            data-testid="create-card-btn"
          >
            <div className="w-12 h-12 rounded-full bg-gray-100 group-hover:bg-gray-200 flex items-center justify-center transition-colors">
              <Plus className="w-6 h-6 text-gray-600" />
            </div>
            <p className="text-sm font-medium text-gray-600 group-hover:text-gray-700">Crear Tarjeta Desechable</p>
          </button>
        </div>
      </div>

      {/* Card Detail Panel */}
      {selectedCard && (
        <CardDetailPanel 
          card={selectedCard} 
          onCardUpdate={handleCardUpdate}
          onReturnFunds={handleReturnFunds}
          onDestroyCard={handleDestroyCard}
        />
      )}

      {/* Create Card Dialog */}
      <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
        <DialogContent data-testid="create-card-dialog">
          <DialogHeader>
            <DialogTitle>Crear Tarjeta Desechable</DialogTitle>
            <DialogDescription>
              Selecciona el emisor de la red para tu nueva tarjeta desechable de débito.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-3">
              <label className="text-sm font-medium">Emisor de Red</label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => setSelectedBrand('VISA')}
                  className={`p-4 border-2 rounded-lg flex flex-col items-center gap-2 transition-all ${
                    selectedBrand === 'VISA' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                  }`}
                  data-testid="brand-visa"
                >
                  <CreditCard className="w-8 h-8" />
                  <span className="font-medium">VISA</span>
                </button>
                <button
                  onClick={() => setSelectedBrand('Mastercard')}
                  className={`p-4 border-2 rounded-lg flex flex-col items-center gap-2 transition-all ${
                    selectedBrand === 'Mastercard' ? 'border-orange-500 bg-orange-50' : 'border-gray-200 hover:border-gray-300'
                  }`}
                  data-testid="brand-mastercard"
                >
                  <CreditCard className="w-8 h-8" />
                  <span className="font-medium">Mastercard</span>
                </button>
              </div>
              <p className="text-xs text-gray-500 italic">Próximamente: Otras redes</p>
            </div>
            <Button 
              onClick={handleCreateCard} 
              disabled={creating}
              className="w-full"
              data-testid="confirm-create-card"
            >
              {creating ? 'Creando...' : 'Crear Tarjeta'}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Cards;