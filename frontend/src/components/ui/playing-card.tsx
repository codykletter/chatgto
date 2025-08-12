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
export const PlayingCard = ({ card }: { card: string }) => {
    const { rank, suit, color } = getCardDetails(card);
    return (
        <div className={`playing-card ${color}`}>
            <span className="card-rank">{rank}</span>
            <span className="card-suit">{suit}</span>
        </div>
    );
};