"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import "./poker.css"; // Import the new CSS

interface Scenario {
    id: string;
    category: string;
    position: string;
    stack_size: number;
    hole_cards: string[];
    community_cards: string[];
    action_options: string[];
}

// Helper to get card details
const getCardDetails = (card: string) => {
    const rank = card.slice(0, -1);
    const suit = card.slice(-1);
    const suitSymbol = {
        's': '♠', 'h': '♥', 'd': '♦', 'c': '♣'
    }[suit] || '';
    const color = (suit === 'h' || suit === 'd') ? 'red' : 'black';
    return { rank, suit: suitSymbol, color };
};

// PlayingCard component
const PlayingCard = ({ card }: { card: string }) => {
    const { rank, suit, color } = getCardDetails(card);
    return (
        <div className={`playing-card ${color}`}>
            <span className="card-rank">{rank}</span>
            <span className="card-suit">{suit}</span>
        </div>
    );
};


export default function TrainingPage() {
  const router = useRouter();
  const [scenario, setScenario] = useState<Scenario | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchScenario = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/practice/scenarios/cash_game");
        if (!response.ok) {
          throw new Error("Failed to fetch scenario");
        }
        const data = await response.json();
        if (data.length > 0) {
          const randomIndex = Math.floor(Math.random() * data.length);
          setScenario(data[randomIndex]);
        } else {
          setScenario(null);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "An unknown error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchScenario();
  }, []);

  if (loading) {
    return <p className="text-center mt-10">Loading scenario...</p>;
  }

  if (error) {
    return <p className="text-center mt-10 text-red-500">Error: {error}</p>;
  }

  if (!scenario) {
    return <p className="text-center mt-10">No scenario found.</p>;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-800 p-4">
        <div className="poker-table">
            <div className="community-cards-area">
                {scenario.community_cards.length > 0 ? (
                    scenario.community_cards.map((card) => <PlayingCard key={card} card={card} />)
                ) : (
                    <p className="text-white">No community cards</p>
                )}
            </div>

            <div className="player-hand-area">
                {scenario.hole_cards.map((card) => <PlayingCard key={card} card={card} />)}
            </div>
        </div>
        <div className="actions-area">
            {scenario.action_options.map((action) => (
            <Button key={action} size="lg" className="min-w-[120px]">
                {action}
            </Button>
            ))}
        </div>
        <Button variant="link" className="mt-4 text-white" onClick={() => router.push('/dashboard')}>
            Back to Dashboard
        </Button>
    </div>
  );
}