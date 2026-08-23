"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { DecisionBadge } from "@/components/decision-badge";
import { CATEGORIES, type FraudPrediction } from "@/lib/types";

function nowLocalDatetime() {
  const offsetMs = new Date().getTimezoneOffset() * 60000;
  return new Date(Date.now() - offsetMs).toISOString().slice(0, 16);
}

const DEFAULTS = {
  transaction_id: "",
  cc_num: "4111111111111111",
  amt: "120.50",
  merchant: "fraud_Kirlin and Sons",
  category: "shopping_pos",
  gender: "F" as "F" | "M",
  dob: "1990-05-14",
  city_pop: "50000",
  lat: "-12.0464",
  long: "-77.0428",
  merch_lat: "-12.10",
  merch_long: "-77.05",
  trans_time: nowLocalDatetime(),
};

export function PredictForm() {
  const [form, setForm] = useState(DEFAULTS);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<FraudPrediction | null>(null);
  const [error, setError] = useState<string | null>(null);

  function update<K extends keyof typeof form>(key: K, value: (typeof form)[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const payload = {
      transaction_id: form.transaction_id || `web-${crypto.randomUUID()}`,
      cc_num: form.cc_num,
      amt: Number(form.amt),
      merchant: form.merchant,
      category: form.category,
      gender: form.gender,
      dob: form.dob,
      city_pop: Number(form.city_pop),
      lat: Number(form.lat),
      long: Number(form.long),
      merch_lat: Number(form.merch_lat),
      merch_long: Number(form.merch_long),
      trans_time: new Date(form.trans_time).toISOString(),
    };

    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const body = await res.json();

      if (!res.ok) {
        const detail =
          typeof body.detail === "string"
            ? body.detail
            : JSON.stringify(body.detail ?? body);
        throw new Error(detail);
      }

      setResult(body as FraudPrediction);
      toast.success("Prediccion calculada");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Error desconocido";
      setError(message);
      toast.error("Fallo la prediccion");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Evaluar transaccion</CardTitle>
        <CardDescription>
          Envia los datos de una transaccion a <code>/predict</code> y
          obten probabilidad de fraude y decision.
        </CardDescription>
      </CardHeader>
      <form onSubmit={onSubmit}>
        <CardContent className="grid gap-4 sm:grid-cols-2">
          <div className="grid gap-2">
            <Label htmlFor="transaction_id">ID de transaccion (opcional)</Label>
            <Input
              id="transaction_id"
              placeholder="auto-generado si se deja vacio"
              value={form.transaction_id}
              onChange={(e) => update("transaction_id", e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="cc_num">Numero de tarjeta</Label>
            <Input
              id="cc_num"
              required
              value={form.cc_num}
              onChange={(e) => update("cc_num", e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="amt">Monto</Label>
            <Input
              id="amt"
              type="number"
              step="0.01"
              min="0.01"
              required
              value={form.amt}
              onChange={(e) => update("amt", e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="merchant">Comercio</Label>
            <Input
              id="merchant"
              required
              value={form.merchant}
              onChange={(e) => update("merchant", e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="category">Categoria</Label>
            <Select
              value={form.category}
              onValueChange={(value) => update("category", value as string)}
            >
              <SelectTrigger id="category" className="w-full">
                <SelectValue placeholder="Selecciona categoria" />
              </SelectTrigger>
              <SelectContent>
                {CATEGORIES.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {cat}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="grid gap-2">
            <Label htmlFor="gender">Genero</Label>
            <Select
              value={form.gender}
              onValueChange={(value) => update("gender", value as "F" | "M")}
            >
              <SelectTrigger id="gender" className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="F">F</SelectItem>
                <SelectItem value="M">M</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="grid gap-2">
            <Label htmlFor="dob">Fecha de nacimiento</Label>
            <Input
              id="dob"
              type="date"
              required
              value={form.dob}
              onChange={(e) => update("dob", e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="city_pop">Poblacion de la ciudad</Label>
            <Input
              id="city_pop"
              type="number"
              min="0"
              required
              value={form.city_pop}
              onChange={(e) => update("city_pop", e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="lat">Latitud titular</Label>
            <Input
              id="lat"
              type="number"
              step="any"
              required
              value={form.lat}
              onChange={(e) => update("lat", e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="long">Longitud titular</Label>
            <Input
              id="long"
              type="number"
              step="any"
              required
              value={form.long}
              onChange={(e) => update("long", e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="merch_lat">Latitud comercio</Label>
            <Input
              id="merch_lat"
              type="number"
              step="any"
              required
              value={form.merch_lat}
              onChange={(e) => update("merch_lat", e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="merch_long">Longitud comercio</Label>
            <Input
              id="merch_long"
              type="number"
              step="any"
              required
              value={form.merch_long}
              onChange={(e) => update("merch_long", e.target.value)}
            />
          </div>
          <div className="grid gap-2 sm:col-span-2">
            <Label htmlFor="trans_time">Fecha/hora de la transaccion</Label>
            <Input
              id="trans_time"
              type="datetime-local"
              required
              value={form.trans_time}
              onChange={(e) => update("trans_time", e.target.value)}
            />
          </div>
        </CardContent>
        <CardFooter className="flex flex-col items-stretch gap-4">
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Evaluando..." : "Evaluar transaccion"}
          </Button>

          {error && (
            <Alert variant="destructive">
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {result && (
            <div className="rounded-lg border p-4 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Decision</span>
                <DecisionBadge decision={result.decision} />
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                  Probabilidad de fraude
                </span>
                <span className="font-mono font-medium">
                  {(result.fraud_probability * 100).toFixed(2)}%
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                  Distancia titular-comercio
                </span>
                <span className="font-mono font-medium">
                  {result.distance_km.toFixed(2)} km
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">ID</span>
                <span className="font-mono text-xs">{result.transaction_id}</span>
              </div>
            </div>
          )}
        </CardFooter>
      </form>
    </Card>
  );
}
