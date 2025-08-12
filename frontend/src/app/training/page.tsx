"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

interface Scenario {
    id: string;
    category: string;
    position: string;
    stack_size: number;
    hole_cards: string[];
    community_cards: string[];
    action_options: string[];
}

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
          // Select a random scenario from the list
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
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
      <Card className="w-full max-w-4xl">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-2xl">Training Scenario</CardTitle>
          <Button variant="outline" onClick={() => router.push('/dashboard')}>
            Back to Dashboard
          </Button>
        </CardHeader>
        <CardContent className="grid gap-6">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="p-4 bg-gray-200 dark:bg-gray-800 rounded-lg">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Position</p>
              <p className="text-xl font-bold">{scenario.position}</p>
            </div>
            <div className="p-4 bg-gray-200 dark:bg-gray-800 rounded-lg">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Stack Size</p>
              <p className="text-xl font-bold">{scenario.stack_size} BB</p>
            </div>
            <div className="p-4 bg-gray-200 dark:bg-gray-800 rounded-lg">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Hole Cards</p>
              <p className="text-xl font-bold">{scenario.hole_cards.join(" ")}</p>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-2 text-center">Community Cards</h3>
            <div className="flex justify-center space-x-2">
              {scenario.community_cards.length > 0 ? (
                scenario.community_cards.map((card, index) => (
                  <div key={index} className="p-4 w-16 h-24 flex items-center justify-center bg-white dark:bg-gray-700 rounded-md border-2 border-gray-300 dark:border-gray-600">
                    <span className="text-2xl font-bold">{card}</span>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 dark:text-gray-400">No community cards yet.</p>
              )}
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-2 text-center">Your Action</h3>
            <div className="flex justify-center space-x-4">
              {scenario.action_options.map((action) => (
                <Button key={action} size="lg" className="min-w-[120px]">
                  {action}
                </Button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}