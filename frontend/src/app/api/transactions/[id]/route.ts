import { NextResponse } from "next/server";
import { BackendError, getTransaction } from "@/lib/backend";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;

  try {
    const transaction = await getTransaction(id);
    return NextResponse.json(transaction);
  } catch (err) {
    if (err instanceof BackendError) {
      return NextResponse.json({ detail: err.detail }, { status: err.status });
    }
    return NextResponse.json({ detail: "Error al contactar el backend" }, { status: 502 });
  }
}
