import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CardItem from '../components/CardItem';
import CardDetailPanel from '../components/CardDetailPanel';
import { Button } from '../components/ui/button';
import { Search } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Cards = () => {
  const [cards, setCards] = useState([]);
  const [selectedCardId, setSelectedCardId] = useState(null);
  const [loading, setLoading] = useState(true);

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
      {/* Cards Scroller */}
      <div className="space-y-3">
        <h2 className="text-base md:text-lg font-semibold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>Mis Tarjetas</h2>
        <div className="flex gap-3 md:gap-4 overflow-x-auto snap-x snap-mandatory pb-2 scrollbar-hide" data-testid="cards-list">
          {cards.map((card) => (
            <CardItem
              key={card.id}
              card={card}
              selected={card.id === selectedCardId}
              onClick={() => handleCardSelect(card.id)}
            />
          ))}
        </div>
      </div>

      {/* Card Detail Panel */}
      <CardDetailPanel card={selectedCard} onCardUpdate={handleCardUpdate} />
    </div>
  );
};

export default Cards;