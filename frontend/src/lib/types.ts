// Espejo de backend/app/schemas.py y backend/app/constants.py.
// Si cambian ahi, actualizar aqui.

export const CATEGORIES = [
  "entertainment",
  "food_dining",
  "gas_transport",
  "grocery_net",
  "grocery_pos",
  "health_fitness",
  "home",
  "kids_pets",
  "misc_net",
  "misc_pos",
  "personal_care",
  "shopping_net",
  "shopping_pos",
  "travel",
] as const;

export type Category = (typeof CATEGORIES)[number];

export interface TransactionInput {
  transaction_id: string;
  cc_num: string;
  amt: number;
  merchant: string;
  category: string;
  gender: "M" | "F";
  dob: string; // YYYY-MM-DD
  city_pop: number;
  lat: number;
  long: number;
  merch_lat: number;
  merch_long: number;
  trans_time: string; // ISO datetime
}

export interface FraudPrediction {
  transaction_id: string;
  fraud_probability: number;
  decision: "allow" | "review" | "block";
  distance_km: number;
}

export interface Transaction extends TransactionInput {
  fraud_probability?: number;
  decision?: string;
  distance_km?: number;
  created_at?: string;
}

export interface ApiError {
  detail: string;
}
