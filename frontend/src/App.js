import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import Sidebar from './components/Sidebar';
import CardItem from './components/CardItem';
import CardDetailPanel from './components/CardDetailPanel';
import { Button } from './components/ui/button';
import { Search, Menu } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [cards, setCards] = useState([]);
  const [selectedCardId, setSelectedCardId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [seeded, setSeeded] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      // Try to fetch cards first
      const response = await axios.get(`${API}/cards`);
      if (response.data && response.data.length > 0) {
        setCards(response.data);
        setSelectedCardId(response.data[0].id);
        setSeeded(true);
      } else {
        // No cards found, need to seed
        setSeeded(false);
      }
    } catch (error) {
      console.error('Error fetching cards:', error);
      setSeeded(false);
    } finally {
      setLoading(false);
    }
  };

  const handleSeedData = async () => {
    try {
      setLoading(true);
      await axios.post(`${API}/dev/seed`);
      await initializeApp();
    } catch (error) {
      console.error('Error seeding data:', error);
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
      <div className="flex items-center justify-center min-h-screen bg-[hsl(var(--background))]">
        <div className="text-center">
          <div className="text-2xl font-bold text-[#00CED1] mb-2" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>aira</div>
          <p className="text-muted-foreground">Cargando...</p>
        </div>
      </div>
    );
  }

  if (!seeded) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[hsl(var(--background))] px-4">
        <div className="text-center space-y-4">
          <div className="text-3xl font-bold text-[#00CED1] mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>aira</div>
          <p className="text-muted-foreground mb-4">No hay tarjetas disponibles</p>
          <Button onClick={handleSeedData} className="bg-[#00CED1] hover:bg-[#00B3B5]">
            Cargar datos de ejemplo
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-[hsl(var(--background))]" data-testid="app-container">
      <Sidebar isMobileOpen={mobileMenuOpen} onMobileClose={() => setMobileMenuOpen(false)} />
      
      <main className="flex-1 overflow-auto w-full">
        {/* Header */}
        <header className="sticky top-0 z-30 bg-white border-b border-[#E5E7EB] px-4 md:px-6 py-3 md:py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 md:gap-4 flex-1">
              {/* Mobile Menu Button */}
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setMobileMenuOpen(true)}
                className="lg:hidden hover:bg-[#F7F8FA]"
                data-testid="mobile-menu-button"
              >
                <Menu size={24} />
              </Button>
              
              <h1 className="text-xl md:text-2xl font-bold text-[#111827]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>aira</h1>
              
              {/* Search Bar - Hidden on small mobile */}
              <div className="hidden sm:flex items-center gap-2 bg-[#F7F8FA] px-3 md:px-4 py-2 rounded-lg w-full max-w-sm">
                <Search size={18} className="text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Escoger diseños"
                  className="bg-transparent border-0 outline-none w-full text-sm"
                />
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-[#00CED1] flex items-center justify-center text-white font-semibold text-sm md:text-base">
                JN
              </div>
            </div>
          </div>
        </header>

        {/* Content */}
        <div className="p-4 md:p-6 space-y-4 md:space-y-6">
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
      </main>
    </div>
  );
}

export default App;