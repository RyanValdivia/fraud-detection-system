import { Badge } from "@/components/ui/badge";

const LABELS: Record<string, string> = {
  allow: "Permitir",
  review: "Revisar",
  block: "Bloquear",
};

const VARIANTS: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  allow: "default",
  review: "secondary",
  block: "destructive",
};

export function DecisionBadge({ decision }: { decision: string }) {
  const variant = VARIANTS[decision] ?? "outline";
  const label = LABELS[decision] ?? decision;
  return <Badge variant={variant}>{label}</Badge>;
}
