import { PlayingCard } from "./playing-card";

interface CommunityCardsProps {
  cards: string[];
}

export const CommunityCards = ({ cards }: CommunityCardsProps) => {
  return (
    <div className="community-cards-area">
      {cards.map((card) => (
        <PlayingCard key={card} card={card} />
      ))}
    </div>
  );
};