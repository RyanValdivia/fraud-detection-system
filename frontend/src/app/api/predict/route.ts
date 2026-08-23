import { NextRequest, NextResponse } from "next/server";
import { BackendError, predictTransaction } from "@/lib/backend";

export async function POST(request: NextRequest) {
  const payload = await request.json();

  try {
    const prediction = await predictTransaction(payload);
    return NextResponse.json(prediction);
  } catch (err) {
    if (err instanceof BackendError) {
      return NextResponse.json({ detail: err.detail }, { status: err.status });
    }
    return NextResponse.json({ detail: "Error al contactar el backend" }, { status: 502 });
  }
}
