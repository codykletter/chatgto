"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import "./poker.css"; // Import the new CSS

interface GtoAction {
    action: string;
    ev: number;
    explanation?: string;
}

interface Scenario {
    id: string;
    category: string;
    position: string;
    stack_size: number;
    hole_cards: string[];
    community_cards: string[];
    gto_actions: GtoAction[];
    correct_action: GtoAction;
}

interface Feedback {
    is_correct: boolean;
    chosen_action_ev: number;
    correct_action: GtoAction;
    ev_difference: number;
    explanation: string;
    alternative_line: GtoAction[] | null;
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
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [isActionTaken, setIsActionTaken] = useState(false);

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

  useEffect(() => {
    fetchScenario();
  }, []);

  const handleAction = async (action: string) => {
    if (!scenario) return;
    setIsActionTaken(true);
    try {
      const response = await fetch("http://localhost:8000/api/v1/practice/attempt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario_id: scenario.id, action: action }),
      });
      if (!response.ok) throw new Error("Failed to submit action");
      const data = await response.json();
      setFeedback(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unknown error occurred");
    }
  };

  const fetchNextScenario = () => {
    setLoading(true);
    setFeedback(null);
    setIsActionTaken(false);
    setScenario(null);
    fetchScenario();
  }

  if (loading) return <p className="text-center mt-10">Loading scenario...</p>;
  if (error) return <p className="text-center mt-10 text-red-500">Error: {error}</p>;
  if (!scenario) return <p className="text-center mt-10">No scenario found.</p>;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-4">
        <div className="poker-table">
            <div className="community-cards-area">
                {scenario.community_cards.length > 0 ? (
                    scenario.community_cards.map((card) => <PlayingCard key={card} card={card} />)
                ) : (
                    <p className="text-gray-400">Pre-flop</p>
                )}
            </div>
            <div className="player-hand-area">
                {scenario.hole_cards.map((card) => <PlayingCard key={card} card={card} />)}
            </div>
        </div>
        <div className="actions-area">
            {scenario.gto_actions.map((gto_action) => (
              <Button key={gto_action.action} size="lg" className="min-w-[120px]" onClick={() => handleAction(gto_action.action)} disabled={isActionTaken}>
                  {gto_action.action}
              </Button>
            ))}
        </div>
        {feedback && (
            <div className="feedback-area mt-4 p-4 rounded-lg bg-gray-800 w-full max-w-2xl text-center">
                <h2 className={`text-2xl font-bold mb-2 ${feedback.is_correct ? "text-green-400" : "text-red-400"}`}>
                    {feedback.is_correct ? "Correct!" : "Incorrect"}
                </h2>
                <p className="text-lg">{feedback.explanation}</p>
                <div className="grid grid-cols-2 gap-4 mt-4 text-left">
                    <div className="bg-gray-700 p-3 rounded">
                        <h3 className="font-bold">Your Play</h3>
                        <p>EV: <span className="font-mono">{feedback.chosen_action_ev.toFixed(2)}</span></p>
                    </div>
                    <div className="bg-gray-700 p-3 rounded">
                        <h3 className="font-bold">Optimal Play</h3>
                        <p>Action: {feedback.correct_action.action}</p>
                        <p>EV: <span className="font-mono">{feedback.correct_action.ev.toFixed(2)}</span></p>
                    </div>
                </div>
                <p className="mt-4 text-lg">EV Difference: <span className={`font-mono ${feedback.ev_difference < 0 ? 'text-red-400' : 'text-green-400'}`}>{feedback.ev_difference.toFixed(2)}</span></p>
                {feedback.alternative_line && (
                    <div className="mt-4 pt-4 border-t border-gray-600">
                        <h3 className="text-xl font-bold mb-2">Alternative Lines</h3>
                        {feedback.alternative_line.map(alt => (
                            <div key={alt.action} className="bg-gray-700 p-3 rounded mb-2 text-left">
                                <p><span className="font-bold">{alt.action}</span> (EV: <span className="font-mono">{alt.ev.toFixed(2)}</span>)</p>
                                {alt.explanation && <p className="text-sm text-gray-400 mt-1">{alt.explanation}</p>}
                            </div>
                        ))}
                    </div>
                )}
                <Button onClick={fetchNextScenario} className="mt-4">
                    Next Scenario
                </Button>
            </div>
        )}
        <Button variant="link" className="mt-4 text-white" onClick={() => router.push('/dashboard')}>
            Back to Dashboard
        </Button>
    </div>
  );
}