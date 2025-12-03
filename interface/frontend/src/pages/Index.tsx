import { useState } from "react";
import PredictionForm from "@/components/PredictionForm";
import PredictionResult from "@/components/PredictionResult";
import MarketTrends from "@/components/MarketTrends";
import { Building2 } from "lucide-react";

interface PredictionData {
  price: number;
  minPrice: number;
  maxPrice: number;
}

const Index = () => {
  const [predictionResult, setPredictionResult] = useState<PredictionData | null>(null);

  return (
    <div className="min-h-screen bg-gradient-bg">

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 md:py-12">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Introduction */}
          <div className="text-center space-y-3 animate-in fade-in-50 slide-in-from-top-4 duration-700">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground">
              Estimez le prix de votre bien immobilier
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Obtenez une estimation précise basée sur l'intelligence artificielle et les données du marché tunisien
            </p>
          </div>

          {/* Form */}
          <div className="animate-in fade-in-50 slide-in-from-bottom-4 duration-700 delay-150">
            <PredictionForm onPredictionResult={setPredictionResult} />
          </div>

          {/* Results */}
          {predictionResult && (
            <div className="mt-8">
              <PredictionResult 
                price={predictionResult.price}
                minPrice={predictionResult.minPrice}
                maxPrice={predictionResult.maxPrice}
              />
            </div>
          )}

          {/* Info Section */}
          {!predictionResult && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 animate-in fade-in-50 slide-in-from-bottom-4 duration-700 delay-300">
              <div className="bg-card/50 backdrop-blur-sm rounded-xl p-6 shadow-md border border-border/50 hover:shadow-lg transition-all">
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <span className="text-2xl">🎯</span>
                </div>
                <h3 className="font-semibold text-foreground mb-2">Précision</h3>
                <p className="text-sm text-muted-foreground">
                  Modèle entraîné sur des milliers de transactions immobilières réelles
                </p>
              </div>

              <div className="bg-card/50 backdrop-blur-sm rounded-xl p-6 shadow-md border border-border/50 hover:shadow-lg transition-all">
                <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-4">
                  <span className="text-2xl">⚡</span>
                </div>
                <h3 className="font-semibold text-foreground mb-2">Rapide</h3>
                <p className="text-sm text-muted-foreground">
                  Obtenez une estimation en quelques secondes seulement
                </p>
              </div>

              <div className="bg-card/50 backdrop-blur-sm rounded-xl p-6 shadow-md border border-border/50 hover:shadow-lg transition-all">
                <div className="w-12 h-12 rounded-lg bg-success/10 flex items-center justify-center mb-4">
                  <span className="text-2xl">🇹🇳</span>
                </div>
                <h3 className="font-semibold text-foreground mb-2">Local</h3>
                <p className="text-sm text-muted-foreground">
                  Spécialisé dans le marché immobilier tunisien
                </p>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/40 bg-card/30 backdrop-blur-lg mt-16">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-sm text-muted-foreground">
            © 2025 ImmoPredict Tunisie
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
