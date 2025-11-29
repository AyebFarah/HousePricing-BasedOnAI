import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, PieChart, Pie, Cell } from "recharts";
import { TrendingUp, BarChart3, PieChartIcon } from "lucide-react";

// Données simulées - Dans votre version réelle, ces données viendront de votre API
const cityPrices = [
  { city: "Tunis", avgPrice: 180000, count: 450, growth: 5.2 },
  { city: "La Marsa", avgPrice: 320000, count: 180, growth: 7.8 },
  { city: "Sousse", avgPrice: 145000, count: 320, growth: 4.1 },
  { city: "Hammamet", avgPrice: 250000, count: 210, growth: 6.5 },
  { city: "Sfax", avgPrice: 135000, count: 280, growth: 3.9 },
  { city: "Monastir", avgPrice: 160000, count: 190, growth: 4.7 },
  { city: "Ariana", avgPrice: 195000, count: 340, growth: 5.8 },
  { city: "Bizerte", avgPrice: 125000, count: 150, growth: 3.2 },
];

const monthlyTrends = [
  { month: "Jan", vente: 165000, location: 850 },
  { month: "Fév", vente: 168000, location: 870 },
  { month: "Mar", vente: 172000, location: 890 },
  { month: "Avr", vente: 175000, location: 910 },
  { month: "Mai", vente: 180000, location: 920 },
  { month: "Jun", vente: 183000, location: 950 },
  { month: "Jul", vente: 188000, location: 970 },
  { month: "Aoû", vente: 192000, location: 990 },
  { month: "Sep", vente: 195000, location: 1010 },
  { month: "Oct", vente: 198000, location: 1030 },
  { month: "Nov", vente: 201000, location: 1050 },
  { month: "Déc", vente: 205000, location: 1080 },
];

const propertyTypes = [
  { name: "Appartements", value: 45, color: "hsl(210 100% 45%)" },
  { name: "Maisons", value: 28, color: "hsl(25 95% 53%)" },
  { name: "Villas", value: 15, color: "hsl(142 76% 36%)" },
  { name: "Studios", value: 8, color: "hsl(195 100% 50%)" },
  { name: "Autres", value: 4, color: "hsl(215 16% 47%)" },
];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-card border border-border rounded-lg shadow-lg p-3">
        <p className="font-semibold text-foreground mb-1">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} className="text-sm" style={{ color: entry.color }}>
            {entry.name}: {entry.name.includes("location") ? `${entry.value} TND` : `${entry.value.toLocaleString('fr-TN')} TND`}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function MarketTrends() {
  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold text-foreground flex items-center justify-center gap-2">
          <TrendingUp className="h-8 w-8 text-primary" />
          Analyse du Marché Immobilier
        </h2>
        <p className="text-muted-foreground">
          Visualisez les tendances et comparez les prix à travers la Tunisie
        </p>
      </div>

      <Tabs defaultValue="cities" className="w-full">
        <TabsList className="grid w-full grid-cols-3 mb-6">
          <TabsTrigger value="cities" className="flex items-center gap-2">
            <BarChart3 className="h-4 w-4" />
            Prix par Ville
          </TabsTrigger>
          <TabsTrigger value="types" className="flex items-center gap-2">
            <PieChartIcon className="h-4 w-4" />
            Types de Biens
          </TabsTrigger>
          <TabsTrigger value="trends" className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            Tendances
          </TabsTrigger>
        </TabsList>

        {/* Prix par Ville */}
        <TabsContent value="cities" className="space-y-4">
          <Card className="shadow-lg border-0 bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle>Prix Moyen par Ville</CardTitle>
              <CardDescription>
                Comparaison des prix moyens des biens immobiliers dans les principales villes tunisiennes
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={cityPrices} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis 
                    dataKey="city" 
                    angle={-45}
                    textAnchor="end"
                    height={100}
                    stroke="hsl(var(--foreground))"
                    tick={{ fill: 'hsl(var(--foreground))' }}
                  />
                  <YAxis 
                    stroke="hsl(var(--foreground))"
                    tick={{ fill: 'hsl(var(--foreground))' }}
                    tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar 
                    dataKey="avgPrice" 
                    fill="hsl(var(--primary))"
                    radius={[8, 8, 0, 0]}
                    name="Prix moyen"
                  />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tendances Temporelles */}
        <TabsContent value="trends" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="shadow-md border-0 bg-gradient-to-br from-primary/10 to-primary/5">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Prix Moyen Vente</p>
                    <p className="text-3xl font-bold text-foreground">205k TND</p>
                    <p className="text-xs text-success mt-1">+24% cette année</p>
                  </div>
                  <div className="p-3 rounded-full bg-primary/20">
                    <TrendingUp className="h-6 w-6 text-primary" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="shadow-md border-0 bg-gradient-to-br from-accent/10 to-accent/5">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Loyer Moyen</p>
                    <p className="text-3xl font-bold text-foreground">1,080 TND</p>
                    <p className="text-xs text-success mt-1">+27% cette année</p>
                  </div>
                  <div className="p-3 rounded-full bg-accent/20">
                    <TrendingUp className="h-6 w-6 text-accent" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="shadow-md border-0 bg-gradient-to-br from-success/10 to-success/5">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Transactions</p>
                    <p className="text-3xl font-bold text-foreground">2,450</p>
                    <p className="text-xs text-success mt-1">+12% ce mois</p>
                  </div>
                  <div className="p-3 rounded-full bg-success/20">
                    <BarChart3 className="h-6 w-6 text-success" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Types de Biens */}
        <TabsContent value="types" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="shadow-lg border-0 bg-card/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Distribution par Type</CardTitle>
                <CardDescription>
                  Répartition des biens immobiliers par catégorie
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={propertyTypes}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {propertyTypes.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value: any) => [`${value}%`, "Part de marché"]}
                      contentStyle={{ 
                        backgroundColor: 'hsl(var(--card))', 
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '8px'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card className="shadow-lg border-0 bg-card/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Statistiques par Type</CardTitle>
                <CardDescription>
                  Détails des catégories de biens
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {propertyTypes.map((type, index) => (
                    <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors">
                      <div className="flex items-center gap-3">
                        <div 
                          className="w-4 h-4 rounded-full" 
                          style={{ backgroundColor: type.color }}
                        />
                        <span className="font-medium text-foreground">{type.name}</span>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-foreground">{type.value}%</p>
                        <p className="text-xs text-muted-foreground">du marché</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="shadow-lg border-0 bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle>Prix Moyen par Type de Bien</CardTitle>
              <CardDescription>
                Comparaison des prix moyens selon la catégorie
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart 
                  data={[
                    { type: "Studio", price: 95000 },
                    { type: "Appartement", price: 175000 },
                    { type: "Maison", price: 280000 },
                    { type: "Villa", price: 450000 },
                    { type: "Duplex", price: 320000 },
                  ]}
                  margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis 
                    dataKey="type"
                    stroke="hsl(var(--foreground))"
                    tick={{ fill: 'hsl(var(--foreground))' }}
                  />
                  <YAxis 
                    stroke="hsl(var(--foreground))"
                    tick={{ fill: 'hsl(var(--foreground))' }}
                    tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar 
                    dataKey="price" 
                    fill="hsl(var(--primary))"
                    radius={[8, 8, 0, 0]}
                    name="Prix moyen"
                  />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
