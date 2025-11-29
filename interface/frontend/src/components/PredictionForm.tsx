import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Home, MapPin, Ruler, Calendar, Bath, BedDouble } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface FormData {
  room_count: string;
  bathroom_count: string;
  size: string;
  location: string;
  category: string;
  type: string;
}

interface PredictionFormProps {
  onPredictionResult: (result: {
    price: number;
    minPrice: number;
    maxPrice: number;
  }) => void;
}

const tunisianCities = [
  "ariana",
  "mahdia",
  "sousse",
  "tunis",
  "nabeul",
  "ben arous",
  "zaghouan",
  "la manouba",
  "bizerte",
  "sfax",
  "monastir",
  "médenine",
  "gabès",
  "gafsa",
  "béja",
  "kasserine",
  "kairouan",
  "tozeur",
  "jendouba",
  "le kef",
  "sidi bouzid",
  "siliana",
  "tataouine",
].map((city) => city.charAt(0).toUpperCase() + city.slice(1));

const categories = [
  "Appartements",
  "Terrains et Fermes",
  "Bureaux et Plateaux",
  "Maisons et Villas",
  "Locations de vacances",
  "Colocations",
];

export default function PredictionForm({
  onPredictionResult,
}: PredictionFormProps) {
  const { toast } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    room_count: "",
    bathroom_count: "",
    size: "",
    location: "",
    category: "",
    type: "",
  });

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (
      !formData.room_count ||
      !formData.bathroom_count ||
      !formData.size ||
      !formData.location ||
      !formData.category ||
      !formData.type
    ) {
      toast({
        title: "Champs manquants",
        description: "Veuillez remplir tous les champs du formulaire.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);

    try {
      const API_URL = "http://localhost:5000/predict";

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          room_count: parseFloat(formData.room_count),
          bathroom_count: parseFloat(formData.bathroom_count),
          size: parseFloat(formData.size),
          location: formData.location,
          category: formData.category,
          type: formData.type,
        }),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la prédiction");
      }

      const data = await response.json();

      // Le backend devrait retourner { price: number, min_price: number, max_price: number }
      onPredictionResult({
        price: data.predicted_price,
        minPrice: data.conf_low,
        maxPrice: data.conf_high,
      });

      toast({
        title: "Prédiction réussie !",
        description: "Le prix estimé a été calculé avec succès.",
      });
    } catch (error) {
      console.error("Erreur:", error);
      toast({
        title: "Erreur",
        description:
          "Impossible de se connecter à l'API. Vérifiez que le serveur est démarré.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-lg border-0 bg-card/50 backdrop-blur-sm">
      <CardHeader className="space-y-1 pb-6">
        <CardDescription className="text-base">
          Remplissez les informations pour obtenir une estimation précise du
          prix
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Nombre de chambres */}
            <div className="space-y-2">
              <Label htmlFor="room_count" className="flex items-center gap-2">
                <BedDouble className="h-4 w-4 text-primary" />
                Nombre de chambres
              </Label>
              <Input
                id="room_count"
                type="number"
                min="1"
                placeholder="Ex: 3"
                value={formData.room_count}
                onChange={(e) =>
                  handleInputChange("room_count", e.target.value)
                }
                className="transition-all focus:shadow-md"
              />
            </div>

            {/* Nombre de salles de bain */}
            <div className="space-y-2">
              <Label
                htmlFor="bathroom_count"
                className="flex items-center gap-2"
              >
                <Bath className="h-4 w-4 text-primary" />
                Salles de bain
              </Label>
              <Input
                id="bathroom_count"
                type="number"
                min="1"
                placeholder="Ex: 2"
                value={formData.bathroom_count}
                onChange={(e) =>
                  handleInputChange("bathroom_count", e.target.value)
                }
                className="transition-all focus:shadow-md"
              />
            </div>

            {/* Surface */}
            <div className="space-y-2">
              <Label htmlFor="size" className="flex items-center gap-2">
                <Ruler className="h-4 w-4 text-primary" />
                Surface (m²)
              </Label>
              <Input
                id="size"
                type="number"
                min="1"
                placeholder="Ex: 120"
                value={formData.size}
                onChange={(e) => handleInputChange("size", e.target.value)}
                className="transition-all focus:shadow-md"
              />
            </div>

            {/* Ville */}
            <div className="space-y-2">
              <Label htmlFor="location" className="flex items-center gap-2">
                <MapPin className="h-4 w-4 text-primary" />
                Ville
              </Label>
              <Select
                value={formData.location}
                onValueChange={(value) => handleInputChange("location", value)}
              >
                <SelectTrigger
                  id="location"
                  className="transition-all focus:shadow-md"
                >
                  <SelectValue placeholder="Sélectionnez une ville" />
                </SelectTrigger>
                <SelectContent className="max-h-60">
                  {tunisianCities.map((city) => (
                    <SelectItem key={city} value={city}>
                      {city}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Catégorie */}
            <div className="space-y-2">
              <Label htmlFor="category">Catégorie</Label>
              <Select
                value={formData.category}
                onValueChange={(value) => handleInputChange("category", value)}
              >
                <SelectTrigger
                  id="category"
                  className="transition-all focus:shadow-md"
                >
                  <SelectValue placeholder="Type de bien" />
                </SelectTrigger>
                <SelectContent>
                  {
                    categories.map((category) => (
                      <SelectItem key={category} value={category}>
                        {category}
                      </SelectItem>
                    ))
                  }
                </SelectContent>
              </Select>
            </div>

            {/* Type (Vente/Location) */}
            <div className="space-y-2">
              <Label htmlFor="type">Type de transaction</Label>
              <Select
                value={formData.type}
                onValueChange={(value) => handleInputChange("type", value)}
              >
                <SelectTrigger
                  id="type"
                  className="transition-all focus:shadow-md"
                >
                  <SelectValue placeholder="Vente ou Location" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="À Vendre">Vente</SelectItem>
                  <SelectItem value="À Louer">Location</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button
            type="submit"
            className="w-full h-12 text-base font-semibold bg-gradient-primary hover:opacity-90 transition-all shadow-md hover:shadow-lg"
            disabled={isLoading}
          >
            {isLoading ? "Calcul en cours..." : "Prédire le prix"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
