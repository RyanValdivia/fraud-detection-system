"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableRow,
} from "@/components/ui/table";
import { DecisionBadge } from "@/components/decision-badge";
import type { Transaction } from "@/lib/types";

export function TransactionLookup() {
  const [id, setId] = useState("");
  const [loading, setLoading] = useState(false);
  const [tx, setTx] = useState<Transaction | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!id.trim()) return;

    setLoading(true);
    setError(null);
    setTx(null);

    try {
      const res = await fetch(`/api/transactions/${encodeURIComponent(id.trim())}`);
      const body = await res.json();

      if (!res.ok) {
        const detail = typeof body.detail === "string" ? body.detail : "No encontrada";
        throw new Error(detail);
      }

      setTx(body as Transaction);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Error desconocido";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Buscar transaccion</CardTitle>
        <CardDescription>
          Consulta una prediccion ya guardada por <code>transaction_id</code>.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <form onSubmit={onSubmit} className="flex items-end gap-2">
          <div className="grid gap-2 flex-1">
            <Label htmlFor="lookup-id">ID de transaccion</Label>
            <Input
              id="lookup-id"
              placeholder="test-integration-..."
              value={id}
              onChange={(e) => setId(e.target.value)}
            />
          </div>
          <Button type="submit" disabled={loading}>
            {loading ? "Buscando..." : "Buscar"}
          </Button>
        </form>

        {loading && <Skeleton className="h-32 w-full" />}

        {error && (
          <Alert variant="destructive">
            <AlertTitle>No encontrada</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {tx && (
          <Table>
            <TableBody>
              <TableRow>
                <TableCell className="text-muted-foreground">ID</TableCell>
                <TableCell className="font-mono text-xs">
                  {tx.transaction_id}
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="text-muted-foreground">Comercio</TableCell>
                <TableCell>{tx.merchant}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="text-muted-foreground">Categoria</TableCell>
                <TableCell>{tx.category}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="text-muted-foreground">Monto</TableCell>
                <TableCell className="font-mono">
                  {Number(tx.amt).toFixed(2)}
                </TableCell>
              </TableRow>
              {tx.decision && (
                <TableRow>
                  <TableCell className="text-muted-foreground">Decision</TableCell>
                  <TableCell>
                    <DecisionBadge decision={tx.decision} />
                  </TableCell>
                </TableRow>
              )}
              {typeof tx.fraud_probability === "number" && (
                <TableRow>
                  <TableCell className="text-muted-foreground">
                    Probabilidad
                  </TableCell>
                  <TableCell className="font-mono">
                    {(tx.fraud_probability * 100).toFixed(2)}%
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
