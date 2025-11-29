import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, AlertCircle } from "lucide-react";

interface PredictionResultProps {
  price: number;
  minPrice: number;
  maxPrice: number;
}

export default function PredictionResult({ price, minPrice, maxPrice }: PredictionResultProps) {
  const formatPrice = (value: number) => {
    return new Intl.NumberFormat('fr-TN', {
      style: 'currency',
      currency: 'TND',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const errorMargin = Math.round(price - minPrice);

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-xl border-0 bg-gradient-to-br from-primary/5 to-accent/5 backdrop-blur-sm animate-in fade-in-50 slide-in-from-bottom-4 duration-500">
      <CardHeader className="pb-4">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-success/10">
            <TrendingUp className="h-5 w-5 text-success" />
          </div>
          <CardTitle className="text-2xl font-bold">Estimation du Prix</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Prix estimé principal */}
        <div className="text-center py-6 px-4 bg-gradient-primary rounded-xl shadow-lg">
          <p className="text-sm font-medium text-primary-foreground/80 mb-2">Prix estimé</p>
          <p className="text-5xl font-bold text-primary-foreground mb-1">
            {formatPrice(price)}
          </p>
          <p className="text-xs text-primary-foreground/70">
            Basé sur les données du marché tunisien
          </p>
        </div>

        {/* Intervalle de confiance */}
        <div className="bg-card rounded-lg p-5 space-y-4 shadow-md">
          <div className="flex items-start gap-2">
            <AlertCircle className="h-5 w-5 text-accent mt-0.5" />
            <div className="flex-1">
              <h3 className="font-semibold text-foreground mb-2">Intervalle de confiance</h3>
              <p className="text-sm text-muted-foreground mb-3">
                Le prix réel devrait se situer dans cette fourchette (± {formatPrice(errorMargin)})
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-background/50 rounded-lg p-4 border border-border">
              <p className="text-xs text-muted-foreground mb-1">Prix minimum</p>
              <p className="text-2xl font-bold text-foreground">{formatPrice(minPrice)}</p>
            </div>
            <div className="bg-background/50 rounded-lg p-4 border border-border">
              <p className="text-xs text-muted-foreground mb-1">Prix maximum</p>
              <p className="text-2xl font-bold text-foreground">{formatPrice(maxPrice)}</p>
            </div>
          </div>
        </div>

        {/* Note d'information */}
        <div className="bg-muted/50 rounded-lg p-4 text-sm text-muted-foreground">
          <p className="text-center">
            💡 <span className="font-medium">Cette estimation est basée sur un modèle d'apprentissage automatique</span> entraîné sur des données réelles du marché immobilier tunisien.
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
